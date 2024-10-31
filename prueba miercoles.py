import re
import pickle
from itertools import product

proposiciones_guardadas = {}

def cargar_proposiciones():
    global proposiciones_guardadas
    try:
        with open('proposiciones.pkl', 'rb') as file:
            proposiciones_guardadas = pickle.load(file)
            print("Proposiciones cargadas correctamente.")
    except (FileNotFoundError, EOFError):
        print("No se encontraron proposiciones guardadas, se empezará desde cero.")

def guardar_proposiciones():
    with open('proposiciones.pkl', 'wb') as file:
        pickle.dump(proposiciones_guardadas, file)
        print("Proposiciones guardadas correctamente.")

def guardar_proposiciones_txt():
    with open('proposiciones.txt', 'w', encoding='utf-8') as file:
        for letra, proposicion in proposiciones_guardadas.items():
            file.write(f"{letra}: {proposicion}\n")
    print("Proposiciones guardadas en proposiciones.txt correctamente.")

def identificar_proposiciones(oracion):
    operadores = {
        " y ": "∧",
        " o ": "∨",
        "no ": "¬",
        " pero ": "∧",
        " además, ": "∧",
        " Además, ": "∧",
        ", ": "∧"
    }

    for conector, simbolo in operadores.items():
        oracion = oracion.replace(conector, simbolo)

    proposiciones_simples = re.split(r'[∧∨]', oracion)
    operadores_encontrados = re.findall(r'[∧∨]', oracion)
    
    letras = []
    for i, prop in enumerate(proposiciones_simples):
        prop = prop.strip()
        if '¬' in prop:
            letras.append('¬' + chr(65 + i))
            proposiciones_guardadas[f'¬{chr(65 + i)}'] = prop.replace('¬', 'no ')
        else:
            letras.append(chr(65 + i))
            proposiciones_guardadas[chr(65 + i)] = prop

    nueva_oracion = ""
    for i in range(len(letras)):
        nueva_oracion += letras[i]
        if i < len(operadores_encontrados):
            nueva_oracion += operadores_encontrados[i]
    
    return nueva_oracion, letras

def evaluar_franqueza(frase, valores):
    for letra, valor in valores.items():
        frase = frase.replace(letra, str(valor))
    # Evalúa la expresión lógica
    return eval(frase.replace('∧', ' and ').replace('∨', ' or ').replace('¬', ' not '))

def generar_tabla_verdad(frase):
    letras_unicas = sorted(set(filter(lambda c: c.isalpha(), frase)))
    combinaciones = list(product([True, False], repeat=len(letras_unicas)))
    
    print("\nTabla de Verdad:")
    print(" | ".join(letras_unicas) + " | Resultado |")
    print("-" * (len(letras_unicas) * 4 + 12))
    
    for combinacion in combinaciones:
        valores = dict(zip(letras_unicas, combinacion))
        resultado = evaluar_franqueza(frase, valores)
        print(" | ".join(str(int(valores[l])) for l in letras_unicas) + f" | {int(resultado)} |")

def revisar_proposiciones():
    print("Proposiciones guardadas:")
    for letra, proposicion in proposiciones_guardadas.items():
        print(f"{letra}: {proposicion}")

# Cargar proposiciones al inicio
cargar_proposiciones()

# Ejemplo de uso de la función
oracion = input("Por favor, ingresa una proposición: ")
frase_con_cambios, letras = identificar_proposiciones(oracion)

print("Frase con cambios:", frase_con_cambios)
print("Frases sustituidas por letras:", letras)

# Generar la tabla de verdad
generar_tabla_verdad(frase_con_cambios)

# Revisar y mostrar proposiciones guardadas
revisar_proposiciones()

# Guardar proposiciones después de cada ejecución
guardar_proposiciones()
guardar_proposiciones_txt()
