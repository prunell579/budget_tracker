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
    def from_normal_dict(cls, normal_dict: list) -> "Operation":
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

    def add_operation(self, operation: Operation):
        self.operations[operation.id] = operation
        self.processed_operations_ids.add(operation.id)

    def jsonfy(self):
        operations_db_as_dict = dict.fromkeys(asdict(self).keys())
        operations_db_as_dict['processed_operations_ids'] = list(self.processed_operations_ids.copy())

        for sha_id, operation_obj in self.operations.items():
            operations_db_as_dict[sha_id] = operation_obj.jsonfy()

        return operations_db_as_dict
    
    def write_to_file(self):
        json_string =  json.dumps(self.jsonfy(), indent=4, ensure_ascii=False)
        with open('operations_database.js','w', encoding='utf-8') as f:
            f.write(json_string)

