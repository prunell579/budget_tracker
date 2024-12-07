import sys

sys.path.append('.')
import model.operations as ops

if __name__ == '__main__':
    user_db = ops.OperationsDatabase.load_from_json()

    category_options_output_string = ''
    i = 1
    opt_to_category = {}
    for category in ops.Operation.SupportedCategories:
        category_options_output_string += str(i) + ' - ' + category.value + '\n'
        opt_to_category[i] = category.value
        i += 1

    for op in user_db.get_operations():
        if op.category is None:
            op.summary()
            category_choice = input(category_options_output_string)
            op.category = ops.Operation.SupportedCategories(opt_to_category[int(category_choice)])

    # update db with category info
    user_db.write_to_file()

    

