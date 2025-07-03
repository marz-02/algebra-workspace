from symbolic_math import Expr, Var, Const, Neg, Add, Mult, Frac, Eq
from symbolic_math.utils import tokenize_latex, parse_latex_expression

from typing import Optional

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


#line1xx = line1xx.move_expr(idofy, "lhs" , "rhs")
#print("\n",line1xx,"\n")

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
equation2 = Eq( Add( Var("x"), Var("y")),Var("z"))

y_id = (equation1.get_subexprs()[0]).get_subexprs()[1].get_id()

print(equation1.depth_search(y_id))  # Should return the Var("y") object

path = equation1.get_path_to(y_id)
print(len(path) if path is not None else 0)

print(equation1.get_path_to(y_id),"yo mr white")  # Should return the path to Var("y")

print(equation1.path_display(y_id))  # Should print the path to Var("y")

print(equation1.remove_expr(y_id))

#print(equation2.remove_expr("afsdfasdf"))

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

x = Var("x")
xid = x.id

y = Var("y")
yid = y.id

z = Var("z")
zid = z.id

eq1 = Eq(Add(x, y), z)

# 2. x = y + z
eq2 = Eq(x, Add(y, z))

# 3. x / y = z
eq3 = Eq(Frac(x, y), z)

# 4. (x + y) / z = Const(1)
eq4 = Eq(Frac(Add(x, y), z), Const(1))

# 5. (x * y) + (z / 2) = Const(0)
eq5 = Eq(
    Add(
        Mult(x, y),
        Frac(z, Const(2))
    ),
    Const(0)
)

# 6. Nested fraction: ((x / y) / z) = Const(5)
eq6 = Eq(Frac(Frac(x, y), z), Const(5))

# 7. Flat multiplication: x * y * z = 3
eq7 = Eq(Mult(x, y, z), Const(3))

# 8. x + x = 2x
eq8 = Eq(Add(y, z), Mult(Const(2), x))

print("\n--------------------------------------------------------")
print(eq1)
print(eq2)
print(eq3)
print(eq4)
print(eq5)
print(eq6)
print(eq7)
print(eq8)
print("--------------------------------------------------------\n")

[eq1,eq2,eq3,eq4,eq5,eq6,eq7,eq8] # type: ignore
[xid,yid,zid] # type: ignore
i1 = 1
i2 = 1

for equation in [eq1,eq2,eq3,eq4,eq5,eq6,eq7,eq8]:
    for var in [x,y,z]:
        print("\n")
        if i2 is 4:
            i1 += 1
            i2 = 1

        print(f"#{i1}.{i2}")
        i2 += 1
        print(equation)
        print(f"moving {var}")
        #print((equation.remove_expr(id)))
        #path: Optional[list] = equation.get_path_to(id)
        try:
            if var in equation[0]:
                print(equation.move_expr(var.get_id(),"lhs","rhs"))
            elif var in equation[1]:
                print(equation.move_expr(var.get_id(),"rhs","lhs"))
        #print(equation.move_expr(id,"lhs","rhs"))
        except ValueError as e:
            print(f"Error: {e}")

