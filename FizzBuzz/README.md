# FizzBuzz
This is a command line implemantation of FizzBuzz problem.

## How to run
This program doesn't need any additional packages. It runs on python3 from commandline. 
Help from the program explaining how to use it:
```
usage: FizzBuzz.py [-h] n m

A FizzBuzz implementation for numbers falling in range (0, 10000)

positional arguments:
  n           defines from which number the FizzBuzz should start
  m           defines which number would be last in the FizzBuzz

optional arguments:
  -h, --help  show this help message and exit

```

## Problem
Below is the description of the problem provided by recruiter.
### Requirements 
Write a program that prints the integers from n to m (inclusive), but
- for multiples of three, print Fizz (instead of the number)
- for multiples of five, print Buzz (instead of the number)
- for multiples of both three and five, print FizzBuzz (instead of the number)

Input numbers need to satisfy condition 1 &lt;= n &lt; m &lt;= 10000.
### Input
Two numbers in two lines (n, m).
### Output
One result per line as described in requirements.
### Example
#### Sample input:  
3  
16  
#### Sample output:  
Fizz  
4  
Buzz  
Fizz  
7  
8  
Fizz  
Buzz  
11  
Fizz  
13  
14  
FizzBuzz  
16  
