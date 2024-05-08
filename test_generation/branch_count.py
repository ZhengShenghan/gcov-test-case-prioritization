import json
import os
import sys

def count_branches_in_json(json_data):
    branch_count = 0
    for file in json_data["files"]:
        for line in file["lines"]:
            branch_count += len(line["branches"])
    return branch_count


# Count the branches
program = sys.argv[1]
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
program_path = os.path.join(parent_dir, "benchmarks", program)
json_path = os.path.join(program_path, f"{program}.gcov.json")
with open(json_path,'r') as f:
    json_data = json.load(f)
branch_count = count_branches_in_json(json_data)
print(f"Total number of branches: {branch_count}")
