from hanoi.nodes.game import PerformMove, perform_move
from hanoi.graph.graph import is_solved
from hanoi.graph.state import HanoiState


def test_perform_move_legal():
    temp_state: HanoiState = {
        "tower_1": [1, 2, 3],
        "tower_2": [],
        "tower_3": [],
        "notepad": "",
        "reasoning": "",
        "error": ""
    }
    towers: PerformMove = perform_move(1, 3, temp_state)

    assert towers["from_tower"] == [2, 3] and towers["to_tower"] == [1] and towers["error"] == ""


def test_perform_move_illegal_unknow_tower():
    temp_state: HanoiState = {
        "tower_1": [2, 3, 4],
        "tower_2": [1],
        "tower_3": [],
        "notepad": "",
        "reasoning": "",
        "error": ""
    }
    towers: PerformMove = perform_move(1, 4, temp_state)

    print(towers["error"])
    assert not towers["error"] == "legal"


def test_perform_move_illegal_same_towers():    
    temp_state: HanoiState = {
        "tower_1": [2, 3, 4],
        "tower_2": [1],
        "tower_3": [],
        "notepad": "",
        "reasoning": "",
        "error": ""
    }
    towers: PerformMove = perform_move(2, 2, temp_state)

    print(towers["error"])
    assert not towers["error"] == "legal"


def test_perform_move_illegal_bigger_disk():
    temp_state: HanoiState = {
        "tower_1": [2, 3, 4],
        "tower_2": [1],
        "tower_3": [],
        "notepad": "",
        "reasoning": "",
        "error": ""
    }
    towers: PerformMove = perform_move(1, 2, temp_state)

    print(towers["error"])
    assert not towers["error"] == "legal"


def test_perform_move_illegal_empty_tower():
    temp_state: HanoiState = {
        "tower_1": [2, 3, 4],
        "tower_2": [1],
        "tower_3": [],
        "notepad": "",
        "reasoning": "",
        "error": ""
    }
    towers: PerformMove = perform_move(3, 2, temp_state)

    print(towers["error"])
    assert not towers["error"] == "legal"


def test_is_solved_answer_solved():
    state_1: HanoiState = {
        "tower_1": [],
        "tower_2": [],
        "tower_3": [1, 2, 3, 4],
        "notepad": "",
        "reasoning": ""
    }

    state_2: HanoiState = {
        "tower_1": [],
        "tower_2": [],
        "tower_3": [1, 2, 3, 4, 5, 6, 7],
        "notepad": "",
        "reasoning": ""
    }

    assert is_solved(state_1) == "solved"
    assert is_solved(state_2) == "solved"


def test_is_solved_answer_not_solved():
    state_1: HanoiState = {
        "tower_1": [1, 2],
        "tower_2": [],
        "tower_3": [3, 4, 5, 6],
        "notepad": "",
        "reasoning": ""
    }

    state_2: HanoiState = {
        "tower_1": [],
        "tower_2": [],
        "tower_3": [2, 3, 1],
        "notepad": "",
        "reasoning": ""
    }

    assert is_solved(state_1) == "not solved"
    assert is_solved(state_2) == "not solved"
