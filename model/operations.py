from dataclasses import dataclass, field
from datetime import datetime
import hashlib

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

@dataclass
class OperationsDatabase():
    operations: set
    processed_operations_ids: set

