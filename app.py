import sys
from flask import Flask, render_template

sys.path.append('.')
import model.operations as ops

app = Flask(__name__)

@app.route('/')
def index():
    user_db = ops.OperationsDatabase.load_from_json()

    # Calculate the total amounts per category
    categories = [
                    ops.Operation.SupportedCategories('LIVING'), 
                    ops.Operation.SupportedCategories('WANTS'), 
                    ops.Operation.SupportedCategories('SAVINGS')
                ]
    
    category_totals = {}
    for category in categories:
        category_totals[category.value] = user_db.compute_amount_per_category(category)
    
    return render_template('index.html', category_totals=category_totals)

if __name__ == '__main__':
    app.run(debug=True)
