import json
import sys
import os

def count_branches_and_construct_set(json_data):
    branch_set = set()
    branch_count = 0
    for file in json_data["files"]:
        for line in file["lines"]:
            for i, branch in enumerate(line["branches"]):
                branch_id = f'{file["file"]}-{line["line_number"]}-{i}'
                if branch["count"] > 0:
                    branch_set.add(branch_id + "-T")
                else:
                    branch_set.add(branch_id + "-F")
                branch_count += 1
    return branch_count, branch_set

# Load the JSON data from the file
program = sys.argv[1]
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
program_path = os.path.join(parent_dir, "benchmarks", program)
json_path = os.path.join(program_path, f"{program}.gcov.json")
with open(json_path, 'r') as f:
    json_data = json.load(f)

# Count the branches and construct the set
total_branches, branch_set = count_branches_and_construct_set(json_data)
print(f"Total branches in JSON file: {total_branches}")

# Write the branch set to a text file
with open('branch_ids_json.txt', 'w') as f:
    for branch_id in branch_set:
        f.write(f"{branch_id}\n")

print(f"Branch IDs have been written to branch_ids.txt")
