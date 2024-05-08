#!/usr/bin/env python

import os
import sys
import random
import subprocess
import json

def count_statement_and_construct_set(json_data):
    statement_set = set()
    statement_count = 0
    for file in json_data["files"]:
        for line in file["lines"]:
            statement_count += 1
            statement_id = f'{file["file"]}-{line["line_number"]}'
            if line["count"] > 0:
                statement_set.add(statement_id + "-T")
            else:
                statement_set.add(statement_id + "-F")
            statement_count += 1
    return statement_count, statement_set

program = sys.argv[1]
method = sys.argv[2]
print("Program:", program)
print("Method:", method)
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
print("Parent directory:", parent_dir)
benchmark_path = os.path.join(parent_dir, "benchmarks")
print("Benchmark directory:", benchmark_path)
program_path = os.path.join(parent_dir, "benchmarks", program)
print("program path", program_path)
test_suite_path = os.path.join(parent_dir, "test_suites", program)
print("Testsuite directory:", test_suite_path)

with open(f"{benchmark_path}/{program}/universe.txt") as f:
    tests = f.read().splitlines()


# Get the number of statement
print("start collecting statement info")
if program == 'totinfo' or program == 'replace':
    compile_command = f"gcc -Wno-return-type -fprofile-arcs -ftest-coverage -g -o {os.path.join(benchmark_path, program, program)} {os.path.join(benchmark_path, program, program)}.c -lm"
else:
    compile_command = f"gcc -Wno-return-type -fprofile-arcs -ftest-coverage -g -o {os.path.join(benchmark_path, program, program)} {os.path.join(benchmark_path, program, program)}.c"

cd_command = f'cd {benchmark_path}/{program}'
gen_command = f'gcov {program}.c'
gen_statement_command = f'gcov -b -c {program}'
exe_command = f'./{program} {tests[0]}'
# json_command = f'gcov -j -i -b -c {program}'
json_command = f'gcov --json-format -b -c {program}'
unzip_command = f'gunzip {program}.gcov.json.gz'

# compile
#print("compile command", compile_command)
os.system(compile_command)
#print("Compile Done!")
# generate gcov file
#print("gcov command", gen_command)
os.system(f'{cd_command};{gen_command}')
#print("gcov generated!")

# execute once to generate gcda file
#print("execute command", exe_command)
#subprocess.run(exe_command,shell=True, cwd=program_path, check=True)
#print("execute done!")

# add statement info to gcov
#print("gcov add statement command", gen_statement_command)
output = subprocess.check_output(f'{cd_command};{gen_statement_command}', shell=True, text=True)
#print("output", output)
#print("statement info added!")
# count statement number
num_statement = 0
for line in output.splitlines():
    if "statement executed" in line:
        num_statement = line.split()[-1]
        print(f"Number of statement: {num_statement}")
        break
# remove .gcov .gcda .gcno in dir
for extension in ['.c.gcov', '.gcda', '.gcno']:
    file_path = os.path.join(program_path, f"{program}{extension}")
    if os.path.exists(file_path):
        os.remove(file_path)
print("delete gcov in working dir")
# move the .gcov .gcda . gcno in scrupt dir to work dir
for extension in ['.c.gcov', '.gcda', '.gcno']:
    file_path = os.path.join(current_dir, f"{program}{extension}")
    if os.path.exists(file_path):
        os.system(f'mv {file_path} {program_path}')
print("move to working dir!")

# # generate json.zip
# os.system(f'{cd_command};{json_command}')
# print("json.zip generated!")

# # unzip json.zip
# os.system(f'{cd_command};{unzip_command}')
# print("unzip done!")

# remove json for multiple rounds
json_remove_path = os.path.join(program_path, f"{program}.gcov.json")
print("json remove path", json_remove_path)
if os.path.exists(json_remove_path):
    os.remove(json_remove_path)

