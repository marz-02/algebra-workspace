
function renderExpr(expr) {
  if (expr.type === "Eq") {
    const eq = document.createElement("span");
    eq.className = "equation";

    const lhs = document.createElement("span");
    lhs.className = "expression lhs";
    lhs.id = "lhs";
    lhs.appendChild(renderExpr(expr.lhs));

    const equals = document.createElement("span");
    equals.className = "equals";
    equals.textContent = "=";

    const rhs = document.createElement("span");
    rhs.className = "expression rhs";
    rhs.id = "rhs";
    rhs.appendChild(renderExpr(expr.rhs));

    eq.appendChild(lhs);
    eq.appendChild(equals);
    eq.appendChild(rhs);
    return eq;
  }

  if (expr.type === "Add") {
    const add = document.createElement("span");
    add.className = "expression add";
    expr.terms.forEach((term, i) => {
      add.appendChild(renderExpr(term));
      if (i < expr.terms.length - 1) {
        const plus = document.createElement("span");
        plus.className = "operator";
        plus.textContent = "+";
        add.appendChild(plus);
      }
    });
    return add;
  }

  if (expr.type === "Var") {
    const v = document.createElement("span");
    v.className = "expression var";
    v.textContent = expr.name;
    v.id = expr.id;
    v.setAttribute("draggable", "true");
    return v;
  }

  return document.createTextNode("?");
}
function enableDragging() {
  document.querySelectorAll(".expression.var").forEach(el => {
    el.addEventListener("dragstart", event => {
      event.dataTransfer.setData("text/plain", el.id);
      console.log("Dragging", el.id);
    });
  });

  document.querySelectorAll(".lhs, .rhs").forEach(target => {
    target.addEventListener("dragover", event => {
      event.preventDefault(); // Allow drop
    });

    target.addEventListener("drop", event => {
      event.preventDefault();
      const draggedId = event.dataTransfer.getData("text/plain");
      const targetId = target.id;

      console.log(`Dropped ${draggedId} onto ${targetId}`);
    });
  });
}
const expr1 = {
  type: "add",
  terms: ["x", "y", "z"]
};

function renderExpression(expr) {
  const container = document.createElement("div");
  container.className = "expression";

  expr.terms.forEach((term, index) => {
    const termDiv = document.createElement("div");
    termDiv.className = "term";
    termDiv.textContent = term;
    container.appendChild(termDiv);

    if (index < expr.terms.length - 1) {
      const op = document.createElement("div");
      op.className = "op";
      op.textContent = getSymbol(expr.type);
      container.appendChild(op);
    }
  });

  return container;
}

function getSymbol(type) {
  switch (type) {
    case "add": return "+";
    case "mult": return "×";
    case "sub": return "−";
    case "div": return "÷";
    default: return "?";
  }
}
/*
document.addEventListener("DOMContentLoaded", () => {
  const paper = document.getElementById("paper");
  const exprElem = renderExpression(expr1);
  paper.appendChild(exprElem);
});
*/