# Mini Langage - Interpréteur

## Lancement

```bash
cd {path}/THL
py calcBase.py
```

Mode terminal interactif : chaque ligne saisie est un programme complet terminé par `;`.

---

## Fonctionnalités implémentées

### Affectation et print

```
x = 4; x = x + 3; print(x);
```

### Noms de variables multi-caractères

```
Var = 10; autreVar = Var + 5; print(Var);
```

### Affectation élargie et incrément/décrément

```
x = 9; x += 4; x++; print(x);
```

Opérateurs supportés : `++`, `--`, `+=`, `-=`, `*=`, `/=`

### Structures conditionnelles : if / elif / else

```
x = 5; if(x < 3){ print(0); } elif(x < 7){ print(1); } else{ print(2); };
```

### Boucle while

```
x = 4; while(x < 30){ x = x + 3; print(x); };
```

### Boucle for

```
for(i = 0; i < 4; i = i + 1){ print(i * i); };
```

### Boucle do while

```
x = 0; do{ x = x + 1; print(x); }while(x < 3);
```

### Commentaires

```
// commentaire sur une ligne
/* commentaire
   sur plusieurs lignes */
x = 42; print(x);
```

### Fonctions sans valeur de retour (void)

```
function affiche(a, b){ print(a + b); }; affiche(3, 5);
```

### Fonctions avec valeur de retour

```
function add(a, b){ return a + b; }; x = add(3, 5); print(x);
```

### Return coupe-circuit

```
function add(a, b){ return a + b; print(666); }; x = add(3, 5); print(x);
```
`print(666)` ne s'exécute pas.

### Scope des variables (pile de contextes)

Chaque appel de fonction empile un nouveau contexte de variables. Quand la fonction se termine, ce contexte est détruit. Une variable locale ne peut jamais écraser une variable du scope parent.

```
a = 99; function add(a, b){ return a + b; }; x = add(3, 5); print(a);
```
Affiche `99` : le paramètre `a` de la fonction n'écrase pas la variable globale `a`.

État de la pile pendant l'exécution :
- Avant l'appel : `[{a: 99}]`
- Pendant add(3,5) : `[{a: 99}, {a: 3, b: 5}]`
- Après l'appel : `[{a: 99}]`

### Fonctions récursives

```
function fact(n){ if(n == 0){ return 1; }; return n * fact(n - 1); }; print(fact(5));
```
Affiche `120`.
