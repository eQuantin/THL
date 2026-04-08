# Mini Langage - Interpréteur

## Lancement

```bash
cd {path}/THL
py calcBase.py
```

Mode terminal interactif : chaque ligne saisie est un programme complet terminé par `;`.

## Fonctionnalités implémentées

### Affectation et print

#### variable
```
mut variable = 4; variable = variable + 3; print(variable);
```

#### constante
```
const constante = 3; print(constante);
```

#### reaffectation d'une constante
```
const constante1 = 3; constante1 = 4;
```
```
Erreur: impossible de réassigner la constante 'constante1'
```

---

### Affectation et incrément/décrément

```
mut x = 9; x += 4; x++; print(x);
```

### Noms de variables multi-caractères

```
mut myVar = 10; mut otherVar = myVar + 5; print(otherVar);
```

### Structures conditionnelles : if / elif / else

```
mut y = 5; if(y < 3){ print(3); } elif(y < 5){ print(5); } elif(y < 7){ print(7); } else{ print(0); };
```

### Boucle while

```
mut z = 4; while(z < 30){ print(z); z = z + 3; };
```

### Boucle for

```
for(mut i = 0; i < 4; i = i + 1){ print(i * i); };
```

### Boucle do while

```
mut j = 0; do{ j = j + 1; print(j); }while(j < 3);
```

### Commentaires

```
// commentaire sur une ligne
mut u = 42; print(u);
```

Les commentaires multilignes ne fonctionnent pas en mode terminal interactif, puisqu'on ne lit qu'une ligne à la fois
```
/* commentaire
   sur plusieurs lignes */
mut s = 21; print(s);
```

### Fonctions sans valeur de retour (void)

```
function affiche(a, b){ print(a + b); }; affiche(3, 5);
```

### Fonctions avec valeur de retour

```
function add(c, d){ return c + d; }; mut k = add(3, 5); print(k);
```

### Return coupe-circuit

```
function add(e, f){ return e + f; print(666); }; mut l = add(3, 5); print(l);
```

### Scope des variables (pile de contextes)

```
mut g = 99; function add(g, h){ return g + h; }; mut k = add(3, 5); print(g);
```

### Fonctions récursives

```
function fact(n){ if(n == 0){ return 1; }; return n * fact(n - 1); }; print(fact(5));
```
