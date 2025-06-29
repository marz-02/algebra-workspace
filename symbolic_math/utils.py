from .base import Expr 

from .leaves import Var, Const
from .operations import Neg, Add, Mult, Frac, Eq

from typing import List
from collections import Counter
import uuid

import re

def my_strip1(string):
    result = []
    buffer = ''
    depth = 0

    for char in string:
        if char == '[':
            if depth > 0:
                buffer += char
            depth += 1

        elif char == ']':
            depth -= 1
            if depth > 0:
                buffer += char

        elif char == ',' and depth == 1:
            result.append(buffer.strip().strip('"'))
            buffer = ''
        else:
            buffer += char

    if buffer:
        result.append(buffer.strip().strip('"'))

    return result


def my_strip2(flat_list):
    deep_list = []
    for element in flat_list:
        if element.startswith('['):
            nested = my_strip1(element)
            deep_list.append(my_strip2(nested))
        else:
            deep_list.append(element)
    return deep_list


def str_to_expression_list(str: str) -> list:
    """
    Converts a string representation of a list to an actual list.
    Handles nested lists and removes quotes around elements.
    """
    flat_list = my_strip1(str)
    return my_strip2(flat_list)

def from_mathjson(obj) -> Expr:
    if isinstance(obj, list):
        head = obj[0]

        if head == "Add":
            terms = [from_mathjson(arg) for arg in obj[1:]]
            return Add(*terms)

        elif head == "Multiply":
            factors = [from_mathjson(arg) for arg in obj[1:]]
            return Mult(*factors)

        elif head == "Negate":
            return Neg(from_mathjson(obj[1]))

        elif head == "Divide":
            num = from_mathjson(obj[1])
            denom = from_mathjson(obj[2])
            return Frac(num, denom)

        elif head == "Equal":
            lhs = from_mathjson(obj[1])
            rhs = from_mathjson(obj[2])
            return Eq(lhs, rhs)

        else:
            raise ValueError(f"Unsupported MathJSON operation: {head}")

    elif isinstance(obj, str):
        return Var(obj)

    elif isinstance(obj, (int, float)):
        return Const(obj)

    else:
        raise TypeError(f"Invalid MathJSON token: {obj}")

def user_input_to_expression_tree(user_input: str) -> Expr:
    """
    Converts user input (string) to an expression tree.
    Handles both LaTeX and MathJSON formats. No it doesnt lol
    """
    list_expression = str_to_expression_list(user_input)
    expression_tree = from_mathjson(list_expression)
    return expression_tree 











class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def next(self):
        tok = self.peek()
        self.pos += 1
        return tok

def tokenize_latex(expr: str):
    token_pattern = r'''
        (\\[a-zA-Z]+)      |  # LaTeX commands like \frac, \sqrt
        ([{}()])           |  # Brackets
        ([+\-*/=])         |  # Operators
        (\d+\.\d+|\d+)     |  # Numbers (float or int)
        ([a-zA-Z])            # Variables or single-letter names
    '''
    tokens = re.findall(token_pattern, expr, re.VERBOSE)
    # Flatten and remove empty strings
    tokens = [token for group in tokens for token in group if token]
    return tokens

def parse_latex_expression(latex: str) -> Expr:
    tokens = tokenize_latex(latex)
    ts = TokenStream(tokens)
    return parse_expression(ts)


def parse_expression(ts: TokenStream) -> Expr:
    term = parse_term(ts)
    while ts.peek() in ('+', '-'):
        op = ts.next()
        right = parse_term(ts)
        if op == '+':
            term = Add(term, right)
        else:
            term = Add(term, Neg(right))  # Represent subtraction as + Neg
    return term

def parse_term(ts: TokenStream) -> Expr:
    factor = parse_factor(ts)
    while ts.peek() in ('*', '/'):
        op = ts.next()
        right = parse_factor(ts)
        if op == '*':
            factor = Mult(factor, right)
        else:
            factor = Frac(factor, right)
    return factor

def parse_factor(ts: TokenStream) -> Expr:
    tok = ts.peek()

    if tok == '-':
        ts.next()
        return Neg(parse_factor(ts))
    
    if tok == '\\frac':
        ts.next()  # consume \frac
        assert ts.next() == '{'
        numerator = parse_expression(ts)
        assert ts.next() == '}'
        assert ts.next() == '{'
        denominator = parse_expression(ts)
        assert ts.next() == '}'
        return Frac(numerator, denominator)

    if tok == '{':
        ts.next()
        expr = parse_expression(ts)
        assert ts.next() == '}'
        return expr

    if re.match(r'\d+', tok):  # Constant
        ts.next()
        return Const(int(tok))

    if re.match(r'[a-zA-Z]', tok):  # Variable
        ts.next()
        return Var(tok)

    raise ValueError(f"Unexpected token: {tok}")

def latex_to_expression_tree(latex: str) -> Eq:
    side_list = latex.split("=")
    if len(side_list) != 2:
        raise ValueError("Input must contain exactly one '=' sign.")
    lhs = parse_latex_expression(side_list[0].strip())
    rhs = parse_latex_expression(side_list[1].strip())
    return Eq(lhs, rhs)




