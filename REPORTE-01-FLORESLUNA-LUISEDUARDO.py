"""Tenemos que hacer un log in, por lo tanto, hay que solicitar información al usuario, claramente mediante la función input. Pero hay que indicarle al usuario que es lo que necesitamos
"""
"""Tenemos que tener una base de datos con los nombre de los diferentes usuarios y sus respectivas contraseñas, pero con relaciones uno a uno. Un diccionario son la opción"""

Credenciales={'Carlos':'carl02', 'Jimmy':'EmTech', 'Monse':'HIMYM'}
#Ahora, podemos usar un ciclo while para repetir la solicitud de usuario y contraseña de forma indeterminada, o hasta que se alcance un número determinado de intentos.
Acceso=False
Intentos=0

while not Acceso:  
  Intentos+=1
  print("Favor de introducir el nombre de usuario")
  nombre_de_usuario=input("Nombre de usuario:")
  if nombre_de_usuario in Credenciales.keys():
    print("Favor de introducir la contraseña:")
    contraseña=input("Contraseña:")
    if contraseña == Credenciales[nombre_de_usuario]:
      Acceso=True
    else:
      print("Contraseña incorrecta, pruebe de nuevo")
      print(f"Lleva {Intentos} intentos, el límite es de 3")
  else: 
    print("Usuario no encontrado, pruebe de nuevo")
    print(f"Lleva {Intentos} intentos, el límite es de 3")
  #Si se superan los 3 intentos, se cierra el programa
  if Intentos > 3:
    exit()
print(f'Bienvenido {nombre_de_usuario}')


"""Primero importamos la base de datos que vamos a analizar, como se encuentra en un archivo .py podemos importarlo de la siguiente forma. """

from lifestore_file import lifestore_searches, lifestore_sales,lifestore_products


# encoding: utf-8

"""lifestore_searches = [id_search, id product]

lifestore_sales = [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]

lifestore_products = [id_product, name, price, category, stock]"""
"""Lo primero que vamos a hacer es calcular los productos con mayores ventas, es decir, aquellos productos que no fueron devueltos, es decir, donde refund=0. Para cada id_product podemos buscar la cantidad de veces que aparece en lifestore_sales."""

#Sabemos que los id_product comienzan desde 1 y terminan en el número de listas dentro de lifestore_products, pero range se trunca un número antes del límite superior, por lo que hay que sumar un 1 para abarcar todas las listas.

#Generamos una lista para almacenar las diferentes valores de la id_product, el nombre del producto y el número de ventas asociadas. 
Ventas_por_id_product= []

for producto in lifestore_products:
  #Cada id_producto se tiene que comparar con las id_product de las transacciones de lifestore_sales para asegurarse que corresponden al mismo producto, y también debemos de asegurarnos que no hubo devolución.

  #Inicializamos una variable asociada a cada id_producto para guardar el número de ventas que tiene asociadas. En cada iteración se inicializa de Numero_ventas.
  id_producto=producto[0]
  Numero_ventas=0
  Nombre_producto=producto[1]
  #Iteramos sobre las diferentes ventas.
  for venta in lifestore_sales:
    #La id_producto de la lista venta está en la posición 1 de la lista asociada a la venta, y la devolución está en la posición 4 de la lista.
    if id_producto == venta[1] and venta[4] == 0:
      #Si se cumplen ambas condiciones, entonces hay una venta más
      Numero_ventas += 1
  
  #Luego de saber el número de ventas hay que almacenar ambos valores. 
  Ventas_por_id_product.append([id_producto, Numero_ventas,Nombre_producto])
#Visualizamos la id_producto  y su número de ventas.
#print(Ventas_por_id_product)

#Podemos utilizar la función sorted() para ordenar una lista, en este caso, esta lista anidada, o lista de listas. Esta función sorted() tiene un parámetro llamado key= que permite elegir una función que nos retorne un valor que vamos a usar para la clasificación; en este caso vamos a usar lambda (una función que no necesita especificarse como las otras que normalmente manejamos) para obtener el segundo valor de la lista, es decir, el número de ventas como valor a usar para la clasificación.

#Podemos especificar que sea el orden descendente con el parámetro reverse, es decir, de mayores ventas a menores ventas.


Ventas_por_id_product_ordenadas= sorted(Ventas_por_id_product, key= lambda x: x[1], reverse=True)

#Visualizamos
#print(Ventas_por_id_product_ordenadas)

"""Ahora, únicamente hay que devolver los id_products de las 5 primeras listas de la lista Ventas_por_id_product_ordenadas"""
ID_más_vendidos=[]
for posicion in range(0,5):
  id_producto=Ventas_por_id_product_ordenadas[posicion][2]
  ID_más_vendidos.append(id_producto)

print(ID_más_vendidos)

