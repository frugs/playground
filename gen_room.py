import random

from constants import ROOM_SIZE


def mirror_h(blockers):
    return [(pos[0], ROOM_SIZE - 1 - pos[1]) for pos in blockers]


def mirror_v(blockers):
    return [(ROOM_SIZE - 1 - pos[0], pos[1]) for pos in blockers]


def gen_empty_room():
    return {"blockers": []}


def gen_obstacle_room():
    num_blockers = random.randrange(6, 10)
    blockers = list(
        {
            (random.randrange(2, ROOM_SIZE // 2), random.randrange(2, ROOM_SIZE // 2))
            for _ in range(num_blockers)
        }
    )
    blockers.extend(mirror_v(blockers))
    blockers.extend(mirror_h(blockers))

    return {"blockers": blockers}


def gen_divided_room():
    tl_blockers = [(i, ROOM_SIZE // 2) for i in range(ROOM_SIZE // 2)]
    br_blockers = mirror_v(mirror_h(tl_blockers))

    tr_blockers = mirror_h(([(ROOM_SIZE // 2, i) for i in range(ROOM_SIZE // 2)]))
    bl_blockers = mirror_v(mirror_h(tr_blockers))

    blockers = tl_blockers + br_blockers + tr_blockers + bl_blockers

    random.shuffle(blockers)
    unblocked = 0
    unblock_h = random.randrange(2, ROOM_SIZE // 2 - 2)
    unblock_v = random.randrange(2, ROOM_SIZE // 2 - 2)
    for pos in blockers:
        if unblocked < 3 and (
            pos[0] == unblock_h
            or pos[0] == ROOM_SIZE - 1 - unblock_h
            or pos[1] == unblock_v
            or pos[1] == ROOM_SIZE - 1 - unblock_v
        ):
            unblocked += 1
            blockers.remove(pos)

    return {"blockers": blockers}


def gen_room():
    population = [gen_empty_room, gen_divided_room, gen_obstacle_room]
    cum_weights = [0.2, 0.4, 1]
    return random.choices(population, cum_weights=cum_weights)[0]()


def main():
    import json

    print(json.dumps(gen_room()))


if __name__ == "__main__":
    main()
