#Autor
#César Daniel Bravo Alvarado





##### Explicare linea por linea el codigo para que personas que no esten familiarizadas con el lenguaje lo puedan
##### entender mejor

#### Primero en toda esta region lo que realizo es una importacion de las librerias que usare
import matplotlib.pyplot as plt #matplotlib sirve para poder presentar graficas e imagenes (en terminos genrales)
import cv2                      #cv2 es la palabra clave para llamar a opencv en su version de python, aqui se encuentran
                                #multiples herramientas para la manipulacion de imagenes    
import numpy as np              #numpy es una libreria muy conocida de python en la cual nos permite trabajar con matrices
import math                     #math es una libreria incluida dentro de python en la cual se incluyen funciones matematicas
import pandas as pd             #Pandas es una libreria la cual me permite crear bases de datos y guardarlas en la computadora


###### Empieza el codigo
img = cv2.imread("frotis.jpg") #Primero leemos la imagen con cv2, podemos leerlo tambien plt pero cv2 nos permite obtener la imagen en un formato long
plt.imshow(img) #Grafica la imagen
plt.figure() #Crea una nueva imagen para graficar una nueva imagen
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #Cambia el formato de la imagen que introducimos en la linea 23, esto se hace debido a que con cv2 las imagenes
                                     #son importadas con organizacion de colores de BGR, esto lo pasa a RGB
plt.imshow(img) #Grafica la imagen con los cambios de BGR a RGB

######## Estas lineas de la 23 a la 28 solo son para mostrar el cambio de color BGR a RGB por lo que no son esenciales

img = cv2.imread("frotis.jpg")  #Volvemos a importarlo, solo en caso que se desee eliminar la lineas anteriores
img_grey = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) #Cambia el formato a escala de grises
plt.imshow(img_grey,cmap="gray") #Muestra la imagen pero con una escala de grises
plt.figure() 



######Aqui empieza el analisis para detectar la celulas, lo que yo hice fue considerar otro camino que puede ser posible
######Tanto eliminiar las marcas de agua como ir seprando las imagenes
##Figura 1
thresh=200  #Primero establecemos un thresh, cuando el valor es mas alto este se encontrara mas sensible a los bordes
            #Esto solo se vera ya cuando lo apliquemos a nuestra función, por el momento es solo una variable int

ret,thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY) #Esta funcion nos permite umbralizar nuestra imagen
#El primer argumento es la imagen, el segundo es nuestro valor de umbral (osea thresh), el tercer valor es la intensidad maxima
#El cuarto nos permite establecer que la imagen se encontrara en un formato de true y false (255 o 0)
contours, _ = cv2.findContours(thresh_img, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE) #Con esta funcion lo que buscamos son nuestro bordes,con el segundo argumento nos permite
                                                                #Establecer una jerarquia entre los bordes de tal forma que podamos identificar los borde principales
                                                                #El tercer argumento es el que nos permite que despues de que nuestra funcion identificara multiples bordes
                                                                #y los reconocera como una unica forma
img_contours = np.zeros(img.shape)  #Aqui se crea una matriz con las dimensiones de la imagen que estamos trabajando
cv2.drawContours(img_contours, contours, -1, (0,255,0), 2) #Una vez que tenemos los bordes de lo que hacemos es llenar esa matriz (en este caso imagen) que se encuentra vacio


plt.imshow(img_contours) #Mostamos la imagen que creamos
cv2.imwrite("Contornos.jpg",img_contours) #Guardamos una copia de los contornos en la imagen se llama Contornos.jpg

contours_area = [] #Creamos una variable lista que esta vacia

for con in contours: #Empezamos un ciclo for
    a = cv2.contourArea(con) #Con cada elemento del contorno, identificamos el area y lo guardaremos en una variable que ira cambiando llamada a
    if 3 <= a <= 440:  #Aqui determinamos el rango de valores con el cual determiaremos si es una celula o no, en base a su area.
        contours_area.append(con) #Los elementos que pasen la sentencia if segan guardados en la lista contours_area
        #El ciclo for termina a partir de este punto

#print(len(contours_area)) #Solo para saber la longitud de la lista que se formo, desde aqui podemos saber cuantas celulas se encontraron.
contourCircle= []  #Ahora dejamos una lista vacia para el contorno

