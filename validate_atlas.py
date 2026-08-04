#!/usr/bin/env python3
import os
import re
import sys

def slugify(text):
    # Lowercase
    s = text.lower()
    # Remove anything not alphanumeric, space, or hyphen
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    # Replace spaces with hyphens
    s = re.sub(r'\s+', '-', s)
    # Replace multiple hyphens with single hyphen
    s = re.sub(r'-+', '-', s)
    return s

def run_validation():
    print("==================================================")
    print("Running Systemic Intelligence Atlas Validation Suite")
    print("==================================================")

    files = [
        "THE_ATLAS_OF_SYSTEMIC_INTELLIGENCE.md",
        "universal_leverage_atlas (1).md",
        "universal_leverage_atlas (3).md",
        "universal_leverage_atlas_v6.md"
    ]
    readme_path = "README.md"

    # 1. Check all files existence
    for path in files + [readme_path]:
        if not os.path.exists(path):
            print(f"[FAIL] Missing file: {path}")
            return False
    print("[PASS] All files exist.")

    # 2. Check index links in README.md point to THE_ATLAS_OF_SYSTEMIC_INTELLIGENCE.md
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    with open("THE_ATLAS_OF_SYSTEMIC_INTELLIGENCE.md", "r", encoding="utf-8") as f:
        atlas_content = f.read()

    atlas_headings_raw = re.findall(r'^##\s+([0-9]+\.\s*.*)', atlas_content, re.MULTILINE)
    valid_slugs = {slugify(h): h for h in atlas_headings_raw}

    readme_links = re.findall(r'\[[0-9]+\.\s*[^\]]+\]\(\./THE_ATLAS_OF_SYSTEMIC_INTELLIGENCE\.md#(.*)\)', readme_content)

    if len(readme_links) != 52:
        print(f"[FAIL] Expected 52 index links in README.md, but found {len(readme_links)}")
        return False

    for anchor in readme_links:
        if anchor not in valid_slugs:
            print(f"[FAIL] README.md has invalid/mismatched anchor link: #{anchor}")
            return False
    print("[PASS] README.md index links map perfectly to THE_ATLAS_OF_SYSTEMIC_INTELLIGENCE.md.")

    # 3. Process and validate each file
    for path in files:
        print(f"\nValidating file: {path}")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract entry headings
        headings = re.findall(r'^##\s+([0-9]+)\.\s*(.*)', content, re.MULTILINE)
        print(f"  Found {len(headings)} entries.")

        # Check for em-dashes
        headings_full = re.findall(r'^##\s+.*', content, re.MULTILINE)
        for h in headings_full:
            if "—" in h:
                print(f"  [FAIL] Heading contains em-dash '—': {h}")
                return False

        # Specific file structural validation
        if path == "THE_ATLAS_OF_SYSTEMIC_INTELLIGENCE.md":
            raw_entries = re.split(r'^## ', content, flags=re.MULTILINE)[1:]
            entries = [entry for entry in raw_entries if re.match(r'^[0-9]+[a-z]?\.', entry.strip())]

            required_sections = [
                "Category / Strength",
                "Move Classification",
                "### The Five Questions (From Abstraction to Implementation)",
                "### Boundary Conditions",
                "- **Where the Principle Breaks:**",
                "### Detailed Mechanism & Application",
                "- **What the Mechanism Is:**",
                "- **Why It Works:**",
                "- **How It Fails:**",
                "- **Technical Expertise Implementation:**",
                "- **How Far the Analogy Can Safely Extend:**",
                "- **Where the Analogy Breaks:**"
            ]
            for idx, entry_text in enumerate(entries, 1):
                first_line = entry_text.split('\n')[0]
                for section in required_sections:
                    if section not in entry_text:
                        print(f"  [FAIL] Entry {idx} (\"{first_line}\") is missing: \"{section}\"")
                        return False
            print(f"  [PASS] All {len(entries)} entries possess 100% complete structured metadata and subheadings.")

        elif path == "universal_leverage_atlas (1).md":
            raw_entries = re.split(r'^## ', content, flags=re.MULTILINE)[1:]
            entries = [entry for entry in raw_entries if re.match(r'^[0-9]+[a-z]?\.', entry.strip())]

            required_sections = [
                "Move Classification",
                "### The Five Questions (From Abstraction to Implementation)",
                "### Detailed Mechanism & Application",
                "- **What the Mechanism Is:**",
                "- **Why It Works:**",
                "- **How It Fails:**",
                "- **Technical Expertise Implementation:**",
                "- **How Far the Analogy Can Safely Extend:**",
                "- **Where the Analogy Breaks:**"
            ]
            for idx, entry_text in enumerate(entries, 1):
                first_line = entry_text.split('\n')[0]
                for section in required_sections:
                    if section not in entry_text:
                        print(f"  [FAIL] Entry {idx} (\"{first_line}\") is missing: \"{section}\"")
                        return False
            print(f"  [PASS] All {len(entries)} entries possess 100% complete structured metadata and subheadings.")

        elif path in ["universal_leverage_atlas (3).md", "universal_leverage_atlas_v6.md"]:
            # Check simpler structure: must have **Technical Expertise Implementation...:**
            raw_entries = re.split(r'^## ', content, flags=re.MULTILINE)[1:]
            entries = [entry for entry in raw_entries if re.match(r'^[0-9]+[a-z]?\.', entry.strip())]

            for idx, entry_text in enumerate(entries, 1):
                first_line = entry_text.split('\n')[0]
                # Validate Technical Expertise Implementation
                if "**Technical Expertise Implementation" not in entry_text:
                    print(f"  [FAIL] Entry {idx} (\"{first_line}\") is missing 'Technical Expertise Implementation' section.")
                    return False
            print(f"  [PASS] All {len(entries)} entries possess Technical Expertise Implementation.")

    print("\n==================================================")
    print("ALL FILES ARE 100% VALIDATED AND IN COMPLIANCE!")
    print("==================================================")
    return True

if __name__ == "__main__":
    success = run_validation()
    if not success:
        sys.exit(1)
    sys.exit(0)
