# iv109_project

## Autorky:
Viktória Vozárová, 433334 
Katarína Kjestová, 433820

##Téma : Robot – sběr pokladu
Variace na příklad zmíněný na přednášce. Robot se pohybuje v
čtvercové mřížce, na některých polích jsou poklady, které má posbírat, případně zdi, díry,
a pod. Vytvořte genetický algoritmus, který bude vytvářet navigační kód pro robota (tak aby
posbíral co nejvíce pokladu).

##Genetické algoritmy
sú heuristické postupy, aplikujúce princípy z evolučnej biológie. Používame ich na riešenie zložitých problémov. Cieľom býva nájsť stav splňujúci počiatočné podmienky.


##Aplikácia
Pri aplikovaní genetického algoritmu sme použili obecné schéma : 
1. Inicializace
2. Výber jedincov z populácie
3. Kríženie, Mutácia, Reprodukcia
4. Ohodnotenie nových jedincov

1.Inicializácia


2. Výber jedincov z populácie - selekcia.
K selekcii sme využili princíp **váženej rulety**, ktorá dostáva percentuálne taký podiel, a tým pádom možnosť byť vybratý ku kríženiu, ako dobré ohodonotenie dostal.

3. Kríženie, Mutácia
Kríženie je založené na genetickom princípe kríženia, a teda kombinovaní genetického kódu rodičov. Nech máme otca **O** a matku **M**. Rozhodneme sa, že rozdelenie nastane na **i**-tej pozícii. Potom potomci **P,Q** sú určení: **P** = O[0..i].M[i+1..n], **Q** = M[0..i].O[i+1..m]
Mutácia nastáva po krížei. Každý nový jedinec sa s určitou **malou** pravdepodobnosťou zmutuje



Výstupom je najzdatnejší jedinec, v našom prípade postupnosť krokov pre robota.



Uvažujme cestu robota ako funckiu. Robota vž
