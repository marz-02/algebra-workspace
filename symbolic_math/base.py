from typing import List
from collections import Counter
import uuid

class Expr:
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())
        self.side = None

    def __repr__(self):
        return str(self)

    def equivalent_to(self, other: "Expr") -> bool:
        ...

    def get_id(self):
        return self.id

    def find_by_id(self, target_id):
        if self.id == target_id:
            return self
        
        for subexpr in self.get_subexprs():
            result = subexpr.find_by_id(target_id)
            if result is not None:
                return result
        
        return None