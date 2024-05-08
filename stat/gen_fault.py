#!/usr/bin/env python3

import os
import subprocess
import re

# Define the path to the benchmarks and test suites
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
print("Parent directory:", parent_dir)
benchmark_path = os.path.join(parent_dir, "benchmarks")
print("Benchmark directory:", benchmark_path)
test_suites_path = os.path.join(parent_dir, "test_suites")
print("Test suite directory:", test_suites_path)
programs = ['printtokens2', 'replace','tcas','schedule','schedule2','printtokens','totinfo']
# Function to compile a program
def compile_program(program_path, program = ''):
    if program in programs:# for fault program path
        print("program path", program_path)
        fault_folder = os.path.basename(program_path)
        print("fault folder name", fault_folder)
        if program == 'totinfo' or program == 'replace':
            compile_command = f"gcc -Wno-return-type -fprofile-arcs -ftest-coverage -g -o {os.path.join(benchmark_path, program, fault_folder, program)} {os.path.join(benchmark_path, program, fault_folder, program)}.c -lm"
        else:
            compile_command = f"gcc -Wno-return-type -fprofile-arcs -ftest-coverage -g -o {os.path.join(benchmark_path, program, fault_folder, program)} {os.path.join(benchmark_path, program, fault_folder, program)}.c"
        print("debug info for compile", compile_command)
        subprocess.run(compile_command, shell=True, check=True)
    else: # for benchmark program
        print("program path", program_path)
        program = os.path.basename(program_path)
        if program == 'totinfo' or program == 'replace':
            compile_command = f"gcc -Wno-return-type -fprofile-arcs -ftest-coverage -g -o {os.path.join(benchmark_path, program, program)} {os.path.join(benchmark_path, program, program)}.c -lm"
        else:
            compile_command = f"gcc -Wno-return-type -fprofile-arcs -ftest-coverage -g -o {os.path.join(benchmark_path, program, program)} {os.path.join(benchmark_path, program, program)}.c"
        print("debug info for compile", compile_command)
        subprocess.run(compile_command, shell=True, check=True)

# Function to run a test suite and check for exposed faults
def run_test_suite(program, test_suite):
    original_program_path = f"{benchmark_path}/{program}"
    test_suite_path = f"{test_suites_path}/{program}/{test_suite}_test_suite.txt"
    print("program input for run_test_suite", program)
    # Compile the original program
    compile_program(original_program_path)
    print("original program path", original_program_path)
    # Run the test suite on the original program
    original_outputs = []
    with open(test_suite_path, 'r') as tests:
        for test in tests:
            test = test.strip()
            print("test case", test)
            parts = test.split('<')
            print('split by <',parts)
            args = parts[0].split()
            input_file = None
            if len(parts) > 1:
                input_filename = parts[-1].strip()
                input_file_path = os.path.join(original_program_path, input_filename)
                print("input filename", input_filename)
                print("input file path", input_file_path)
                input_file = open(input_file_path, 'r')
            try:
                result = subprocess.run([f"{original_program_path}/{program}"] + args, stdin=input_file, capture_output=True, text=True)
                # output = result.stdout.strip()
                output = f"{result.stdout.strip()}, Exit code: {result.returncode}"
                print("output in try", output)
            except subprocess.CalledProcessError as e:
                # output = e.stderr.strip()
                output = f"{e.stderr.strip()}, Exit code: {e.returncode}"
                print("output in except", output)
            finally:
                if input_file:
                    input_file.close()
            original_outputs.append(output)

    # Check for exposed faults in each faulty version
    exposed_faults = []
    for version in os.listdir(original_program_path):
        if version.startswith("v"):
            faulty_program_path = f"{original_program_path}/{version}"
            print("faulty program path", faulty_program_path)
            compile_program(faulty_program_path, program)
            print("fault program compiled!")
            # Run the test suite on the faulty version
            with open(test_suite_path, 'r') as tests:
                for i, test in enumerate(tests):
                    test = test.strip()
                    print("test case", test)
                    parts = test.split('<')
                    print('split by <',parts)
                    args = parts[0].split()
                    input_file = None
                    # Check if there is input redirection in the test case
                    if len(parts) > 1:
                        input_filename = parts[-1].strip()
                        # Construct the absolute path to the input file
                        input_file_path = os.path.join(original_program_path, input_filename)
                        input_file = open(input_file_path, 'r')
                        # Remove the redirection part from the arguments
                    try:
                        result = subprocess.run([f"{faulty_program_path}/{program}"] + args, stdin=input_file, capture_output=True, text=True)
                        # faulty_output = result.stdout.strip()
                        faulty_output = f"{result.stdout.strip()}, Exit code: {result.returncode}"
                        print("output in try", faulty_output)
                    except subprocess.CalledProcessError as e:
                        # faulty_output = e.stderr.strip()
                        faulty_output = f"{e.stderr.strip()}, Exit code: {e.returncode}"
                        print("output in except", faulty_output)
                    finally:
                        if input_file:
                            input_file.close()

                    # Compare the output with the original program
                    if faulty_output != original_outputs[i]:
                        exposed_faults.append(version)
                        break

    return exposed_faults

