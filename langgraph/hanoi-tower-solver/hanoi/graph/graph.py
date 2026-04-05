from hanoi.nodes.game import game_node
from hanoi.graph.consts import *
from hanoi.graph.state import HanoiState
from langgraph.graph import START, END, StateGraph


def is_solved(state: HanoiState) -> str:
    tower_1 = state["tower_1"]
    tower_2 = state["tower_2"]
    tower_3 = state["tower_3"]

    if len(tower_1) == 0 and len(tower_2) == 0:
        if tower_3 == sorted(tower_3):
            return "solved"

    return "not solved"


builder = StateGraph(HanoiState)

builder.add_node(GAME, game_node) 

builder.set_entry_point(GAME)
builder.add_conditional_edges(
    GAME,
    is_solved,
    {
        "solved": END,
        "not solved": GAME
    }
)

game = builder.compile()
# draw_info = game.get_graph()
# print(draw_info)