from .base import Expr

from typing import List
from collections import Counter
import uuid

class Add(Expr):
    def __init__(self, *terms: Expr):
        self.terms: List[Expr] = list(terms)
        self.id = str(uuid.uuid4())

    def __str__(self):
        for i, term in enumerate(self.terms):
            if i == 0:
                expression = str(term)
            else:
                if isinstance(term, Neg):
                    expression += " - " + str(term.expr) 
                else:
                    expression += " + " + str(term)
        return expression
        #return " + ".join(str(term) for term in self.terms)

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
    
     
    def pop_expr(self, target_id): 
        terms = self.get_subexprs()
        target = self.find_by_id(target_id)
        if target in terms:
            terms.remove(target)
            new_Add = Add(*terms)
            #print("popped!")
            #print("New Add:", new_Add, "Target:", target)
            #print(type(new_Add), type(target))
            return new_Add, target
        print("Not deep enuf!")
        return self, target

    def to_dict(self):
        return {
            "type": "add",
            "terms": [term.to_dict() for term in self.terms],
            "id": self.id
        }

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

    def to_dict(self):
        return {
            "type": "neg",
            "expr": self.expr.to_dict(),
            "id": self.id
        }   

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
    
    def to_dict(self):
        return {
            "type": "mult",
            "factors": [factor.to_dict() for factor in self.factors],
            "id": self.id
        }

class Frac(Expr):
    #Review this code, it was written by co-pilot and I don't know if it works
    def __init__(self, numerator: Expr, denominator: Expr):
        self.numerator = numerator
        self.denominator = denominator
        self.id = str(uuid.uuid4())

    def __str__(self):
        return f"({self.numerator}/{self.denominator})"

    def __eq__(self, other):
        return (isinstance(other, Frac) and self.numerator == other.numerator and self.denominator == other.denominator)

    def get_subexprs(self):
        return [self.numerator, self.denominator]

    def set_subexprs(self, new_numerator, new_denominator):
        self.numerator = new_numerator
        self.denominator = new_denominator

    def flatten(self):
        return Frac(self.numerator.flatten(), self.denominator.flatten())

    def to_dict(self):
        return {
            "type": "frac",
            "numerator": self.numerator.to_dict(),
            "denominator": self.denominator.to_dict(),
            "id": self.id
        }
    
    def to_latex(self):
        num_latex = self.numerator.to_latex()
        den_latex = self.denominator.to_latex()
        return f"\\frac{num_latex}{den_latex}"

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
    
    def flatten(self):
        # Flatten both sides of the equation
        lhs_flat = self.lhs.flatten()
        rhs_flat = self.rhs.flatten()
        return Eq(lhs_flat, rhs_flat)

#This is terrible, but it works for now


    
    
    def pop_expr(self, target_id, from_side, to_side):
        if from_side == "lhs":
            return self.lhs.pop_expr(target_id)
        elif from_side == "rhs":
            return self.rhs.pop_expr(target_id)
        
    def move_expr(self, target_id, from_side, to_side):
        new_expr, popped_term = self.pop_expr(target_id, from_side, to_side)

        if from_side == "lhs":
            lhs_new = new_expr
            rhs_new = Add(self.rhs, Neg(popped_term)).flatten() if to_side == "rhs" else self.rhs
        elif from_side == "rhs":
            rhs_new = new_expr
            lhs_new = Add(self.lhs, Neg(popped_term)).flatten() if to_side == "lhs" else self.lhs
        else:
            raise ValueError("Invalid side")

        return Eq(lhs_new, rhs_new)
    
    def to_dict(self):
        return {
            "type": "eq",
            "lhs": self.lhs.to_dict(),
            "rhs": self.rhs.to_dict(),
            "id": self.id
        }