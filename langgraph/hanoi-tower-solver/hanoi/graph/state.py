from typing import TypedDict, List, Annotated
from operator import add


class HanoiState(TypedDict):
    """Defines what is the position of each disk."""
    reasoning: str
    notepad: str
    tower_1: List[int]
    tower_2: List[int]
    tower_3: List[int]
    error: str
    previous_move: str
