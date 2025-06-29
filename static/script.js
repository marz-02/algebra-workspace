document.addEventListener("DOMContentLoaded", () => {
  console.log("script.js loaded");

  // === Section 1: DOM references ===
  const testButton = document.getElementById("testButton");
  const loadExprButton = document.getElementById("loadExprButton");
  const line = document.getElementById("line1");
  const mathField = document.getElementById("mathField");
  
  const submitMathButton = document.getElementById("addButton");

  // === Section 2: Event listeners ===
  if (testButton) {
    testButton.addEventListener("click", () => {
      console.log("Test button clicked!");
      const payload = { expr: "2x + 3" };

      fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(res => res.json())
        .then(data => console.log("Response from /process:", data));
    });
  }

  if (loadExprButton) {loadExprButton.addEventListener("click", loadExpression);}



  submitMathButton.addEventListener("click", () => {
    console.log("Add Expression button clicked!");
    const latex = mathField.value;
    const tree = mathField.getValue("math-json")
    console.log("LaTeX input:", tree);
    sendUserInput(tree); // Send the LaTeX input to the server
  
  // You could also send it to Flask here
});

  // === Section 3: Fetch on page load ===

  /*
  fetch("/expression")
    .then(res => res.json())
    .then(expr => {
      if (line) {
        line.innerHTML = "";
        line.appendChild(renderExpr(expr));
        enableDragging();  // assumes this is a defined function
      }
    });
  */

  // === Section 4: Functions ===

function sendUserInput(input) {
  console.log("Sending user input:", input);
  fetch("/process", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input })
  })
    .then(res => res.json())
    .then(data => {
      console.log("Response from /process:", data);
      // Don't update DOM here — just log or handle silently
    })
    .catch(err => console.error("Error in sendUserInput:", err));
}

  function loadExpression() {
    fetch("/get_expression") //Fetch is a built-in function in JavaScript that allows you to HTTP requests. Sends GET to flask route /get_expression
      .then(res => res.json())
      .then(data => {
        console.log("Received:", data);
        debugdisplay(data); // Display the data in a debug plackard
      })
      .catch(err => console.error("Fetch error:", err));
    
    console.log("Load expression button clicked!");  
    ;
  }

});

function debugdisplay(data) {
  const plackard = document.createElement("div");
  plackard.className = "debug-display";
  const line1 = document.createElement("div");
  const line2 = document.createElement("div");
  line1.className = "line";
  line2.className = "line";
  line1.id = "line1.1";
  line2.id = "line1.2";
  plackard.appendChild(line1);
  plackard.appendChild(line2);
  
  line1.textContent = JSON.stringify(data, null, 2);
  line2.appendChild(renderExpr(data)); // Assuming data.expr is the expression object

  document.body.appendChild(plackard);
}
function renderExpr(expr) {
  if (expr.type === "var") {
    const v = document.createElement("span");
    v.className = "expression var";
    v.textContent = expr.name;
    v.id = expr.id;
    v.setAttribute("draggable", "true");
    return v;
  }
  else if (expr.type === "const") {
    const c = document.createElement("span");
    c.className = "expression const";
    c.textContent = expr.value;
    c.id = expr.id;
    c.setAttribute("draggable", "true");
    return c;
  }
  else if (expr.type === "neg") {
    const neg = document.createElement("span");
    neg.className = "expression neg";
    neg.textContent = "-";
    neg.appendChild(renderExpr(expr.expr));
    return neg;
  }
else if (expr.type === "add") {
  const add = document.createElement("span");
  add.className = "expression add";

  expr.terms.forEach((term, i) => {
    let isNeg = term.type === "neg";

    // First term: show normally (neg or not)
    if (i === 0) {
      if (isNeg) {
        const minus = document.createElement("span");
        minus.className = "operator";
        minus.textContent = "-";
        add.appendChild(minus);
        add.appendChild(renderExpr(term.expr));  // Skip outer neg
      } else {
        add.appendChild(renderExpr(term));
      }
    } else {
      const op = document.createElement("span");
      op.className = "operator";
      op.textContent = isNeg ? " - " : " + ";
      add.appendChild(op);

      if (isNeg) {
        add.appendChild(renderExpr(term.expr));  // Skip outer neg
      } else {
        add.appendChild(renderExpr(term));
      }
    }
  });

  return add;
}
  else if (expr.type === "mult") {
    const mult = document.createElement("span");  
    mult.className = "expression mult";
    expr.factors.forEach((factor, i) => {
      mult.appendChild(renderExpr(factor));
      if (i < expr.factors.length - 1) {
        const times = document.createElement("span");
        times.className = "operator";
        times.textContent = "×"; // Use multiplication sign
        mult.appendChild(times);
      }
    });
    return mult;
  }
  else if (expr.type === "eq") {
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
}




  