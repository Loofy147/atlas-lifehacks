#!/usr/bin/env python3
"""
ARC Task Solver Runner
Loads test challenges, executes arc_solver task inference, and formats adaptive submission JSON.
"""

import json
import os
import sys
from arc_solver import solve_task

def main():
    data_dir = "./data/arc-prize-2026-arc-agi-2"
    challenges_path = os.path.join(data_dir, "arc-agi_test_challenges.json")
    output_path = "adaptive_submission.json"

    if not os.path.exists(challenges_path):
        print(f"Error: Challenges file not found at '{challenges_path}'.")
        sys.exit(1)

    print(f"Loading challenges from '{challenges_path}'...")
    with open(challenges_path, "r") as f:
        challenges = json.load(f)

    submission = {}
    total = len(challenges)
    print(f"Processing {total} tasks with adaptive solver...")

    for task_id, task_data in challenges.items():
        train_pairs = task_data.get("train", [])
        test_inputs = task_data.get("test", [])

        task_preds = []
        for test_item in test_inputs:
            test_inp = test_item["input"]
            a1, a2 = solve_task(train_pairs, test_inp)
            task_preds.append({
                "attempt_1": a1,
                "attempt_2": a2
            })
        submission[task_id] = task_preds

    print(f"Writing adaptive predictions for {len(submission)} tasks to '{output_path}'...")
    with open(output_path, "w") as f:
        json.dump(submission, f)

    print("Task processing complete.")

if __name__ == "__main__":
    main()
