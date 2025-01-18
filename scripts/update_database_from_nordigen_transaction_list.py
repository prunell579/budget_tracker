import os
import pickle as pkl
import sys
sys.path.append('.')
import model.operations as ops

def beancount_transaction_to_normal_dict(bc_transaction):

    assert (len(bc_transaction.postings) == 1)

    standard_format_dict = {
                            'date': bc_transaction.date,
                            'amount': float(bc_transaction.postings[0].units.number),
                            'description': bc_transaction.narration,
                            # 'account_label': bc_transaction.postings[0].account,
                            'account_label': 'boursorama', # TODO decide how to handle the accounts
                            'category': None
                            }

    return standard_format_dict


if __name__ == '__main__':
    file_2_process = 'data/nordigen_transaction_list_1224.pkl'
    with open(file_2_process, 'rb') as f:
        transactions = pkl.load(f)

    normalized_dicts = []
    for transaction in transactions:
        normalized_dicts.append(beancount_transaction_to_normal_dict(transaction))

    operations_list = []
    for normal_dict in normalized_dicts:
        operations_list.append(ops.Operation.from_normal_dict(normal_dict))

    # update json database
    try:
        user_db = ops.OperationsDatabase.load_from_json()
    except FileNotFoundError:
        user_db = ops.OperationsDatabase({}, set())

    new_op_detected = False
    for op in operations_list:
        if op.id not in user_db.processed_operations_ids:
            new_op_detected = True
            print('New operation detected')
            user_db.add_operation(op)

    if new_op_detected:
        user_db.write_to_file()
    else:
        print('Nothing to do')

    # move processed files
    archived_folder = os.path.join(os.path.abspath('data'), 'archived')
    
    os.rename(file_2_process, os.path.join(archived_folder, os.path.basename(file_2_process)))
