# -*- coding: utf-8 -*-


class THLRuntimeError(Exception):
    pass


reserved = {
    "if": "IF",
    "else": "ELSE",
    "elif": "ELIF",
    "while": "WHILE",
    "do": "DO",
    "for": "FOR",
    "function": "FUNCTION",
    "print": "PRINT",
    "return": "RETURN",
    "mut": "MUT",
    "const": "CONST",
    "True": "TRUE",
    "False": "FALSE",
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
    "STRING",
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
    ("right", "UMINUS"),
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

t_TRUE = r"True"
t_FALSE = r"False"

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


def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t


t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_comment(t):
    r"(\/\/[^\n]*)|(\/\*[\s\S]*?\*\/)"
    t.lexer.lineno += t.value.count("\n")


import ply.lex as lex

lex.lex()

stack = [{}]  # pile de contextes : stack[0] = global, stack[-1] = contexte courant
functions = {}

_returning = False  # True quand on a rencontré un return
_return_value = 0  # valeur du return en cours


def lire_variable(nom) -> int | bool | str:
    for contexte in reversed(stack):
        if nom in contexte:
            v = contexte[nom]
            return v[1] if isinstance(v, tuple) and v[0] == "__const__" else v
    raise THLRuntimeError(f"variable '{nom}' non définie")


def ecrire_variable(nom, valeur):
    for contexte in reversed(stack):
        if nom in contexte:
            if isinstance(contexte[nom], tuple) and contexte[nom][0] == "__const__":
                raise THLRuntimeError(f"impossible de réassigner la constante '{nom}'")
            contexte[nom] = valeur
            return
    raise THLRuntimeError(f"variable '{nom}' non déclarée")


def entrer_dans_fonction(parametres: dict):
    stack.append(parametres)


def sortir_de_fonction():
    stack.pop()


def evalExpr(t):
    if type(t) is bool:
        return t
    if type(t) is int:
        return t
    if type(t) is str:
        return lire_variable(t)
    if type(t) is tuple:
        if t[0] == "call":
            func_name = t[1]
            args = t[2] if len(t) > 2 else []

            if func_name not in functions:
                raise THLRuntimeError(f"Erreur: fonction '{func_name}' non définie")

            func = functions[func_name]
            params = func[1]
            body = func[2]
            arg_values = [evalExpr(arg) for arg in args]

            global _returning, _return_value
            entrer_dans_fonction({params[i]: arg_values[i] for i in range(len(params))})
            evalInst(body)
            result = _return_value
            _returning = False
            _return_value = 0
            sortir_de_fonction()
            return result
        if t[0] == "str_lit":
            return t[1]
        if t[0] == "neg":
            return -evalExpr(t[1])
        if t[0] == "+":
            return evalExpr(t[1]) + evalExpr(t[2])
        if t[0] == "-":
            return evalExpr(t[1]) - evalExpr(t[2])
        if t[0] == "*":
            return evalExpr(t[1]) * evalExpr(t[2])
        if t[0] == "/":
            divisor = evalExpr(t[2])
            if divisor == 0:
                raise THLRuntimeError("Erreur: division par 0")
            return evalExpr(t[1]) / divisor
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
            return True if evalExpr(t[1]) and evalExpr(t[2]) else False
        if t[0] == "||":
            return True if evalExpr(t[1]) or evalExpr(t[2]) else False
        if t[0] == "post_incr":
            old_value = lire_variable(t[1])
            ecrire_variable(t[1], old_value + 1)
            return old_value
        if t[0] == "post_decr":
            old_value = lire_variable(t[1])
            ecrire_variable(t[1], old_value - 1)
            return old_value
        if t[0] == "pre_incr":
            new_value = lire_variable(t[1]) + 1
            ecrire_variable(t[1], new_value)
            return new_value
        if t[0] == "pre_decr":
            new_value = lire_variable(t[1]) - 1
            ecrire_variable(t[1], new_value)
            return new_value
        if t[0] == "pre_add":
            new_value = lire_variable(t[1]) + evalExpr(t[2])
            ecrire_variable(t[1], new_value)
            return new_value
        if t[0] == "pre_sub":
            new_value = lire_variable(t[1]) - evalExpr(t[2])
            ecrire_variable(t[1], new_value)
            return new_value
        if t[0] == "pre_mul":
            new_value = lire_variable(t[1]) * evalExpr(t[2])
            ecrire_variable(t[1], new_value)
            return new_value
        if t[0] == "pre_div":
            divisor = evalExpr(t[2])
            if divisor == 0:
                raise THLRuntimeError("Erreur: division par 0")
            new_value = lire_variable(t[1]) / divisor
            ecrire_variable(t[1], new_value)
            return new_value

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
        elif t[0] == "declare":
            nom, valeur = t[2], evalExpr(t[3])
            if nom in stack[-1]:
                raise THLRuntimeError(f"variable '{nom}' déjà déclarée dans ce scope")
            if t[1] == "const":
                stack[-1][nom] = ("__const__", valeur)
            else:
                stack[-1][nom] = valeur
        elif t[0] == "assign":
            ecrire_variable(t[1], evalExpr(t[2]))
        elif t[0] == "return":
            global _returning, _return_value
            _return_value = evalExpr(t[1]) if len(t) > 1 else 0
            _returning = True
        elif t[0] == "expr":
            valeur = evalExpr(t[1])
            # print(f"{valeur}")
        elif t[0] == "bloc":
            evalInst(t[1])
            if not _returning:
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
                if _returning:
                    break
        elif t[0] == "for":
            evalInst(t[1])
            condition = t[2]
            expr = t[3]
            body = t[4]
            while evalExpr(condition):
                evalInst(body)
                if _returning:
                    break
                evalExpr(expr)
        elif t[0] == "do_while":
            condition = t[2]
            body = t[1]
            evalInst(body)
            while not _returning and evalExpr(condition):
                evalInst(body)
    elif t == "empty":
        pass


def p_start(p):
    "start : bloc"
    p[0] = p[1]
    print(p[0])
    evalInst(p[0])


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


def p_statement_return(p):
    """statement : RETURN expression
    |              RETURN"""
    if len(p) == 3:
        p[0] = ("return", p[2])
    else:
        p[0] = ("return",)


def p_statement_declare(p):
    """statement : declare"""
    p[0] = p[1]


def p_declare(p):
    """declare : MUT VAR EGAL expression
    |            CONST VAR EGAL expression"""
    p[0] = ("declare", p[1], p[2], p[4])


def p_statement_assign(p):
    "statement : assign"
    p[0] = p[1]


def p_assign(p):
    "assign : VAR EGAL expression"
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


def p_statement_for(p):
    """statement : FOR LPAREN assign SEMI expression SEMI expression RPAREN LCBRACKET bloc RCBRACKET
    |              FOR LPAREN declare SEMI expression SEMI expression RPAREN LCBRACKET bloc RCBRACKET"""
    p[0] = ("for", p[3], p[5], p[7], p[10])


def p_statement_do_while(p):
    """statement : DO LCBRACKET bloc RCBRACKET WHILE LPAREN expression RPAREN"""
    p[0] = ("do_while", p[3], p[7])


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
    p[0] = ("if", p[3], p[6])


def p_conditional_elif(p):
    """elif : ELIF LPAREN expression RPAREN LCBRACKET bloc RCBRACKET"""
    p[0] = ("elif", p[3], p[6])


def p_conditional_else(p):
    """else : ELSE LCBRACKET bloc RCBRACKET"""
    p[0] = ("else", p[3])


def p_expression_string(p):
    """expression : STRING"""
    p[0] = ("str_lit", p[1])


def p_expression_uminus(p):
    """expression : MINUS expression %prec UMINUS"""
    p[0] = ("neg", p[2])


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
    """expression : VAR INCR
    |               VAR DECR
    |               INCR VAR
    |               DECR VAR
    """
    if p[2] == "++":
        p[0] = ("post_incr", p[1])
    elif p[2] == "--":
        p[0] = ("post_decr", p[1])
    elif p[1] == "++":
        p[0] = ("pre_incr", p[2])
    elif p[1] == "--":
        p[0] = ("pre_decr", p[2])


def p_expression_func_call(p):
    """expression : VAR LPAREN arg_list RPAREN
    |               VAR LPAREN RPAREN"""
    func_name = p[1]
    args = p[3] if len(p) == 5 else []
    p[0] = ("call", func_name, args)


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_bool(p):
    """expression : TRUE
    |              FALSE"""
    if p[1] == "True":
        p[0] = True
    if p[1] == "False":
        p[0] = False


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_var(p):
    "expression : VAR"
    p[0] = p[1]


def p_error(p):
    if p:
        raise THLRuntimeError(
            f"erreur de syntaxe ligne {p.lineno}: token inattendu '{p.value}'"
        )
    else:
        raise THLRuntimeError("erreur de syntaxe: fin de fichier inattendue")


import ply.yacc as yacc

yacc.yacc()

if __name__ == "__main__":
    while True:
        try:
            prompt = "calc > "
            s = input(prompt)
            yacc.parse(s)
        except THLRuntimeError as e:
            print(f"Erreur: {e}")
        except EOFError:
            break
        except KeyboardInterrupt:
            break
        except SyntaxError:
            pass
