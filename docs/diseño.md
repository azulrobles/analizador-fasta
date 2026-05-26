# Diseño del Analizador de Secuencias FASTA

## Objetivo del diseño

Este documento describe cómo se organizará el programa antes de escribir el código.

La idea principal es dividir el problema en partes pequeñas. Cada parte tendrá una responsabilidad clara.

```mermaid
flowchart TD
    A([Inicio]) --> B[Leer argumentos]
    B --> C[Leer archivo FASTA]
    C --> D{¿El archivo existe?}
    D -- No --> E[Mostrar error y terminar]
    D -- Sí --> F[Separar encabezados y secuencias]
    F --> G[Calcular longitud y GC]
    G --> H{¿Pasa filtros?}
    H -- Sí --> I[Guardar en resultados]
    H -- No --> J[Omitir secuencia]
    I --> K{¿Quedan secuencias?}
    J --> K
    K -- Sí --> G
    K -- No --> L[Escribir archivo TSV]
    L --> M([Fin])
```