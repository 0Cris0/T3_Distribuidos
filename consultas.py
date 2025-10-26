import json

def read_possible_values(nombre_var: str, base_datos: dict, transacciones_activas: dict):
    print(f" > Consulta: READ_POSSIBLE_VALUES {nombre_var}")
    valores = []
    if(nombre_var in base_datos):
        valores.append(base_datos[nombre_var])
    for n_tran in transacciones_activas:
        tran = transacciones_activas[n_tran]
        if(nombre_var in tran.bd):
            valores.append(tran.bd[nombre_var])
    return json.dumps(list(valores))

def read_commit(nombre_var: str, base_datos: str):
    print(f" > Consulta: READ_COMMIT {nombre_var}")
    valor = "NULL"
    if(nombre_var in base_datos):
        valor = base_datos[nombre_var]
    return valor