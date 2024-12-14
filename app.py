import sys
from flask import Flask, jsonify, redirect, render_template, request, url_for
from datetime import datetime

sys.path.append('.')
import model.operations as ops

app = Flask(__name__)

# Global variable for the database
user_db =  ops.OperationsDatabase.load_from_json()
supported_categories_in_frontend = (
                                    ops.Operation.SupportedCategories('LIVING'), 
                                    ops.Operation.SupportedCategories('WANTS'), 
                                    ops.Operation.SupportedCategories('SAVINGS')
                                    )

# backend should serve json data to front end
# html items will take the json data and send it over to js scripts if needed

@app.route('/')
def index():

    # hardcoded values for budget
    budgeted_amounts = {
                        ops.Operation.SupportedCategories('LIVING').value: 900.00,
                        ops.Operation.SupportedCategories('WANTS').value: 560.00,
                        ops.Operation.SupportedCategories('SAVINGS').value: 750.00,
                        }

    now = datetime.now()
    yymm = (now.year, now.month)
    
    spent_amounts = user_db.compute_amount_per_categories(list(supported_categories_in_frontend), yymm=yymm)
    operations_list = user_db.get_operations(yymm=yymm)


    return render_template('index.html',
                            spent_amounts=spent_amounts,
                            budgeted_amounts=budgeted_amounts,
                            operation_list=operations_list)


@app.route('/update-category', methods=['POST'])
def update_category():
    global user_db
    data = request.json
    operation_id = data.get('operation_id')
    new_category = data.get('new_category')
    # Update the category in your OperationsDatabase
    if operation_id in user_db.operations:
        user_db.operations[operation_id].category = ops.Operation.SupportedCategories(new_category)
        return jsonify({'success': True, 'message': 'Category updated successfully.'})
    else:
        return jsonify({'success': False, 'message': 'Operation not found.'}), 404

@app.route('/get-chart-data', methods=['GET'])
def get_chart_data():
    global user_db
    amounts = user_db.compute_amount_per_categories(list(supported_categories_in_frontend))
    return jsonify({"amounts": amounts})


@app.route('/save', methods=['POST'])
def save():
    global user_db
    print('Saving db...')
    user_db.write_to_file()
    return redirect(url_for('index'))

@app.route('/reset',  methods=['POST'])
def reset():
    global user_db
    print('resetting to last saved db...')
    user_db = ops.OperationsDatabase.load_from_json()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
