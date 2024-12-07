
import sys
sys.path.append('.')

import model.boursorama_parser as bourso_parser
import model.operations as ops

# read files in /data folder
# generate list of normalized operation dicts
# generate list of operations
# load current database (json format)
# if sha not present in current, add operation to database
# move the processed files to data/archived

if __name__ == '__main__':

    csv_filepaths = bourso_parser.get_list_of_csv_files('data')
    normalized_dicts = bourso_parser.normalize_dicts_from_boursorama(csv_filepaths)
    operations_list = []
    for normal_dict in normalized_dicts:
        operations_list.append(ops.Operation.from_normal_dict(normal_dict))

    user_db = ops.OperationsDatabase.load_from_json()

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
