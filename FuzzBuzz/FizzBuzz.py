#!/usr/bin/env python3
import argparse


def check_n(value):
    if value.isdigit():
        int_value = int(value)
        if 1 <= int_value < 10000:
            return int_value
    raise argparse.ArgumentTypeError(
        "First argument provided \"{0}\" is not an integer in the range of 1 to 9999".format(value))


def check_m(value):
    if value.isdigit():
        int_value = int(value)
        if 1 < int_value <= 10000:
            return int_value
    raise argparse.ArgumentTypeError(
        "Second argument provided \"{0}\" is not an integer in the range of 2 to 10000".format(value))


def get_commandline_arguments():
    parser = argparse.ArgumentParser(description='A FizzBuzz implementation for numbers falling in range (0, 10000')
    parser.add_argument('n', type=check_n,
                        help='defines from which number the FizzBuzz should start')
    parser.add_argument('m', type=check_m,
                        help='defines which number would be last in the FizzBuzz')

    args = parser.parse_args()

    if args.n >= args.m:
        raise argparse.ArgumentTypeError(
            "First argument provided \"{0}\" is not smaller from the second argument \"{1}\"".format(args.n, args.m))
    return args


def get_fuzz_buzz(n):
    result = ""
    if not n % 3:
        result += "Fizz"
    if not n % 5:
        result += "Buzz"
    if not result:
        result = n
    return result


if __name__ == '__main__':
    cmd_args = get_commandline_arguments()
    for number in range(cmd_args.n, cmd_args.m+1):
        print(get_fuzz_buzz(number))
