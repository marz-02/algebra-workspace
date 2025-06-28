from flask import Flask, render_template, request, jsonify
from symbolic_math import Expr, Var, Const, Neg, Add, Mult, Eq
import uuid
app = Flask(__name__) #Creates a new Flask application instance.

expr = Eq(
    Add(Var("x")),
    Add(Var("z"), Neg(Var("y")))
)

expr_dict = expr.to_dict()

@app.route("/get_expression", methods=["GET"])
def get_expression():
    return jsonify(expr_dict)




def generate_expression():
    def make_var(name):
        return {"type": "Var", "name": name, "id": str(uuid.uuid4())}
    
    def make_add(lhs, rhs):
        return {"type": "Add", "terms": [lhs, rhs], "id": str(uuid.uuid4())}
    
    def make_eq(lhs, rhs):
        return {"type": "Eq", "lhs": lhs, "rhs": rhs, "id": str(uuid.uuid4())}
    
    # Example: x + y = z
    x = make_var("x")
    y = make_var("y")
    z = make_var("z")
    return make_eq(make_add(x, y), z)

@app.route("/expression")
def expression():
    return jsonify(generate_expression())



#Defines the homepage route (/). 
#When you visit http://..., flask calls index() and returns the rendered index.html from our templates folder
@app.route("/")
def index():
    return render_template("index.html")  # Loads the page

#Defines an API route /process that accepts POST requests.
#Reads JSON data from the incoming request (request.get_json()).
#Gets the expression string from the "expr" field.
@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    expr_input = data.get("expr", "")
    
    # Placeholder response logic (you can connect expression.py later)
    print(f"User input received: {expr_input}")
    return jsonify({
        "status": "success",
        "message": f"You sent: {expr_input}"
    })

if __name__ == "__main__":
    app.run(debug=True)
