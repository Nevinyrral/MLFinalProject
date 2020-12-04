# MLFinalProject - Ricardo Montaño

## Instalación

#### Instalar Conda

Instalar Anaconda para tener acceso al manejador de paquetes Conda

#### Puesta en marcha

Descargar proyecto
```
git clone https://github.com/Nevinyrral/MLFinalProject.git
cd MLFinalProject
```

Creación de entorno Conda e instalación de dependencias
```
conda create --name <env> --file conda_specs
```

Inicialización de servidor
```
FLASK_APP=main.py flask run 
```

## Uso

Este proyecto expone un REST API en la interfaz http://localhost:5000 de tipo
post llamado /simulate

#### POST /simulate

Cuerpo de la petición (En test.json se encuentra este ejemplo):

´´´
{
    "player": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [10, 0, 0, 0, 0, 0, 0, 0, 0],
        [6, 9, 0, 0, 0, 0, 0, 0, 0],
        [3, 5, 8, 0, 0, 0, 0, 0, 0],
        [1, 2, 4, 7, 0, 0, 0, 0, 0]
    ],
    "opponent": [
        [0, 0, 0, 0, 0, 7, 4, 2, 1],
        [0, 0, 0, 0, 0, 0, 8, 5, 3],
        [0, 0, 0, 0, 0, 0, 0, 9, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 10],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "iterations": 100000
}
´´´

Estructura:

player: el estado del juego del jugador que inicia jugando, las fichas están
numeradas de 1 al 10

player: el estado del juego del jugador que juega de segundo, las fichas están
numeradas de 1 al 10

iterations: número de iteraciones para el árbol de búsqueda Monte Carlo


Respuesta (En response_example.json se encuentra este ejemplo):

´´´
{
    "flow": [
        {
            "actions": [ [ 6, 2 ] ],
            "opponent_turn": true,
            "state": [
                [ 0, 0, 0, 0, 0, 2, 2, 2, 2 ],
                [ 0, 0, 0, 0, 0, 0, 2, 2, 2 ],
                [ 0, 0, 0, 0, 0, 0, 0, 2, 2 ],
                [ 0, 0, 0, 0, 0, 0, 0, 0, 2 ],
                [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                [ 1, 0, 0, 0, 0, 0, 0, 0, 0 ],
                [ 1, 1, 1, 0, 0, 0, 0, 0, 0 ],
                [ 1, 1, 1, 0, 0, 0, 0, 0, 0 ],
                [ 1, 1, 0, 1, 0, 0, 0, 0, 0 ]
            ],
            "times_visited": 9825
        }
    ],
    "next_move": [ [ 6, 2 ] ]
}
´´´

flow: contiene el flujo de la simulación con mejor puntaje
- actions: los movimientos necesarios para llegar al estado
- opponent_turn: al terminar este estado, será es turno del jugador oponente
- state: representación matricial
- times_visited: número de veces que el algoritmo visitó el nodo correspondiente 
la estado
next_move: siguente movimiento recomendado por el algoritmo

