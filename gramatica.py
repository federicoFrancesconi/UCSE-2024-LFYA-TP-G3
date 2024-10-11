from collections import defaultdict

class Gramatica:
    esLL1 = False
    gramaticaejemplo = "A : b c \n A : a b \n A : d B \n B : d e \n B : f"
    
    producciones=defaultdict(list)
    first = defaultdict(list)

    #Lo que hace esta funcion es tomar la gramatica de entrada y separar en key-value con los antecedentes y los consecuentes con la estructura {antecedente:[(consecuente),(consecuente)],}
    def generar_producciones(gramatica):
        reglas = gramatica.strip().split('\n')
        producciones=defaultdict(list)
        for regla in reglas:
            antecedente,consecuente = regla.strip().split(':')
            antecedente= antecedente.strip()
            consecuente = tuple(consecuente.split(" "))
            producciones[antecedente].append(consecuente)
        return producciones
    
    def generar_first_para_no_terminal(no_terminal, gramatica_procesada, firsts_por_nt): #Lo que hace esta funcion es calcular recursivamente los firsts para cada no terminal
        if no_terminal in firsts_por_nt and firsts_por_nt[no_terminal]: #Primero verifico que los first no esten calculados, si lo estan lo devuelvo
            return firsts_por_nt[no_terminal]
        
        firsts_por_nt[no_terminal] = set()  #Creamos un SET para agregar los no terminales (Y no tener que verificar que esten repetidos)
        
        # Recorremos las reglas del no terminal
        for consecuente in gramatica_procesada[no_terminal]:
            for value in consecuente:
                if value.islower() and value != 'lambda':  # Es un terminal
                    firsts_por_nt[no_terminal].add(value)
                    break
                elif value.isupper():  # Es un no terminal
                    first_value_nt = generar_first_para_no_terminal(value, gramatica_procesada, firsts_por_nt)
                    firsts_por_nt[no_terminal].update(first_value_nt)
                    
                    # Si el FIRST del no terminal contiene lambda, seguimos buscando
                    if 'lambda' not in first_value_nt:
                        break
                elif value == 'lambda':
                    firsts_por_nt[no_terminal].add('lambda')
                    break
        
        return firsts_por_nt[no_terminal]

    def generar_firsts_por_regla(gramatica_procesada):
        firsts_por_nt = defaultdict(set)
        firsts_por_regla = defaultdict(list) #Esto va a ser asi: {A:{(first),(first),(first)], B:[(first),(first),(first)]}
        # Lo que hago en la primer pasada es calcular los first por no terminal para tener la lista completa de firsts de cada nt, de esta forma cuando en alguna regla haya A -> B ya tengo calculados los first de B
        for antecedente in gramatica_procesada:  # Recorremos el diccionario que contiene las reglas
            for consecuente in gramatica_procesada[antecedente]:  # Recorremos cada NT y sus reglas
                for value in consecuente:  # Recorro los valores dentro del consecuente
                    if value.islower() and value != 'lambda':  # Si es un terminal lo agregamos
                        firsts_por_nt[antecedente].add(value)
                        break
                    elif value.isupper():  # Si es un no terminal
                        # Aquí obtenemos el FIRST del no terminal recursivamente
                        first_value_nt = generar_first_para_no_terminal(value, gramatica_procesada, firsts_por_nt)
                        firsts_por_nt[antecedente].update(first_value_nt)
                        
                        # Si el FIRST contiene lambda, seguimos analizando el siguiente símbolo en la regla
                        if 'lambda' not in first_value_nt:
                            break
                    elif value == 'lambda':
                        firsts_por_nt[antecedente].add('lambda')
                        break
        #Ahora que tengo calculados los firsts para cada no terminal, los voy a calcular por regla:
        for antecedente in gramatica_procesada: 
            for consecuente in gramatica_procesada[antecedente]: #A
                for value in consecuente: 
                    if value.islower() and value != 'lambda':  
                        firsts_por_regla[antecedente].append(tuple(value))
                        break #Hago el break para que salga del for, ya que al haber encontrado el first, no tiene mas nada que hacer dentro de esa regla
                    elif value.isupper(): #Aca vamos a tener que hacer la consideracion de que lambda este en los first, por lo que vamos a tener que buscar los firsts del siguiente
                        firsts =  tuple(firsts_por_nt[value])
                        firsts_por_regla[antecedente].append(firsts)
                        if 'lambda' in firsts and value != consecuente[-1]:  #Hay que hacer este if para que tenga 
                            continue
                        else:
                            break
                    elif value == 'lambda':
                        firsts_por_regla[antecedente].append(tuple(value))
                        break
        return firsts_por_regla



                        


                   



            
    
    

        

    # Esta función debe implementar la lógica suficiente para que al imprimir en pantalla una instancia de este objeto
    # a la que se le haya invocado dicho método previamente se muestre la gramática de la siguiente manera:
    # por cada regla o producción mostrar dicha regla y a continuación los First, Follows y Selects correspondientes.
    def setear(self, gramatica):
        return
    
    # Devuelve true en caso de que la cadena se derive de la gramática y false en caso contrario. 
    def evaluar_cadena(self, cadena):
        return
    
    # Funcion para imprimir la gramatica
    def __str__(self):
        return ""
    