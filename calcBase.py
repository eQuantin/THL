# -*- coding: utf-8 -*-

reserved = {
    "if": "IF",
    "else": "ELSE",
    "elif": "ELIF",
    "while": "WHILE",
    # "do": "DO",
    # "for": "FOR",
    "function": "FUNCTION",
    "print": "PRINT",
}

tokens = [
    "NUMBER",
    "VAR",
    "MINUS",
    "PLUS",
    "TIMES",
    "DIVIDE",
    "LPAREN",
    "RPAREN",
    # "LSBRACKET",
    # "RSBRACKET",
    "LCBRACKET",
    "RCBRACKET",
    "OR",
    "AND",
    "SEMI",
    "COMMA",
    "EGAL",
    "INF",
    "SUP",
    "EGALEGAL",
    "INFEGAL",
    "SUPEGAL",
    "INCR",
    "DECR",
    "PLUSEGAL",
    "MINUSEGAL",
    "TIMESEGAL",
    "DIVEGAL",
] + list(reserved.values())

precedence = (
    ("right", "INCR", "DECR"),
    ("left", "OR"),
    ("left", "AND"),
    (
        "nonassoc",
        "INF",
        "INFEGAL",
        "EGAL",
        "EGALEGAL",
        "SUP",
        "SUPEGAL",
        "PLUSEGAL",
        "MINUSEGAL",
        "TIMESEGAL",
        "DIVEGAL",
    ),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    # ("left", "IMPLICIT_MULT"),
)

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"

t_LPAREN = r"\("
t_RPAREN = r"\)"
# t_LSBRACKET = r"\["
# t_RSBRACKET = r"\]"
t_LCBRACKET = r"\{"
t_RCBRACKET = r"\}"
t_SEMI = r"\;"
t_COMMA = r"\,"
# t_DQUOTE = r"\""

t_OR = r"\|\|"
t_AND = r"\&\&"

t_EGAL = r"\="

t_INF = r"\<"
t_SUP = r"\>"
t_INFEGAL = r"\<\="
t_SUPEGAL = r"\>\="
t_EGALEGAL = r"\=\="

t_INCR = r"\+\+"
t_DECR = r"\-\-"
t_PLUSEGAL = r"\+\="
t_MINUSEGAL = r"\-\="
t_TIMESEGAL = r"\*\="
t_DIVEGAL = r"\/\="


def t_VAR(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "VAR")  # Check for reserved words
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex

lex.lex()

names = {}
functions = {}


def evalExpr(t):
    if type(t) is int:
        return t
    if type(t) is str:
        if t in names:
            return names[t]
        else:
            print(f"Erreur: variable '{t}' non définie")
            return 0
    if type(t) is tuple:
        if t[0] == "call":
            func_name = t[1]
            args = t[2] if len(t) > 2 else []

            if func_name not in functions:
                print(f"Erreur: fonction '{func_name}' non définie")
                return 0

            func = functions[func_name]
            params = func[1]
            body = func[2]
            arg_values = [evalExpr(arg) for arg in args]

            for i in range(len(params)):
                names[params[i]] = arg_values[i]

            evalInst(body)
            return 0
        if t[0] == "+":
            return evalExpr(t[1]) + evalExpr(t[2])
        if t[0] == "-":
            return evalExpr(t[1]) - evalExpr(t[2])
        if t[0] == "*":
            return evalExpr(t[1]) * evalExpr(t[2])
        if t[0] == "/":
            return evalExpr(t[1]) / evalExpr(t[2])
        if t[0] == "<":
            return evalExpr(t[1]) < evalExpr(t[2])
        if t[0] == "<=":
            return evalExpr(t[1]) <= evalExpr(t[2])
        if t[0] == ">":
            return evalExpr(t[1]) > evalExpr(t[2])
        if t[0] == ">=":
            return evalExpr(t[1]) >= evalExpr(t[2])
        if t[0] == "==":
            return evalExpr(t[1]) == evalExpr(t[2])
        if t[0] == "&&":
            return evalExpr(t[1]) and evalExpr(t[2])
        if t[0] == "||":
            return evalExpr(t[1]) or evalExpr(t[2])
        if t[0] == "post_incr":
            var = t[1]
            if var in names:
                old_value = names[var]
                names[var] += 1
                return old_value
            else:
                print(f"Erreur: variable '{var}' non définie")
                return 0
        if t[0] == "post_decr":
            var = t[1]
            if var in names:
                old_value = names[var]
                names[var] -= 1
                return old_value
            else:
                print(f"Erreur: variable '{var}' non définie")
                return 0
        if t[0] == "pre_incr":
            var = t[1]
            if var in names:
                names[var] += 1
                return names[var]
            else:
                print(f"Erreur: variable '{var}' non définie")
                return 0
        if t[0] == "pre_decr":
            var = t[1]
            if var in names:
                names[var] -= 1
                return names[var]
            else:
                print(f"Erreur: variable '{var}' non définie")
                return 0
        if t[0] == "pre_add":
            var = t[1]
            if var in names:
                names[var] += evalExpr(t[2])
                return names[var]
            else:
                print(f"Erreur: variable '{var}' non définie")
                return 0
        if t[0] == "pre_sub":
            var = t[1]
            if var in names:
                names[var] -= evalExpr(t[2])
                return names[var]
            else:
                print(f"Erreur: variable '{var}' non définie")
                return 0
        if t[0] == "pre_mul":
            var = t[1]
            if var in names:
                names[var] *= evalExpr(t[2])
                return names[var]
            else:
                print(f"Erreur: variable '{var}' non définie")
                return 0

        if t[0] == "pre_div":
            var = t[1]
            if var in names:
                names[var] /= evalExpr(t[2])
                return names[var]
            else:
                print(f"Erreur: variable '{var}' non définie")
                return 0

    return 0


