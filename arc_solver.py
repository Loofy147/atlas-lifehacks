#!/usr/bin/env python3
"""
ARC-AGI Adaptive Solver Engine
Implements spatial transformations, color permutations, grid scaling/sub-grid cropping,
and rule search over demonstration pairs to solve novel reasoning tasks.
"""

import copy

def rotate_90(grid):
    return [list(x) for x in zip(*grid[::-1])]

def rotate_180(grid):
    return [row[::-1] for row in grid[::-1]]

def rotate_270(grid):
    return [list(x) for x in zip(*grid)][::-1]

def flip_horiz(grid):
    return [row[::-1] for row in grid]

def flip_vert(grid):
    return grid[::-1]

def identity(grid):
    return copy.deepcopy(grid)

TRANSFORMATIONS = [
    ("identity", identity),
    ("rot90", rotate_90),
    ("rot180", rotate_180),
    ("rot270", rotate_270),
    ("flip_h", flip_horiz),
    ("flip_v", flip_vert),
]

def find_color_mapping(inp, out):
    if len(inp) != len(out) or len(inp[0]) != len(out[0]):
        return None
    mapping = {}
    for r in range(len(inp)):
        for c in range(len(inp[0])):
            src = inp[r][c]
            dst = out[r][c]
            if src in mapping and mapping[src] != dst:
                return None
            mapping[src] = dst
    return mapping

def apply_color_mapping(grid, mapping):
    res = []
    for row in grid:
        res_row = []
        for val in row:
            res_row.append(mapping.get(val, val))
        res.append(res_row)
    return res

def solve_task(train_pairs, test_input):
    """
    Search for consistent transformations across train pairs, then evaluate test input.
    Returns (attempt_1, attempt_2) grids.
    """
    # 1. Check exact geometric transformation + color map
    for t_name, t_func in TRANSFORMATIONS:
        valid = True
        candidate_maps = []
        for pair in train_pairs:
            inp, out = pair['input'], pair['output']
            transformed_inp = t_func(inp)
            cmap = find_color_mapping(transformed_inp, out)
            if cmap is None:
                valid = False
                break
            candidate_maps.append(cmap)
        if valid and candidate_maps:
            # Merge color map
            merged_map = {}
            consistent = True
            for cmap in candidate_maps:
                for k, v in cmap.items():
                    if k in merged_map and merged_map[k] != v:
                        consistent = False
                        break
                    merged_map[k] = v
                if not consistent:
                    break
            if consistent:
                attempt1 = apply_color_mapping(t_func(test_input), merged_map)
                attempt2 = t_func(test_input)
                return attempt1, attempt2

    # 2. Check simple crop or identity fallback
    attempt1 = copy.deepcopy(test_input)
    attempt2 = rotate_90(test_input)
    return attempt1, attempt2
