(1)Prerequisites  
ubuntu 20.04, gcc (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0  

(2)Introduction
The repo is built for comparing the effectiveness of different kinds of test case prioritization
methods in exposing faults via multiple coverage criteria. The whole repo is based on UNIX tool called [gcov](https://gcc.gnu.org/onlinedocs/gcc/Gcov.html). It's from a course project[1].

It has provided with a set of 7 relatively small benchmark programs written in C. Each program
is associated with a set of faults and a set of test cases. 
Program Name  # of Available Faults  # of Available Test Cases
tcas          41                     1590
totinfo       23                     1026
schedule      9                      2634
schedule2     9                      2679
printtokens   7                      4072
printtokens2  9                      4057
replace       31                     5542

All benchmark programs are contained within a folder named "benchmarks". Within this folder,
there is a subdirectory for each of the seven benchmark programs.
Within the subdirectory for a benchmark program, you will find the following folders and files:
1. The benchmark program
The benchmark program is specified as a .c file, and possibly one or more associated .h
files.
Example: Program tcas is located in the file "benchmarks/tcas/tcas.c" (there are no
associated .h files for this program).
2. The set of faults
The faults are specified as a set of "faulty versions" that are associated with each
benchmark program (one fault per faulty version). Each faulty version is contained
within a folder that is named with the letter "v", followed by the number of the faulty
version. The program code for each faulty version is identical to that of the (original)
benchmark program, except for a slight modification to the code that represents the fault.
Example: Program tcas is associated with 41 different faulty versions, contained in the
folders named "benchmarks/tcas/v1" through "benchmarks/tcas/v41".
3. The set of test cases
The test cases are specified in the file "universe.txt" (one test case per line).
Example: The test cases for program tcas are contained in the file
"benchmarks/tcas/universe.txt".
4. Test case input file directories
Any other folders that may be present contain input files that are used by the associated
test cases. You don't need to do anything with these folders except to make sure they are
present in the current working directory when running the benchmark program.

Coverage Criteria
We will consider 2 different kinds of coverage criteria in this project.
1. Statement coverage. Statement coverage is the selection of tests so that every statement
has been executed at least once.
2. Branch coverage. Branch coverage is a requirement according to which, for each
conditional branch in the program (such as due to if statements, loops etc.), the branch
condition must have been true at least once and false at least once during testing.

Test Case Prioritization
Test case prioritization techniques schedule test cases in an execution order according to some
criterion. Here are the prioritization methods you will use:
1. Random prioritization. Randomly order the test cases in a test suite.
2. Total Coverage prioritization. Prioritize test cases according to the total number of
statements/branches they cover simply by sorting them in order of their total
statement/branch coverage.
3. Additional Coverage prioritization. Iteratively perform the following two steps until all
statements/branches are covered by at least one test case: (i) select a test case that yields
the greatest additional statement/branch coverage; and (ii) then adjust the coverage
information on subsequent test cases to indicate their coverage of statements/branches not
yet covered by a test already chosen for the suite.

(3)Usage
There are 5 folders in this project.  

1. benchmarks
benchmarks programs and mutants

2. test generation
  test_generation contains scripts to collect branch coverage and generate branch test suites

  branch_one_shot.py: will generate all branch test suites for one time. To run it, under test_generation, run 'python3 branch_one_shot.py'  

  statement_one_shot.py: will generate all statement test suites for one time. To run it, under test_generation, run 'python3 statement_one_shot.py'  

  branch.py: generate branch test suite for specific program and prioritization method. To run it, under test_generation, run 'python3 branch_one_shot.py <program> <method>'(ex. python3 branch.py tcas add)  

  statement.py: generate statement test suite for specific program and prioritization method. To run it, under test_generation, run 'python3 statement_one_shot.py <program> <method>'(ex. python3 statement.py tcas add)  

3. stat
  stat contains script to generate analysis result  

  gen_fault.py: generate detailed fault information including which mutant is detected by the test suite. To run it, under spec, run 'python3 gen_fault.py' and it will generate a fault_exposing_results.txt  

  gen_csv.py: create data table according to the spec. It will read from fault_exposing_results.txt to collect information  

4. test suites
  test_suites contain all the test suites generated by the script in test_generation

5. report
  contain a pdf version fo the report

(4)Running the Tests  
1. under test_generation  
python3 branch_one_shot.py  
python3 statement_one_shot.py  
2. under stat  
python3 gen_fault.py  
python3 gen_csv.py  

(4)Note  
Almost every parts of the script have detailed description. Check it out!

REFERENCE: [1]https://www.coursicle.com/ucr/courses/CS/206/