N0 =[];AreaList=[];PerimeterList=[];CircularityList=[]; #Creamos multiples listas vacias para guardar valores que se usaran en nuestro xmls
a2 = 0 #Guardo una variable a que funcionara como contador, no use a porque a ya lo estaba usando para un area
for con in contours_area: #Usamos los valores guardados en la lista contours_area 
    perimeter = cv2.arcLength(con, True) #Obtenemos la longitud de cada uno de los contours area y con la cual obtendremos nuestro perimetro de cada celula
    area = cv2.contourArea(con) #cv2 tambien nos permite obtner el area que conforma a cada una de las imagenes
    circularity = 4*math.pi*(area/(perimeter*perimeter)) #Calculamos la circularidad
    contourCircle.append(con) 
    a2 = a2+1
    print("No. Figura:\t{}\nArea:\t{:.2f}\nPerimetro:\t{:.2f}\nCircularidad\t{:.2f}\n\n\n".format(a2,area,perimeter,circularity))
    N0.append(a2);AreaList.append(area);PerimeterList.append(perimeter) #Vamos pasandolo todo a listas para pasarlo a un diccionario
    CircularityList.append(circularity)

print(len(AreaList),len(PerimeterList),len(CircularityList))


Figura1= { "Area":AreaList, "Perimetro":PerimeterList,
          "Circularity":CircularityList} #Aqui creamos un diccionario, para facilitar el añadirlo a un documento de excel
DataFrame=pd.DataFrame(data=Figura1,dtype=np.int8) #Creamos una base de datos o dataframe
DataFrame.to_excel("Figura1.xlsx") #Lo guardamos en la computadora con el nombre Figura1.xlsx



#Aqui repetimos casi todo pero para figura 2, solo cambiamos en el thresh y en los limites del area
##Figura 2
thresh=100

ret1,thresh_img1 = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
contours1, _ = cv2.findContours(thresh_img1, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
img_contours1 = np.zeros(img.shape)
cv2.drawContours(img_contours1, contours1, -1, (255,255,0), 2)

plt.imshow(img_contours1)
cv2.imwrite("Contornos2.jpg",img_contours1)

contours_area1 = []

for con in contours1:
    a = cv2.contourArea(con)
    if 290 < a< 1500:
        contours_area1.append(con)

print(len(contours_area1))

N0 =[];AreaList=[];PerimeterList=[];CircularityList=[];
contourCircle1= []
a3 = 0
for con in contours_area1:
    perimeter1 = cv2.arcLength(con, True)
    area1 = cv2.contourArea(con)
    if perimeter1 == 0:
        break
    circularity1 = 4*math.pi*(area1/(perimeter1*perimeter1))
    contourCircle.append(con)
    a3 = a3+1
    print("No. Figura:\t{}\nArea:\t{:.2f}\nPerimetro:\t{:.2f}\nCircularidad\t{:.2f}\n\n\n".format(a3,area1,perimeter1,circularity1))
    N0.append(a3);AreaList.append(area1);PerimeterList.append(perimeter1)
    CircularityList.append(circularity1)

Figura1= { "Area":AreaList, "Perimetro":PerimeterList,
          "Circularity":CircularityList}
DataFrame=pd.DataFrame(data=Figura1,dtype=np.int8)
DataFrame.to_excel("Figura2.xlsx")




##Figura 3
## La figura 3 se creara como un producto de las dos imagenes anteriores, como la coloree con colores ditintos, se logra distinguir.

imagenfusionada = cv2.addWeighted(src1=img_contours, alpha=0.5, src2=img_contours1,
                                  beta=0.5, gamma=0)

plt.imshow(imagenfusionada)
cv2.imwrite("Contornos1.jpg",imagenfusionada) #Guardamos la imagen 3 con el nombre Contornos1.jpg



#############Quise agregarle un poco mas de juego con respecto a lo que vimos en el curso y agrege estructuras morfologicas, cree para 2 casos pero en lo personal
#############la que mas me agrado fue la estructura morfologica de cierre
kernel= np.ones((9,9),np.uint8)
plt.figure()

Cierre = cv2.morphologyEx(img_contours,cv2.MORPH_CLOSE,kernel)
plt.imshow(Cierre)

Dilatacion = cv2.dilate(img_contours,kernel,iterations=1)
plt.imshow(Dilatacion)

plt.figure()
Dilatacion1 = cv2.dilate(img_contours1,kernel,iterations=2)
plt.imshow(Dilatacion1)

plt.figure()
Cierre1 = cv2.morphologyEx(img_contours1,cv2.MORPH_CLOSE,kernel)
plt.imshow(Cierre1)


###########Junte las 2 imagenes con una estructura morfologica de cierre
imagenfusionada = cv2.addWeighted(src1=Cierre, alpha=0.5, src2=Cierre1,
                                  beta=0.5, gamma=0)
plt.imshow(imagenfusionada)
cv2.imwrite("EstructuramorfologicaCierreCierreMasCierre.jpg",imagenfusionada)

###########Junte las 2 imagenes con una estructura morfologica una de cierre y otra de diltatacion
imagenfusionada = cv2.addWeighted(src1=Cierre, alpha=0.5, src2=Dilatacion1,
                                  beta=1, gamma=0)
plt.imshow(imagenfusionada)
cv2.imwrite("EstructuramorfologicaCierreCierreMasDilatacion.jpg",imagenfusionada)

