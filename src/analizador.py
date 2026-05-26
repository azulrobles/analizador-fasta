import argparse
import sys


def parsear_argumentos():
    """Leer opciones de línea de comandos"""
    parser = argparse.ArgumentParser(
        description="Analiza secuencias FASTA y filtra por criterios GC y longitud"
    )
    parser.add_argument(
        "-i",
        "--input",
        default="data/ejemplo.fasta",
        help="Ruta del archivo FASTA a analizar",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="resultados.tsv",
        help="Archivo de salida TSV (default: resultados.tsv)",
    )
    parser.add_argument(
        "--min-len",
        type=int,
        default=0,
        help="Longitud mínima de secuencia (default: 0)",
    )
    parser.add_argument(
        "--max-len",
        type=int,
        default=float("inf"),
        help="Longitud máxima de secuencia (default: sin límite)",
    )
    parser.add_argument(
        "--min-gc", type=float, default=0, help="Contenido GC mínimo en % (default: 0)"
    )
    parser.add_argument(
        "--max-gc",
        type=float,
        default=100,
        help="Contenido GC máximo en % (default: 100)",
    )

    return parser.parse_args()


def leer_fasta(ruta):
    """
    Leer el archivo FASTA y devolver secuencias

    Args:
        ruta: Ruta del archivo FASTA

    Returns:
        tupla: (encabezado, secuencia)
    """
    encabezado_actual = None
    secuencia_actual = ""

    try:
        with open(ruta, "r") as archivo:
            for linea in archivo:
                linea = linea.strip()

                # Saltar líneas vacías
                if not linea:
                    continue

                # Si la línea comienza con ">", es un encabezado
                if linea.startswith(">"):
                    # Guardar la secuencia anterior si existe
                    if encabezado_actual is not None and secuencia_actual != "":
                        yield (encabezado_actual, secuencia_actual)

                    # Actualizar encabezado y reiniciar secuencia
                    encabezado_actual = linea[1:]  # Quitar el ">"
                    secuencia_actual = ""
                else:
                    # Acumular la secuencia
                    secuencia_actual += linea

            # Guardar la última secuencia si existe
            if encabezado_actual is not None and secuencia_actual != "":
                yield (encabezado_actual, secuencia_actual)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta}'", file=sys.stderr)
        sys.exit(1)


def calcular_gc(secuencia):
    """
    Calcular el contenido GC

    Args:
        secuencia: Cadena de ADN (solo A, T, G, C)

    Returns:
        float: Porcentaje de GC (0-100)
    """
    secuencia_upper = secuencia.upper()
    longitud = len(secuencia_upper)

    if longitud == 0:
        return 0

    g_count = secuencia_upper.count("G")
    c_count = secuencia_upper.count("C")
    gc_count = g_count + c_count

    return (gc_count / longitud) * 100


def calcular_estadisticas(encabezado, secuencia):
    """
    Calcular longitud y GC para una secuencia

    Args:
        encabezado: Identificador de la secuencia
        secuencia: Cadena de ADN

    Returns:
        dict: Diccionario con estadísticas
    """
    longitud = len(secuencia)
    gc_porcentaje = calcular_gc(secuencia)

    # Contar G y C individuales
    secuencia_upper = secuencia.upper()
    g_count = secuencia_upper.count("G")
    c_count = secuencia_upper.count("C")
    gc_count = g_count + c_count

    return {
        "encabezado": encabezado,
        "secuencia": secuencia,
        "longitud": longitud,
        "g_count": g_count,
        "c_count": c_count,
        "gc_count": gc_count,
        "gc_porcentaje": gc_porcentaje,
    }


def pasa_filtros(stats, args):
    """
    Decidir si una secuencia pasa los filtros

    Args:
        stats: Diccionario con estadísticas de la secuencia
        args: Argumentos de línea de comandos

    Returns:
        bool: True si pasa todos los filtros
    """
    longitud = stats["longitud"]
    gc = stats["gc_porcentaje"]

    # Verificar filtros
    if longitud < args.min_len:
        return False
    if longitud > args.max_len:
        return False
    if gc < args.min_gc:
        return False
    if gc > args.max_gc:
        return False

    return True


def escribir_resultados(secuencias_filtradas, ruta):
    """
    Guardar resultados en TSV

    Args:
        secuencias_filtradas: Lista de diccionarios con estadísticas
        ruta: Ruta del archivo de salida
    """
    try:
        with open(ruta, "w") as archivo:
            # Encabezado simplificado
            archivo.write("Encabezado\tLongitud\tGC%\n")

            for stats in secuencias_filtradas:
                linea = (
                    f"{stats['encabezado']}\t"
                    f"{stats['longitud']}\t"
                    f"{stats['gc_porcentaje']:.2f}\n"
                )
                archivo.write(linea)

        print(f"Resultados guardados en: {ruta}")

    except IOError as e:
        print(f"Error al escribir el archivo '{ruta}': {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """
    Coordinar el análisis completo de secuencias FASTA.

    1. Parsea argumentos de línea de comandos
    2. Lee secuencias del archivo FASTA
    3. Calcula estadísticas para cada secuencia
    4. Filtra secuencias según los criterios especificados
    5. Guarda resultados filtrados en archivo TSV

    Returns:
        None (sale con código 0 en caso de éxito, 1 en caso de error)
    """
    args = parsear_argumentos()

    secuencias_filtradas = []
    total_secuencias = 0

    print(f"Leyendo archivo FASTA: {args.input}")
    print(f"Filtros aplicados:")
    print(f"  - Longitud: {args.min_len} - {args.max_len}")
    print(f"  - GC%: {args.min_gc} - {args.max_gc}\n")

    # Procesar cada secuencia del archivo FASTA
    for encabezado, secuencia in leer_fasta(args.input):
        total_secuencias += 1

        # Calcular estadísticas
        stats = calcular_estadisticas(encabezado, secuencia)

        # Mostrar información
        print(f"Secuencia: {stats['encabezado']}")
        print(f"  Longitud: {stats['longitud']}")
        print(
            f"  G: {stats['g_count']}, C: {stats['c_count']}, G+C: {stats['gc_count']}"
        )
        print(f"  GC%: {stats['gc_porcentaje']:.2f}%", end="")

        # Verificar filtros
        if pasa_filtros(stats, args):
            secuencias_filtradas.append(stats)
            print(" ✓")
        else:
            print(" ✗ (filtrada)")
        print()

    # Guardar resultados
    print(f"\nTotal de secuencias: {total_secuencias}")
    print(f"Secuencias que pasan los filtros: {len(secuencias_filtradas)}")

    escribir_resultados(secuencias_filtradas, args.output)


if __name__ == "__main__":
    main()
