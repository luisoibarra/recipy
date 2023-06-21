# TODO

- [ ] Grafos entre recetas.
  - Dado una query, devolver un ranking con las recetas que mas se parezcan
  - Se podria utilizar algun tipo de embedding y devolver un ranking basado en distancia o similaridad de coseno.
  - Los nodos son las recetas y las aristas son la metrica usada con un threshold para que no sea un grafo completo.
- [ ] Filtrar las recetas mas rankeadas en food.com para disminuir la cantidad. 230000 son demasiadas para el procesamiento.
- [ ] Grafos entre ingredientes.
- [ ] Crear grafo bipartito más pequeño.
  - Dejar solamente los ingredientes del grafo de ingredientes (los que contienen hasta un 85-90% de las ocurrencias de ingredientes).
  - Buscar una manera de rankear las recetas, de forma que tenga sentido filtrarlas.

## Ranking Recetas

- [ ] El ranking se basasra en el uso de ingredientes, la representacion vectorial de la receta sera un one-hot encoding de los ingredientes.
- [x] Una vez se tenga esta representacion se aplicara algun metodo de ranking
  - Vectorial
    - TF-IDF

- [x] Usar el tfidf en streamlit
- [x] Hacer un autoencoder simple con convolucionales y luego si algo con transformer.
- [x] BUSCAR MANERA DE REDUCIR LA CANTIDAD DE RECETASSSSSS
  - Definir metrica asociada a los ingredientes connectados

## Propuesta

1. Receta-Receta Semantico [x]
    - Disminuir recetas: (Ranking de recetas)
    - Embedding semantico
    - Se hace el grafo

2. Ingrediente-Acci'on (Intruccion)
    - Sacar los pares ingrediente-accion y ingrediente-accion-ingredinete
    - Se hace el grafo con pesos normalizados
    - Se pregunta

3. Substitution Network
    - Sacar pares de ignredientes substituidos
    - Sacar aumentos/disminuciones de cantidades 

4. Probar el k-clique con el grafo pmi.

5. Llenar esas paginas (Recipe details y Ingredient Details)

## Para terminar

- [ ] Informe
  - Empezar repositorio de informe
  - Abstract
  - Introduction
  - Why?
  - How?
  - Implementation
  - Fotos de grafos y de las estadísticas
  - Conclusions
- [ ] Definir los grafos a usar en streamlit, que tengan consistencia
  - Bipartito 5000
  - Semantic Sim 5000 0.9
  - Ingrediente Jaccard, PMI, completos? Revisar la cantidad de ingredientes.
  - Todo de foodcom.
