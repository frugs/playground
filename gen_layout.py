import random

from dir_utils import opposite, dir_to_vec
from gen_room import gen_room, gen_empty_room
from vec_utils import vec_sum


def try_gen_layout():
    # generate a linear layout
    num_nodes = random.randrange(7, 10)
    nodes = [{"id": i, "exits": []} for i in range(num_nodes)]

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

    for i, node in enumerate(nodes):
        node["room"] = (
            gen_room([ex["dir"] for ex in node["exits"]])
            if i < num_nodes - 1
            else gen_empty_room([])
        )

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
