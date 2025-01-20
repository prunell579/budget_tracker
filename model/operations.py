from dataclasses import dataclass, field, asdict
from datetime import datetime
import hashlib
import json
from enum import Enum

@dataclass
class Operation():

    # for further interactiviy with user, this can be converted to a mutable class
    class SupportedCategories(Enum):
        LIVING = 'LIVING'
        WANTS = 'WANTS'
        SAVINGS = 'SAVINGS'
        INTERNAL_TRANSFER = 'INTERNAL_TRANSFER'
        SELF_LOAN = 'SELF_LOAN'
        INCOME = 'INCOME'
        UNKNOWN = 'UNKNOWN'

    date: datetime
    amount: float
    description: str
    account_label: str
    category: str = None
    id: str = field(init=False)

    def __post_init__(self):
        id = self.date.isoformat() + '_' + format(self.amount, ".2f") + self.description + self.account_label
        self.id = hashlib.sha256(id.encode()).hexdigest()

    @classmethod
    def from_normal_dict(cls, normal_dict: dict) -> "Operation":
        return cls(
                            date=normal_dict['date'],
                            amount=normal_dict['amount'],
                            description=normal_dict['description'],
                            account_label=normal_dict['account_label'],
                            category=normal_dict['category']
                        )

    def summary(self):
        print(f"Date: {self.date.strftime('%Y-%m-%d')} | "
            f"Amount: {self.amount:.2f} | "
            f"Description: {self.description} | "
            f"Account Label: {self.account_label} | "
            f"Category: {self.category if self.category else 'N/A'}")

    def belongs_to_month_and_year(self, year: int, month: int):
        if self.date.year == year and self.date.month == month:
            return True
        return False

    def jsonfy(self):
        raw_dict = asdict(self)
        raw_dict['date'] = raw_dict['date'].isoformat()
        try:
            raw_dict['category'] = raw_dict['category'].value
        except AttributeError:
            pass

        return raw_dict

@dataclass
class OperationsDatabase():
    operations: dict[int, Operation]
    processed_operations_ids: set


    @classmethod
    def from_normal_dicts(cls, normal_dicts: list[dict]) -> "OperationsDatabase":
        db = cls({}, set())
        for normal_dict in normal_dicts:
            db.add_operation(Operation.from_normal_dict(normal_dict))

        return db

    @classmethod
    def load_from_json(cls, json_filepath='operations_database.json'):
        with open(json_filepath, 'r', encoding='utf-8') as f:
            loaded_dict = json.load(f)

        cls.check_database_json_file(loaded_dict)

        # only thing missing from the dict to be normal: type of the date attribute
        db = cls({}, set())
        for _, operation_dict in loaded_dict['operations'].items():
            operation_dict['date'] = datetime.fromisoformat(operation_dict['date'])
            try:
                operation_dict['category'] = Operation.SupportedCategories(operation_dict['category'])
            except ValueError:
                pass
            db.add_operation(Operation.from_normal_dict(operation_dict))

        return db
    
    @staticmethod
    def check_database_json_file(loaded_dict: dict):
        # check if the operation id coincides with its key
        for sha_id_key, operation_obj in loaded_dict['operations'].items():
            if sha_id_key != operation_obj['id']:
                raise ValueError(f"Error with json file: Operation id {operation_obj['id']} does not coincide with its key {sha_id_key}")

        # check if the processed_operations_ids set is a set of unique elements
        processed_ids_set = set(loaded_dict['processed_operations_ids'])
        if len(loaded_dict['processed_operations_ids']) != len(processed_ids_set):
            raise ValueError("Error with json file: processed_operations_ids set is not a set of unique elements")
        
        # check if the processed_operations_ids set is identical to the operations keys
        operation_keys_set = set(loaded_dict['operations'].keys())
        if processed_ids_set != operation_keys_set:
            missing_in_set = processed_ids_set - operation_keys_set
            error_msg = "The following operation key ids were not found in the processed ids set {}".format(missing_in_set)
            raise ValueError("Error with json file: processed_operations_ids set is not identical to the operations keys\n" + error_msg)

    def add_operation(self, operation: Operation):
        self.operations[operation.id] = operation
        self.processed_operations_ids.add(operation.id)


    def get_operations(self, yymm: tuple[int,int]=None, ops_in_json_format=False) -> list[Operation]:
        if yymm:
            ops =  [op for op in self.operations.values() if op.belongs_to_month_and_year(yymm[0], yymm[1])]
        else:
            ops = self.operations.values()

        if ops_in_json_format:
            return [op.jsonfy() for op in ops]
        return ops
    
    def get_operations_by_category(self, category: Operation.SupportedCategories, yymm: tuple[int,int]=None) -> list[Operation]:
        return [op for op in self.get_operations(yymm) if category==op.category]

    def compute_amount_per_category(self, category: Operation.SupportedCategories, yymm: tuple[int, int]=(), fabs=True):
        amount = sum(op.amount for op in self.get_operations_by_category(category, yymm))
        if fabs:
            amount = abs(amount)

        return amount
    
    def compute_amount_per_categories(self,
                                      categories: list[Operation.SupportedCategories],
                                      yymm: tuple[int, int]=(), 
                                      fabs=True,
                                      dict_keys_as_values=True) -> dict:
        amounts = {}

        for category in categories:
            if dict_keys_as_values:
                cat_key = category.value
            else:
                cat_key = category

            amounts[cat_key] = self.compute_amount_per_category(category, yymm, fabs)

        return amounts

    def jsonfy(self):
        operations_db_as_dict = dict.fromkeys(asdict(self).keys())
        operations_db_as_dict['processed_operations_ids'] = sorted(self.processed_operations_ids.copy())

        operations_db_as_dict['operations'] = {}
        for sha_id, operation_obj in self.operations.items():
            operations_db_as_dict['operations'][sha_id] = operation_obj.jsonfy()

        return operations_db_as_dict
    
    def write_to_file(self):
        json_string =  json.dumps(self.jsonfy(), indent=4, ensure_ascii=False)
        with open('operations_database.json','w', encoding='utf-8') as f:
            f.write(json_string)
