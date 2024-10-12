# Comentarios Generales:
# Para agregar varios elementos a un set se usa .update

from collections import defaultdict
# Usamos defaultdict para:
# * Generar keys automáticamente si agregamos y aún no están en el diccionario
# * Poder tratar un diccionario como si fuese otra estructura de datos (list o set)

def es_no_terminal(simbolo):
    return simbolo[0].isupper()

def es_terminal(simbolo):
    return simbolo.islower() and simbolo != 'lambda'

def es_lambda(simbolo):
    return simbolo == 'lambda'

#Recibe una gramática y genera un diccionario de la forma {antecedente:[(consecuente),(consecuente)],}
def generar_producciones(gramatica):
    reglas = gramatica.strip().split('\n')
    producciones = defaultdict(list)
    
    for regla in reglas:
        regla = regla.strip()
        antecedente, consecuente = regla.split(':')
        antecedente = antecedente.strip()
        consecuente = tuple(consecuente.strip().split())

        # Aprovechamos defaultdict y trabajamos un diccionario como una lista
        producciones[antecedente].append(consecuente)

    return producciones

# Calcula recursivamente los Firsts para cada NT
def generar_firsts_para_no_terminal(no_terminal, gramatica_procesada, firsts_por_nt):
    # Condicion de corte: los Firsts ya fueron calculados
    if no_terminal in firsts_por_nt and firsts_por_nt[no_terminal]:
        return firsts_por_nt[no_terminal]
    
    # Eliminamos duplicados metiendo los Firsts del NT en un set
    # TODO: ver si esto es necesario
    firsts_por_nt[no_terminal] = set()
    
    # Recorremos las reglas del NT
    for consecuente in gramatica_procesada[no_terminal]:
        for simbolo in consecuente:
            if es_terminal(simbolo):
                firsts_por_nt[no_terminal].add(simbolo)
                break
            elif es_no_terminal(simbolo):
                # Aplicamos la recursión
                first_value_nt = generar_firsts_para_no_terminal(simbolo, gramatica_procesada, firsts_por_nt)
                firsts_por_nt[no_terminal].update(first_value_nt)
                
                # Si en los Firsts del NT está lambda, seguimos buscando
                if 'lambda' not in first_value_nt:
                    break
            elif es_lambda(simbolo):
                firsts_por_nt[no_terminal].add('lambda')
                break
    
    return firsts_por_nt[no_terminal]

def generar_firsts(gramatica_procesada):
    firsts_por_nt = defaultdict(set)
    firsts_por_regla = defaultdict(list)

    # Generamos los Firsts por NT
    # TODO: sacar esta parte y que se encargue generar_firsts_por_no_terminal
    for antecedente in gramatica_procesada:
        for consecuente in gramatica_procesada[antecedente]:
            for simbolo in consecuente:
                if es_terminal(simbolo):
                    firsts_por_nt[antecedente].add(simbolo)
                    break
                elif es_no_terminal(simbolo):
                    first_value_nt = generar_firsts_para_no_terminal(simbolo, gramatica_procesada, firsts_por_nt)
                    firsts_por_nt[antecedente].update(first_value_nt)
                    if 'lambda' not in first_value_nt:
                        break
                elif es_lambda(simbolo):
                    firsts_por_nt[antecedente].add('lambda')
                    break

    # Generamos los Firsts por regla
    for antecedente in gramatica_procesada:
        for consecuente in gramatica_procesada[antecedente]:
            firsts = set()
            for simbolo in consecuente:
                if es_terminal(simbolo):
                    # TODO: por qué usa corchetes para simbolo?
                    # Regla 1: Si tengo una regla que deriva en un único terminal, ese terminal está en el conjunto de los firsts
                    # Regla 2.a: Si tengo una regla donde hay un terminal seguido de algo, ese terminal esta en el conjunto de los firsts
                    firsts.add(simbolo)
                    break
                elif es_no_terminal(simbolo):
                    # Regla 2.b: Los símbolos derivados de un NT que deriva de un NT, son del firsts del primer NT
                    # Por dicha regla agregamos los Firsts del NT, exceptuando 'lambda' (aún no sabemos si corresponde agregarlo)
                    firsts.update(firsts_por_nt[simbolo] - {'lambda'})
                    # Regla 3: Si todo A puede no venir, los firsts de B están incluidos en los firsts de S.
                    # En este caso, si lambda está en los firsts del NT, no cortamos y seguimos con más simbolos
                    if 'lambda' not in firsts_por_nt[simbolo]:
                        break
                else:
                    # Regla 4: Si existe la posibilidad de que todos los caminos deriven en lambda, entonces lambda está en los firsts
                    firsts.add('lambda')
            firsts_por_regla[antecedente].append((tuple(consecuente), firsts))
    
    return firsts_por_regla, firsts_por_nt

