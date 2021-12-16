#!/usr/bin/env python3
import argparse


def check_if_valid_path(path):
    return path


def check_if_existing_path(path):
    return path


def check_if_valid_data_file(path):
    return path


def check_if_valid_currencies_file(path):
    return path


def check_if_valid_matching_file(path):
    return path


def check_if_valid_output_file(path):
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
    parser.add_argument('result_file', type=check_if_valid_output_file, default='top_products.csv',
                        help='Path where output will be saved. Default is "top_products.csv". '
                             'Path should either lead to an empty file or file should not yet exist.')

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
