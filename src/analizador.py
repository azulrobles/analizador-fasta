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