# get statement coverage for each test
test_coverage_map = dict()
whole_statement_coverage = set()
for test in tests:
    # remove gcda file
    remove_path = os.path.join(program_path, f"{program}.gcda")
    if os.path.exists(remove_path):
        os.remove(remove_path)
    # remove json
    json_remove_path = os.path.join(program_path, f"{program}.gcov.json")
    print("json remove path", json_remove_path)
    if os.path.exists(json_remove_path):
        os.remove(json_remove_path)
    # execute the test gen new gcda file
    exe_command = exe_command = f'./{program} {test}'
    try:
        result = subprocess.run(exe_command,shell=True, cwd=program_path, check=True)
    # Check the exit code and handle errors
    except subprocess.CalledProcessError as e:
        print(f"Error executing test: {test}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
    # move gcda file to working dir
    mv_path = os.path.join(current_dir, f"{program}.gcda")
    if os.path.exists(mv_path):
        os.system(f'mv {mv_path} {program_path}')
    # generate json file
    os.system(f'{cd_command};{json_command}')
    os.system(f'{cd_command};{unzip_command}')
    # call coverage function
    with open(os.path.join(program_path,f'{program}.gcov.json'),'r') as f:
        json_data = json.load(f)
    _, statement_coverage = count_statement_and_construct_set(json_data)
    whole_statement_coverage = whole_statement_coverage | (statement_coverage)
    test_coverage_map[test] = statement_coverage
    
print("Number of elements in the set:", len(whole_statement_coverage))

# Write the statement set to a text file
with open('statement_ids_compute.txt', 'w') as f:
    for statement_id in whole_statement_coverage:
        f.write(f"{statement_id}\n")

print(f"statement IDs have been written to statement_ids.txt")
# Prioritization methods
# methods = ['random', 'total', 'add']
# for method in methods:
if method == 'total':
    
    # Sort the tests based on the number of unique statement they cover
    sorted_tests = sorted(tests, key=lambda test: len(test_coverage_map[test]), reverse=True)

    # Initialize the set to keep track of covered statement
    covered_statement = set()

    # Initialize the list to keep track of selected tests for the test suite
    selected_tests = []

    # Iterate through the sorted tests
    for test in sorted_tests:
        test_statement = test_coverage_map[test]
        # Check if the test covers any new statement
        if not test_statement.issubset(covered_statement):
            # Add the test to the selected tests list
            selected_tests.append(test)
            # Update the set of covered statement
            covered_statement.update(test_statement)#     # Write the selected test cases to the file
#     os.makedirs(f'{test_suite_path}/{program}', exist_ok=True)
#     with open(f'{test_suite_path}/{program}/{method}_statement.txt', 'w') as f:
#         for i in order:
#             f.write(test[i] + '\n')


    print("Selected tests for the total prioritization strategy:")
    for test in selected_tests:
        print(test)
    output_path = os.path.join(test_suite_path, "statement_total_test_suite.txt")
    with open(output_path, 'w') as f:
        for test in selected_tests:
            f.write(test + '\n')
elif method == 'random':
    # Create a copy of the tests list and shuffle it
    shuffled_tests = tests.copy()
    random.shuffle(shuffled_tests)

    # Initialize the set to keep track of covered statement
    covered_statement = set()

    # Initialize the list to keep track of selected tests for the test suite
    selected_tests = []

    # Iterate through the shuffled tests
    for test in shuffled_tests:
        test_statement = test_coverage_map[test]
        # Check if the test covers any new statement
        if not test_statement.issubset(covered_statement):
            # Add the test to the selected tests list
            selected_tests.append(test)
            # Update the set of covered statement
            covered_statement.update(test_statement)
    print("Selected tests for the random prioritization strategy:")
    for test in selected_tests:
        print(test)
    output_path = os.path.join(test_suite_path, "statement_random_test_suite.txt")
    with open(output_path,'w') as f:
        for test in selected_tests:
            f.write(test + '\n')


if method == 'add':
    # Initialize the set to keep track of covered statement
    covered_statement = set()

    # Initialize the list to keep track of selected tests for the test suite
    selected_tests = []

    # Iterate until all statement are covered or all tests have been considered
    while covered_statement != whole_statement_coverage and tests:
        # Select the test that covers the most additional statement
        best_test = max(tests, key=lambda test: len(test_coverage_map[test] - covered_statement))
        # Update the set of covered statement and the list of selected tests
        covered_statement.update(test_coverage_map[best_test])
        selected_tests.append(best_test)
        # Remove the selected test from the list of tests
        tests.remove(best_test)

    print("Selected tests for the add prioritization strategy:")
    for test in selected_tests:
        print(test)
    output_path = os.path.join(test_suite_path, "statement_add_test_suite.txt")
    with open(output_path, 'w') as f:
        for test in selected_tests:
            f.write(test + '\n')
    
