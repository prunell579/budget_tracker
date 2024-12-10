import sys

sys.path.append('.')
import model.operations as ops

if __name__ == '__main__':
    user_db = ops.OperationsDatabase.load_from_json()


    print(user_db.get_operations(yymm=(2024,12)))
    print(user_db.get_operations_by_category(ops.Operation.SupportedCategories.LIVING, yymm=(2024,12)))
    print(user_db.compute_amount_per_category(ops.Operation.SupportedCategories.WANTS, yymm=(2024,12)))