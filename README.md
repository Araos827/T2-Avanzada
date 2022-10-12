# Tarea 02: DCCafé :school_satchel:


## Consideraciones generales :octocat:

<La Tarea esta implementada casi por completo, lo unico que no implemente fueron: que se puedan borrar los objetos del mapa, los atajos de teclas especiales y que se cobre el dinero al comprar cosas. La pausa tampoco esta implementada 100%, el boton comenzar y el pausa hacen lo mismo(comenzar la partida), a ultimo minuto me dejaron de funcionar los QTimers asi que tuve que improvisar y lograr ese comportamiento con QThreads. Bonuses no implementados.>

### Cosas implementadas y no implementadas :white_check_mark: :x:

* <Ventana de Inicio<sub></sub>>: Hecha completa

* <Ventana de Juego<sub>2</sub>>: Me faltó hacer que se descontara la plata del DCCafe cuando se compra algo de la tienda y que se puedan eliminar con un click. Todo lo demas de este item esta implementado.

    * <Ventana de pre-ronda<sub>2.1</sub>>: Implemente correctamente el drag and drop con señales, lo unico que no pasa es que se descuente el dinero del DCCafe
    * <Ventana de pre-ronda<sub>2.3</sub>>: No implementado

* <Entidades<sub></sub>>: Hecha completa

* <Funcionalidades Extra<sub></sub>>: No implementado

* <Tiempo<sub>2</sub>>: la pausa y boton comenzar hacen lo mismo que es cambair el atributo dcc.disponible a True o False, lo que permite comenzar la ronda despues de comprar, pausa no implementada<>

* <Bonus<sub></sub>>: No implementado

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Hay que correro y sha esta

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

Nada nuevo, solo lo visto en clases y lo que aparecia en el enunciado

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```CustomLabels```: Contiene a ```DraggableLabel```, ```DropLabel```, que son los labels personalizados para poder hacer el drag and drop, me base en codigo sacado de stack overflow, de un link que encontre en un issue.

2. ```dccafe```: Hecha para Modelar la entidad del dccafe, ahi esta implentada toda la logica del juego y es la clase que se compone de todas las otras clases que son parte del juego, por desgracia esa pura clase tiene mas de 400 lineas de codigo asi que na po, F.

3. ```main```: Hecha para Instanciar todas las entidades importantes y conectar las señales correspondientes

4. ```parametros```: Hecha para Contener todos los parametros modificables del juego, como tiempos, cantidades iniciales, etc.

5. ```threads```: Contiene a ```PrepararPlato``` y a ```MiuEnzo``` el cual no es un thread pero a ultima hora me di cuenta que dccafe era muy largo para estar ahi asi que lo tuve que intercambiar con el mesero, perdon por ese desorden.

6. ```windows```: Hecha para Modelar las ventanas del frontend y toda la parte grafica


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <Al chocar con un chef en estado de espera de entregar un plato se le pasa la instancia del plato al mesero y se define el atributo plato del chef asignandosele la variable None, esto provoca que instantaneamente el chef vuelva al estado desocupado Y chocando con el mesero, por lo que se gatilla el metodo que lo hace volver a cocinar un plato. Solo con los chefs que quedan piscionados en pixeles multiplos de 10 se logra el efecto de tener que salir del hitbox y entrar denuevo para poder reactivar el metodo PrepararBocadillo/a> 


PD: <Como ultima consideracion quisiera mencionar que por alguna razon que no logré descifrar, aveces los clientes se quedan pegados en su mesa y la mesa queda inhabilitada, intuyo que debe tener que ver con el termino del thread o algo asi. Considerando esto, puede darse el caso de que todas las mesas de la ronda se inhabiliten y el programa deje de avanzar ya que nos pidieron que para que llegue un cliente necesariamente debe haber una mesa desocupada.>


-------


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<https://stackoverflow.com/questions/50232639/d>: este hace \<la logica del drag and drop> y está implementado en el archivo <CustomLabels> en las líneas <6 -> 46>

}#   T 2 - A v a n z a d a  
 