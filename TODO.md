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
