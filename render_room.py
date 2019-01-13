import PIL.Image

from constants import CELL_SIZE, ROOM_SIZE
from vec_utils import vec_mul


def render_room(room):
    blocker = PIL.Image.new("RGB", (CELL_SIZE, CELL_SIZE), "blue")
    gap = PIL.Image.new("RGB", (CELL_SIZE, CELL_SIZE), "black")

    image = PIL.Image.new(
        "RGBA", ((CELL_SIZE + 1) * ROOM_SIZE, (CELL_SIZE + 1) * ROOM_SIZE), (0, 0, 0, 0)
    )

    for pos in room["blockers"]:
        image.paste(blocker, vec_mul(pos, (CELL_SIZE, CELL_SIZE)))

    for pos in room["gaps"]:
        image.paste(gap, vec_mul(pos, (CELL_SIZE, CELL_SIZE)))

    return image


def main():
    from gen_room import gen_room

    image = render_room(gen_room(["s", "e"]))
    image.show()


if __name__ == "__main__":
    main()
