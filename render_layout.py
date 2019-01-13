import PIL.Image

from constants import CELL_SIZE, ROOM_SIZE
from render_room import render_room
from vec_utils import vec_sum


def render_layout(layout):
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0

    for node in layout:
        x = node["loc"][0]
        y = node["loc"][1]
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    image = PIL.Image.new(
        "RGBA", (width * CELL_SIZE * ROOM_SIZE, height * CELL_SIZE * ROOM_SIZE)
    )

    room_bg = PIL.Image.new(
        "RGBA", (CELL_SIZE * ROOM_SIZE, CELL_SIZE * ROOM_SIZE), "white"
    )
    h_wall = PIL.Image.new("RGBA", (CELL_SIZE * ROOM_SIZE, CELL_SIZE), "blue")
    v_wall = PIL.Image.new("RGBA", (CELL_SIZE, CELL_SIZE * ROOM_SIZE), "blue")
    doorway = PIL.Image.new("RGBA", (CELL_SIZE, CELL_SIZE), "white")
    room_bg.paste(h_wall, (0, 0))
    room_bg.paste(v_wall, (0, 0))
    room_bg.paste(h_wall, (0, CELL_SIZE * (ROOM_SIZE - 1)))
    room_bg.paste(v_wall, (CELL_SIZE * (ROOM_SIZE - 1), 0))

    def door_cell(direction: str):
        return {
            "n": (CELL_SIZE * 2, 0),
            "s": (CELL_SIZE * 2, CELL_SIZE * (ROOM_SIZE - 1)),
            "e": (CELL_SIZE * (ROOM_SIZE - 1), CELL_SIZE * 2),
            "w": (0, CELL_SIZE * 2),
        }[direction]

    for node in layout:
        left = (node["loc"][0] - min_x) * CELL_SIZE * ROOM_SIZE
        top = (node["loc"][1] - min_y) * CELL_SIZE * ROOM_SIZE

        image.paste(room_bg, (left, top))

        for ex in node["exits"]:
            door_pos = vec_sum(door_cell(ex["dir"]), (left, top))
            image.paste(doorway, door_pos)

        room_image = render_room(node["room"])
        image.paste(room_image, (left, top), room_image)

    return image


def main():
    from gen_layout import gen_layout

    image = render_layout(gen_layout())
    image.show()


if __name__ == "__main__":
    main()
