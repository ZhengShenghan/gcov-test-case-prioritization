import os
import csv

# Define the path to the test suites and results
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
test_suites_path = os.path.join(parent_dir, "test_suites")
benchmark_path = os.path.join(parent_dir, "benchmarks")
results_path = os.path.join(parent_dir, "stat", "fault_exposing_results.txt")


# Read the results from the results file
results = {}
with open(results_path, 'r') as file:
    for line in file:
        parts = line.strip().split()
        program = parts[0]
        test_suite = parts[2]
        faults = parts[-1][1:-1].split(',')
        faults_part = line.split(':')[-1].strip().strip('[]')
        faults_list = faults_part.split(', ')
        # print(faults_list)
        if faults[0] == '':
            faults = []
        if program not in results:
            results[program] = {}
        results[program][test_suite] = len(faults_list)

# Create a CSV file with the experimental results
csv_file = os.path.join(parent_dir, "stat", "experimental_results.csv")
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Program', 'Test Suite', 'Size', 'Faults Exposed'])

    for program in os.listdir(test_suites_path):
        program_path = os.path.join(test_suites_path, program)
        for test_suite_file in os.listdir(program_path):
            if test_suite_file.endswith('_test_suite.txt'):
                test_suite_name = test_suite_file.split('_test_suite')[0]
                test_suite_size = sum(1 for line in open(os.path.join(program_path, test_suite_file)))
                faults_exposed = results.get(program, {}).get(test_suite_name, 0)
                writer.writerow([program, test_suite_name, test_suite_size, faults_exposed])
        universe_test_suite_name = 'universe'
        universe_test_suite_file = 'universe.txt'
        universe_path = os.path.join(benchmark_path, program)
        universe_test_suite_size = sum(1 for line in open(os.path.join(universe_path, universe_test_suite_file)))
        universe_faults_exposed = results.get(program, {}).get(universe_test_suite_name, 0)
        writer.writerow([program,universe_test_suite_name,universe_test_suite_size,universe_faults_exposed])
print(f"CSV file generated: {csv_file}")