#Podemos aplicar un procedimiento similar para encontrar a aquellos productos con mayores búsquedas, sólamente hay que ver cuántas veces aparece el id_product en las listas de la lista products_searches.
Busquedas=[]

for producto in lifestore_products:
  Número_de_busquedas=0
  id_producto=producto[0]
  nombre=producto[1]
  for busqueda in lifestore_searches:
    if id_producto==busqueda[1]:
      Número_de_busquedas+=1
  Busquedas.append([id_producto,Número_de_busquedas,nombre])

Busquedas_ordenadas= sorted(Busquedas, key= lambda x: x[1], reverse=True)

productos_más_buscados=[]
for posicion in range(0,10):
  nombre_producto=Busquedas_ordenadas[posicion][2]
  productos_más_buscados.append(nombre_producto)

print(productos_más_buscados)

"""Ahora, vamos a diseñar un código para encontrar los 5 productos con menores ventas y los 10 productos con menores búsquedas, pero por categoria. En este caso, mucho del desarrollo tendrá que ser similar, aunque únicamente hay que asegurarnos de estar filtrando información referente a la categoria, esto se puede abordar con un condicional if y un ciclo for que itere sobre las diferentes categorias. """

#Primero obtenemos las categorias que existen, nos vamos fijando en las categorias, y si no la hemos encontrado antes, la agregamos a una lista que contiene las categorias, así evitamos valores repetidos.

categorias=[]
for producto in lifestore_products:
  if not producto[3] in categorias:
    categorias.append(producto[3])
#print(categorias)
#Ahora que tenemos las categorias, podemos iterar sobre ellas para obtener los 5 productos menos vendidos con el enfoque anterior.
Productos_menos_vendidos_por_categoria=[]
for categoria in categorias:
  if categoria == "memorias usb":
    Productos_menos_vendidos=[]
    Ventas=[]
    for producto in lifestore_products:
      if producto[3] == categoria:
        Número_de_ventas=0
        for venta in lifestore_sales:
          if producto[0]==venta[1] and venta[4]==0:
            Número_de_ventas+=1
      
        Ventas.append([producto[0],Número_de_ventas,producto[1]])

    Ventas_ordenadas = sorted(Ventas, key= lambda x: x[1], reverse=False)
    for posicion in range(0,2):
      id_producto=Ventas_ordenadas[posicion][2]
      Productos_menos_vendidos.append(id_producto)
    Productos_menos_vendidos_por_categoria.append([categoria,Productos_menos_vendidos])
  else:
    Productos_menos_vendidos=[]
    Ventas=[]
    for producto in lifestore_products:
      if producto[3] == categoria:
        Número_de_ventas=0
        for venta in lifestore_sales:
          if producto[0]==venta[1] and venta[4]==0:
            Número_de_ventas+=1
      
        Ventas.append([producto[0],Número_de_ventas,producto[1]])

    Ventas_ordenadas = sorted(Ventas, key= lambda x: x[1], reverse=False)
    for posicion in range(0,5):
      id_producto=Ventas_ordenadas[posicion][2]
      Productos_menos_vendidos.append(id_producto)
    Productos_menos_vendidos_por_categoria.append([categoria,Productos_menos_vendidos])

#Vamos a mostrar el ID de los productos menos vendidos por categoría

print(Productos_menos_vendidos_por_categoria)

"""Podemos aplicar el mismo método para buscar los 10 con menores búsquedas"""

Productos_menos_buscados_por_categoria=[]
for categoria in categorias:
  if categoria == "memorias usb":
    Productos_menos_buscados=[]
    Busquedas=[]
    for producto in lifestore_products:
      if producto[3] == categoria:
        Número_de_busquedas=0
        for busqueda in lifestore_searches:
          if producto[0]==busqueda[1]:
            Número_de_busquedas+=1
      
        Busquedas.append([producto[0],Número_de_busquedas,producto[1]])

    Busquedas_ordenadas = sorted(Busquedas, key= lambda x: x[1], reverse=False)
    for posicion in range(0,2):
      id_producto=Busquedas_ordenadas[posicion][2]
      Productos_menos_buscados.append(id_producto)
    Productos_menos_buscados_por_categoria.append([categoria,Productos_menos_buscados])
  else:
    Productos_menos_buscados=[]
    Busquedas=[]
    for producto in lifestore_products:
      if producto[3] == categoria:
        Número_de_busquedas=0
        for busqueda in lifestore_searches:
          if producto[0]==busqueda[1]:
            Número_de_busquedas+=1
      
        Busquedas.append([producto[0],Número_de_busquedas,producto[1]])

    Busquedas_ordenadas = sorted(Busquedas, key= lambda x: x[1], reverse=False)
    for posicion in range(0,9):
      id_producto=Busquedas_ordenadas[posicion][2]
      Productos_menos_buscados.append(id_producto)
    Productos_menos_buscados_por_categoria.append([categoria,Productos_menos_buscados])
  

