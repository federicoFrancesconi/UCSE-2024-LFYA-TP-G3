from collections import defaultdict

def generar_producciones(gramatica):
        reglas = gramatica.strip().split('\n')
        producciones = defaultdict(list)
        for regla in reglas:
            antecedente, consecuente = regla.strip().split(':')
            antecedente = antecedente.strip()
            consecuente = tuple(consecuente.strip().split())
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
                first_value_nt = generar_first_para_no_terminal(value, gramatica_procesada, firsts_por_nt) #Vamos a generar recursivamente los first para los no terminales.
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
    firsts_por_regla = defaultdict(list)

    for antecedente in gramatica_procesada:
        for consecuente in gramatica_procesada[antecedente]:
            for value in consecuente:
                if value.islower() and value != 'lambda':
                    firsts_por_nt[antecedente].add(value)
                    break
                elif value.isupper():
                    first_value_nt = generar_first_para_no_terminal(value, gramatica_procesada, firsts_por_nt)
                    firsts_por_nt[antecedente].update(first_value_nt)
                    if 'lambda' not in first_value_nt:
                        break
                elif value == 'lambda':
                    firsts_por_nt[antecedente].add('lambda')
                    break

    for antecedente in gramatica_procesada:
        for consecuente in gramatica_procesada[antecedente]:
            for value in consecuente:
                if value.islower() and value != 'lambda':
                    firsts_por_regla[antecedente].append((tuple(consecuente), {value}))
                    break
                elif value.isupper():
                    firsts = set(firsts_por_nt[value])
                    
                    # Agregar FIRSTS de ese no terminal, quitando 'lambda'
                    firsts_por_regla[antecedente].append((tuple(consecuente), firsts - {'lambda'}))
                    
                    # Si 'lambda' está en FIRSTS, seguimos revisando el siguiente símbolo
                    if 'lambda' in firsts:
                        if value == consecuente[-1]:  # Si es el último símbolo, permitimos agregar 'lambda'
                            firsts_por_regla[antecedente].append((tuple(consecuente), {'lambda'}))
                        else:
                            continue
                    else:
                        break
                elif value == 'lambda' and len(consecuente) == 1:  # Solo agregamos lambda si es el único símbolo
                    firsts_por_regla[antecedente].append((tuple(consecuente), {'lambda'}))
                    break
    
    return firsts_por_regla, firsts_por_nt


#Ahora vamos a calcular los follow yey
def generar_follows(gramatica_procesada, firsts_por_nt):

    follows = defaultdict(set)
    cambios = True #Con una iteracion no basta para sacar los follow, por lo que hacemos un while que va a tomar cambios en los follow
    while cambios:
        cambios = False
        for antecedente in gramatica_procesada:
            for consecuente in gramatica_procesada[antecedente]:
                for indice,caracter in enumerate(consecuente):
                    if caracter.isupper(): #Es un no terminal y podemos sacar algun follow de el :P
                        if indice + 1 < len(consecuente): #Si no esta al final de la cadena
                            siguiente = consecuente[indice+1]
                            if siguiente.islower():  # El siguiente es un terminal
                                if siguiente not in follows[caracter]:  #Si no lo añadi anteriormente, lo añado y marco cambios en True
                                    follows[caracter].add(siguiente)  
                                    cambios = True

                            elif siguiente.isupper(): #Si un no terminal esta seguido de otro no terminal, agregamos sus firsts :v
                                first_siguiente = firsts_por_nt[siguiente] - {'lambda'} #Saco lambda de los firsts, por las dudas je
                                if not first_siguiente.issubset(follows[caracter]): #Aca pregunto si los first del siguiente ya estan contenidos en los follow (En caso de ya estar presentes no entro al if)
                                    follows[caracter].update(first_siguiente) #Si faltan elementos de los first del elemento siguiente, los agrego al set (se usa .update cuando se añaden varios elementos a un set).
                                    cambios = True
                                if 'lambda' in firsts_por_nt[siguiente]:
                                    if not follows[antecedente].issubset(follows[caracter]):  #Hago la misma validacion que antes
                                        follows[caracter].update(follows[antecedente])  #Si los follows ya estan en el subconjunto no se agregan, de lo contrario si
                                        cambios = True



                        else: #Osea, si es el utlimo en la cadena
                            if not follows[antecedente].issubset(follows[caracter]):  
                                follows[caracter].update(follows[antecedente])  
                                cambios = True

    return follows

if __name__ == "__main__":
    gramaticaejemplo = "A : b A \n A : a \n A : A B c \n A : lambda \n B : b"
    
    # Generamos las producciones a partir de la gramática
    producciones = generar_producciones(gramaticaejemplo)
    
    # Calculamos FIRSTs por regla y FIRSTs por no terminal
    firsts_por_regla, firsts_por_nt = generar_firsts_por_regla(producciones)
    
    # Calculamos FOLLOWs por no terminal
    follows = generar_follows(producciones, firsts_por_nt)

    # Imprimimos los resultados en el formato solicitado
    for antecedente, reglas in firsts_por_regla.items():
        for regla, firsts in reglas:
            follow_nt = follows[antecedente]
            print(f"{antecedente} : {' '.join(regla)} {{{', '.join(firsts)}}} {{{', '.join(follow_nt)}}}")