def evalInst(t):
    if type(t) is tuple:
        if t[0] == "func_def":
            func_name = t[1]
            params = t[2]
            body = t[3]
            functions[func_name] = ("function", params, body)
        elif t[0] == "call_stmt":
            # Function call as a statement
            evalExpr(t[1])
        elif t[0] == "print":
            valeur = evalExpr(t[1])
            print(f"{valeur}")
        elif t[0] == "assign":
            variable = t[1]
            valeur = evalExpr(t[2])
            names[variable] = valeur
        elif t[0] == "expr":
            valeur = evalExpr(t[1])
            # print(f"{valeur}")
        elif t[0] == "bloc":
            evalInst(t[1])
            evalInst(t[2])
        elif t[0] == "if":
            condition = evalExpr(t[1])
            if_body = t[2]
            elif_list = t[3] if len(t) > 3 else []
            else_body = t[4] if len(t) > 4 else None

            if condition:
                evalInst(if_body)
            else:
                executed = False
                for elif_item in elif_list:
                    elif_cond = evalExpr(elif_item[1])
                    elif_body = elif_item[2]
                    if elif_cond:
                        evalInst(elif_body)
                        executed = True
                        break

                if not executed and else_body is not None:
                    evalInst(else_body[1])
        elif t[0] == "while":
            condition = t[1]
            body = t[2]
            while evalExpr(condition):
                evalInst(body)

    elif t == "empty":
        pass


def p_start(p):
    "start : bloc"
    p[0] = p[1]


def p_bloc(p):
    """bloc : bloc statement SEMI
    |         statement SEMI"""
    p[0] = ("bloc", p[1], p[2])


def p_statement_expr(p):
    """statement : PRINT LPAREN expression RPAREN"""
    p[0] = ("print", p[3])


def p_statement_plain_expr(p):
    """statement : expression"""
    p[0] = ("expr", p[1])


def p_statement_func_def(p):
    """statement : FUNCTION VAR LPAREN param_list RPAREN LCBRACKET bloc RCBRACKET
    |              FUNCTION VAR LPAREN RPAREN LCBRACKET bloc RCBRACKET"""
    func_name = p[2]
    if len(p) == 9:
        params = p[4]
        body = p[7]
    else:
        params = []
        body = p[6]
    p[0] = ("func_def", func_name, params, body)


def p_statement_func_call(p):
    """statement : VAR LPAREN arg_list RPAREN
    |              VAR LPAREN RPAREN"""
    func_name = p[1]
    if len(p) == 5:
        args = p[3]
    else:
        args = []
    p[0] = ("call_stmt", ("call", func_name, args))


def p_statement_assign(p):
    "statement : VAR EGAL expression"
    p[0] = ("assign", p[1], p[3])


def p_statement_if(p):
    """statement : if elif_chain else
    |                 if elif_chain
    |                 if else
    |                 if
    """
    if_cond = p[1][1]
    if_body = p[1][2]

    match len(p):
        case 4:
            p[0] = ("if", if_cond, if_body, p[2], p[3])
        case 3:
            if isinstance(p[2], list):  # recursive elif_chain
                p[0] = ("if", if_cond, if_body, p[2], None)
            else:
                p[0] = ("if", if_cond, if_body, [], p[2])
        case _:
            p[0] = ("if", if_cond, if_body, [], None)


def p_statement_while(p):
    """statement : WHILE LPAREN expression RPAREN LCBRACKET bloc RCBRACKET"""
    p[0] = ("while", p[3], p[6])


