
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