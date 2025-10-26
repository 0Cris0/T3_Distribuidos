from clases import Transaccion, Servidor
import re
import json

def procesar_input(test: str) -> dict:
    with open(test, "r", encoding="utf-8") as f:
        lineas = f.read()
    lineas_limpias = re.sub(r"//.*", "", lineas)
    json_instrucciones = json.loads(lineas_limpias)

    print(" = Instrucciones obtenidas del input: ========")
    for key in json_instrucciones:
        print(f"    <<{key}>>: {json_instrucciones[key]}")
    print(" =========")
    return json_instrucciones

def añadir_tran_servidores(tran: Transaccion, s_activos: dict) -> None:
    for n_serv in s_activos:
        server = s_activos[n_serv]
        server.transacciones[tran.nombre] = "ABIERTO"

def obtener_var_R(tran: Transaccion) -> list:
    var_R = []
    for tiempo_op in tran.operaciones:
        operacion = tran.operaciones[tiempo_op]
        if(operacion["comando"] == "READ"):
            var_R.append(operacion["n_var"])
    return var_R

def obtener_var_W(tran: Transaccion) -> list:
    var_W = []
    for tiempo_op in tran.operaciones:
        operacion = tran.operaciones[tiempo_op]
        if(operacion["comando"] == "WRITE"):
            var_W.append(operacion["n_var"])
    return var_W

def obtener_vars(trans: Transaccion) -> list:
    var_T_read = obtener_var_R(trans)
    var_T_write = obtener_var_W(trans)
    vars_T = var_T_read + var_T_write
    return vars_T