def run_universe_test_suite(program):
    original_program_path = f"{benchmark_path}/{program}"
    test_suite_path = f"{benchmark_path}/{program}/universe.txt"
    print("program input for run_test_suite", program)
    # Compile the original program
    compile_program(original_program_path)
    print("original program path", original_program_path)
    # Run the test suite on the original program
    original_outputs = []
    with open(test_suite_path, 'r') as tests:
        for test in tests:
            test = test.strip()
            print("test case", test)
            parts = test.split('<')
            print('split by <',parts)
            args = parts[0].split()
            input_file = None
            if len(parts) > 1:
                input_filename = parts[-1].strip()
                input_file_path = os.path.join(original_program_path, input_filename)
                print("input filename", input_filename)
                print("input file path", input_file_path)
                input_file = open(input_file_path, 'r')
            try:
                result = subprocess.run([f"{original_program_path}/{program}"] + args, stdin=input_file, capture_output=True, text=True)
                # output = result.stdout.strip()
                output = f"{result.stdout.strip()}, Exit code: {result.returncode}"
                print("output in try", output)
            except subprocess.CalledProcessError as e:
                # output = e.stderr.strip()
                output = f"{e.stderr.strip()}, Exit code: {e.returncode}"
                print("output in except", output)
            except UnicodeDecodeError as e:
                faulty_output = "Error: UnicodeDecodeError"
                print("output in except", faulty_output)
            finally:
                if input_file:
                    input_file.close()
            original_outputs.append(output)
    # Check for exposed faults in each faulty version
    exposed_faults = []
    for version in os.listdir(original_program_path):
        if version.startswith("v"):
            faulty_program_path = f"{original_program_path}/{version}"
            print("faulty program path", faulty_program_path)
            compile_program(faulty_program_path, program)
            print("fault program compiled!")
            # Run the test suite on the faulty version
            with open(test_suite_path, 'r') as tests:
                for i, test in enumerate(tests):
                    test = test.strip()
                    print("test case", test)
                    parts = test.split('<')
                    print('split by <',parts)
                    args = parts[0].split()
                    input_file = None
                    # Check if there is input redirection in the test case
                    if len(parts) > 1:
                        input_filename = parts[-1].strip()
                        # Construct the absolute path to the input file
                        input_file_path = os.path.join(original_program_path, input_filename)
                        input_file = open(input_file_path, 'r')
                        # Remove the redirection part from the arguments
                    try:
                        result = subprocess.run([f"{faulty_program_path}/{program}"] + args, stdin=input_file, capture_output=True, text=True)
                        faulty_output = f"{result.stdout.strip()}, Exit code: {result.returncode}"
                        print("output in try", faulty_output)
                    except subprocess.CalledProcessError as e:
                        faulty_output = f"{e.stderr.strip()}, Exit code: {e.returncode}"
                        print("output in except", faulty_output)
                    except UnicodeDecodeError as e:
                        faulty_output = "Error: UnicodeDecodeError"
                        print("output in except", faulty_output)
                    finally:
                        if input_file:
                            input_file.close()

                    # Compare the output with the original program
                    if faulty_output != original_outputs[i]:
                        exposed_faults.append(version)
                        break

    return exposed_faults
# Evaluate the fault-exposing potential for each test suite
# Define the output file path
output_file_path = os.path.join(parent_dir, "stat", "fault_exposing_results.txt")

# Open the output file for writing
with open(output_file_path, 'w') as output_file:
    for program in programs:
        for test_suite in os.listdir(f"{test_suites_path}/{program}"):
            if test_suite.endswith("_test_suite.txt"):
                test_suite_name = test_suite.split('_test_suite')[0]
                print("test suite name", test_suite_name)
                exposed_faults = run_test_suite(program, test_suite_name)
                print(f"{program} - {test_suite_name} test suite exposes faults: {exposed_faults}")
                output_file.write(f"{program} - {test_suite_name} test suite exposes faults: {exposed_faults}\n")
                # print(1)
        # use universe test suites
        universe_test_suite_name = 'universe'
        print("test suite name", universe_test_suite_name)
        exposed_faults = run_universe_test_suite(program)
        print(f"{program} - {universe_test_suite_name} test suite exposes faults: {exposed_faults}")
        output_file.write(f"{program} - {universe_test_suite_name} test suite exposes faults: {exposed_faults}\n")
