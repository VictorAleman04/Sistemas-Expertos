def convertir_a_clausula_horn(oracion):
    # Separar la oración en fragmentos usando " y "
    fragmentos = oracion.split(" y ")
    
    # Crear una lista para los fragmentos negados excepto el último
    clausula_horn = [
        f"no {fragmento.strip()}" if not fragmento.strip().startswith("no ") else fragmento.strip()
        for fragmento in fragmentos[:-1]
    ]
    
    # Agregar el último fragmento sin negación
    ultimo_fragmento = fragmentos[-1].strip()
    clausula_horn.append(ultimo_fragmento[3:] if ultimo_fragmento.startswith("no ") else ultimo_fragmento)

    # Unir los fragmentos con " o "
    return " o ".join(clausula_horn)

def procesar_archivo():
    # Leer el archivo de entrada
    try:
        with open("oraciones.txt", 'r', encoding='utf-8') as archivo_entrada:
            oraciones = [linea.strip() for linea in archivo_entrada if linea.strip()]
    except FileNotFoundError:
        print("El archivo oraciones.txt no fue encontrado.")
        return

    # Procesar y guardar en el archivo de salida
    with open("oraciones_horn.txt", 'w', encoding='utf-8') as archivo_salida:
        for oracion in oraciones:
            # Convertir a cláusula de Horn
            oracion_horn = convertir_a_clausula_horn(oracion)
            
            # Imprimir la oración antes y después de la conversión
            print(f"Original: {oracion}")
            print(f"Convertida a cláusula de Horn: {oracion_horn}\n")

            # Guardar en el archivo de salida
            archivo_salida.write(f"{oracion_horn}\n\n")

    print("Conversiones guardadas en oraciones_horn.txt.")

# Ejecutar el proceso
procesar_archivo()
