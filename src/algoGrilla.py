import argparse, datetime, random, string,time

FRASES = 'frases.csv'
PALABRAS = 'palabras.csv'

def main():
	''' En el caso que al ejecutar el programa se le pase el -s, el programa imprimira la grilla completa y finalizara la ejecuccion.
	En caso de ingresar -n seguido del numero de grilla retomara en una grilla ya jugada. Finalmente si no se ingresa otro parametro ingresara en el modo interactivo'''
	parser = argparse.ArgumentParser(description='Generador de Algogrillas')
	parser.add_argument('-s', '--solucion', action='store_true', help='imprimir la solución')
	parser.add_argument('-n', '--numero', help='número de algogrilla')
	args = parser.parse_args()

	if args.numero and args.numero.isdigit():
		numero_de_algogrilla = int(args.numero)
	else:
		numero_de_algogrilla = int(datetime.datetime.now().timestamp())
	random.seed(numero_de_algogrilla)

	imprimir_solucion = args.solucion # es True si el usuario incluyó la opción -s
	if imprimir_solucion:
		grilla_completa(crear_grilla(),numero_de_algogrilla)
		return 
	else:
		grilla_interactiva(crear_grilla(),numero_de_algogrilla)



def crear_grilla():
    '''Crea la grilla apartir de dos archivos uno de frases y otro de palabras, eligiendo palabras al azar  que encajan en la frase, y devuelve
    un diccionario donde la clave es la palabra y los valores son[silabas,definicion], asi como a su ves la frase, con sus columnas y autor
    '''
    palabras_grilla={}
    diccionario_frases,diccionario_palabras,lista_palabras=diccionarios_archivos(FRASES,PALABRAS)
    frase_elegida=elegir_frase(diccionario_frases)
    frase_mitad1,frase_mitad2,autor,columna1,columna2=dividir_frase(frase_elegida)
    columna1=int(columna1)
    columna2=int(columna2)
    while len(palabras_grilla) < len(frase_mitad2):
        palabra=lista_palabras[random.randint(0,len(lista_palabras)-1)]
        if len(palabra)>=columna2 and palabra[columna1-1]== frase_mitad1[len(palabras_grilla)] and palabra[columna2-1]== frase_mitad2[len(palabras_grilla)]:
            palabras_grilla[palabra]=diccionario_palabras[palabra]
            continue
    if len(frase_mitad1) > len(frase_mitad2):
        while True:
            palabra=lista_palabras[random.randint(0,len(lista_palabras)-1)]
            if len(palabra) < columna2:
                if palabra[columna1-1]== frase_mitad1[len(frase_mitad1)-1:]:
                    palabras_grilla[palabra]=diccionario_palabras[palabra]
                    break
    return palabras_grilla,frase_elegida,columna1,columna2,frase_mitad1,frase_mitad2


