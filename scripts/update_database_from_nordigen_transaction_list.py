import pickle as pkl

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
    with open('data/nordigen_transaction_list_1224.pkl', 'rb') as f:
        transactions = pkl.load(f)

    normalized_dicts = []
    for transaction in transactions:
        normalized_dicts.append(beancount_transaction_to_normal_dict(transaction))

