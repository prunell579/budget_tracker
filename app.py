import sys
from flask import Flask, render_template

sys.path.append('.')
import model.operations as ops

app = Flask(__name__)

# Global variable for the database
user_db =  ops.OperationsDatabase.load_from_json()

@app.route('/')
def index():

    # Calculate the total amounts per category
    categories = [
                    ops.Operation.SupportedCategories('LIVING'), 
                    ops.Operation.SupportedCategories('WANTS'), 
                    ops.Operation.SupportedCategories('SAVINGS')
                ]
    

    category_totals = {}
    for category in categories:
        category_totals[category.value] = user_db.compute_amount_per_category(category, fabs=True)

    # hardcoded values for budget
    budgeted_amounts = {
                        ops.Operation.SupportedCategories('LIVING').value: 900.00,
                        ops.Operation.SupportedCategories('WANTS').value: 560.00,
                        ops.Operation.SupportedCategories('SAVINGS').value: 750.00,
                        }

    return render_template('index.html', categories=[cat.value for cat in categories],
                                        spent_amounts=category_totals,
                                        budgeted_amounts=budgeted_amounts,
                                        operation_list=user_db.operations)

if __name__ == '__main__':
    app.run(debug=True)