def grilla_interactiva(funcion,numero_de_algogrilla):
	'''Recibe una funcion y el numero de algogrilla.
	Esta funcion es la que actua cuando se implementa el programa en modo interactivo.
	Imprime el juego con las palabras censuradas y pide que se ingrese un numero y luego la palabra. Si es correcta, se la pone en la grilla y elimina sus silabas y definicion.
	Si no se acierta, se sigue intentando hasta que ingrese 0 o se complete
	 '''
	palabras_grilla,frase_elegida,columna1,columna2,frase_mitad1,frase_mitad2=funcion
	palabras= palabras_grilla.keys()
	lista_palabras_grilla={}
	palabra_ingresada=''
	numero_ingresado=-1
	lista_palabras=[]
	dicc_frases_silabas={}
	lista_numeros=[]
	for i,x in enumerate(palabras,1):
		lista_palabras_grilla[i]=x,palabras_grilla[x],('.' * len(x))
		lista_palabras.append(x)
	while numero_ingresado !=0:
		print('ALGOGRILLA NUMERO {}'.format(numero_de_algogrilla),'\n','\n')
		imprimir_grilla(frase_mitad1,lista_palabras_grilla,lista_palabras,columna1,columna2)
		print('\n','DEFINICIONES','\n')
		for x in lista_palabras_grilla.items():    #imprime las definiciones
			print(x[0],x[1][1][1])
		imprimir_silabas(lista_palabras_grilla)
		if len(lista_palabras_grilla) == 0:
			print('Felicidades, completaste la grilla')
			return
		print('\n','Al finalizar leerá una frase de {}'.format(frase_elegida[2]))
		numero_ingresado=int(input('Ingrese un número de palabra o 0 para terminar: '))
		if numero_ingresado in lista_numeros:
			print('El numero de palabra ya fue adivinado, ingrese otro numero')
			numero_ingresado=int(input('Ingrese un número de palabra o 0 para terminar: '))
		if numero_ingresado == 0:
			return  
		if numero_ingresado not in lista_palabras_grilla:
			print('Ingrese un numero valido')
			numero_ingresado=int(input('Ingrese un número de palabra o 0 para terminar: '))
		palabra_ingresada=input('Ingrese la definición de la palabra: ')
		if palabra_ingresada in lista_palabras_grilla[numero_ingresado]:
			lista_palabras_grilla.pop(numero_ingresado)
			lista_numeros.append(numero_ingresado)
			print('¡Correcto!')
			time.sleep(0.5)
		else:
			print('¡Incorrecto!')
			time.sleep(0.5)
	
def grilla_completa(funcion,numero_de_algogrilla):
	'''Recibe una funcion , que contiene las palabras de la grilla con sus respectivas silabas y definiciones.
	Imprime la grilla completa, con sus palabras completadas, definiciones, silabas'''
	palabras_grilla,frase,columna1,columna2,frase_mitad1,frase_mitad2=funcion
	valores=palabras_grilla.values()
	print('ALGOGRILLA NUMERO {}'.format(numero_de_algogrilla),'\n','\n')
	palabras= palabras_grilla.keys()
	for i,x in enumerate(palabras,1):    #genera la grilla, ya resuelta
		if len(x) < columna2:
			print(i,x[0:columna1-1]+x[columna1-1].upper()+x[columna1:],sep=' ')
			continue
		if i<10:
			print(i,x[0:columna1-1]+x[columna1-1].upper()+x[columna1:columna2-1]+x[columna2-1].upper()+x[columna2:],sep='  ')
		else:
			print(i,x[0:columna1-1]+x[columna1-1].upper()+x[columna1:columna2-1]+x[columna2-1].upper()+x[columna2:])
	print('\n','DEFINICIONES')
	for i,x in enumerate(valores,1):			#imprime las definiciones
		if i<10:
			print(i,x[1],sep='  ')
		else:
			print(i,x[1])
	print('\n','SILABAS')
	print(silabas_ordenada(valores),'\n')  			#imprime las silabas
	print('Al finalizar leerá una frase de {}'.format(frase[2]))

def silabas_ordenada(diccionario):
	''' Recibe un diccionario donde los primeros valores son las silabas y las devuelve ordenadas alfabeticamente'''
	lista_silabas=[]
	for x in diccionario:
		lista_silabas.append(x[0].replace('-',','))
	silabas=','.join(lista_silabas)
	return sorted(silabas.split(','))
	
def diccionarios_archivos(archivo1,archivo2):
    ''' Recibe un archivo de frases y otro de palabras.Agarra cada palabra y cada frase y las guarda.
    Devuelve dos diccionarios.Uno de frases donde la clave es un numero y los valores son [frases,columnas,autor] y otro donde la clave es una palabra y sus valores son
    [silabas,definicion]
    '''
    diccionario_palabras={}
    diccionario_frases={}
    lista_palabras=[]
    with open(FRASES) as frases,open(PALABRAS) as palabras:
        for i,x in enumerate(frases):
            frases= x.split('|')
            diccionario_frases[i] = frases
        for i in palabras:
            try:
                palabra,silaba,definicion=i.split('|')
                palabra_simplificada=simplificar_palabra(palabra)
                diccionario_palabras[palabra_simplificada]=[silaba,definicion.strip('\n')]
                lista_palabras.append(palabra_simplificada)
            except ValueError:
                continue

    return diccionario_frases,diccionario_palabras,lista_palabras




