from ast import Tuple
from typing import TypedDict, List

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate


class HanoiState(TypedDict):
    """Defines what is the position of each disk."""
    tower_1: List[int]
    tower_2: List[int]
    tower_3: List[int]
    reasoning: str
    #previous_moves


# tower_1: [1, 2, 3]
# tower_2: []
# tower_3: []


class Move(BaseModel):
    move: Tuple[int, int] = Field(
        description="Stores the move as (from_tower, to_tower) and moves the top most disk from one tower to another tower."
    )
    reason: str = Field(
        description="Stores the reasoning behind the move."
    )
    notepad: str = Field(
        description="Notepad to write some learnings, observations and future planning."
    )



llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(Move)
system = ""
prompt_template = ChatPromptTemplate(
    [
        ("system", system),
        ("human", "State of the Game: {tower_1}\n{tower_2}\n{tower_3}\nYour reasonings: {reason}\nYour notepad: {notepad}")
    ]
)



def gameplay(state: HanoiState):
    tower_1 = state['tower_1']
    tower_2 = state['tower_2']
    tower_3 = state['tower_3']

    # move = gameplay_chain.invoke()