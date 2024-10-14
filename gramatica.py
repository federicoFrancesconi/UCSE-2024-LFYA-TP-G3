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


# Recibe una gramática y genera un diccionario de la forma {antecedente:[(consecuente),(consecuente)],}
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

    producciones_limpias = limpiar_producciones(producciones)
    return producciones_limpias


def limpiar_producciones(producciones):
    # Regla 1: Eliminar producciones innecesarias
    for antecedente in list(producciones.keys()):
        for consecuente in list(producciones[antecedente]):
            if len(consecuente) == 1 and antecedente == consecuente[0]:
                producciones[antecedente].remove(consecuente)


    return producciones


# Calcula recursivamente los Firsts para cada NT
def generar_firsts_para_no_terminal(no_terminal, gramatica_procesada, firsts_por_nt):
    # Condicion de corte: los Firsts del NT ya fueron calculados
    if no_terminal in firsts_por_nt and firsts_por_nt[no_terminal]:
        return firsts_por_nt[no_terminal]

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

    # Regla 1: El distinguido siempre tiene como follows al menos a '$'
    distinguido = list(gramatica_procesada.keys())[0]
    follows[distinguido].add('$')

    # La generación de los Follows termina cuando ya no hay cambios en iteraciones sucesivas
    cambios = True
    while cambios:
        cambios = False
        # Recorremos todos los consecuentes buscando apariciones de NTs
        for antecedente in gramatica_procesada:
            for consecuente in gramatica_procesada[antecedente]:
                for indice_inicial, simbolo in enumerate(consecuente):
                    # Solo si es un NT aporta a la generación de los Follows
                    if es_no_terminal(simbolo):
                        # Mientras siga habiendo lambda en los Follows, seguimos buscando
                        hay_lambda = True
                        indice_siguiente = indice_inicial
                        while hay_lambda:
                            # Si no es el último símbolo del consecuente (tiene algo a la derecha)
                            if indice_siguiente + 1 < len(consecuente):
                                indice_siguiente += 1
                                siguiente = consecuente[indice_siguiente]
                                if es_terminal(siguiente):
                                    # Si no lo añadi anteriormente, lo añado y aviso del cambio
                                    if siguiente not in follows[simbolo]:
                                        follows[simbolo].add(siguiente)
                                        cambios = True
                                    hay_lambda = False

                                elif es_no_terminal(siguiente):
                                    # Regla 2: Si un NT esta seguido de otro NT, los Firsts del segundo (menos lambda),
                                    # pertenecen a los Follows del primero
                                    firsts_siguiente = firsts_por_nt[siguiente]
                                    firsts_siguiente_sin_lambda = firsts_siguiente - {'lambda'}

                                    # Solo agrego dichos Firsts si no los agregué aún
                                    if not firsts_siguiente_sin_lambda.issubset(follows[simbolo]):
                                        follows[simbolo].update(firsts_siguiente_sin_lambda)
                                        cambios = True

                                    hay_lambda = 'lambda' in firsts_siguiente
                            # Si no tiene nada a la derecha
                            else:
                                # Regla 3: Si llegaste hasta el final y seguís con lambda, podes tomar como follows los follows de tu superior
                                if not follows[antecedente].issubset(follows[simbolo]):
                                    follows[simbolo].update(follows[antecedente])
                                    cambios = True
                                hay_lambda = False

    # Ordenamos los Follows para que la salida sea deterministica (sino cambia con cada ejecución)
    follows_ordenados = {}
    for no_terminal, follows_del_nt in follows.items():
        follows_ordenados[no_terminal] = sorted(follows_del_nt)

    return follows_ordenados
def generar_select(gramatica_procesada, firsts, follows):
    # La estructura va a ser un defaultdict {A: [(consecuente, select), (consecuente, select)]}
    select = defaultdict(list)
    for antecedente in gramatica_procesada:
        for consecuente, firsts_consecuente in firsts[antecedente]:
            # Por ahora los select de la regla van a ser los firsts del primer consecuente
            select_por_regla = set(firsts_consecuente)
            # Si tenes lambda, te llevas tus Follows en lugar de lambda
            if 'lambda' in firsts_consecuente:
                select_por_regla.discard('lambda')
                select_por_regla.update(follows[antecedente])
            select[antecedente].append((consecuente, select_por_regla))
    return select

class Gramatica:
    esLL1 = True
    producciones = defaultdict(list)
    firsts = defaultdict(list)
    follows = defaultdict(set)
    select = defaultdict(list)

    # Esta función debe implementar la lógica suficiente para que al imprimir en pantalla una instancia de este objeto
    # a la que se le haya invocado dicho método previamente se muestre la gramática de la siguiente manera:
    # por cada regla o producción mostrar dicha regla y a continuación los First, Follows y Selects correspondientes.
    def setear(self, gramatica):
        self.producciones = generar_producciones(gramatica)

        self.firsts, firsts_por_nt = generar_firsts(self.producciones)

        self.follows = generar_follows(self.producciones, firsts_por_nt)

        self.select = generar_select(self.producciones, self.firsts, self.follows)

        # Chequear si es gramatica ambigua:
        for antecedente in self.select:
            select_simbolos = set()
            for (consecuente, selects_produccion) in self.select[antecedente]:
                if not select_simbolos.isdisjoint(selects_produccion):
                    self.esLL1 = False
                    return
                select_simbolos.update(selects_produccion)

    # Devuelve true en caso de que la cadena se derive de la gramática y false en caso contrario. 
    def evaluar_cadena(self, cadena):
        # Para poder tomar terminales que involucren múltiples caracteres, tenemos que pasarlos con espacio (' ') entre ellos
        cadena = cadena.split()

        # Si la gramática no es LL1, no puedo evaluar la cadena
        if self.esLL1 is False:
            return None

        # Genero una tabla donde los terminales sean las columnas y los no terminales las filas
        tabla = {}
        for antecedente in self.producciones:
            for consecuente, select in self.select[antecedente]:
                for simbolo in select:
                    # Relleno las celdas con los consecuentes de las reglas donde el NT sea el antecedente y el terminal este en los selects
                    tabla[(antecedente, simbolo)] = consecuente

        no_terminales = list(self.producciones.keys())
        distinguido = no_terminales[0]
        stack = [distinguido]

        indice = 0
        look = cadena[indice]
        while stack:
            s = stack.pop()
            if s in no_terminales:
                l = tabla.get((s, look))
                # Si no se esperaba el símbolo de la entrada, la cadena no pertenece a la gramática
                if l is None:
                    print(f"Error: no se esperaba {look} a la entrada")
                    return False
                l = l[::-1]
                stack.extend(l)
            elif s == look:
                indice += 1
                if indice < len(cadena):
                    look = cadena[indice]
                else:
                    break
            else:
                print('Error')

        # Si look termina en '$' la cadena pertenece a la gramática, sino no
        return look == '$'

    # Funcion para imprimir la gramatica
    def __str__(self):
        resultado = ""
        for antecedente in self.producciones:
            for (consecuente, firsts_regla) in self.firsts[antecedente]:
                follows = self.follows[antecedente]
                # Tenemos que filtrar por el primer select encontrado porque la busqueda nos arroja una lista
                select_regla =[select_regla for regla, select_regla in self.select[antecedente] if regla == consecuente][0]
                resultado = resultado + f"{antecedente} : {' '.join(consecuente)} [{', '.join(firsts_regla)}] [{', '.join(follows)}] [{', '.join(select_regla)}]\n"
        return resultado
