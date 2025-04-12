Fueron probadas varias estrategias para crear el agente jugador de hex,
que en general se pueden agrupar en estas categorías:
-Elección del algoritmo (MonteCarloTreeSearch,Minimax,BestFirstSearch,A*)
-Optimización de parámetros del algoritmo
-Estrategias para seleccionar movimientos (Movement selection policy, o MSP)
-Función heurística

## Algortimo KBeamSearchV1
El algoritmo elegido KBeamSearchV1 tiene como espacio de búsqueda el conjunto de posibles tableros.

Este mantiene un conjunto de los k mejores estados y mientras tenga tiempo disponible elige el mejor estado para expandir la búsqueda por él. El siguiente estado a expandir se elige basado en una heurística
h1(n) = -h(n), más sobre h(n) despúes, por tanto se considera KBeamSearchV1 un ejemplo de Greedy Best First Search. Al expandir un estado se considera una cantidad fija,establecida cómo parámetro, de estados vecinos a lo sumo, los cuales son influenciados por la pólitica de selección CenterDomination. Esta decisión hace que el algoritmo sea incompleto, sin
embargo permite explorar en mayor profundidad el espacio de búsqueda. Al expandir un estado se añaden sus vecinos
al conjunto de estados, y se descartan estados de forma que solo queden los k mejores, esto focaliza la búsqueda en una
dirección en específico en el espacio de búsqueda y se pierde optimalidad en la solución encontrada pero se gana en profundidad. 

Puntos fuertes de KBeamSearchV1:
-Explora estados en profundidad
-Aunque asimptóticamente otras versiones de KBeamSearch tiene la misma complejidad,
KBeamSearchV1 tiene una constante mucho menor y esto influye a medida que crece el
tamaño del tablero.

Puntos débiles de KBeamSearch:
-Incompleto (puede no encontrar la mejor solución)
-No es óptimo (puede que el camino por el que encuentre un estado no sea de costo mínimo)
-Dificultad para 'rematar' debido a la política CenterDomination. (Rematar es por ejemplo que puedas ganar
jugando en una casilla del borde del tablero)

```
S = estado inicial
k = tamaño de la frontera
m = cantidad máxima de vecinos a expandir
p = función para rankear vecinos
F = frontera
h = heuristica
best = estado de mayor h encontrado

best = S
F = F + {S}
mientras haya tiempo:
    s = x en F tal que h(x) sea máximo
    best = s si h(s) < h(best)
    F = F - {s}
    V = vecinos s
    M = a lo sumo los m estados en V de mayor p
    F = F + M
    F = a lo sumo los k estados de mayor h en F
```

## Heurística h(n)
Sea n un estado (con un tablero de hex asociado)
h(n) es el costo del camino de costo mínimo desde un extremo del tablero al otro (el extremo adecuado según el jugador).
En dicho tablero para el jugador 1, los costos de moverse a las casillas son:
-costo 1 para moverse a una casilla con 0 (desocupada)
-costo 0 para moverse a una casilla con 1 (del mismo jugador)
-costo infinito para moverse a una casilla con 2 (del otro jugador)

La heurística h(n) es admisible, sin embargo gran cantidad de estados suelen compartir
este valor en la práctica, por tanto esta es una limitación de h(n), no es suficientemente descriptiva del estado, es ´muy optimista´.

h(n) es admisible porque en cualquier estado n, no se puede conectar el tablero con menos de h(n) movimientos, 
en particular con menos de 2*n movimientos considerando que se juega de forma alternada.

Si n es un estado y O es un estado objetivo:
    Considerando el costo de n, como f(n) = cantidad de fichas jugadas
    Considerando el costo minimo de llegar de n a O como g(n)
    Se cumple f(n) + h(n) <= g(n)

## Center Domination (Política de selección de movimientos)
La idea de tener una pólitica de selección de movimientos consiste en que no todos los movimientos son igual de buenos y
podemos considerar solo los más prometedores para ahorrarnos exploración y ganar en explotación.

CenterDomination es una política global, porque no considera el estado actual del tablero, y le asigna importancia
a los movimientos (en este caso las casillas) basado en su cercanía al centro (longitud del camino de longitud mínima
de la casilla al centro).

Ventajas de CenterDomination:
    - En las primeras jugadas (suelen ser unas pocas) hace que se domine el centro y se cree una estructura buena.
Desventajas:
    - En medio juego favorece jugadas que no van a disminuir el costo del tablero, haciendo que se creen grupos en
    el centro
    - En juego tardío (alrededor de las 2n jugadas) se ignoran los 'remates' y se atiende a seguir dominando el centro.

El fallo de CenterDomination como política es que asume que jugar en el centro siempre es bueno, pero en el transcurso de
un juego de Hex parece que va perdiendo importancia el centro y la van ganando los extremos.

Para el futuro:
Hacer una política que escale con el paso del tiempo (cantidad de jugadas)
Incluir de algún modo la noción de que al inicio los más importante es el centro y en la fase tardía son los extremos.

## Otras ideas exploradas

## Política de selección de movimiento local
Se dice local porque analiza el estado actual del tablero.

Se creó una 'base de datos' de patrones (279 patrones!!!) y se definieron dos funciones de utilidad sobre ellos.
Estas funciones de utilidad favorecen jugadas del tipo : Pon una ficha donde conectes grupos disjuntos de tus fichas
y bloquees grupos disjuntos de fichas del rival por más de 1 movimiento.
 .B
A.A Poner una A en el punto del centro hará que conectes y bloquees a la vez. Buena jugada.
BB

Al usar esta política en este y otros algoritmos se vieron mejoras significativas en la calidad de las jugadas que exploraban primero. Sin embargo este tipo de análisis es más costoso y como la función de heurística h (usada también en otros algoritmos ) es ´muy optimista´, no fueron capaces de explotar estas jugadas.

## Mejorando la heurística
Para mejorar la heurística se pueden considerar varias opciones:

Con Dijsktra se puede construir un DAG de los caminos de costo mínimo de extremo a extremo.
Si se considera este DAG como un grafo sin dirección en las aristas, se pueden analizar este
grafo en busca de puntos de articulación y extraer conclusiones del tipo: si existe alguno, quiere decir que si el rival
juega en esta casilla el costo del camino de costo mínimo aumentará en 1 al menos.
Aunque esto es costoso.

Se puede aprovechar el análisis local y usar como heurística los valores de las jugadas. Un estado n es una secuencia
de jugadas j1,j2,...,jn. Donde cada jugada par te da puntos y cada jugada impar te quita puntos. Esto puede combinarse
con el algoritmo de minimax y es una mejora significativa pues calcular el costo de una jugada se hace en tiempo constante.

## Optimización de párametros
Usando métodos de simulación es posible calcular estadísticas sobre los agentes y modificar los parámetros para ver el impacto sobre las estadísticas.
