# Valuation Service
This is a commandline program that counts top product of given data. For broader explanation of the problem solved by it go to [problem section below.](#Problem)
## How to run
This program doesn't need any additional packages. It runs on python3 from commandline. 
Help from the program explaining how to use it:
```
usage: valuation_service.py [-h] data currencies matching

A Valuation Service for choosing top products according to matching
requirements.

positional arguments:
  data        Path to csv file containing data with products details. It
              should have columns id, price, currency, quantity and
              matching_id.
  currencies  Path to csv file containing data regarding currencies rates. It
              should have columns currency and ratio.
  matching    Path to csv file containing requirements for matching data. It
              should have columns matching_id and top_priced_count.

optional arguments:
  -h, --help  show this help message and exit
```
## Handling problematic situations
During processing files there can be several problems with data provided. Below is a list with these problems with explanation how it is handled.

|Problem|Solution|Explanation|
|---|---|---|
|Provided file doesn't exist|Raises `ArgumentTypeError`| Without any of the three files it is not possible to count anything. That's why program raises exception and stops execution. It also informs which file is not existing. |
|Provided file doesn't have expected columns|Raises `ArgumentTypeError`| There are very specific columns for each file in description of the problem. Without any of them there is some crucial information missing. Program stops execution raising exception with information which file is botched. |
|File for output already contains some data|Raises `FileExistsError`| There maybe some crucial information in this file that will be destroyed by replacing or adding different data. For this reason it stops execution with an error. The specification of the problem points to which file result should be saved. I would suggest to allow user to change the path by providing optional argument. |
|Currency not found in currency file|Logs error message| In case some rows of certain `matching_id` don't have currency the whole matching is omitted and an error log is printed. There may be a lot of other matching that could be correctly calculated. I assume that user would like to know what is the result of the rest of correct matching so I don't stop the program. It will provide output for all matching that can be calculated. |
|One of the matching is incomplete|Logs error message| As above in case of one of the rows in matching file being incomplete we want to have calculations for others, correct ones. That's why error is logged and rest of the matching is calculated. |

## Logging
Default logging is set to `INFO` level. If change to `DEBUG` level it shows info about which matching is processed and what is the output for this particular matching.

To change logging level change variable `_LOGGING_LEVEL` at the beginning of the `valuation_service.py` to desired level.

## Problem
Below is the description of the problem provided by recruiter.

### Requirements
You are building a valuation service.

Read the input data. From products with particular matching_id take those with
the highest total price (price * quantity), limit data set by top_priced_count and
aggregate prices.

Unit tests are required.
### Input
In the input there are three files containing:
- data.csv - product representation with price,currency,quantity,matching_id
- currencies.csv - currency code and ratio to PLN, i.e. GBP,2.4 can be
converted to PLN as follows 1 PLN * 2.4
- matchings.csv - matching data matching_id,top_priced_count
### Output
Save the results as top_products.csv. Output file shall have five columns:
matching_id, total_price, avg_price, currency, ignored_products_count.
#### Input files
currencies.csv

| currency | ratio |
|---|---|
|GBP|2.4|
|EU|2.1|
|PLN|1|

data.csv

| id | price | currency | quantity | matching_id |
|---|---|---|---|---|
|1|1000|GBP|2|3|
|2|1050|EU|1|1|
|3|2000|PLN|1|1|
|4|1750|EU|2|2|
|5|1400|EU|4|3|
|6|7000|PLN|3|2|
|7|630|GBP|5|3|
|8|4000|EU|1|3|
|9|1400|GBP|3|1|

matchings.csv

|matching_id|top_priced_count|
|---|---|
|1|2|
|2|2|
|3|3|