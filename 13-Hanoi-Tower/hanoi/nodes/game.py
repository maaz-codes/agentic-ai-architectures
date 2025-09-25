from time import sleep
from typing import TypedDict
from hanoi.graph.state import HanoiState
from hanoi.chains.gameplay import gameplay_chain, Move


class PerformMove(TypedDict):
    from_tower: str
    to_tower: str
    error: str


def check_legal_move(from_tower: int, to_tower: int, state: HanoiState):
    """To check whether the move given by AI is legal or not."""

    if from_tower not in [1, 2, 3] or to_tower not in [1, 2, 3]:
        return "The towers value should be either 1, 2 or 3."
    
    from_tower_disks = state[f"tower_{from_tower}"]
    to_tower_disks = state[f"tower_{to_tower}"]

    if from_tower == to_tower:
        return "The values of towers should be different and not same."
    elif len(from_tower_disks) == 0:
        return "Cannot move from empty tower."
    elif len(to_tower_disks) != 0:
        if from_tower_disks[0] > to_tower_disks[0]:
            return "Cannot move bigger disk on top of smaller disk"
    return "legal"


def perform_move(from_tower: int, to_tower: int, state: HanoiState) -> PerformMove:
    legal_msg: str = check_legal_move(from_tower, to_tower, state)
    if legal_msg == "legal":
        print(f"Performing Move... from {from_tower} to {to_tower}")
    else:
        return {"from_tower": state["tower_1"], "to_tower": state["tower_2"], "error": legal_msg}
    
    sleep(1)
    
    move_from = state[f"tower_{from_tower}"]
    move_to = state[f"tower_{to_tower}"]

    disk: int = move_from.pop(0)
    move_to.insert(0, disk)

    return {"from_tower": move_from, "to_tower": move_to, "error": ""}


def game_node(state: HanoiState):
    tower_1 = state['tower_1']
    tower_2 = state['tower_2']
    tower_3 = state['tower_3']
    reasoning = state["reasoning"]
    notepad = state["notepad"]
    error = state["error"]
    previous_move = state["previous_move"]

    response: Move = gameplay_chain.invoke({
        "tower_1": tower_1,
        "tower_2": tower_2,
        "tower_3": tower_3,
        "reasoning": reasoning,
        "notepad": notepad,
        "error": error,
        "previous_move": previous_move
    })

    print(f"state:\n1:{state["tower_1"]}\n2: {state["tower_2"]}\n3: {state["tower_3"]}\nNotepad: {state["notepad"]}\nReasoning: {state["reasoning"]}\nError: {state["error"]}")

    move_from = response.from_tower
    move_to = response.to_tower
    reasoning = response.reasoning
    notepad = response.notepad

    towers =  perform_move(move_from, move_to, state)

    if move_to not in [1, 2, 3] or move_from not in [1, 2, 3] or towers["error"] != "":
        move_from = 1
        move_to = 2

    new_state = {
        f"tower_{move_from}": towers["from_tower"],
        f"tower_{move_to}": towers["to_tower"],
        "reasoning": reasoning,
        "notepad": notepad,
        "error": towers["error"],
        "previous_move": f"Moved top disk from tower {move_from} to tower {move_to}."
    }
    
    return new_state
