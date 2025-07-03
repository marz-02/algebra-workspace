from .base import Expr
from .leaves import Var, Const

from typing import List
from typing import Optional
from collections import Counter
import uuid

class Add(Expr):
    def __init__(self, *terms: Expr | None):
        if None in terms:
            terms_list = list(terms)
            while None in terms_list:
                terms_list.remove(None)
            terms_filtered: tuple[Expr, ...] = tuple([t for t in terms_list if t is not None])
        else:
            terms_filtered: tuple[Expr, ...] = tuple([t for t in terms if t is not None])

        self.terms: List[Expr] = list(terms_filtered)
        self.id = str(uuid.uuid4())

    def __str__(self):
        expression = ""
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

    def clone(self, *new_terms, keep_id = True):
        new_Add = Add(*new_terms)
        if keep_id == True:
            new_Add.id = self.id

        return new_Add

    def set_subexprs(self, *new_terms):
        self.terms: List[Expr] = list(new_terms)
    
    def replace(self, old, new):
        if self == old:
            return new

        new_terms = []
        changed = False

        for term  in self.terms:
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
    
     
    #Pop
    """
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
    """

    def to_dict(self) -> dict:
        return {
            "type": "add",
            "terms": [term.to_dict() for term in self.terms],
            "id": self.id
        }

class Neg(Expr):
    def __init__(self, expr: Expr):
        if isinstance(expr, Neg):
            self.expr = expr.expr
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

    def clone(self, *new_terms, keep_id = True):
        if len(new_terms) > 1:
            raise ValueError("You used more than 1 term in Neg, Neg can not handle that yet")
    
        new_Neg = Neg(*new_terms)
        if keep_id == True:
            new_Neg.id = self.id
        return new_Neg
    
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
        
        if None in factors:
            factors_list = [f for f in factors if f is not None]
            factors = tuple(factors_list)


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

    def clone(self, *new_factors, keep_id = True):

        new_Mult = Mult(*new_factors)
        if keep_id == True:
            new_Mult.id = self.id

        return new_Mult
    
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
        if numerator is None and denominator != None:
            self.numerator = Const(1)
            self.denominator = denominator
        elif denominator is None and numerator != None:
            self.numerator = numerator
            self.denominator = Const(1)
        elif numerator is None and denominator is None: #Not sure if this case is needed
            self.numerator = Const(1)
            self.denominator = Const(1)
        else:
            self.numerator = numerator
            self.denominator = denominator
        
        self.id = str(uuid.uuid4())

    #This was added for pylance by copilot
    def replace(self, old, new):
        if self == old:
            return new
        numerator_replaced = self.numerator.replace(old, new)
        denominator_replaced = self.denominator.replace(old, new)
        if numerator_replaced == self.numerator and denominator_replaced == self.denominator:
            return self
        return Frac(numerator_replaced, denominator_replaced)

    def __str__(self):
        numerator_str = self.numerator
        denominator_str = self.denominator
        
        if isinstance(self.numerator, Add):
            numerator_str = f"({self.numerator})"
        if isinstance(self.denominator, Add):
            denominator_str = f"({self.denominator})"

        return f"({numerator_str}/{denominator_str})"

    def __eq__(self, other):
        return (isinstance(other, Frac) and self.numerator == other.numerator and self.denominator == other.denominator)

    def get_subexprs(self):
        return [self.numerator, self.denominator]

    def set_subexprs(self, new_numerator, new_denominator):
        self.numerator = new_numerator
        self.denominator = new_denominator

    def clone(self, *new_terms, keep_id = True):
        if len(new_terms) > 2:
            raise ValueError("You used more than 2 term in Frac, Frac can only take 2")
            
        new_Frac = Frac(*new_terms)
        if keep_id == True:
            new_Frac.id = self.id
        return new_Frac
    
    def flatten(self):
        num_flat = self.numerator.flatten()
        den_flat = self.denominator.flatten()
        # If denominator is 1, just return the numerator
        if isinstance(den_flat, Const) and str(den_flat.value) == "1":
            return num_flat
        return Frac(num_flat, den_flat)

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

    def __len__(self):
        return 2  # numerator and denominator

    def __getitem__(self, index):
        if index == 0:
            return self.numerator
        elif index == 1:
            return self.denominator
        else:
            raise IndexError("Frac only supports indices 0 (numerator) and 1 (denominator)")