def p_param_list(p):
    """param_list : param_list COMMA VAR
    |               VAR"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_arg_list(p):
    """arg_list : arg_list COMMA expression
    |             expression"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_elif_chain(p):
    """elif_chain : elif_chain elif
    |               elif"""
    if len(p) == 3:
        if isinstance(p[1], list):  # recursive elif_chain
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1]]


def p_conditional_if(p):
    """if : IF LPAREN expression RPAREN LCBRACKET bloc RCBRACKET"""
    p[0] = ("if_part", p[3], p[6])


def p_conditional_elif(p):
    """elif : ELIF LPAREN expression RPAREN LCBRACKET bloc RCBRACKET"""
    p[0] = ("elif", p[3], p[6])


def p_conditional_else(p):
    """else : ELSE LCBRACKET bloc RCBRACKET"""
    p[0] = ("else", p[3])


def p_expression_binop(p):
    """expression : expression AND expression
    |               expression OR expression
    |               expression PLUS expression
    |               expression MINUS expression
    |               expression TIMES expression
    |               expression DIVIDE expression
    """
    match p[2]:
        case "&&":
            p[0] = ("&&", p[1], p[3])
        case "||":
            p[0] = ("||", p[1], p[3])
        case "+":
            p[0] = ("+", p[1], p[3])
        case "-":
            p[0] = ("-", p[1], p[3])
        case "*":
            p[0] = ("*", p[1], p[3])
        case "/":
            p[0] = ("/", p[1], p[3])
        case _:
            pass


# def p_expression_implicit_mult_prec_paren(p):
#     """expression : NUMBER LPAREN expression RPAREN %prec IMPLICIT_MULT
#     |               VAR LPAREN expression RPAREN %prec IMPLICIT_MULT
#     """
#     p[0] = ("*", p[1], p[3])


# def p_expression_implicit_mult_post_paren(p):
#     """expression : LPAREN expression RPAREN NUMBER %prec IMPLICIT_MULT
#     |               LPAREN expression RPAREN VAR %prec IMPLICIT_MULT
#     """
#     p[0] = ("*", p[2], p[4])


# def p_expression_implicit_mult_multi_paren(p):
#     """expression : LPAREN expression RPAREN LPAREN expression RPAREN %prec IMPLICIT_MULT"""
#     p[0] = ("*", p[2], p[5])


def p_expression_binop_comp(p):
    """expression : expression SUP expression
    |               expression INF expression
    |               expression SUPEGAL expression
    |               expression INFEGAL expression
    |               expression EGALEGAL expression"""
    match p[2]:
        case ">":
            p[0] = (">", p[1], p[3])
        case "<":
            p[0] = ("<", p[1], p[3])
        case ">=":
            p[0] = (">=", p[1], p[3])
        case "<=":
            p[0] = ("<=", p[1], p[3])
        case "==":
            p[0] = ("==", p[1], p[3])
        case _:
            pass


def p_expression_binop_assign(p):
    """expression : VAR PLUSEGAL expression
    |               VAR MINUSEGAL expression
    |               VAR TIMESEGAL expression
    |               VAR DIVEGAL expression
    """
    match p[2]:
        case "+=":
            p[0] = ("pre_add", p[1], p[3])
        case "-=":
            p[0] = ("pre_sub", p[1], p[3])
        case "*=":
            p[0] = ("pre_mul", p[1], p[3])
        case "/=":
            p[0] = ("pre_div", p[1], p[3])
        case _:
            pass


def p_expression_incr(p):
    """expression : INCR expression
    |               DECR expression
    |               expression INCR
    |               expression DECR
    """
    if p[2] == "++":
        p[0] = ("post_incr", p[1])
    elif p[2] == "--":
        p[0] = ("post_decr", p[1])
    elif p[1] == "++":
        p[0] = ("pre_incr", p[2])
    elif p[1] == "--":
        p[0] = ("pre_decr", p[2])


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_var(p):
    "expression : VAR"
    p[0] = p[1]


def p_error(p):
    print("Syntax error in input!")


import sys

import ply.yacc as yacc

yacc.yacc()

if __name__ == "__main__":
    if len(sys.argv) > 1:  # mode file
        filename = sys.argv[1]
        try:
            with open(filename, "r") as f:
                content = f.read()
                result = yacc.parse(content)
                if result:
                    evalInst(result)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except Exception as e:
            print(f"Error reading file: {e}")
    else:  # mode terminal
        while True:
            try:
                prompt = ">> "
                s = input(prompt)
                result = yacc.parse(s)
                if result:
                    evalInst(result)
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            except SyntaxError:
                pass
