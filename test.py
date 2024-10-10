import pytest
from gramatica import Gramatica

# Una gramática LL(1) sin recursión a derecha
# Una gramática LL(1) con recursión a derecha
# Una gramática LL(1) que incluya lambda en sus derivaciones
# Una gramática LL(1) que no incluya lambda en sus derivaciones
# Una gramática LL(1) con reglas de producción innecesarias.
# Una gramática LL(1) con símbolos inaccesibles desde el axioma.
# Una gramática LL(1) con no terminales no generativos.
# Por cada uno de los incisos previos, una gramática que no sea LL(1).
# Una gramática no LL(1) con recursión a izquierda

# Hacemos un fixture dinámico
@pytest.fixture
def gramatica_fixture(request):
    g = Gramatica()
    g.setear(request.param)
    return g

# TODO: faltaría representar el atributo esLL1 en salida_esperada
class TestGramatica:
    @pytest.mark.parametrize("descripcion, gramatica_entrada, salida_esperada", (
        ("LL(1) sin recursión a derecha y sin lambda",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f",
            "A : b c [b] [$] [b] \n A : a b [a] [$] [a] \n A : d B [d] [$] [d] \n B : d e [d] [$] [d] \n B : f [f] [$] [f]"),
        ("NO LL(1) sin recursión a derecha y sin lambda",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f",
            "A : b c [b] [$] [b] \n A : a b [a] [$] [a] \n A : d B [d] [$] [d] \n A : a [a] [$] [a] \n B : d e [d] [$] [d] \n B : f [f] [$] [f]"),

        ("LL(1) con recursión a derecha", 
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n B : j B",
            "A : b c [b] [$] [b] \n A : a b [a] [$] [a] \n A : d B [d] [$] [d] \n B : d e [d] [$] [d] \n B : f [f] [$] [f] \n B : j B [j] [$] [j]"),
        ("NO LL(1) con recursión a derecha",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n B : j B",
            "A : b c [b] [$] [b] \n A : a b [a] [$] [a] \n A : d B [d] [$] [d] \n A : a [a] [$] [a] \n B : d e [d] [$] [d] \n B : f [f] [$] [f] \n B : j B [j] [$] [j]"),

        ("LL(1) con lambda en sus derivaciones",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n B : lambda",
            "A : b c [b] [$] [b] \n A : a b [a] [$] [a] \n A : d B [d] [$] [d] \n B : d e [d] [$] [d] \n B : f [f] [$] [f] \n B : lambda [lambda] [$] [$]"),
        ("NO LL(1) con lambda en sus derivaciones",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n B : lambda",
            "A : b c [b] [$] [b] \n A : a b [a] [$] [a] \n A : d B [d] [$] [d] \n A : a [a] [$] [a] \n B : d e [d] [$] [d] \n B : f [f] [$] [f] \n B : lambda [lambda] [$] [$]"),

        ("LL(1) con reglas innecesarias",
            "A : b c \n A : a b \n A : d B \n A : A \n B : d e \n B : f",
            "A : b c [b] [$] [b] \n A : a b [a] [$] [a] \n A : d B [d] [$] [d] \n B : d e [d] [$] [d] \n B : f [f] [$] [f]"),
        ("NO LL(1) con reglas innecesarias",
            "A : b c \n A : a b \n A : d B \n A : A \n A : a \n B : d e \n B : f",
            "A : b c [b] [$] [b] \n A : a b [a] [$] [a] \n A : d B [d] [$] [d] \n A : [a] [$] [a] \n B : d e [d] [$] [d] \n B : f [f] [$] [f]"),

        ("LL(1) con símbolos inaccesibles desde el axioma",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n C : j k",
            "A : b c [b] [$] [b] \n A : a b [a] [$] [a] \n A : d B [d] [$] [d] \n B : d e [d] [$] [d] \n B : f [f] [$] [f]"),         
        ("NO LL(1) con símbolos inaccesibles desde el axioma",
            "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n C : j k",
            "A : b c [b] [$] [b] \n A : a b [a] [$] [a] \n A : d B [d] [$] [d] \n A : [a] [$] [a] \n B : d e [d] [$] [d] \n B : f [f] [$] [f]"),

        ("LL(1) con no terminales no generativos",
            "A : d A \n A : b B \n A : a \n B : b B",    
            "A : d A [d] [$] [d] \n A : a [a] [$] [a]"),
        ("NO LL(1) con no terminales no generativos",
            "S : P Q \n S : a S b \n S : P \n S : R \n P : a P Q  \n P : a \n Q : Q b \n Q : lambda \n R : R b"
            "S : P Q [a] [b, $] [a] \n S : a S b [a] [b, $] [a] \n S : P [a] [b, $] [a] \n P : a P Q [a] [b, $] [a] \n P : a [a] [b, $] [a] \n Q : Q b [lambda] [b, $] [b, $] \n Q : lambda [lambda] [b, $] [b, $]"),

        ("No LL(1) con recursión a izquierda",
            "S : S a A \n S : b B \n A : a B \n A : c \n B : B b \n B : d",
            "S : S a A [b] [$, a] [b] \n S : b B [b] [$, a] [b] \n A : a B [a] [$, a] [a] \n A : c [c] [$, a] [c] \n B : B b [d] [$, a, b] [d] \n B : d [d] [$, a, b] [d]"),

        # Tomamos el mismo autómata que en LL(1) sin recursión a derecha
        ("Terminales y NO terminales con más de una letra",
            "Axiom : barb c \n Axiom : a barb \n Axiom : d B \n B : d e \n B : fuzz",
            "Axiom : barb c [barb] [$] [barb] \n Axiom : a barb [a] [$] [a] \n Axiom : d B [d] [$] [d] \n B : d e [d] [$] [d] \n B : fuzz [fuzz] [$] [fuzz]"),

    ), indirect=["gramatica_entrada"])  # Le pasamos reglas al fixture
    def test_setear(self, descripcion, salida_esperada):
        g = gramatica_fixture
        assert g.__str__() == salida_esperada, f"Error al setear gramática: {descripcion}"
    

    # Comentamos los tests de gramáticas NO LL(1) porque no debería poder evaluarse ninguna cadena en esos casos
    @pytest.mark.parametrize("descripcion, gramatica_entrada, cadena, pertenece", (
        ("LL(1) sin recursión a derecha y sin lambda",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f",
            "dde",
            True),
        ("LL(1) sin recursión a derecha y sin lambda",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f",
            "ddf",
            False),

        # ("NO LL(1) sin recursión a derecha y sin lambda",
        #     "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f",
        #     "bc",
        #     True),
        # ("NO LL(1) sin recursión a derecha y sin lambda",
        #     "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f",
        #     "cadena",
        #     False),

        ("LL(1) con recursión a derecha", 
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n B : j B",
            "djjjde",
            True),
        ("LL(1) con recursión a derecha", 
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n B : j B",
            "djjjdf",
            False),

        # ("NO LL(1) con recursión a derecha",
        #     "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n B : j B",
        #     "cadena",
        #     True),
        # ("NO LL(1) con recursión a derecha",
        #     "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n B : j B",
        #     "cadena",
        #     False),

        ("LL(1) con lambda en sus derivaciones",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n B : lambda",
            "dj",
            True),
        ("LL(1) con lambda en sus derivaciones",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n B : lambda",
            "de",
            False),

        # ("NO LL(1) con lambda en sus derivaciones",
        #     "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n B : lambda",
        #     "cadena",
        #     True),
        # ("NO LL(1) con lambda en sus derivaciones",
        #     "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n B : lambda",
        #     "cadena",
        #     False),

        ("LL(1) con reglas innecesarias",
            "A : b c \n A : a b \n A : d B \n A : A \n B : d e \n B : f",
            "dde",
            True),
        ("LL(1) con reglas innecesarias",
            "A : b c \n A : a b \n A : d B \n A : A \n B : d e \n B : f",
            "ddf",
            False),

        # ("NO LL(1) con reglas innecesarias",
        #     "A : b c \n A : a b \n A : d B \n A : A \n A : a \n B : d e \n B : f",
        #     "cadena",
        #     True),
        # ("NO LL(1) con reglas innecesarias",
        #     "A : b c \n A : a b \n A : d B \n A : A \n A : a \n B : d e \n B : f",
        #     "cadena",
        #     False),

        ("LL(1) con símbolos inaccesibles desde el axioma",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n C : j k",
            "bc",
            True),
        ("LL(1) con símbolos inaccesibles desde el axioma",
            "A : b c \n A : a b \n A : d B \n B : d e \n B : f \n C : j k",
            "be",
            False),

        # ("NO LL(1) con símbolos inaccesibles desde el axioma",
        #     "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n C : j k",
        #     "cadena",
        #     True),
        # ("NO LL(1) con símbolos inaccesibles desde el axioma",
        #     "A : b c \n A : a b \n A : d B \n A : a \n B : d e \n B : f \n C : j k",
        #     "cadena",
        #     False),

        ("LL(1) con no terminales no generativos",
            "A : d A \n A : b B \n A : a \n B : b B",    
            "dddddddda",
            True),
        ("LL(1) con no terminales no generativos",
            "A : d A \n A : b B \n A : a \n B : b B",    
            "ad",
            False),

        # ("NO LL(1) con no terminales no generativos",
        #     "S : P Q \n S : a S b \n S : P \n S : R \n P : a P Q  \n P : a \n Q : Q b \n Q : lambda \n R : R b",
        #     "cadena",
        #     True),
        # ("NO LL(1) con no terminales no generativos",
        #     "S : P Q \n S : a S b \n S : P \n S : R \n P : a P Q  \n P : a \n Q : Q b \n Q : lambda \n R : R b",
        #     "cadena",
        #     False),

        # ("No LL(1) con recursión a izquierda",
        #     "S : S a A \n S : b B \n A : a B \n A : c \n B : B b \n B : d",
        #     "cadena",
        #     True),
        # ("No LL(1) con recursión a izquierda",
        #     "S : S a A \n S : b B \n A : a B \n A : c \n B : B b \n B : d",
        #     "cadena",
        #     False),

        ("Terminales y NO terminales con más de una letra",
            "Axiom : barb c \n Axiom : a barb \n Axiom : d B \n B : d e \n B : fuzz",
            "d fuzz",
            True),
        ("Terminales y NO terminales con más de una letra",
            "Axiom : barb c \n Axiom : a barb \n Axiom : d B \n B : d e \n B : fuzz",
            "barb d",
            False),
    ), indirect=["gramatica_entrada"])  # Pass "reglas" to fixture again
    def test_evaluar_cadena(self, descripcion, cadena, pertenece):
        g = gramatica_fixture
        result = g.evaluar_cadena(cadena)
        assert result == pertenece, f"Error al evaluar cadena {cadena} con gramática {descripcion}"
