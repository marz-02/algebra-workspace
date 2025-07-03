from .base import Expr

from typing import List
from collections import Counter
import uuid


class Var(Expr):
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name

    def __hash__(self):
        return hash(("Var", self.name))

    def get_subexprs(self):
        return []

    def clone(self): #Might need to raise an error
        new_Var = Var(self.name)
        new_Var.id = self.id
        return new_Var
    
    def replace(self, old, new):
        if self == old:
            return new
        return self

    def flatten(self):
        return self

    def to_latex(self):
        return f"{{{self.name}}}"
    
    def to_dict(self):
        return {"type": "var", "name": self.name, "id": self.id}
    
    """
    def depth_search(self, target_id, depth=-100):
        depth += 1
        if self.id == target_id:
            return depth
        return None
    """
class Const(Expr):
    def __init__(self, value):
        self.value = str(value)
        self.id = str(uuid.uuid4())

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, Const) and self.value == other.value

    def __hash__(self):
        return hash(("Const", self.value))
    
    def get_subexprs(self):
        return []

    def clone(self): #Might need to raise an error
        new_Const = Const(self.value)
        new_Const.id = self.id
        return new_Const
    
    
    def replace(self, old, new):
        if self == old:
            return new
        return self

    def flatten(self):
        return self

    def to_latex(self):
        return f"{{{self.value}}}"
    
    def to_dict(self):
        return {"type": "const", "value": self.value, "id": self.id}

    """    
    def depth_search(self, target_id, depth=-100):
        depth += 1
        if self.id == target_id:
            return depth
        return None
    """