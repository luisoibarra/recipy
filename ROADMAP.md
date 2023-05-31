# Roadmap

## Primera Etapa: Recolección de datos

1. Ver las bases de datos que contienen recetas y recolectarlas.
2. Crear una base de datos conjunta con los datos disponibles.
    1. Definir los features a analizar. Recetas e ingredientes tienen que estar.
        - Nombre de receta (Requerido)
        - Nombre de ingrediente (Requerido)
        - Posibles cambios de ingredientes (Opcional)
        - Cantidades de ingredientes (Opcional)
        - Cualquier otra cosa que se pueda extraer (Tener en cuenta que no todas las BDs extraen la misma información)
    2. Por cada base de datos recolectada hacer un pipeline de procesamiento que extraiga los features.
3. Hacer algún tipo de visualización de la base de datos conjunta.
    - Objetivo:
        1. Encontrar errores.
        2. Tener información elemental de los datos.
        3. Encontrar patrones simples.
        4. Tener algunas gráficas para el informe.

## Segunda Etapa: Creación del Engine

### Backend

El backend será un paquete de python el cual se basará en el análisis de grafos.

**Objetivo:**

- Abstraer la complejidad del analisis de datos del frontend.
- Permitir la posible integración con otros sistemas una vez esté hecho.

**Features:**

- Convertir los datos procesados en distintos tipos de grafos.
  - Receta <-> Receta Por similitud de ingredientes.
  - Ingrediente <-> Ingrediente Por similitud de recetas.
  - Receta <-> Ingrediente Por uso en estas.
- Poder realizar queries sobre los grafos.
  - Búsqueda de recetas por nombre
  - Búsqueda de ingredientes por nombre
  - Búsqueda de recetas teniendo un conjunto de ingredientes disponibles
  - Búsqueda de posibles cambios de ingredientes en recetas, dado que no se tiene un ingrediente

### Frontend

El frontend permitirá el uso del paquete del back importándolo directamente. Se hará en streamlit.

**Objetivo:**

- Permitir la fácil interacción del usuario con el back.
- Visualizar los elementos devueltos de manera que se pueda obtener una buena UX.

**Features:**

- Búsqueda de recetas por nombre
- Búsqueda de ingredientes por nombre
- Búsqueda de recetas teniendo un conjunto de ingredientes disponibles
- Búsqueda de posibles cambios de ingredientes en recetas, dado que no se tiene un ingrediente

## Tercera etapa: Agrego de más features

En dependencia de los datos encontrados se pueden hacer otros tipos de procesimientos.

## Cuarta etapa: Creación del informe

En latex, se debe poner los conjuntos de datos, los features utilizados, el procesamiento que se hizo sobre los datos y el porqué, grafos extraídos, imágenes de grafos, métricas de grafos, patrones encontrados en los grafos, etc.
