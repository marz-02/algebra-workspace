from typing import List

import os #this is for printing in the console
from collections import Counter

import uuid

print("Hellow from Neovim!")


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

class Add(Expr):
    def __init__(self, *terms: Expr):
        self.terms: List[Expr] = list(terms)
        self.id = str(uuid.uuid4())

    def __str__(self):
        return " + ".join(str(term) for term in self.terms)

    def __eq__(self, other):
        return (isinstance(other, Add) and self.terms == other.terms)

    def get_subexprs(self):
        return self.terms

    def set_subexprs(self, *new_terms):
        self.terms: List[Expr] = list(new_terms)
    
    def replace(self, old, new):
        if self == old:
            return new

        new_terms = []
        changed = False

        for term in self.terms:
            replaced = term.replace(old, new)
            if replaced != term:
                changed = True
            new_terms.append(replaced)
        if not changed:
            return self

        return Add(*new_terms)

    def flatten(self):
        flat_terms = []

        for term in self.terms:
            flat_term = term.flatten()

            if isinstance(flat_term, Add):
                flat_terms.extend(flat_term.terms)  #flatten one level
            else:
                flat_terms.append(flat_term)

        return Add(*flat_terms)

    def equivalent_to(self, other):
        return isinstance(other, Add) and Counter(self.flatten().terms) == Counter(other.flatten().terms)

    def to_latex(self) -> str:
        # 1) Flatten
        flat = self.flatten().terms

        # 2) Convert each term
        parts = []
        for term in flat:
            latex_term = term.to_latex()

            # 3) If the term *were* another Add (shouldn't happen after flatten),
            #    you'd parenthesize—but flatten prevents that.
            #    Multiplications or Vars/Consts just go straight in.
            parts.append(f"{{{latex_term}}}")

        # 4) Join with plus signs
        return " + ".join(parts)
    
     
    def pop_expr2(self, target_id): 
        terms = self.get_subexprs()
        target = self.find_by_id(target_id)
        if target in terms:
            terms.remove(target)
            new_Add = Add(terms)
            print("popped!")
            return new_Add, target
        print("Not deep enuf!")     
        

class Neg(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr
        self.id = str(uuid.uuid4())

    def __str__(self):
        if isinstance(self.expr, Add):
            return f"-({self.expr})"
        return f"-{self.expr}"

    def __eq__(self, other):
        return isinstance(other, Neg) and self.expr == other.expr

    def __hash__(self):
        return hash(("Neg", self.expr))

    def get_subexprs(self):
        return [self.expr]

    def replace(self, old, new):
        if self == old:
            return new
        replaced = self.expr.replace(old, new)
        return Neg(replaced) if replaced != self.expr else self

    def flatten(self):
        # For now, don't distribute negation
        return Neg(self.expr.flatten())

    def equivalent_to(self, other):
        return isinstance(other, Neg) and self.expr.equivalent_to(other.expr)

    def to_latex(self):
        inner = self.expr.to_latex()
        if isinstance(self.expr, Add):
            return f"-\\left({inner}\\right)"
        return f"-{inner}"        

class Mult(Expr):
    def __init__(self, *factors: Expr):
        self.factors: List[Expr] = list(factors)
        self.id = str(uuid.uuid4())

    def __str__(self):
        #return "".join(str(factor) for factor in self.factors)
        
        parts = [] #Each part comes from a factor, they will be put together to from a string

        for factor in self.factors:
            if isinstance(factor, Add):
                parts.append(f"({factor})") # Intead now we process a factor if its an Add class, we add brackets ()
            else:
                parts.append(str(factor)) #Appending a factor (in str form) just like we did previously
        

        return "".join(parts)

    def __eq__(self, other):
        return (isinstance(other, Mult) and self.factors == other.factors)
                
    def get_subexprs(self):
        return self.factors
    
    def set_subexprs(self, *new_factors):
        self.factors: List[Expr] = list(new_factors)

    def replace(self, old, new):
        if self == old:
            return new

        new_factors = []
        changed = False

        for factor in self.factors:
            replaced = factor.replace(old, new)
            if replaced != factor:
                changed = True
            new_factors.append(replaced)

        if not changed:
            return self

        return Mult(*new_factors)


    def flatten(self):
        flat_factors = []

        for factor in self.factors:
            flat_factor = factor.flatten()

            if isinstance(flat_factor, Mult):
                flat_factors.extend(flat_factor.factors)
            else:
                flat_factors.append(flat_factor)

        return Mult(*flat_factors)


    def equivalent_to(self, other):
        return isinstance(other, Mult) and Counter(self.flatten().factors) == Counter(other.flatten().factors)


    def to_latex(self):
        parts = []
        for factor in self.flatten().factors:
            if isinstance(factor, Add):
                parts.append(f"({factor.to_latex()})")
            else:
                parts.append(factor.to_latex())
        return "".join(f"{{{p}}}" for p in parts)

class Eq(Expr):
    def __init__(self, lhs: Expr, rhs: Expr):
        self.lhs = lhs
        self.rhs = rhs
        self.id = str(uuid.uuid4())

    def __str__(self):
        return " = ".join((str(self.lhs), str(self.rhs)))
    
    def __eq__(self, other):
        return( isinstance(other, Eq) and self.lhs == other.lhs and self.rhs == other.rhs)

    def get_subexprs(self):
        return [self.lhs, self.rhs]
    
    def set_subexprs(self, new_lhs, new_rhs):
        self.lhs = new_lhs
        self.rhs = new_rhs

#This is terrible, but it works for now

    def pop_expr(self, target_id, side):
        if side == "lhs":
            return self.lhs.pop_expr(target_id)
        elif side == "rhs":
            return self.rhs.pop_expr(target_id)
        
    def move_expr(self, target_id, side):
        new_expr, poppie = self.pop_expr(target_id, side)

        if side == "lhs":
            self.lhs = new_expr
            self.rhs = Add(self.rhs, poppie)
x = Var("x")

y = Var("y")

z = Var("z")

a = Const("5")

line1 = Eq(
    Add( Var("x"), Var("y")),
    Var("z")
)

q = Var("q")

qid = q.get_id()

line2 = Eq(
    Add( Var("x"), q),
    Var("z")
)

#print(line1.get_id())

#print(line2.find_by_id(qid), qid)
"""
assert Add(x,y) == Add(x, y)
assert Add(x,y) != Add(y,x)

assert Mult(x,y) == Mult(x, y)
assert Mult(x,y) != Mult(y,x)

console_width = os.get_terminal_size().columns

xPy = Add(x,y)

xPyPz = Add(xPy,z)

xPyPz.flatten()


print("-" * console_width, "\n" + "Test Environment: \n")


print(Add(x, y).equivalent_to(Add(y, x)))  # True ✅
print(Add(x, y).equivalent_to(Add(x, y)))  # True ✅
print(Add(x, y).equivalent_to(Add(x, z)))  # False ❌


print(Add(x, y).equivalent_to(Mult(x, y)))  # False ❌
print(Add(x).equivalent_to(Add(x, x)))     # False ❌

print("\n" + ("_" * console_width))
"""
