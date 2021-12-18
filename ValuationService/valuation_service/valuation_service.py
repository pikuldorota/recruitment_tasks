#!/usr/bin/env python3
import argparse
import logging
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
    data['total_price'] = data.price * data.quantity


def convert_currency_to_PLN(data, currency):
    currency_dict = {row['currency']: row['ratio'] for _, row in currency.iterrows()}
    for curr in data['currency'].unique():
        if not pd.isna(curr) and (curr not in currency_dict or pd.isna(currency_dict[curr])):
            logging.error('Ratio for currency was not found. This matching will be omitted.')
            return False
    data['price'] = data.apply(lambda row: row['price'] if pd.isna(row['currency']) else round(row['price'] / currency_dict[row['currency']], 2), axis=1)
    data['currency'] = data.apply(lambda row: row['currency'] if pd.isna(row['price']) or pd.isna(row['currency']) else 'PLN', axis=1)
    return True


def check_if_all_same_currency(data):
    return len(data['currency'].unique()) == 1


def get_required_data(data, matchings, currency):

    def process_row(matching_id, top_priced_count):
        if pd.isna(matching_id) or pd.isna(top_priced_count):
            logging.error('Matching misses data. Omitting this matching.')
            return

        matched_products = data.loc[data['matching_id'] == matching_id]
        if not check_if_all_same_currency(matched_products):
            return
        if not convert_currency_to_PLN(data, currency):
            return

        matched_products = matched_products.sort_values(by=['total_price'], ascending=False)
        top_products = matched_products.head(top_priced_count)
        row_dict = {'matching_id': matching_id,
                    'currency': matched_products['currency'].values[0],
                    'total_price': top_products['total_price'].sum(),
                    'avg_price': round(matched_products['price'].mean(), 2),
                    'ignored_products_count': max(0, matched_products.shape[0] - top_priced_count)}
        return row_dict

    result = [process_row(matching_id, top) for matching_id, top in matchings.values]
    result = pd.DataFrame([row for row in result if row is not None],
                          columns=['matching_id', 'total_price', 'avg_price', 'currency', 'ignored_products_count'])
    return result


def save_results(result, path="output.csv"):
    if validate_that_output_file_is_empty_or_nonexistent(path):
        result.to_csv(path, index=False)


if __name__ == '__main__':
    cmd_args = get_commandline_arguments()
