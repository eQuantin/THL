# ============================================================
#  MINI EXEMPLE : pile de contextes (scope des variables)
# ============================================================

# La "pile" : une liste de dictionnaires
# Chaque dictionnaire = un contexte (global, ou une fonction)
stack = [{}]   # on commence avec UN contexte vide (le global)


# --- Les 3 opérations fondamentales ---

def lire_variable(nom):
    """Cherche une variable en partant du haut de la pile."""
    # reversed() permet de parcourir de la fin (haut) vers le début (bas)
    for contexte in reversed(stack):
        if nom in contexte:
            return contexte[nom]
    raise NameError(f"Variable '{nom}' inconnue")

def ecrire_variable(nom, valeur):
    """Ecrit une variable dans le contexte du dessus (le plus récent)."""
    stack[-1][nom] = valeur

def entrer_dans_fonction(parametres: dict):
    """Empile un nouveau contexte avec les paramètres de la fonction."""
    stack.append(parametres)

def sortir_de_fonction():
    """Dépile le contexte de la fonction (on l'oublie)."""
    stack.pop()


# ============================================================
#  TEST : simuler  b=0 ; add(5,3) ; print(b)
# ============================================================

print("=== Etat initial ===")
ecrire_variable("b", 0)
print("stack :", stack)          # [{"b": 0}]

print("\n=== On entre dans add(x=5, y=3) ===")
entrer_dans_fonction({"x": 5, "y": 3})
print("stack :", stack)          # [{"b": 0}, {"x": 5, "y": 3}]

print("\n=== Dans add : result = x + y ===")
x = lire_variable("x")          # cherche dans le haut -> trouve dans {"x":5,"y":3}
y = lire_variable("y")
ecrire_variable("result", x + y)
print("stack :", stack)          # [{"b": 0}, {"x": 5, "y": 3, "result": 8}]

print("\n=== Dans add : est-ce qu'on voit b du contexte global ? ===")
print("b =", lire_variable("b")) # cherche haut -> pas là, descend -> trouve dans global

print("\n=== Dans add : b = 999 (essai d'écraser b global) ===")
ecrire_variable("b", 999)        # écrit dans le contexte DU DESSUS, pas en global
print("stack :", stack)          # b global est intact !

print("\n=== On sort de add ===")
sortir_de_fonction()             # on jette le contexte de add
print("stack :", stack)          # [{"b": 0}]  ← b est resté 0 !

print("\n=== print(b) après add ===")
print("b =", lire_variable("b")) # 0, pas 999
