from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import typing

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


