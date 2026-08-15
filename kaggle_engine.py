#!/usr/bin/env python3
"""
Kaggle Competition Engine CLI
Provides utilities to list active competitions, inspect details, download datasets, and submit predictions.
"""

import argparse
import os
import sys
from kaggle.api.kaggle_api_extended import KaggleApi

def get_api():
    api = KaggleApi()
    api.authenticate()
    return api

def cmd_list(args):
    api = get_api()
    res = api.competitions_list(search=args.search, page=args.page)
    competitions = getattr(res, 'competitions', res)
    print(f"{'Ref/ID':<65} | {'Deadline':<20} | {'Category':<12} | {'Reward':<12} | {'Teams':<6}")
    print("-" * 125)
    for comp in competitions:
        ref = str(getattr(comp, 'ref', getattr(comp, 'id', 'N/A')))
        deadline = str(getattr(comp, 'deadline', 'N/A'))
        category = str(getattr(comp, 'category', 'N/A'))
        reward = str(getattr(comp, 'reward', 'N/A'))
        teams = str(getattr(comp, 'team_count', getattr(comp, 'teamCount', 'N/A')))
        print(f"{ref:<65} | {deadline:<20} | {category:<12} | {reward:<12} | {teams:<6}")

def cmd_info(args):
    api = get_api()
    res = api.competition_list_files(args.competition)
    files = getattr(res, 'files', res)
    print(f"Files for competition '{args.competition}':")
    for file in files:
        name = getattr(file, 'name', str(file))
        size = getattr(file, 'size', 'N/A')
        print(f"  - {name} ({size} bytes)")

def cmd_download(args):
    api = get_api()
    path = args.path or f"./data/{args.competition}"
    os.makedirs(path, exist_ok=True)
    print(f"Downloading files for '{args.competition}' to '{path}'...")
    api.competition_download_files(args.competition, path=path, unzip=True)
    print("Download completed successfully.")

def cmd_submit(args):
    api = get_api()
    print(f"Submitting '{args.file}' to competition '{args.competition}' with message: '{args.message}'...")
    api.competition_submit(file_name=args.file, message=args.message, competition=args.competition)
    print("Submission transmitted successfully.")

def main():
    parser = argparse.ArgumentParser(description="Kaggle Competition Engine CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-command help")

    # List
    p_list = subparsers.add_parser("list", help="List competitions")
    p_list.add_argument("--search", type=str, default="", help="Search query filter")
    p_list.add_argument("--page", type=int, default=1, help="Page number")
    p_list.set_defaults(func=cmd_list)

    # Info
    p_info = subparsers.add_parser("info", help="Get competition files info")
    p_info.add_argument("competition", type=str, help="Competition identifier (e.g. arc-prize-2026-arc-agi-3)")
    p_info.set_defaults(func=cmd_info)

    # Download
    p_dl = subparsers.add_parser("download", help="Download competition dataset")
    p_dl.add_argument("competition", type=str, help="Competition identifier")
    p_dl.add_argument("--path", type=str, default=None, help="Output directory path")
    p_dl.set_defaults(func=cmd_download)

    # Submit
    p_sub = subparsers.add_parser("submit", help="Submit prediction file")
    p_sub.add_argument("competition", type=str, help="Competition identifier")
    p_sub.add_argument("file", type=str, help="Path to submission CSV/file")
    p_sub.add_argument("message", type=str, help="Submission description message")
    p_sub.set_defaults(func=cmd_submit)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
