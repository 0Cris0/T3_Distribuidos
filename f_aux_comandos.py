import json

from clases import Transaccion, Servidor
from f_aux import procesar_input, añadir_tran_servidores
from f_aux import obtener_var_R, obtener_var_W, obtener_vars

def forwards(trans: Transaccion, t_activos: dict)->bool:
    print("Forwards validation")
    vars_T_W = obtener_var_W(trans)
    for t_name in t_activos:
        if(t_name != trans.nombre):
            otra_trans = t_activos[t_name]
            if(otra_trans.estado not in ["EN_PREPARACION", "ABIERTA"]):
                continue
            for tiempo_op in otra_trans.operaciones:
                operacion = otra_trans.operaciones[tiempo_op]
                if(operacion["comando"] == "READ" and operacion["n_var"] in vars_T_W):
                    if(tiempo_op <= trans.t_can_commit and trans.t_inicio <= tiempo_op):
                        return False
    return True
# f_aux_comandos.py
def backwards(trans: Transaccion, t_activos: dict) -> bool:
    print("Backwards validation")
    vars_T_R = set(obtener_var_R(trans))
    for t_name, otra_trans in t_activos.items():
        if t_name == trans.nombre:
            continue
        if getattr(otra_trans, "estado", "") != "CONFIRMADA":
            continue
        vars_Tj_W = set(obtener_var_W(otra_trans))
        if not (vars_T_R & vars_Tj_W):
            continue
        tj_commit = getattr(otra_trans, "t_commit", -1)
        if tj_commit != -1 and trans.t_inicio <= tj_commit <= trans.t_can_commit:
            return False
    return True



def validacion_1(tipo_validacion: str, trans: Transaccion, t_activos: dict) -> bool:
    if(tipo_validacion == "forward"):
        return forwards(trans, t_activos)
    else:
        return backwards(trans, t_activos)

def validacion_2(serv: Servidor, trans: Transaccion, t_activos: dict) -> bool:
    for transaccion in serv.transacciones:
        if(transaccion == trans.nombre):
            continue
        otro_estado = serv.transacciones[transaccion]
        if(otro_estado != "EN_PREPARACION"):
            continue
        # Osea, ya sé que existe otra T' esperando Commit
        var_T_read = obtener_var_R(trans)
        var_T_write = obtener_var_W(trans)
        vars_T = var_T_read + var_T_write
        for var in vars_T:
            if(var in serv.var_reservadas):
                return False
            
        # Ahora veo lo de generar conflicto
        otra_t = t_activos[transaccion]
        for tiempo_op in otra_t.operaciones:
            operacion = otra_t.operaciones[tiempo_op]
            if(operacion["comando"] == "WRITE" and operacion["n_var"] in var_T_read):
                return False
    return True


def aplicar_cambios_locales(trans: Transaccion, servidor: Servidor):
    for tiempo_op in trans.operaciones:
        operacion = trans.operaciones[tiempo_op]
        if(operacion["comando"]=="WRITE"):
            var = operacion["n_var"]
            valor = operacion["valor"]
            if(valor != "DELETE"):
                servidor.bd[var] = valor
            else:
                servidor.bd.pop(var)
            # Ahora libero
            # if(var in servidor.var_reservadas):
            #     servidor.var_reservadas.pop(var)

def aplicar_cambios_globales(trans: Transaccion, base_datos: dict):
    for tiempo_op in trans.operaciones:
        operacion = trans.operaciones[tiempo_op]
        if(operacion["comando"]=="WRITE"):
            var = operacion["n_var"]
            valor = operacion["valor"]
            if(valor != "DELETE"):
                base_datos[var] = valor
            else:
                base_datos.pop(var)

def abortar_transaccion(s_activos: dict, tran: Transaccion):
    # Cambio estado general
    tran.estado = "ABORTADA"
    for s_name in s_activos:
        servidor = s_activos[s_name]
        if(tran.nombre in servidor.transacciones):
            estado = servidor.transacciones[tran.nombre]
            if(estado == "EN_PREPARACION"):
                # Liberar variables
                vars_T = obtener_vars(tran)
                for var in servidor.var_reservadas:
                    if(var in vars_T):
                        servidor.var_reservadas.pop(var)
                # Cambiar estado en el servidor
                servidor.transacciones[tran.nombre] = "ABORTADA"

def invalidar_transaccion(s_activos: dict, tran: Transaccion):
    if tran.estado not in ("ABORTADA", "CONFIRMADA"):
        tran.estado = "INVALIDA"
    for s_name in s_activos:
        servidor = s_activos[s_name]
        if tran.nombre in servidor.transacciones:
            if servidor.transacciones[tran.nombre] not in ("ABORTADA", "CONFIRMADA"):
                servidor.transacciones[tran.nombre] = "INVALIDA"