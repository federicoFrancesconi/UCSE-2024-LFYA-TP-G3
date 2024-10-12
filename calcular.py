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

def generar_first_para_no_terminal(no_terminal, gramatica_procesada, firsts_por_nt):
    if no_terminal in firsts_por_nt and firsts_por_nt[no_terminal]:
        return firsts_por_nt[no_terminal]
    
    firsts_por_nt[no_terminal] = set()
    
    for consecuente in gramatica_procesada[no_terminal]:
        for value in consecuente:
            if value.islower() and value != 'lambda':
                firsts_por_nt[no_terminal].add(value)
                break
            elif value.isupper():
                first_value_nt = generar_first_para_no_terminal(value, gramatica_procesada, firsts_por_nt)
                firsts_por_nt[no_terminal].update(first_value_nt)
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
            firsts = set()
            for value in consecuente:
                if value.islower() and value != 'lambda':
                    firsts.add(value)
                    break
                elif value.isupper():
                    firsts.update(firsts_por_nt[value] - {'lambda'})
                    if 'lambda' not in firsts_por_nt[value]:
                        break
            else:
                firsts.add('lambda')
            firsts_por_regla[antecedente].append((tuple(consecuente), firsts))
    
    return firsts_por_regla, firsts_por_nt

def generar_follows(gramatica_procesada, firsts_por_nt):
    follows = defaultdict(set)
    cambios = True
    follows[next(iter(gramatica_procesada))].add('$')  # Símbolo de fin de entrada en el símbolo inicial

    while cambios:
        cambios = False
        for antecedente in gramatica_procesada:
            for consecuente in gramatica_procesada[antecedente]:
                for indice,caracter in enumerate(consecuente):
                    if caracter.isupper():
                        if indice + 1 < len(consecuente):
                            siguiente = consecuente[indice+1]
                            if siguiente.islower():
                                if siguiente not in follows[caracter]:
                                    follows[caracter].add(siguiente)
                                    cambios = True
                            elif siguiente.isupper():
                                first_siguiente = firsts_por_nt[siguiente] - {'lambda'}
                                if not first_siguiente.issubset(follows[caracter]):
                                    follows[caracter].update(first_siguiente)
                                    cambios = True
                                if 'lambda' in firsts_por_nt[siguiente]:
                                    if not follows[antecedente].issubset(follows[caracter]):
                                        follows[caracter].update(follows[antecedente])
                                        cambios = True
                        else:
                            if not follows[antecedente].issubset(follows[caracter]):
                                follows[caracter].update(follows[antecedente])
                                cambios = True
    return follows

def generar_select(gramatica_procesada, firsts_por_regla, follows_por_nt):
    select = defaultdict(list)

    for antecedente in gramatica_procesada:
        for consecuente, first_consecuente in firsts_por_regla[antecedente]:
            select_regla = set(first_consecuente)  # Comienza con el conjunto de firsts
            select_regla.discard('lambda')  # Asegurarse de que lambda NO esté en el select
            
            if 'lambda' in first_consecuente:
                select_regla.update(follows_por_nt[antecedente])  # Agrega los follows si lambda está en los firsts
            
            select[antecedente].append((consecuente, select_regla))
    
    return select


if __name__ == "__main__":
    gramaticaejemplo = "A : b A \n A : a \n A : A B c \n A : lambda \n B : b"
    
    producciones = generar_producciones(gramaticaejemplo)
    
    firsts_por_regla, firsts_por_nt = generar_firsts_por_regla(producciones)
    
    follows_por_nt = generar_follows(producciones, firsts_por_nt)
    
    select = generar_select(producciones, firsts_por_regla, follows_por_nt)

    for antecedente in producciones:
        for (consecuente, first_consecuente) in firsts_por_regla[antecedente]:
            follow_antecedente = follows_por_nt[antecedente]
            select_consecuente = [regla for regla, select_regla in select[antecedente] if regla == consecuente][0]
            select_regla = [select_regla for regla, select_regla in select[antecedente] if regla == consecuente][0]
            print(f"{antecedente} : {' '.join(consecuente)} {{ {', '.join(first_consecuente)} }} {{ {', '.join(follow_antecedente)} }} {{ {', '.join(select_regla)} }}")
