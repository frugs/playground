from constants import ROOM_SIZE


def opposite(direction: str) -> str:
    return {"n": "s", "s": "n", "w": "e", "e": "w"}[direction]


def dir_to_vec(direction: str) -> (int, int):
    return {"n": (0, -1), "s": (0, 1), "w": (-1, 0), "e": (1, 0)}[direction]


def dir_to_pos(direction: str) -> (int, int):
    return {"n": (3, 0), "s": (3, ROOM_SIZE - 1), "e": (ROOM_SIZE - 1, 3), "w": (0, 3)}[
        direction
    ]
