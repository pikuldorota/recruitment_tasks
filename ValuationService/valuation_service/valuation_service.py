#!/usr/bin/env python3
import argparse
import os
import pandas as pd


def check_if_existing_path(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError('File "{}" does not exist'.format(path))
    return path


def check_if_valid_data_file(path):
    check_if_existing_path(path)

    try:
        data = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise argparse.ArgumentTypeError('File "{}" is not of valid data format'.format(path)) from None

    columns = ['id', 'price', 'currency', 'quantity', 'matching_id']
    for column in columns:
        if column not in data.columns:
            raise argparse.ArgumentTypeError('File "{}" is not of valid data format'.format(path))
    return path


def check_if_valid_currencies_file(path):
    check_if_existing_path(path)

    try:
        currency = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise argparse.ArgumentTypeError('File "{}" is not of valid currency format'.format(path)) from None
    columns = ['currency', 'ratio']
    for column in columns:
        if column not in currency.columns:
            raise argparse.ArgumentTypeError('File "{}" is not of valid currency format'.format(path))
    return path


def check_if_valid_matching_file(path):
    check_if_existing_path(path)

    try:
        matching = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise argparse.ArgumentTypeError('File "{}" is not of valid matching format'.format(path)) from None
    columns = ['matching_id', 'top_priced_count']
    for column in columns:
        if column not in matching.columns:
            raise argparse.ArgumentTypeError('File "{}" is not of valid matching format'.format(path))
    return path


def validate_that_output_file_is_empty_or_nonexistent(path):
    if os.path.isfile(path) and os.path.getsize(path) > 0:
        raise FileExistsError('File "{}" already contains data. Choose different output file.'.format(path))
    return path


def get_commandline_arguments():
    parser = argparse.ArgumentParser(description='A Valuation Service for choosing top products '
                                                 'according to matching requirements.')
    parser.add_argument('data', type=check_if_valid_data_file,
                        help='Path to csv file containing data with products details. '
                             'It should have columns id, price, currency, quantity and matching_id.')
    parser.add_argument('currencies', type=check_if_valid_currencies_file,
                        help='Path to csv file containing data regarding currencies rates. '
                             'It should have columns currency and ratio.')
    parser.add_argument('matching', type=check_if_valid_matching_file,
                        help='Path to csv file containing requirements for matching data. '
                             'It should have columns matching_id and top_priced_count.')

    args = parser.parse_args()
    return args


def add_total_price(data):
    pass


def convert_currency_to_PLN(data, currency):
    pass


def check_if_all_same_currency(data):
    pass


def get_required_data(matching, data):
    pass


def save_results(result, path):
    pass


if __name__ == '__main__':
    cmd_args = get_commandline_arguments()
