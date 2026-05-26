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
        default="secuencias.fasta",
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
