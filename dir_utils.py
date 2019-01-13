def opposite(direction: str) -> str:
    return {"n": "s", "s": "n", "w": "e", "e": "w"}[direction]


def dir_to_vec(direction: str) -> (int, int):
    return {"n": (0, -1), "s": (0, 1), "w": (-1, 0), "e": (1, 0)}[direction]