def dividir_frase(lista):
    '''Recibe una lista que contiene [frase,columnas,autor] y devuelve la frase dividida en la mitas(en caso de ser impar la letra de sobra va a la primer mitad),
    las columnas donde va la frase y el autor'''
    longitud_frase=len(lista[0])
    mitad_frase= longitud_frase/2
    if longitud_frase %2==0:
        mitad1=lista[0][0:int(mitad_frase)]
        mitad2=lista[0][int(mitad_frase):]
    else:
        mitad1=lista[0][0:int(mitad_frase+0.5)]
        mitad2=lista[0][int(mitad_frase+0.5):]
    return mitad1,mitad2,lista[2],lista[1][0],lista[1][1]

def simplificar_palabra(cadena):
    '''Recibe palabras y las simplifica devolviendola'''
    letras_complejas,letras_simplificadas = 'áéíóúüñ','aeiouuñ'
    palabra_simplificada=''
    for x in cadena.lower():
        if x =='(':
            break
        if x in string.ascii_lowercase:
            palabra_simplificada+=x
        if x in letras_complejas:
            posicion=letras_complejas.find(x)
            palabra_simplificada+=letras_simplificadas[posicion]
    return palabra_simplificada

def elegir_frase(diccionario):
    '''Recibe un diccionario, elige una frase al azar y la devuelve siplificada, en una lista que contiene, [frase,columna,autor]'''
    lista_frase=[]
    frase_simplificada=''
    letras_complejas,letras_simplificadas = 'áéíóúüñ','aeiouuñ'
    frases = diccionario[random.randint(0,len(diccionario))]
    frase,columnas,autor=frases
    for letra in frase.lower():
        if letra == '(':
            break
        if letra in string.ascii_lowercase:
            frase_simplificada+=letra
        if letra in letras_complejas:
            posicion=letras_complejas.find(letra)
            frase_simplificada+=letras_simplificadas[posicion]
    lista_frase.append(frase_simplificada)
    columnas=columnas.split(',')
    lista_frase.append(columnas)
    autor=autor.strip('\n')
    lista_frase.append(autor)
    return lista_frase


def imprimir_grilla(frase_mitad1,lista_palabras_grilla,lista_palabras,columna1,columna2):	
	'''Imprime la grilla a jugar con las palabras correspondientes a la frase en mayuscula'''
	for x in range(1,len(frase_mitad1)+1):						
		if x not in lista_palabras_grilla:
			pal=lista_palabras[x-1]								
			if len(lista_palabras[x-1]) < columna2:     
				print(x,pal[0:columna1-1]+
					pal[columna1-1].upper()+
					pal[columna1:],sep=' ')
				continue
			if x<10:
				print(x,pal[0:columna1-1]+
					pal[columna1-1].upper()+pal[columna1:columna2-1]+
					pal[columna2-1].upper()+pal[columna2:],sep='  ')
				continue
			else:
				print(x,pal[0:columna1-1]+pal[columna1-1].upper()+
					pal[columna1:columna2-1]+pal[columna2-1].upper()+pal[columna2:])
				continue
		else:
			palabra=lista_palabras_grilla[x]
		if x < 10:
			print(x,palabra[2],sep='  ')
		else:
			print(x,palabra[2],)

def imprimir_silabas(lista_palabras_grilla):
	'''Imprime las silabas ordenadas alfabeticamente'''
	print('\n','SILABAS')
	lista_silabas_ordenadas=[]
	for x in lista_palabras_grilla.items():         #imprime las silabas ordenadas alfabeticamente
		lista_silabas_ordenadas.append(x[1][1][0])
	silabas=','.join(lista_silabas_ordenadas)
	silabas_csv=silabas.replace('-',',')
	print(sorted(silabas_csv.split(',')))
main()


