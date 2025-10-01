#!/usr/bin/env python3
"""
XML to JSON Parser for Momo.xml
"""

import xmltodict
import json
import re
from typing import List, Dict, Any


def extract_basic_info(sms_body: str) -> Dict[str, str]:
    """Extract basic transaction info from SMS body."""
    # Amount extraction
    amount_match = re.search(r'(\d+(?:,\d+)*)\s*RWF', sms_body)
    amount = amount_match.group(1).replace(',', '') if amount_match else 'Unknown'

    # Detect transaction type
    if 'received' in sms_body.lower():
        transaction_type = 'received'
        sender_match = re.search(r'from ([^(]+)', sms_body)
        sender = sender_match.group(1).strip() if sender_match else 'Unknown'
        receiver = 'You'
    elif 'payment' in sms_body.lower():
        transaction_type = 'payment'
        sender = 'You'
        receiver_match = re.search(r'to ([A-Za-z\s]+)', sms_body)
        receiver = receiver_match.group(1).strip() if receiver_match else 'Unknown'
    elif 'transferred' in sms_body.lower():
        transaction_type = 'transfer'
        sender = 'You'
        receiver_match = re.search(r'to ([^(]+)', sms_body)
        receiver = receiver_match.group(1).strip() if receiver_match else 'Unknown'
    elif 'deposit' in sms_body.lower():
        transaction_type = 'deposit'
        sender = 'Bank'
        receiver = 'You'
    else:
        transaction_type = 'other'
        sender = 'Unknown'
        receiver = 'Unknown'

    return {
        'transaction_type': transaction_type,
        'amount': amount,
        'sender': sender,
        'receiver': receiver
    }

def parse_momo_xml(xml_file_path: str) -> List[Dict[str, Any]]:
    """Parse XML and extract SMS data as JSON objects."""
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        data = xmltodict.parse(file.read())

    sms_list = data['smses']['sms']
    if not isinstance(sms_list, list):
        sms_list = [sms_list]

    transactions = []
    for sms in sms_list:
        body = sms.get('@body', '')
        if 'RWF' in body:  # Only process SMS with money transactions
            info = extract_basic_info(body)
            info['timestamp'] = sms.get('@readable_date', '')
            transactions.append(info)

    return transactions


def main():
    """ Main function to parse XML and save as JSON """
    xml_file = "../data/raw/momo.xml"
    output_file = "../data/parsed_sms.json"

    transactions = parse_momo_xml(xml_file)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transactions, f, indent=2)

    print(f"Parsed {len(transactions)} transactions to {output_file}")
    print(f"Sample: {json.dumps(transactions[0], indent=2)}")


if __name__ == "__main__":
    main()
