# Recipy

## Json format

```json
{
    "Recipe Name": {
        "nombre": "Recipe Name", 
        "ingredientes": [
            {"nombre": "Ingredient 1"}, 
            {"nombre": "Ingredient 2"}, 
            {"nombre": "..."}, 
            {"nombre": "Ingredient n"}
        ], 
        "instrucciones": [
            {"orden": 0, "instruccion": "Instruction 1"},
            {"orden": 1, "instruccion": "Instruction 2"},
            {"orden": 2, "instruccion": "..."},
            {"orden": 3, "instruccion": "Instruction n"}
        ]
    },
}
```

### RecipeNLG

```json
{
    "Recipe Name": {
        "nombre": "Recipe Name", 
        "ingredientes": [
            {"nombre": "Ingredient 1"}, 
            {"nombre": "Ingredient 2"}, 
            {"nombre": "..."}, 
            {"nombre": "Ingredient n"}
        ], 
        "instrucciones": [
            {"orden": 0, "instruccion": "Instruction 1"},
            {"orden": 1, "instruccion": "Instruction 2"},
            {"orden": 2, "instruccion": "..."},
            {"orden": 3, "instruccion": "Instruction n"}
        ],
        "ingredientes_completos": [
            "Complete ingredient description 1",
            "Complete ingredient description 2",
            "...",
            "Complete ingredient description n"
        ]
    },
}
```