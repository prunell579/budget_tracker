from datetime import datetime
import json
import sys
sys.path.append('.')

import model.operations as ops

def nordigen_dict_to_normal_dict(nordigen_dict: dict) -> dict:
    normal_dict = {
        'date': datetime.fromisoformat(nordigen_dict['bookingDate']),
        'amount': float(nordigen_dict['transactionAmount']['amount']),
        'description': ";".join(nordigen_dict['remittanceInformationUnstructuredArray']),
        'account_label': 'boursorama',
        'category': None
    }
    return normal_dict


if __name__ == '__main__':
    with open('data/nordigen_request_example_account.json', 'r') as f:
        transactions_data = json.load(f)

    try:
        user_db = ops.OperationsDatabase.load_from_json()
    except FileNotFoundError:
        user_db = ops.OperationsDatabase({}, set())

    new_op_detected = False
    for booked_transaction in transactions_data['transactions']['booked']:
        op = ops.Operation.from_normal_dict(nordigen_dict_to_normal_dict(booked_transaction))

        if op.id not in user_db.processed_operations_ids:
            user_db.add_operation(op)
            print('New operation detected')
            new_op_detected = True


    if new_op_detected:
        user_db.write_to_file()
    else:
        print('Nothing to do')
