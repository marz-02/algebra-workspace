from flask import Flask, render_template, request, jsonify
from symbolic_math import Expr, Var, Const, Neg, Add, Mult, Frac, Eq
from symbolic_math.utils import tokenize_latex, parse_latex_expression, latex_to_expression_tree, str_to_expression_list, user_input_to_expression_tree
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

@app.route("/process", methods=["POST"])
def process_input():
    data = request.get_json()
    user_input = data.get("input")

    print("Received user input:", user_input)  # This will show up in your Flask terminal
    
    expr_tree = user_input_to_expression_tree(user_input)
    expr_dict = expr_tree.to_dict()

    global CURRENT_EXPRESSION
    CURRENT_EXPRESSION = user_input_to_expression_tree(user_input)

    return jsonify({
        "status": "ok",
        "expr": expr_dict  # This will be used by renderExpr on the frontend
    })

# Global expression tree (for now, just to test)
CURRENT_EXPRESSION = None

@app.route("/move_term", methods=["POST"])
def move_term():
    data = request.get_json()
    term_id = data.get("term_id")
    original_side = data.get("from")  # "lhs" or "rhs"
    target_side = data.get("to")  # "lhs" or "rhs"

    print(f"Move request received: term_id={term_id}, from {original_side} to {target_side}")

    global CURRENT_EXPRESSION

    if CURRENT_EXPRESSION is None:
        return jsonify({"status": "error", "message": "No current expression loaded"}), 400
    print(f"Current expression: {CURRENT_EXPRESSION}")

    
    # THIS IS GOING TO BE USED  
    
    #if original_side in ["lhs", "rhs"] and target_side in ["lhs", "rhs"]:
    #    if original_side != target_side:
    #        CURRENT_EXPRESSION = CURRENT_EXPRESSION.move_expr(term_id, original_side, target_side)
 
    #print(f"Moved expression: {CURRENT_EXPRESSION.move_expr(term_id, original_side, target_side)}")
    
    
    #CURRENT_EXPRESSION = move_expr(self, target_id, side):
    # Basic demonstration logic:
    # Just print, or simulate moving the term.
    # Later: Search for term_id in CURRENT_EXPRESSION and move to target_side
    # For now, just echo back what we got

    return jsonify({
        "status": "ok",
        "term_id": term_id,
        "moved_to": target_side,
        "expr": CURRENT_EXPRESSION.to_dict()  # ✅ Fix here
    })



def extract_add_terms(expr):
    """Returns a list of terms, even if the expression is just a single term."""
    if expr.type == "add":
        return expr.terms.copy()
    else:
        return [expr]

def flip_sign(expr):
    """Returns the negated version of the term."""
    if expr.type == "neg":
        return expr.expr  # Double negation cancels
    else:
          # update to match your class
        return Neg(expr)
"""

@app.route("/move_term", methods=["POST"])
def move_term():
    global current_expr  # We will update this

    data = request.get_json()
    term_id = data["term_id"]
    target_side = data["target_side"]  # "lhs" or "rhs"

    if current_expr is None or current_expr.type != "eq":
        return jsonify({"error": "No valid equation loaded."}), 400

    lhs_terms = extract_add_terms(current_expr.lhs)
    rhs_terms = extract_add_terms(current_expr.rhs)

    # Try to find the term
    found_term = None
    from_side = None

    for side_name, terms in [("lhs", lhs_terms), ("rhs", rhs_terms)]:
        for term in terms:
            if getattr(term, "id", None) == term_id:
                found_term = term
                from_side = side_name
                break
        if found_term:
            break

    if not found_term:
        return jsonify({"error": "Term not found"}), 404

    # Remove term from the original side
    if from_side == "lhs":
        lhs_terms.remove(found_term)
    else:
        rhs_terms.remove(found_term)

    # Flip sign and add to target side
    flipped_term = flip_sign(found_term)
    if target_side == "lhs":
        lhs_terms.append(flipped_term)
    else:
        rhs_terms.append(flipped_term)

    # Rebuild the expression
    from yourmodule import Add, Eq  # update to match your imports
    current_expr = Eq(Add(lhs_terms), Add(rhs_terms))

    return jsonify({"expr": current_expr.to_dict()})

"""
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
