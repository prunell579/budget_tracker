
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

    normalized_dicts = bourso_parser.normalize_dicts_from_boursorama()
    db = ops.OperationsDatabase.from_normal_dicts(normalized_dicts)
    db.write_to_file()
