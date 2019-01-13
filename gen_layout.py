import random

from gen_room import gen_room, gen_empty_room
from vec_utils import vec_sum


def opposite(direction: str) -> str:
    return {"n": "s", "s": "n", "w": "e", "e": "w"}[direction]


def dir_to_vec(direction: str) -> (int, int):
    return {"n": (0, -1), "s": (0, 1), "w": (-1, 0), "e": (1, 0)}[direction]


def try_gen_layout():
    # generate a linear layout
    num_nodes = random.randrange(7, 10)
    nodes = [
        {
            "id": i,
            "exits": [],
            "room": gen_room() if i < num_nodes - 1 else gen_empty_room(),
        }
        for i in range(num_nodes)
    ]

    assert len(nodes) >= 2

    cur_loc = (0, 0)
    nodes[0]["exits"].append({"id": -1, "dir": "s"})
    nodes[0]["loc"] = cur_loc

    for i, node in list(enumerate(nodes))[1:]:
        exits = ["n", "s", "e", "w"]

        prev_exit = nodes[i - 1]["exits"][0]["dir"]
        exits.remove(opposite(prev_exit))
        entrance = random.choice(exits)

        node["exits"].append({"id": i - 1, "dir": entrance})
        nodes[i - 1]["exits"].append({"id": i, "dir": opposite(entrance)})

        cur_loc = vec_sum(cur_loc, dir_to_vec(opposite(entrance)))
        node["loc"] = cur_loc

    return nodes


def verify_layout(layout) -> bool:
    locations = [node["loc"] for node in layout]
    loc_set = set(locations)

    return len(locations) == len(loc_set)


def gen_layout():
    layout = try_gen_layout()
    while not verify_layout(layout):
        layout = try_gen_layout()
    return layout


def main():
    import json

    print(json.dumps(gen_layout()))


if __name__ == "__main__":
    main()