class Eq(Expr):
    def __init__(self, lhs: Optional[Expr] = Const(0), rhs: Optional[Expr] = Const(0)):
        if lhs is None: 
            self.lhs = Const(0)
        else:
            self.lhs = lhs

        if rhs is None:
            self.rhs = Const(0)
        else:
            self.rhs = rhs

        self.id = str(uuid.uuid4())

    def __str__(self):
        return " = ".join((str(self.lhs), str(self.rhs)))
    
    def __eq__(self, other):
        return( isinstance(other, Eq) and self.lhs == other.lhs and self.rhs == other.rhs)
    
    def to_dict(self):
        return {
            "type": "eq",
            "lhs": self.lhs.to_dict(),
            "rhs": self.rhs.to_dict(),
            "id": self.id
            }

    def get_side(self, side: str):
        if side is "lhs":
            return self.lhs
        elif side is "rhs":
            return self.rhs
        else:
            raise ValueError("Get_side did not recieve either 'lhs' or 'rhs'")  
          
    def get_subexprs(self):
        return [self.lhs, self.rhs]
    
    def set_subexprs(self, new_lhs, new_rhs):
        self.lhs = new_lhs
        self.rhs = new_rhs
    
    def clone(self, *new_expressions: Expr, keep_id = True):

        new_Eq: Eq = Eq(*new_expressions)
        if keep_id == True:
            new_Eq.id = self.id
    
        return new_Eq

    def flatten(self):
        # Flatten both sides of the equation
        lhs_flat = self.lhs.flatten()
        rhs_flat = self.rhs.flatten()
        return Eq(lhs_flat, rhs_flat)

    def replace(self, old, new):
        if self == old:
            return new
        lhs_replaced = self.lhs.replace(old, new)
        rhs_replaced = self.rhs.replace(old, new)
        if lhs_replaced == self.lhs and rhs_replaced == self.rhs:
            return self
        return Eq(lhs_replaced, rhs_replaced)

    def to_latex(self):
        lhs_latex = self.lhs.to_latex()
        rhs_latex = self.rhs.to_latex()
        return f"{lhs_latex} = {rhs_latex}"

    def move_expr(self, target_id, origin, dest) -> Expr:
        path: Optional[list] = self.get_path_to(target_id)
        if path is None:
            raise ValueError("get_path_to returned None")
        


        popped_Eq: Optional[Expr] = self.remove_expr(target_id)
        if popped_Eq is None:
            raise ValueError("remove_expr returned None")
        
        target: Optional[Expr] = self.find_by_id(target_id)
        if target is None:
            raise ValueError("find_by_id returned None")
        
        parent_Expr: Expr = path[-2]

        
        
        #This can be streamlined much more
        if isinstance(parent_Expr, Neg):
            Neg_Parent: Expr = path[-3]
            if isinstance(Neg_Parent, Add) or isinstance(Neg_Parent, Add):
                
                for expr in path:
                    if isinstance(expr, Mult) or isinstance(expr, Frac):
                        raise ValueError(f"Can not move {target}, it is nested ")

                inverted_target = target #this variable name is shit
                dest_Expr = Add(self.get_side(dest), inverted_target)
            elif isinstance(Neg_Parent, Mult):
                for expr in path:
                    if isinstance(expr, Add):
                        raise ValueError(f"Can not move {target}, it is nested ")
                
                
                inverted_target = path[-2] #this variable name is shit, also consider naming path[-2]
                dest_Expr = Frac(self.get_side(dest), inverted_target)
            elif isinstance(Neg_Parent, Frac):
                
                for expr in path:
                    if isinstance(expr, Add):
                        raise ValueError(f"Can not move {target}, it is nested ")                
                
                if Neg_Parent.numerator == parent_Expr:
                    inverted_target = path[-2]
                    dest_Expr = Frac(self.get_side(dest), inverted_target)
                elif Neg_Parent.denominator == parent_Expr:
                    inverted_target = path[-2]
                    dest_Expr = Mult(self.get_side(dest), inverted_target)
                else:
                    raise ValueError("Target is not a numerator or denominator in Frac")
            else:
                raise ValueError("Parent of Neg Expr case was not catched")
        elif isinstance(parent_Expr, Add) or isinstance(parent_Expr, Eq):
            
            for expr in path:
                if isinstance(expr, Mult) or isinstance(expr, Frac):
                    raise ValueError(f"Can not move {target}, it is nested ")
                
            inverted_target = Neg(target)
            dest_Expr = Add(self.get_side(dest), inverted_target)
        elif isinstance(parent_Expr, Mult):
            for expr in path:
                if isinstance(expr, Add):
                    raise ValueError(f"Can not move {target}, it is nested ")
            
            inverted_target = target
            dest_Expr = Frac(self.get_side(dest), inverted_target)
        elif isinstance(parent_Expr, Frac):
            # Check if target is numerator or denominator
            for expr in path:
                if isinstance(expr, Add):
                    raise ValueError(f"Can not move {target}, it is nested ")

            
            if parent_Expr.numerator == target:
                inverted_target = target
                dest_Expr = Frac(self.get_side(dest), inverted_target)
            elif parent_Expr.denominator == target:
                inverted_target = target
                dest_Expr = Mult(self.get_side(dest), inverted_target)
            else:
                raise ValueError("Target is not a numerator or denominator in Frac")
        else:
            raise ValueError("Parent Expr case was not catched")
        
        
    

        #run a check here maybe, see if the expr should be allowed to move
        
        #Not sure on the best practice to get a sub expression from self.

        if dest is "rhs":
            
            final_Expr: Expr = self.clone(popped_Eq[0], dest_Expr) 
        
        elif dest is "lhs":
            new_lhs_expr: Expr = Add(self.lhs, inverted_target)
            final_Expr: Expr = self.clone(dest_Expr,popped_Eq[1]) 
        else:
            raise ValueError("Error in last part of function move_expr")

        return final_Expr.flatten()


        



#This is terrible, but it works for now


    
    """
    def pop_expr(self, target_id, from_side, to_side):
        if from_side == "lhs":
            return self.lhs.pop_expr(target_id) # type: ignore
        elif from_side == "rhs":
            return self.rhs.pop_expr(target_id) # type: ignore
    """
                
    """
    def move_expr(self, target_id, from_side, to_side):
        new_expr, popped_term = self.pop_expr(target_id, from_side, to_side) # type: ignore

        if from_side == "lhs":
            lhs_new = new_expr
            rhs_new = Add(self.rhs, Neg(popped_term)).flatten() if to_side == "rhs" else self.rhs # type: ignore
        elif from_side == "rhs":
            rhs_new = new_expr
            lhs_new = Add(self.lhs, Neg(popped_term)).flatten() if to_side == "lhs" else self.lhs # type: ignore
        else:
            raise ValueError("Invalid side")

        return Eq(lhs_new, rhs_new)
    """