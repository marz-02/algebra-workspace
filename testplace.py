from symbolic_math import Var, Const, Add, Mult, Eq

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


line1xx = line1xx.move_expr(idofy, "lhs")
print("\n",line1xx,"\n")

#print(line1xx.pop_expr(idofy, "lhs"))




#thisy = line1xx.find_by_id(idofy)

#thisy = None


print("-------------------------------------------------------------------------------------")

print(line1xx.to_dict())