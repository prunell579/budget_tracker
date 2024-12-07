from dataclasses import dataclass, field, asdict
from datetime import datetime
import hashlib
import json

@dataclass
class Operation():
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
                            account_label=normal_dict['account_label']
                        )

    def jsonfy(self):
        raw_dict = asdict(self)
        raw_dict['date'] = raw_dict['date'].isoformat()
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

        # only thing missing from the dict to be normal: type of the date attribute
        db = cls({}, set())
        for _, operation_dict in loaded_dict['operations'].items():
            operation_dict['date'] = datetime.fromisoformat(operation_dict['date'])
            db.add_operation(Operation.from_normal_dict(operation_dict))

        return db

    def add_operation(self, operation: Operation):
        self.operations[operation.id] = operation
        self.processed_operations_ids.add(operation.id)

    def jsonfy(self):
        operations_db_as_dict = dict.fromkeys(asdict(self).keys())
        operations_db_as_dict['processed_operations_ids'] = list(self.processed_operations_ids.copy())

        operations_db_as_dict['operations'] = {}
        for sha_id, operation_obj in self.operations.items():
            operations_db_as_dict['operations'][sha_id] = operation_obj.jsonfy()

        return operations_db_as_dict
    
    def write_to_file(self):
        json_string =  json.dumps(self.jsonfy(), indent=4, ensure_ascii=False)
        with open('operations_database.json','w', encoding='utf-8') as f:
            f.write(json_string)

