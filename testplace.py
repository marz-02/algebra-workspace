from symbolic_math import Expr, Var, Const, Neg, Add, Mult, Frac, Eq
from symbolic_math.utils import tokenize_latex, parse_latex_expression

import inspect

x = Var("x")

y = Var("y")

z = Var("z")

a = Const("5")

line1 = Eq(
    Add( Var("x"), Var("y")),
    Var("z")
)




"""
q = Var("q")

qid = q.get_id()

line2 = Eq(
    Add( Var("x"), q),
    Var("z")
)
"""
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


###---Test-Zone--------------------------------------------------------------------------

line1xx = Eq(
    Add( Var("x"), Var("y")),
    Var("z")
)
print("-------------------------------------------------------------------------------------")

print("\n",line1xx,"\n")

#print(line1xx.get_subexprs())

idofy = (line1xx.get_subexprs()[0]).get_subexprs()[1].get_id()


line1xx = line1xx.move_expr(idofy, "lhs" , "rhs")
print("\n",line1xx,"\n")

#print(line1xx.pop_expr(idofy, "lhs"))




#thisy = line1xx.find_by_id(idofy)

#thisy = None


print("-------------------------------------------------------------------------------------")

print(line1xx.to_dict())

print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")

x = Var("x")
y = Var("y")
frac = Frac(x, y)
print(frac)

a = Const(1)
b = Add(Var("x"), Const(2))
c = Frac(a, b)
print(c)  # Expect: 1 / (x + 2)

lhs = Frac(Add(Var("x"), Var("y")), Const(2))
rhs = Var("z")
eq = Eq(lhs, rhs)
print(eq)  # Expect: (x + y)/2 = z

a = Add(Var("x"), Frac(Var("y"), Const(2)))
print(a)  # Expect: x + y/2

m = Mult(Const(3), Frac(Var("a"), Var("b")))
print(m)  # Expect: 3 × (a/b)

frac = Frac(Var("x"), Add(Var("y"), Const(1)))
print(frac.to_latex())  # Expect: \frac{x}{y + 1}

latex = r"1+\frac{-x}{z}"
tokens = tokenize_latex(latex)
print(tokens)


latex = r"1+\frac{-x}{z}"
expr = parse_latex_expression(latex)
print(expr,"yep")


lhs = Frac(Add(Var("x"), Var("y")), Const(2))
rhs = Var("z")
eq1 = Eq(lhs, rhs)

equation1 = Eq( Add( Var("x"), Var("y")),Var("z"))

y_id = (equation1.get_subexprs()[0]).get_subexprs()[1].get_id()

print(equation1.depth_search(y_id))  # Should return the Var("y") object

print(equation1.get_path_to(y_id))  # Should return the path to Var("y")

print(equation1.path_display(y_id))  # Should print the path to Var("y")

#print(dir(Expr))  # includes methods, attributes, and special methods


"""
print(Expr.__subclasses__())
print("\n\n")
def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        s for c in cls.__subclasses__() for s in all_subclasses(c)
    )


def list_all_subclasses_and_methods(cls):
    for subclass in all_subclasses(cls):
        print(f"\nSubclass: {subclass.__name__}")
        methods = [name for name, obj in inspect.getmembers(subclass, predicate=inspect.isfunction)
                   if subclass.__dict__.get(name) is obj]
        print(f"Methods: {methods}")

list_all_subclasses_and_methods(Expr)
"""
"""
def is_multiplicative_chain(self, target_id):
    path = self.get_path_to(target_id)
    if path is None:
        return False
    return all(isinstance(node, (Mult, Frac, Pow)) for node in path)
"""