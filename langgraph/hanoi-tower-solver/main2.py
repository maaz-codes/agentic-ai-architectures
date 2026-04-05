from typing import List, Dict, Any, TypedDict, Tuple, Literal
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# Pydantic models for structured output
class Move(BaseModel):
    """Single move in Tower of Hanoi"""
    from_tower: Literal[1, 2, 3] = Field(description="Source tower number (1, 2, or 3)", ge=1, le=3)
    to_tower: Literal[1, 2, 3] = Field(description="Destination tower number (1, 2, or 3)", ge=1, le=3)
    move_number: int = Field(description="Sequential move number starting from 1")

class HanoiMoves(BaseModel):
    """Collection of moves to solve Tower of Hanoi"""
    moves: List[Move] = Field(description="Up to 100 moves to solve the puzzle", max_items=100)
    reasoning: str = Field(description="Brief explanation of the strategy")

# State definition for the graph
class HanoiState(TypedDict):
    towers: List[List[int]]      # Three towers represented as lists
    messages: List[BaseMessage]  # Conversation history
    current_moves: List[Move]    # Current batch of moves to apply
    move_index: int             # Current position in current_moves
    total_moves_made: int       # Total moves made so far
    completed: bool             # Whether puzzle is solved
    error: str                  # Error message if any
    user_input: str             # Latest user input

class ConversationalHanoiAgent:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            openai_api_key=api_key
        )
        # Create structured LLM for move generation
        self.structured_llm = self.llm.with_structured_output(HanoiMoves)
        self.graph = self._create_graph()
    
    def _create_graph(self) -> StateGraph:
        """Create the LangGraph workflow"""
        workflow = StateGraph(HanoiState)
        
        # Add nodes
        workflow.add_node("check_solved", self._check_if_solved)
        workflow.add_node("generate_moves", self._generate_moves)
        workflow.add_node("validate_moves", self._validate_moves)
        workflow.add_node("apply_moves", self._apply_moves)
        workflow.add_node("handle_error", self._handle_error)
        
        # Define the flow
        workflow.set_entry_point("check_solved")
        
        # Conditional routing from check_solved
        workflow.add_conditional_edges(
            "check_solved",
            self._route_from_check,
            {
                "solved": END,
                "generate": "generate_moves"
            }
        )
        
        workflow.add_edge("generate_moves", "validate_moves")
        
        # Conditional routing from validate_moves
        workflow.add_conditional_edges(
            "validate_moves",
            self._route_from_validation,
            {
                "valid": "apply_moves",
                "invalid": "handle_error"
            }
        )
        
        workflow.add_edge("apply_moves", END)
        workflow.add_edge("handle_error", END)
        
        return workflow.compile()
    
    def _check_if_solved(self, state: HanoiState) -> Dict[str, Any]:
        """Check if puzzle is already solved"""
        total_disks = sum(len(tower) for tower in state["towers"])
        is_solved = len(state["towers"][2]) == total_disks and total_disks > 0
        
        return {
            **state,
            "completed": is_solved
        }
    
    def _generate_moves(self, state: HanoiState) -> Dict[str, Any]:
        """Generate next batch of moves using conversational context"""
        if state["completed"]:
            return {
                **state,
                "error": "Puzzle is already solved!"
            }
        
        # Build conversation context
        messages = state["messages"][:]  # Copy existing messages
        
        # Add current state information
        towers_str = self._format_towers(state["towers"])
        moves_made = state["total_moves_made"]
        
        system_prompt = f"""You are a Tower of Hanoi expert having a conversation about solving the puzzle.

Current state after {moves_made} moves:
{towers_str}

Rules:
- Only move one disk at a time
- Only move the top disk from a tower  
- Never place a larger disk on a smaller disk
- Towers are numbered 1, 2, 3
- Goal: Move all disks to Tower 3

Generate up to 100 moves to continue solving. If you can solve it in fewer moves, that's better.
Stop generating moves once the puzzle is solved (all disks on Tower 3).
Provide reasoning for your strategy."""

        if not messages or not isinstance(messages[0], SystemMessage):
            messages.insert(0, SystemMessage(content=system_prompt))
        else:
            messages[0] = SystemMessage(content=system_prompt)  # Update system message
        
        # Add user input as human message
        messages.append(HumanMessage(content=state["user_input"]))
        
        try:
            # Get structured output from LLM
            response = self.structured_llm.invoke(messages)
            
            # Add AI response to conversation
            ai_content = f"Generated {len(response.moves)} moves. Reasoning: {response.reasoning}"
            messages.append(AIMessage(content=ai_content))
            
            return {
                **state,
                "messages": messages,
                "current_moves": response.moves,
                "move_index": 0,
                "error": ""
            }
        except Exception as e:
            return {
                **state,
                "error": f"Error generating moves: {str(e)}"
            }
    
    def _validate_moves(self, state: HanoiState) -> Dict[str, Any]:
        """Validate all generated moves before applying them"""
        if state["error"] or not state["current_moves"]:
            return state
        
        # Create a copy of towers to test moves
        test_towers = [tower[:] for tower in state["towers"]]
        
        for i, move in enumerate(state["current_moves"]):
            from_idx, to_idx = move.from_tower - 1, move.to_tower - 1
            
            # Check basic validity
            if from_idx == to_idx:
                return {
                    **state,
                    "error": f"Move {move.move_number}: Cannot move from tower to itself ({move.from_tower})"
                }
            
            # Check if source tower is empty
            if not test_towers[from_idx]:
                return {
                    **state,
                    "error": f"Move {move.move_number}: Cannot move from empty tower {