from typing import List
from collections import Counter
import uuid

class Expr:
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())
        self.side = None


    def __repr__(self):
        classname = self.__class__.__name__
        if hasattr(self, 'name'):
            return f"{classname}({self.name})"
        elif hasattr(self, 'value'):
            return f"{classname}({self.value})"
        elif hasattr(self, 'get_subexprs'):
            return f"{classname}({','.join(map(repr, self.get_subexprs()))})"
        else:
            return classname

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
    
    def get_path_to(self, target_id, path=None):
        if path is None:
            path = []
        if self.id == target_id:
            return path + [self]
        for sub in self.get_subexprs():
            result = sub.get_path_to(target_id, path + [self])
            if result:
                return result
        return None
    
    def path_display(self, target_id):
        path = self.get_path_to(target_id)

        phrase = "Path to target ID:"
        for element in path:
            phrase += f" {str(element)}  --> " 
        phrase = phrase.rstrip(" --> ")
        return phrase
    
    def is_multiplicative_chain(self, target_id):
        path = self.get_path_to(target_id)
        if path is None:
            return False
        return all(isinstance(node, (Mult, Frac, Pow)) for node in path)