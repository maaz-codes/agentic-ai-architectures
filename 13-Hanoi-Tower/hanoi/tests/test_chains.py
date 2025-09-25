from hanoi.chains.gameplay import Move, gameplay_chain

def test_gameplay():
    tower_1 = []
    tower_2 = [1, 2]
    tower_3 = [3]

    res: Move = gameplay_chain.invoke({
        "tower_1": tower_1,
        "tower_2": tower_2,
        "tower_3": tower_3,
        "notepad": "",
        "reason": "",
        "error": ""
    })

    assert res.from_tower and res.to_tower and res.reason and res.notepad
  