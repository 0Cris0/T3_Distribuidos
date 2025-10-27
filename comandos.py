import json

from clases import Transaccion, Servidor, estados_saltar
from f_aux import procesar_input, añadir_tran_servidores
from f_aux import obtener_var_R, obtener_var_W, obtener_vars

from f_aux_comandos import forwards, backwards, validacion_1, validacion_2
from f_aux_comandos import aplicar_cambios_globales, aplicar_cambios_locales, abortar_transaccion
from f_aux_comandos import invalidar_transaccion

def begin(t_activas: dict, tran: str, s_activos: dict, base_datos: dict, tiempo: int):
    if(tran in t_activas):
        return
    else:
        # Lo añado a activos
        nueva_transaccion = Transaccion(
            bd=json.loads(json.dumps(base_datos)),
            nombre=tran, 
            estado="ABIERTA",
            t_inicio=tiempo,
            t_can_commit=-1,
            t_commit=-1,
            operaciones={}
            )
        t_activas[tran] = nueva_transaccion
        añadir_tran_servidores(nueva_transaccion, s_activos)


def write(operacion: list, t_activas: dict, tran: str, tiempo: int, s_activos: dict):
    argumentos = operacion[2].split(",")
    nombre_var = argumentos[0]
    valor_var = argumentos[1]
    print(f" - [{tran}] Comando: WRITE {nombre_var} -> {valor_var}")
    if(tran not in t_activas): # Salto, no está iniciado
        return

    transaccion_actual = t_activas[tran]
    if(transaccion_actual.estado in estados_saltar):
        return
    if(transaccion_actual.estado == "EN_PREPARACION"):
        invalidar_transaccion(s_activos, transaccion_actual)
        return
    transaccion_actual.operaciones[tiempo] = {
        "comando": "WRITE",
        "n_var": nombre_var,
        "valor": valor_var
    }
    if(valor_var == "DELETE"):
        if(nombre_var in transaccion_actual.bd):
            transaccion_actual.bd.pop(nombre_var)
    else:
        transaccion_actual.bd[nombre_var] = valor_var


def read(operacion: list, t_activas: dict, tran: str, tiempo: int, base_datos: dict, s_activos: dict):
    if(tran not in t_activas): # Salto, no está iniciado
        return
    transaccion_actual = t_activas[tran]
    if(transaccion_actual.estado in estados_saltar):
        return
    
    nombre_var = operacion[2]
    print(f" - [{tran}] Comando: READ {nombre_var}")
    if(transaccion_actual.estado == "EN_PREPARACION"):
        invalidar_transaccion(s_activos, transaccion_actual)
        return
    transaccion_actual.operaciones[tiempo] = {
        "comando": "READ",
        "n_var": nombre_var
    }
    if(nombre_var not in transaccion_actual.bd):
        if(nombre_var not in base_datos):
            invalidar_transaccion(s_activos, transaccion_actual)


def can_commit(tran: str, t_activas: dict, s_activos: dict, tipo_operacion: str, tiempo: int, operacion: list) -> None:
    if tran not in t_activas:  # Salto, no está iniciado
        return
    transaccion_actual = t_activas[tran]
    if transaccion_actual.estado in estados_saltar:
        return

    transaccion_actual.t_can_commit = tiempo
    nombre_servidor = operacion[2]
    servidor_actual = s_activos[nombre_servidor]
    if servidor_actual.transacciones[tran] == "EN_PREPARACION":
        return

    print(f" - [{tran}] Comando: CAN_COMMIT servidor {nombre_servidor}")
    validacion1 = validacion_1(tipo_operacion, transaccion_actual, t_activas)
    validacion2 = validacion_2(servidor_actual, transaccion_actual, t_activas)

    if validacion1 and validacion2:
        for var in obtener_var_W(transaccion_actual):
            servidor_actual.var_reservadas[var] = transaccion_actual.nombre
        servidor_actual.transacciones[tran] = "EN_PREPARACION"
        transaccion_actual.estado = "EN_PREPARACION"
        transaccion_actual.t_can_commit = tiempo
        return

    condicion_forward = (not validacion1 and tipo_operacion == "forward")
    condicion_2PC = (not validacion2)
    if condicion_forward or condicion_2PC:
        return
    else:
        abortar_transaccion(s_activos, transaccion_actual)


def abort(tran: str, t_activas: dict, s_activos: dict):
    if(tran not in t_activas):
        return
    print(f" - [{tran}] Comando: ABORT")
    transaccion_actual = t_activas[tran]
    abortar_transaccion(s_activos, transaccion_actual)


def commit(tran: str, t_activas: dict, s_activos: dict, tiempo: int, base_datos: dict) -> None:
    if tran not in t_activas:
        return
    transaccion_actual = t_activas[tran]
    if transaccion_actual.estado == "ABORTADA":
        return
    print(f" - [{tran}] Comando: COMMIT")

    contador = 0
    for s_name in s_activos:
        servidor = s_activos[s_name]
        if servidor.transacciones.get(tran) == "EN_PREPARACION":
            contador += 1
    v1 = (contador >= len(s_activos)//2 + 1)
    v2 = (transaccion_actual.estado != "INVALIDA")
    v3 = backwards(transaccion_actual, t_activas)

    if v3 is False:
        abortar_transaccion(s_activos, transaccion_actual)
        return

    if v1 and v2 and v3:
        vars_T_write = obtener_var_W(transaccion_actual)
        for s_name in s_activos:
            servidor = s_activos[s_name]

            servidor.transacciones[tran] = "CONFIRMADA"
            aplicar_cambios_locales(transaccion_actual, servidor)

            for t_name in list(servidor.transacciones.keys()):
                if t_name == tran:
                    continue
                if servidor.transacciones[t_name] == "EN_PREPARACION":
                    otro = t_activas[t_name]
                    vars_otro_read = obtener_var_R(otro)
                    for var in vars_otro_read:
                        if var in vars_T_write:
                            abortar_transaccion(s_activos, otro)
                            break

            # Liberar reservas SOLO si las tomo esta transaccion
            for var in obtener_vars(transaccion_actual):
                if (var in servidor.var_reservadas and
                        servidor.var_reservadas[var] == transaccion_actual.nombre):
                    servidor.var_reservadas.pop(var)

        # Confirmacion global
        transaccion_actual.estado = "CONFIRMADA"
        transaccion_actual.t_commit = tiempo
        aplicar_cambios_globales(transaccion_actual, base_datos)