def generar_follows(gramatica_procesada, firsts_por_nt):
    follows = defaultdict(set)

    # TODO: modificar esto porque es rarisimo
    # Regla 1: El distinguido siempre tiene como follows al menos a '$'
    follows[next(iter(gramatica_procesada))].add('$')

    # La generación de los Follows termina cuando ya no hay cambios en iteraciones sucesivas
    cambios = True
    while cambios:
        cambios = False
        for antecedente in gramatica_procesada:
            for consecuente in gramatica_procesada[antecedente]:
                for indice, simbolo in enumerate(consecuente):
                    # Solo si es un NT aporta a la generación de los Follows
                    if es_no_terminal(simbolo):
                        # Si no es el último símbolo del consecuente (es decir: tiene algo a la derecha)
                        if indice + 1 < len(consecuente):
                            siguiente = consecuente[indice+1]
                            if es_terminal(siguiente):
                                # Si no lo añadi anteriormente, lo añado y aviso del cambio
                                if siguiente not in follows[simbolo]:
                                    follows[simbolo].add(siguiente)  
                                    cambios = True
                            
                            elif es_no_terminal(siguiente):
                                # Regla 2: Si un NT esta seguido de otro NT, los Firsts del último (menos lambda),
                                # pertenecen a los Follows del primero
                                firsts_siguiente = firsts_por_nt[siguiente]
                                firsts_siguiente_sin_lambda = firsts_siguiente - {'lambda'}

                                # Solo agrego dichos Firsts si no los agregué aún
                                if not firsts_siguiente_sin_lambda.issubset(follows[simbolo]): 
                                    follows[simbolo].update(firsts_siguiente_sin_lambda)
                                    cambios = True

                                # TODO: pero que pasa si despues del NT que estoy consultando tengo otro NT, no lo contempla
                                if 'lambda' in firsts_siguiente:
                                    # Regla 3: Si llegaste hasta el final y seguís con lambda, podes tomar como follows los follows de tu superior
                                    if not follows[antecedente].issubset(follows[simbolo]):
                                        follows[simbolo].update(follows[antecedente])
                                        cambios = True

                        # Si no tiene nada a la derecha
                        else:
                            # Regla 3: Si llegaste hasta el final y seguís con lambda, podes tomar como follows los follows de tu superior
                            if not follows[antecedente].issubset(follows[simbolo]):  
                                follows[simbolo].update(follows[antecedente])  
                                cambios = True
    return follows

def generar_select(gramatica_procesada, firsts_por_regla, follows_por_nt):
    # La estructura va a ser un defaultdict {A: [(consecuente, select), (consecuente, select)]}
    select = defaultdict(list)
    for antecedente in gramatica_procesada:
        for consecuente, firsts_consecuente in firsts_por_regla[antecedente]:
            #Por ahora los select de la regla van a ser los firsts del primer consecuente
            select_por_regla = set(firsts_consecuente)
            # TODO: mover esto dentro del if (solo se va a hacer si tiene lambda)
            select_por_regla.discard('lambda')
            # Si tenes lambda, te llevas tus Follows en lugar de lambda
            if 'lambda' in firsts_consecuente:
                select_por_regla.update(follows_por_nt[antecedente])
            select[antecedente].append((consecuente, select_por_regla))
    return select

class Gramatica:
    esLL1 = False
                        
    # Esta función debe implementar la lógica suficiente para que al imprimir en pantalla una instancia de este objeto
    # a la que se le haya invocado dicho método previamente se muestre la gramática de la siguiente manera:
    # por cada regla o producción mostrar dicha regla y a continuación los First, Follows y Selects correspondientes.
    def setear(self, gramatica):
        
        # TODO: si no tengo lambda en ningun first, no tiene sentido que calcule los follows

        return
    
    # Devuelve true en caso de que la cadena se derive de la gramática y false en caso contrario. 
    def evaluar_cadena(self, cadena):
        return
    
    # Funcion para imprimir la gramatica
    def __str__(self):
        resultado = ""
        for antecedente in self.producciones:
            for (consecuente, firsts_regla) in self.firsts[antecedente]:
                follows = self.follows[antecedente]
                # Tenemos que filtrar por el primer select encontrado porque la busqueda nos arroja una lista
                select_regla = [select_regla for regla, select_regla in self.select[antecedente] if regla == consecuente][0]
                resultado = resultado + f"{antecedente} : {' '.join(consecuente)} [{', '.join(firsts_regla)}] [{', '.join(follows)}] [{', '.join(select_regla)}]\n"
        return resultado
    