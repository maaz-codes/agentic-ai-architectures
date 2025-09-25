from typing import Literal
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv


load_dotenv()


class Move(BaseModel):
    """Represents a single move in the Tower of Hanoi game. 
    A move consists of taking the topmost disk from one tower and placing it on another tower, 
    following the game's rules (smaller disks on larger disks only).
    """

    reasoning: str = Field(
        ...,
        description=(
            "A clear, strategic explanation of WHY this specific move advances toward "
            "the solution. Describe how this move fits into the recursive Tower of Hanoi "
            "strategy, what disk is being moved, and what this move accomplishes "
            "(e.g., 'exposing a needed disk', 'completing a subproblem', 'following optimal pattern'). "
            "Be specific about the disk size and strategic purpose."
        ),
        min_length=20,
        max_length=200,
        examples=[
            "Moving smallest disk (size 1) from tower 1 to tower 3 to begin the 3-disk solution pattern",
            "Moving medium disk (size 2) to tower 2 to expose the largest disk underneath"
        ]
    )
    
    notepad: str = Field(
        ...,
        description=(
            "Your working notes and strategic planning for this game session. Include: "
            "(1) Current sub-goal you're working on (e.g., 'moving top 2 disks from tower 1 to tower 2'), "
            "(2) Progress tracking (e.g., 'completed step 1 of 3 in current subproblem'), "
            "(3) Next planned moves or observations, "
            "(4) Any patterns or learnings discovered. "
            "This should read like a strategy notebook that helps with future moves."
        ),
        min_length=30,
        max_length=300,
        examples=[
            "Sub-goal: Move top 2 disks from tower 1 to tower 2 using tower 3. Progress: Step 1/3 complete. Next: move medium disk to auxiliary position.",
            "Learned: Always move smallest disk first in each recursive step. Currently solving 3-disk subproblem. Tower 3 ready for largest disk."
        ]
    )
    
    from_tower: Literal[1, 2, 3] = Field(
        ...,
        description=(
            "The source tower number (1, 2, or 3) from which to move the topmost disk. "
            "This tower must contain at least one disk. Tower 1 is the starting tower, "
            "tower 2 is the auxiliary/helper tower, and tower 3 is the destination tower."
        ),
        examples=[1, 2, 3]
    )
    
    to_tower: Literal[1, 2, 3] = Field(
        ...,
        description=(
            "The destination tower number (1, 2, or 3) where the disk will be placed. "
            "The disk being moved must be smaller than the topmost disk on this tower, "
            "or this tower must be empty. Cannot be the same as from_tower."
        ),
        examples=[1, 2, 3]
    )


llm = ChatOpenAI(model="gpt-4o", temperature=0).with_structured_output(Move)
system = """Your Role and Environment:
You are a Tower of Hanoi solving agent operating in a controlled game environment. Your sole task is to analyze the current game state and provide exactly ONE valid move that brings you closer to the solution.

Game Rules (CRITICAL - READ CAREFULLY):
The Tower of Hanoi consists of 3 towers (numbered 1, 2, 3) and multiple disks of different sizes:

Core Rules:
- Only the TOP disk from any tower can be moved
- A disk can only be placed on an EMPTY tower OR on top of a LARGER disk
- You cannot place a larger disk on top of a smaller disk
- Goal: Move all disks from tower 1 to tower 3, maintaining the same order (largest at bottom, smallest at top)

Move Validation:
- from_tower must contain at least one disk (cannot move from empty tower)
- The top disk from from_tower must be smaller than the top disk on to_tower (if to_tower is not empty)
- Tower numbers must be 1, 2, or 3 only

Current Game State Format:
You will receive the current state as:
Previous Reasoning: [your previous reasoning if any]
Previous Notes: [your previous notepad notes if any]
Tower 1: [disk_sizes] (leftmost = top, rightmost = bottom)
Tower 2: [disk_sizes]
Tower 3: [disk_sizes]

IMPORTANT
Always fill the reasoning field first, then the nodepad, and lastly the from_tower and to_tower fields.

Before Each Move:
- Validate: Can the top disk from from_tower legally move to to_tower?
- Strategic Value: Does this move help expose a needed disk or create a useful intermediate configuration?
- Pattern Recognition: Are you following the optimal recursive pattern for Tower of Hanoi?
"""

game_state = """State of the Game:
Your reasonings: {reasoning}
Your notepad: {notepad}
Tower 1: {tower_1}
Tower 2: {tower_2}
Tower 3: {tower_3}
Error: {error}
Previous Move: {previous_move}"""
prompt_template = ChatPromptTemplate(
    [
        ("system", system),
        ("human", game_state)
    ]
)

gameplay_chain = prompt_template | llm

# system = """You are expert at playing Tower of Hanoi and you know all the rules for it.
# You are being placed inside an environment and you are exposed to some functions, one of them being move() where to decide to move the disk from one tower to the other.
# Rules are simple: Move one disk at a time. Bigger disk cannot be on top of smaller disk.
# Environment Details: You will be given a state of the game everytime we are going to call you, and you have access to notepad, where you can write stuff, and reason field where you can reason your moves.
# These fields will all be saved and will be feeded back to you every single time being append one after the other.
# Now the Hanoi Tower representation: There are three towers each represented as an integer: 1, 2, 3 for tower 1, tower 2, tower 3 respectedly.
# Disks are also represented as integers, 1 being the smallest disk and empty list means the tower is empty.
# Since disks on tower is represented by a list, assume from left to right is equivalent to top to bottom of a stack.
# For example state: tower_1: [1, 2, 3]. tower_2: [], tower_3: [] => This means tower one has 3 disks, smallest disk (1) on top followed by disk 2 and at the bottom the biggest disk 3.
# Tower 2 and tower 3 are empty."""
