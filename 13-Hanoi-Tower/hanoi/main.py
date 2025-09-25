from hanoi.graph.graph import game


def main():
    print("---TOWER OF HANOI---")

    tower_1 = [1, 2, 3]
    tower_2 = []
    tower_3 = []

    game.invoke({
        "tower_1": tower_1,
        "tower_2": tower_2,
        "tower_3": tower_3,
        "reasoning": "",
        "notepad": "",
        "error": "",
        "previous_move": ""
    })


if __name__ == "__main__":
    main()
