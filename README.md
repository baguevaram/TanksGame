# TanksGame
Proyecto final de introducción a las ciencias de la computación.

Para el juego se utilizó la librería pygame, por lo tanto puede ser necesario instalarla con el comando: 

pip install pygame

o en su defecto intentar con:

pip3 install pygame


## Construcción del juego

El código fuente tiene comentarios detallados de como se construyó el juego.

## Instrucciones

El objetivo del juego es impactar al rival tantas veces como sea posible.

El juego consiste de un sistema por turnos. En cada turno el tanque del
jugador puede moverse cierta cantidad de distancia, también puede ajustar
el ángulo y el poder de disparo y finalmente, disparar. En total son
20 turnos para terminar el juego. El que haya impactado más al rival será
el ganador.

En cada juego, el terreno será generado aleatoriamente. 
Si no se impacta al rival, el terreno se irá deformando debido al impacto.


## Controles

- A: Mover el tanque a la izquierda
- D: Mover el tanque a la derecha
- Q: Aumentar el ángulo de disparo
- E: Disminuir el ángulo de disparo
- W: Aumentar el poder de disparo
- S: Disminuir el poder de disparo
- J: Disparar