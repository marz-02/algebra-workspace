from typing import List, Optional
from collections import Counter
import uuid
from abc import ABC, abstractmethod

class Expr(ABC):
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())
        self.side = None
        
    value = None

    def __iter__(self):
        """Yield self and all subexpressions recursively (pre-order traversal)."""
        yield self
        for subexpr in self.get_subexprs():
            yield from subexpr

    def __repr__(self):
        classname = self.__class__.__name__
        # Show subexpressions for non-leaf nodes
        if hasattr(self, 'get_subexprs') and self.get_subexprs():
            return f"{classname}({','.join(map(repr, self.get_subexprs()))})"
        elif hasattr(self, 'name') and self.name is not None:
            return f"{classname}({self.name})"
        elif hasattr(self, 'value') and self.value is not None:
            return f"{classname}({self.value})"
        else:
            return classname

    def __len__(self):
        """Return the number of immediate subexpressions."""
        return len(self.get_subexprs())

    def __getitem__(self, index):
        """Allow indexing into the list of subexpressions."""
        return self.get_subexprs()[index]

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
    
    def _depth_search(self, target_id, depth=0):
        depth += 1
        if self.id == target_id:
            return depth
        if len(self.get_subexprs()) == 0: # Is a leaf node
            return None
        for subexpr in self.get_subexprs():
            result = subexpr._depth_search(target_id, depth)
            if result is not None:
                return result
            
    def depth_search(self, target_id):
        """
        Perform a depth-first search to find the target_id.
        Returns the depth if found, otherwise None.
        """
        return self._depth_search(target_id, 0)
    
    def remove_expr(self, target_id, target=None, debug=False) -> Optional["Expr"]: # This is terible...
        # Gets target object on first run
        if target is None:
            target = self.find_by_id(target_id)
            if debug is True:    
                print(f"Target Found: {target}")
            
            if target is None:
                raise ValueError(f"Expression with id = {target_id} not found in tree.")    

        # If we found the target
        if self.id == target.id:
            return None
        
        expressions = []
        for expr in self.get_subexprs():
            result = expr.remove_expr(target_id, target)
            expressions.append(result)
        
        return self.clone(*expressions)
        
    def get_path_to(self, target_id, path=None) -> list | None:
        if path is None:
            path = []
        if self.id == target_id:
            return path + [self]
        for sub in self.get_subexprs():
            result = sub.get_path_to(target_id, path + [self])
            if result:
                return result
        return None
    
    def path_display(self, target_id: str) -> str:
        path: list | None = self.get_path_to(target_id)

        if path is None:
            return "no path"
        
        phrase = "Path to target ID:"
        for element in path:
            phrase += f" {str(element)}  --> " 
        phrase = phrase.rstrip(" --> ")
        return phrase
    
    def is_multiplicative_chain(self, target_id):
        path = self.get_path_to(target_id)
        if path is None:
            return False
        #return all(isinstance(node, (Mult, Frac, Pow)) for node in path)            
    
    
    
    @abstractmethod
    def get_subexprs(self) -> list["Expr"]:
        pass

    @abstractmethod
    def clone(self) -> "Expr":
        pass

    @abstractmethod
    def replace(self, old: "Expr", new: "Expr") -> "Expr":
        pass

    @abstractmethod
    def flatten(self) -> "Expr":
        pass

    @abstractmethod
    def to_latex(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    """    
    @abstractmethod
    def pop_expr(self, target_id, from_side, to_side):
        pass
    """
    
