# UCSE-2024-LFYA-TP-G3

### Integrantes
* Francesconi, Federico.
* Inwinkelried, Santiago.
* Schillino, Facundo.

### Descripción del Proyecto

Desarrollar un programa que cree un parser LL(1) a partir de una gramática dada por el usuario, con el fin de verificar si una cadena forma parte del lenguaje que define dicha gramática. 

El programa debe implementar la clase `Gramatica` en Python, que cuente con los siguientes métodos:

#### 1) `setear(string)`
Esta función debe implementar la lógica suficiente para que, al imprimir en pantalla una instancia de este objeto a la que se le haya invocado dicho método previamente, se muestre la gramática de la siguiente manera: por cada regla o producción, mostrar dicha regla junto con sus First, Follows y Selects correspondientes. 

Además, el objeto debe poseer un campo `EsLL1` de tipo booleano, que indique si la gramática puede reconocerse o no mediante esta técnica.

#### 2) `evaluar_cadena(string)`
Este método debe devolver `True` si la cadena se deriva de la gramática, y `False` en caso contrario.

### Test y Casos de Prueba

Para el módulo mencionado previamente, se deben implementar tests que validen el correcto funcionamiento del mismo. Los tests deben incluir al menos los siguientes casos:

- Una gramática LL(1) sin recursión a derecha.
- Una gramática LL(1) con recursión a derecha.
- Una gramática LL(1) que incluya lambda en sus derivaciones.
- Una gramática LL(1) que no incluya lambda en sus derivaciones.
- Una gramática LL(1) con reglas de producción innecesarias.
- Una gramática LL(1) con símbolos inaccesibles desde el axioma.
- Una gramática LL(1) con no terminales no generativos.
- Para cada uno de los incisos anteriores, una gramática que no sea LL(1).
- Una gramática no LL(1) con recursión a izquierda.

### Consideraciones

El programa debe ser capaz de detectar y resolver:
- Reglas de producción innecesarias.
- Símbolos inaccesibles desde el axioma.
- No terminales no generativos.

#### Detalles importantes:
- Se considera **no terminal** a cualquier palabra que comience con letra mayúscula.
- Terminales y no terminales pueden contener más de una letra.
- El símbolo “:`” y la palabra `lambda` son reservadas.
- El antecedente de la primera regla de la gramática es el no terminal distinguido.
- Las producciones se separan con `\n`, el antecedente del consecuente con `:` y los elementos del consecuente con espacio/s.

<img width="649" alt="Captura de pantalla 2024-10-13 a la(s) 11 16 05 p  m" src="https://github.com/user-attachments/assets/09914648-e7c1-461e-b00e-fd23bf25b3a1">

