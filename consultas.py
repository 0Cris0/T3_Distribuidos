import json

def read_possible_values(nombre_var: str, base_datos: dict, transacciones_activas: dict):
    print(f" > Consulta: READ_POSSIBLE_VALUES {nombre_var}")
    valores, vistos = [], set()

    if nombre_var in base_datos:
        v = base_datos[nombre_var]
        if v not in vistos:
            valores.append(v); vistos.add(v)

    for n_tran in sorted(transacciones_activas.keys()):  # orden determinista
        tran = transacciones_activas[n_tran]
        if getattr(tran, "estado", "") in ("ABIERTA", "EN_PREPARACION"):
            if nombre_var in tran.bd:
                v = tran.bd[nombre_var]
                if v != "DELETE" and v not in vistos:
                    valores.append(v); vistos.add(v)

    return json.dumps(sorted(valores))



def read_commit(nombre_var: str, base_datos: str):
    print(f" > Consulta: READ_COMMIT {nombre_var}")
    valor = "NULL"
    if(nombre_var in base_datos):
        valor = base_datos[nombre_var]
    return valor