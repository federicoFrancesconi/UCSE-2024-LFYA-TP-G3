import pytest
from gramatica import Gramatica

# ---- Tests requeridos por la cátedra: ----
# Una gramática LL(1) sin recursión a derecha
# Una gramática LL(1) con recursión a derecha
# Una gramática LL(1) que incluya lambda en sus derivaciones
# Una gramática LL(1) que no incluya lambda en sus derivaciones
# Una gramática LL(1) con reglas de producción innecesarias.
# Una gramática LL(1) con símbolos inaccesibles desde el axioma.
# Una gramática LL(1) con no terminales no generativos.
# Por cada uno de los incisos previos, una gramática que no sea LL(1).
# Una gramática no LL(1) con recursión a izquierda

class TestGramatica:
    @pytest.mark.parametrize("descripcion, gramatica_entrada, salida_esperada", (
        ("LL(1) sin recursión a derecha y sin lambda",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f",
            "A : b c [b] [$] [b]\nA : a b [a] [$] [a]\nA : d B [d] [$] [d]\nB : d e [d] [$] [d]\nB : f [f] [$] [f]\n"),
        ("NO LL(1) sin recursión a derecha y sin lambda",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f",
            "A : b c [b] [$] [b]\nA : a b [a] [$] [a]\nA : d B [d] [$] [d]\nA : a [a] [$] [a]\nB : d e [d] [$] [d]\nB : f [f] [$] [f]\n"),

        ("LL(1) con recursión a derecha", 
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n B : j B",
            "A : b c [b] [$] [b]\nA : a b [a] [$] [a]\nA : d B [d] [$] [d]\nB : d e [d] [$] [d]\nB : f [f] [$] [f]\nB : j B [j] [$] [j]\n"),
        ("NO LL(1) con recursión a derecha",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n B : j B",
            "A : b c [b] [$] [b]\nA : a b [a] [$] [a]\nA : d B [d] [$] [d]\nA : a [a] [$] [a]\nB : d e [d] [$] [d]\nB : f [f] [$] [f]\nB : j B [j] [$] [j]\n"),

        ("LL(1) con lambda en sus derivaciones",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n B : lambda",
            "A : b c [b] [$] [b]\nA : a b [a] [$] [a]\nA : d B [d] [$] [d]\nB : d e [d] [$] [d]\nB : f [f] [$] [f]\nB : lambda [lambda] [$] [$]\n"),
        ("NO LL(1) con lambda en sus derivaciones",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n B : lambda",
            "A : b c [b] [$] [b]\nA : a b [a] [$] [a]\nA : d B [d] [$] [d]\nA : a [a] [$] [a]\nB : d e [d] [$] [d]\nB : f [f] [$] [f]\nB : lambda [lambda] [$] [$]\n"),

        ("LL(1) con reglas innecesarias",
            "A : b c \n A : a b \n A : d B \n A : A \n B : d e \n B : f",
            "A : b c [b] [$] [b]\nA : a b [a] [$] [a]\nA : d B [d] [$] [d]\nB : d e [d] [$] [d]\nB : f [f] [$] [f]"),
        ("NO LL(1) con reglas innecesarias",
            "A : b c \n A : a b \n A : d B \n A : A \n A : a \n B : d e \n B : f",
            "A : b c [b] [$] [b]\nA : a b [a] [$] [a]\nA : d B [d] [$] [d]\nA : [a] [$] [a]\nB : d e [d] [$] [d]\nB : f [f] [$] [f]\n"),

        ("LL(1) con símbolos inaccesibles desde el axioma",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n C : j k",
            "A : b c [b] [$] [b]\nA : a b [a] [$] [a]\nA : d B [d] [$] [d]\nB : d e [d] [$] [d]\nB : f [f] [$] [f]\n"),         
        ("NO LL(1) con símbolos inaccesibles desde el axioma",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n C : j k",
            "A : b c [b] [$] [b]\nA : a b [a] [$] [a]\nA : d B [d] [$] [d]\nA : [a] [$] [a]\nB : d e [d] [$] [d]\nB : f [f] [$] [f]\n"),

        ("LL(1) con no terminales no generativos",
            "A : d A \n A : b B \n A : a \n B : b B",    
            "A : d A [d] [$] [d]\nA : a [a] [$] [a]\n"),
        ("NO LL(1) con no terminales no generativos",
            "S : P Q \n S : a S b \n S : P \n S : R \n P : a P Q  \n P : a \n Q : Q b \n Q : lambda \n R : R b",
            "S : P Q [a] [$, b] [a]\nS : a S b [a] [$, b] [a]\nS : P [a] [$, b] [a]\nP : a P Q [a] [$, b] [a]\nP : a [a] [$, b] [a]\nQ : Q b [lambda] [$, b] [$, b]\nQ : lambda [lambda] [$, b] [$, b]\n"),

        ("No LL(1) con recursión a izquierda",
            "S : S a A \n S : b B \n A : a B \n A : c \n B : B b \n B : d",
            "S : S a A [b] [$, a] [b]\nS : b B [b] [$, a] [b]\nA : a B [a] [$, a] [a]\nA : c [c] [$, a] [c]\nB : B b [d] [$, a, b] [d]\nB : d [d] [$, a, b] [d]\n"),

        # Tomamos el mismo autómata que en LL(1) sin recursión a derecha
        ("Terminales y NO terminales con más de una letra",
            "Axiom : barb c \n Axiom : a barb \n Axiom : d B \n B : d e \n B : fuzz",
            "Axiom : barb c [barb] [$] [barb]\nAxiom : a barb [a] [$] [a]\nAxiom : d B [d] [$] [d]\nB : d e [d] [$] [d]\nB : fuzz [fuzz] [$] [fuzz]\n"),

        ("NT con lambda en sus derivaciones sucesivos",
            "S : A B C \n A : a \n B : b \n B : lambda \n C : c \n C : lambda",
            "S : A B C [a] [$] [a]\nA : a [a] [$, b, c] [a]\nB : b [b] [$, c] [b]\nB : lambda [lambda] [$, c] [$, c]\nC : c [c] [$] [c]\nC : lambda [lambda] [$] [$]\n"),
    ))
    def test_setear(self, descripcion, gramatica_entrada, salida_esperada):
        g = Gramatica()
        g.setear(gramatica_entrada)
        assert g.__str__() == salida_esperada, f"Error al setear gramática: {descripcion}"
    

    @pytest.mark.parametrize("descripcion, gramatica_entrada, cadena, pertenece", (
        ("LL(1) sin recursión a derecha y sin lambda",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f",
            "d d e $",
            True),
        ("LL(1) sin recursión a derecha y sin lambda",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f",
            "d d f $",
            False),

        ("LL(1) con recursión a derecha", 
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n B : j B",
            "d j j j d e $",
            True),
        ("LL(1) con recursión a derecha", 
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n B : j B",
            "d j j j d f $",
            False),

        ("LL(1) con lambda en sus derivaciones",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n B : lambda",
            "d j $",
            True),
        ("LL(1) con lambda en sus derivaciones",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n B : lambda",
            "d e $",
            False),

        ("LL(1) con reglas innecesarias",
            "A : b c \n A : a b \n A : d B \n A : A \n B : d e \n B : f",
            "d d e $",
            True),
        ("LL(1) con reglas innecesarias",
            "A : b c \n A : a b \n A : d B \n A : A \n B : d e \n B : f",
            "d d f $",
            False),

        ("LL(1) con símbolos inaccesibles desde el axioma",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n C : j k",
            "b c $",
            True),
        ("LL(1) con símbolos inaccesibles desde el axioma",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n C : j k",
            "b e $",
            False),

        ("LL(1) con no terminales no generativos",
            "A : d A \n A : b B \n A : a \n B : b B",    
            "d d d d d d d d a $",
            True),
        ("LL(1) con no terminales no generativos",
            "A : d A \n A : b B \n A : a \n B : b B",    
            "a d $",
            False),

        ("Terminales y NO terminales con más de una letra",
            "Axiom : barb c \n Axiom : a barb \n Axiom : d B \n B : d e \n B : fuzz",
            "d fuzz $",
            True),
        ("Terminales y NO terminales con más de una letra",
            "Axiom : barb c \n Axiom : a barb \n Axiom : d B \n B : d e \n B : fuzz",
            "barb d $",
            False),
    ))
    def test_evaluar_cadena_ll1(self, descripcion, gramatica_entrada, cadena, pertenece):
        g = Gramatica()
        g.setear(gramatica_entrada)
        result = g.evaluar_cadena(cadena)
        assert result == pertenece, f"Error al evaluar cadena {cadena} con gramática {descripcion}"


    @pytest.mark.parametrize("descripcion, gramatica_entrada, cadena, pertenece", (
        ("NO LL(1) sin recursión a derecha y sin lambda",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f",
            "bc",
            None),
        ("NO LL(1) sin recursión a derecha y sin lambda",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f",
            "cadena",
            None),

        ("NO LL(1) con recursión a derecha",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n B : j B",
            "cadena",
            None),
        ("NO LL(1) con recursión a derecha",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n B : j B",
            "cadena",
            None),

        ("NO LL(1) con lambda en sus derivaciones",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n B : lambda",
            "cadena",
            None),
        ("NO LL(1) con lambda en sus derivaciones",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n B : lambda",
            "cadena",
            None),

        ("NO LL(1) con reglas innecesarias",
            "A : b c \n A : a b \n A : d B \n A : A \n A : a \n B : d e \n B : f",
            "cadena",
            None),
        ("NO LL(1) con reglas innecesarias",
            "A : b c \n A : a b \n A : d B \n A : A \n A : a \n B : d e \n B : f",
            "cadena",
            None),

        ("NO LL(1) con símbolos inaccesibles desde el axioma",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n C : j k",
            "cadena",
            None),
        ("NO LL(1) con símbolos inaccesibles desde el axioma",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n C : j k",
            "cadena",
            None),

        ("NO LL(1) con no terminales no generativos",
            "S : P Q \n S : a S b \n S : P \n S : R \n P : a P Q  \n P : a \n Q : Q b \n Q : lambda \n R : R b",
            "cadena",
            None),
        ("NO LL(1) con no terminales no generativos",
            "S : P Q \n S : a S b \n S : P \n S : R \n P : a P Q  \n P : a \n Q : Q b \n Q : lambda \n R : R b",
            "cadena",
            None),

        ("No LL(1) con recursión a izquierda",
            "S : S a A \n S : b B \n A : a B \n A : c \n B : B b \n B : d",
            "cadena",
            None),
        ("No LL(1) con recursión a izquierda",
            "S : S a A \n S : b B \n A : a B \n A : c \n B : B b \n B : d",
            "cadena",
            None),
    ))
    def test_evaluar_cadena_no_ll1(self, descripcion, gramatica_entrada, cadena, pertenece):
        g = Gramatica()
        g.setear(gramatica_entrada)
        result = g.evaluar_cadena(cadena)
        assert result == pertenece, f"Error al evaluar cadena {cadena} con gramática {descripcion}"
