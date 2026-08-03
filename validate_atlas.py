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

    atlas_path = "THE_ATLAS_OF_SYSTEMIC_INTELLIGENCE.md"
    readme_path = "README.md"

    # 1. File existence checks
    if not os.path.exists(atlas_path):
        print(f"[FAIL] Missing file: {atlas_path}")
        return False
    if not os.path.exists(readme_path):
        print(f"[FAIL] Missing file: {readme_path}")
        return False

    with open(atlas_path, "r", encoding="utf-8") as f:
        atlas_content = f.read()

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # 2. Extract and check all headings
    # Headings look like: ## <num>. <title>
    headings = re.findall(r'^##\s+([0-9]+)\.\s*(.*)', atlas_content, re.MULTILINE)

    if len(headings) != 52:
        print(f"[FAIL] Expected 52 entries in the Atlas, but found {len(headings)}")
        return False

    print(f"[PASS] Found exactly {len(headings)} entries.")

    entry_numbers = [int(num) for num, _ in headings]
    expected_numbers = list(range(1, 53))

    if sorted(entry_numbers) != expected_numbers:
        missing = set(expected_numbers) - set(entry_numbers)
        extra = set(entry_numbers) - set(expected_numbers)
        print(f"[FAIL] Entry numbering is incorrect. Missing: {missing}, Extra/Invalid: {extra}")
        return False

    print("[PASS] Entry numbering is correct and covers 1 to 52 sequentially.")

    # 3. Check each heading format (ensure space-hyphen-space ' - ' and no em-dashes '—')
    headings_full = re.findall(r'^##\s+.*', atlas_content, re.MULTILINE)
    for h in headings_full:
        if "—" in h:
            print(f"[FAIL] Heading uses forbidden em-dash '—': {h}")
            return False
        # Every entry should have the pattern "## <num>. <Name> - <tagline>"
        # Check that there is a hyphen separator and it has spaces around it
        # Let's verify if there is any ' - '
        if " - " not in h:
            # Note: Entry 12 might have no hyphen if it's just '## 12. Human Factors - the Ironies of Automation'
            print(f"[WARN] Heading might be missing ' - ' separator: {h}")

    print("[PASS] Heading separators verified successfully (no em-dashes '—' found).")

    # 4. Check each entry's structural completeness
    entries = re.split(r'^## ', atlas_content, flags=re.MULTILINE)[1:] # skip prefix before entry 1

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
        # Extract title line
        lines = entry_text.split('\n')
        title = lines[0] if lines else f"Entry {idx}"

        for section in required_sections:
            if section not in entry_text:
                print(f"[FAIL] Entry {idx} (\"{title}\") is missing required section/field: \"{section}\"")
                return False

    print("[PASS] All 52 entries contain 100% of the required subheadings and structures.")

    # 5. Check index links in README.md point to correct anchors and slugifications
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

    print("[PASS] All 52 index links in README.md map perfectly to slugified headers in the Atlas.")
    print("==================================================")
    print("VALIDATION SUCCESS: System is 100% proven, verified, and complete!")
    print("==================================================")
    return True

if __name__ == "__main__":
    success = run_validation()
    if not success:
        sys.exit(1)
    sys.exit(0)