#Vamos a mostrar el ID de los productos menos buscados por categoría
print(Productos_menos_buscados_por_categoria)

"""Ahora vamos a encontrar los 5 productos con mejores reseñas en promedio y los vamos a almacenar en la lista Mejores_reseñas, y a los 5 productos con las peores reseñas que se van a almacenar en la lista Peores_reseñas. En este caso, se van a considerar todas las transacciones, sin importar si hubo devoluciones, pero no consideraremos aquellos productos que no se vendieron y que no tengan reseñas"""

"""lifestore_searches = [id_search, id product]
lifestore_sales = [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
lifestore_products = [id_product, n ame, price, category, stock]"""


Puntuaciones=[]

#Iteramos sobre cada uno de los productos
for producto in lifestore_products:
  #Vamos a ir guardando las puntuaciones de las diferentes transacciones
  Puntuaciones_de_producto=[]
  for transaccion in lifestore_sales:
    if producto[0] == transaccion[1]:
      Puntuaciones_de_producto.append(transaccion[2])


  if len(Puntuaciones_de_producto) != 0:
    Puntuacion_promedio=(sum(Puntuaciones_de_producto))/(len(Puntuaciones_de_producto))
    Puntuaciones.append([producto[0],Puntuacion_promedio])
  else:
    continue
#Ordenamos las puntuaciones de mayor puntuación a menor puntuación.
#print(Puntuaciones)

Puntuaciones_ordenadas=sorted(Puntuaciones, key= lambda x: x[1], reverse=True)
#print(Puntuaciones_ordenadas)

#Generamos las dos listas.
Mejores_resenas=[]
Peores_resenas=[]

IDs_resenas_ordenadas= [x[0] for x in Puntuaciones_ordenadas]


for i in range(0,5):
  ID=IDs_resenas_ordenadas[i]
  Mejores_resenas.append(lifestore_products[ID][1])

for i in range(len(Puntuaciones_ordenadas)-1,len(Puntuaciones_ordenadas)-6,-1):
  ID=IDs_resenas_ordenadas[i]
  Peores_resenas.append(lifestore_products[ID][1])

print(Mejores_resenas)
print(Peores_resenas)

"""En esta parte final del proyecto tenemos que calcular el Total de ingresos y ventas promedio mensuales,
total anual y meses con más ventas al año"""

"""Lo anterior lo podemos interpretar como calcular el promedio de los ingresos totales (dinero) que se obtienen cada mes, y el promedio de las ventas (número de ventas) que se realizan por mes
"""
"""Luego calcular el total anual de ingresos obtenidos, el total anual de ventas realizadas, y por último, mostrar los meses con más ventas al año."""

from lifestore_file import lifestore_sales,lifestore_products,lifestore_searches 

"""Primero vamos a calcular los ingresos totales por mes, por lo tanto, de la lista de ventas, vamos a filtrar aquellas transacciones que no hayan tenido devoluciones, y que hayan ocurrido en un mes en particular."""

#Importamos una librería que será de utilidad para trabajar con fechas

from datetime import datetime
from statistics import mean
#Establecemos los números de meses
meses=range(1,13)
Ventas=[]
for mes in meses:
  Ventas_del_mes=[]
  for venta in lifestore_sales:
    fecha=datetime.strptime(venta[3], '%d/%m/%Y')
    month=fecha.month
    if venta[4]==0 and mes==month:
      #Podemos crear una lista de todas ganancias del respectivo mes, así, para obtener el número de ventas sólo habrá que calcular la longitud de la lista, y para obtener los ingresos totales, sólamente habrá que sumar todos los valores dentro de la lista. 
      for producto in lifestore_products:
        if venta[1]==producto[0]:
          Ventas_del_mes.append(producto[2])
  Ventas.append([mes,len(Ventas_del_mes),sum(Ventas_del_mes)])

#Ahora, en ventas, tenemos el [mes, ventas realizadas en ese mes, y los ingresos totales de ese mes]
#Podemos separarlos ahora, para calcular los promedios.
Numero_ventas_promedio_por_mes=mean([i[1] for i in Ventas])
print(Numero_ventas_promedio_por_mes)

Ingresos_promedio_por_mes=mean([i[2] for i in Ventas])
print(Ingresos_promedio_por_mes)

#Podemos calcular ahora el total de ingresos y ventas de forma anual 
Ventas_anuales=sum([i[1] for i in Ventas])
Ingresos_anuales=sum([i[2] for i in Ventas])

print(Ventas_anuales)
print(Ingresos_anuales)

#Por último, podemos ordenar los meses en función de las ventas realizadas.
Ventas_ordenadas=sorted(Ventas,key= lambda x:x[1], reverse=True)
meses=[x[0] for x in Ventas_ordenadas]
print(meses)


  