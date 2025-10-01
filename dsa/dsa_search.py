#!/usr/bin/env python3
""" Search Algorithms for Transaction Data """
import json
import time


# Load parsed json data from file and convert to python object
with open("../data/parsed_sms.json", "r", encoding="utf-8") as file:
    transactions = json.load(file)


# Use the transactions with IDs to enable easy search
for i, t in enumerate(transactions, start=1):
    t["id"] = i

# List of the transactions
transactions_list = transactions
# A dictionary of the transactions with an id for each transaction
transactions_dictionary = {t["id"]: t for t in transactions}


# Implementation of linear search function
def linear_search(transactions_list, spec_id):
    for transaction in transactions_list:
        if transaction["id"] == spec_id:
            return transaction
    return None

# Implementation of dictionary lookup to find transaction by key
def dictionary_lookup(transactions_dictionary, spec_id):
    return transactions_dictionary.get(spec_id, None)


# Measure efficiency of the search algos using the last transaction
spec_id = len(transactions)

# Linear search time taken
start_time = time.time()
linear_result = linear_search(transactions_list, spec_id)
end_time = time.time()
linear_total_time = end_time - start_time
print(f"Linear search result: {linear_result}\n")
print(f"Our linear search took a time of {linear_total_time} seconds")

print()

# Dictionary lookup time taken
start_time = time.time()
dict_lookup_result = dictionary_lookup(transactions_dictionary, spec_id)
end_time = time.time()
dict_total_time = end_time - start_time
print(f"Dictionary lookup result: {dict_lookup_result}\n")
print(f"Our dictionary lookup took a time of {dict_total_time} seconds\n")

if (linear_total_time > dict_total_time):
	print("Dictionary lookup is faster than linear search")
else:
	print("linear search is faster than dictionary lookup")
