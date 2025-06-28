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

    def replace(self, old, new):
        if self == old:
            return new
        return self

    def flatten(self):
        return self

    def to_latex(self):
        return f"{{{self.name}}}"

class Const(Expr):
    def __init__(self, value):
        self.value = value
        self.id = str(uuid.uuid4())

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, Const) and self.value == other.value

    def __hash__(self):
        return hash(("Const", self.value))
    
    def get_subexprs(self):
        return []

    def replace(self, old, new):
        if self == old:
            return new
        return self

    def flatten(self):
        return self

    def to_latex(self):
        return f"{{{self.value}}}"