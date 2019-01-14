import random

from typing import List, Tuple

from constants import ROOM_SIZE
from dir_utils import dir_to_pos, dir_to_vec, opposite
from vec_utils import vec_mul, vec_sum


def mirror_h(blockers):
    return [(pos[0], ROOM_SIZE - 1 - pos[1]) for pos in blockers]


def mirror_v(blockers):
    return [(ROOM_SIZE - 1 - pos[0], pos[1]) for pos in blockers]


def gen_empty_room(exit_dirs):
    return {"blockers": [], "gaps": []}


def gen_obstacle_room(exit_dirs):
    num_blockers = random.randrange(6, 10)
    blockers = list(
        {
            (random.randrange(2, ROOM_SIZE // 2), random.randrange(2, ROOM_SIZE // 2))
            for _ in range(num_blockers)
        }
    )
    blockers.extend(mirror_v(blockers))
    blockers.extend(mirror_h(blockers))

    return {"blockers": blockers, "gaps": []}


def gen_divided_room(exit_dirs):
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

    return {"blockers": blockers, "gaps": []}


def gen_gap_platform_room(exit_dirs):
    gaps = [(1, i) for i in range(1, ROOM_SIZE // 2)]
    gaps.extend([(i, 1) for i in range(1, ROOM_SIZE // 2)])
    gaps.extend(
        [
            (ROOM_SIZE // 2 - 1, ROOM_SIZE // 2 - 1),
            (ROOM_SIZE // 2 - 2, ROOM_SIZE // 2 - 1),
            (ROOM_SIZE // 2 - 1, ROOM_SIZE // 2 - 2),
            (ROOM_SIZE // 2 - 2, ROOM_SIZE // 2 - 2),
            (ROOM_SIZE // 2 - 1, ROOM_SIZE // 2 - 3),
            (ROOM_SIZE // 2 - 3, ROOM_SIZE // 2 - 1),
        ]
    )
    gaps.extend([(2, 2), (2, 3), (3, 2)])
    gaps.extend(mirror_h(gaps))
    gaps.extend(mirror_v(gaps))

    for direction in exit_dirs:
        pre_doorway_pos = vec_sum(
            dir_to_pos(direction), dir_to_vec(opposite(direction))
        )
        if pre_doorway_pos in gaps:
            gaps.remove(pre_doorway_pos)

        pre_pre_doorway_pos = vec_sum(pre_doorway_pos, dir_to_vec(opposite(direction)))
        if pre_pre_doorway_pos in gaps:
            gaps.remove(pre_pre_doorway_pos)

    return {"blockers": [], "gaps": list(set(gaps))}


def gen_gap_bridge_room(exit_dirs):
    def gen_bridge(direction: str) -> List[Tuple[int, int]]:
        result = []

        primary_dir_vec = dir_to_vec(opposite(direction))
        secondary_dir_vec = dir_to_vec(
            {"n": "e", "s": "e", "e": "s", "w": "s"}[direction]
        )
        pre_doorway = vec_sum(dir_to_pos(direction), primary_dir_vec)

        result.extend(pre_doorway)
        result.extend(
            [
                vec_sum(pre_doorway, vec_mul(secondary_dir_vec, (i, i)))
                for i in range(ROOM_SIZE // 2)
            ]
        )
        result.extend(
            [
                vec_sum(
                    vec_sum(vec_sum(pre_doorway, primary_dir_vec), secondary_dir_vec),
                    vec_mul(secondary_dir_vec, (i, i)),
                )
                for i in range(ROOM_SIZE // 2 - 1)
            ]
        )

        return result

    gaps = []
    for r in range(1, ROOM_SIZE - 1):
        for c in range(1, ROOM_SIZE - 1):
            if not (
                r > 2
                and r < ROOM_SIZE - 3
                and (c == ROOM_SIZE // 2 or c == ROOM_SIZE // 2 - 1)
            ) and not (
                c > 2
                and c < ROOM_SIZE - 3
                and (r == ROOM_SIZE // 2 or r == ROOM_SIZE // 2 - 1)
            ):
                # Add gaps, leaving a '+' shaped bridge in the middle of the room
                gaps.append((r, c))

    for direction in exit_dirs:
        bridge = gen_bridge(direction)
        for pos in bridge:
            if pos in gaps:
                gaps.remove(pos)

    return {"blockers": [], "gaps": list(set(gaps))}


def gen_room(exit_dirs):
    population = [
        gen_empty_room,
        gen_divided_room,
        gen_gap_platform_room,
        gen_gap_bridge_room,
        gen_obstacle_room,
    ]
    cum_weights = [0.15, 0.3, 0.55, 0.7, 1]
    return random.choices(population, cum_weights=cum_weights)[0](exit_dirs)


def main():
    import json

    print(json.dumps(gen_room(["s", "e"])))


if __name__ == "__main__":
    main()
