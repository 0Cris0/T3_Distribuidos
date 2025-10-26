from __future__ import annotations  # Solo lo dejo por si lo necesitan. Lo pueden eliminar
from sys import argv
import json

# Librerías adicionales por si las necesitan
# No son obligatorias y tampoco tienen que usarlas todas
# No puedes agregar ningún otro import que no esté en esta lista
import re
import os
import typing
import collections
import itertools
import dataclasses
import enum

# Recuerda que no se permite importar otros módulos/librerías a excepción de los creados
# por ustedes o las ya incluidas en este main.py

from clases import Transaccion, Servidor
from comandos import begin, write, read, can_commit, abort, commit


""" def abortar(s_activos: dict, tran: Transaccion):
    # Cambio estado general
    tran.estado = "ABORTADA"
    for s_name in s_activos:
        servidor = s_activos[s_name]
        if(tran.nombre in servidor.transacciones):
            almacenada = servidor.transacciones[tran.nombre]
            if(almacenada.estado == "EN_PREPARACION"):
                # Liberar variables
                vars_T = obtener_vars(tran)
                for var in servidor.var_reservadas:
                    if(var in vars_T):
                        servidor.var_reservadas.pop(var)
                # Cambiar estado en el servidor
                almacenada.estado = "ABORTADA" """

""" def begin(t_activas: dict, tran: str, s_activos: dict, base_datos: dict, tiempo: int):
    print(f" - [{tran}] Comando: {comando}")
    if(tran in t_activas):
        return
    else:
        # Lo añado a activos
        nueva_transaccion = Transaccion(
            bd=json.loads(json.dumps(base_datos)),
            nombre=tran, 
            estado="ABIERTO",
            t_inicio=tiempo,
            t_can_commit=-1,
            t_commit=-1,
            operaciones={}
            )
        t_activas[tran] = nueva_transaccion
        añadir_tran_servidores(nueva_transaccion, s_activos) """

""" def write(operacion: str, transacciones_activas: dict, transaccion: str):
    argumentos = operacion[2].split(",")
    nombre_var = argumentos[0]
    valor_var = argumentos[1]
    print(f" - [{transaccion}] Comando: {comando} {nombre_var} -> {valor_var}")
    if(transaccion not in transacciones_activas): # Salto, no está iniciado
        return

    transaccion_actual = transacciones_activas[transaccion]
    if(transaccion_actual.estado in estados_saltar):
        return
    if(transaccion_actual.estado == "EN_PREPARACION"):
        transaccion_actual.estado = "INVALIDA"
        return
    transaccion_actual.operaciones.append({
        "comando": "WRITE",
        "n_var": nombre_var,
        "valor": valor_var,
        "tiempo": tiempo
    })
    if(nombre_var == "DELETE"):
        if(nombre_var in transaccion_actual.bd):
            transaccion_actual.bd.pop(nombre_var)
    else:
        transaccion_actual.bd[nombre_var] = valor_var """

""" def read(operacion: str, transacciones_activas: dict, transaccion: str):
    if(transaccion not in transacciones_activas): # Salto, no está iniciado
        return

    transaccion_actual = transacciones_activas[transaccion]
    if(transaccion_actual.estado in estados_saltar):
        return
    nombre_var = operacion[2]
    print(f" - [{transaccion}] Comando: {comando} {nombre_var}")
    if(transaccion_actual.estado == "EN_PREPARACION"):
        transaccion_actual.estado = "INVALIDA"
        return
    transaccion_actual.operaciones.append({
        "comando": "READ",
        "n_var": nombre_var,
        "tiempo": tiempo
    })
    if(nombre_var not in transaccion_actual.bd):
        if(nombre_var not in base_datos):
            transaccion_actual.estado = "INVALIDA" """



""" def validacion_1(tipo_validacion: str, trans: Transaccion, t_activos: dict) -> bool:
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
        var_T_read = obtener_var_R(trans)
        var_T_write = obtener_var_W(trans)
        vars_T = var_T_read + var_T_write
        for var in vars_T:
            if(var in Servidor.var_reservadas):
                return False
            
        # Ahora veo lo de generar conflicto
        otra_t = t_activos[transaccion]
        for operacion in otra_t.operaciones:
            if(operacion["comando"] == "WRITE" and operacion["n_var"] in var_T_read):
                return False
    return True """

""" def aplicar_cambios_locales(trans: Transaccion, servidor: Servidor):
    for op in trans.operaciones:
        operacion = trans.operaciones[op]
        if(operacion["comando"]=="WRITE"):
            var = operacion["n_var"]
            valor = operacion["valor"]
            servidor.bd[var] = valor
            # Ahora libero
            # if(var in servidor.var_reservadas):
            #     servidor.var_reservadas.pop(var)

def aplicar_cambios_globales(trans: Transaccion, bd: dict):
    for op in trans.operaciones:
        operacion = trans.operaciones[op]
        if(operacion["comando"]=="WRITE"):
            var = operacion["n_var"]
            valor = operacion["valor"]
            bd[var] = valor """


""" def can_commit(transaccion: str, transacciones_activas: dict, servidores_activos: dict, tipo_operacion: str)->None:
    if(transaccion not in transacciones_activas): # Salto, no está iniciado
        return
    transaccion_actual = transacciones_activas[transaccion]
    if(transaccion_actual.estado == "EN_PREPARACION"):
        return
    if(transaccion_actual.estado == estados_saltar):
        return

    transaccion_actual.t_can_commit = tiempo
    nombre_servidor = operacion[2]
    servidor_actual = servidores_activos[servidor]
    print(f" - [{transaccion}] Comando: {comando} servidor {nombre_servidor}")
    validacion1 = validacion_1(tipo_operacion, transaccion_actual, transacciones_activas)
    validacion2 = validacion_2(servidor_actual, transaccion_actual, transacciones_activas)
    if(validacion1 and validacion2):
        # Proteger las variables
        variables = obtener_vars(transaccion_actual)
        for var in variables:
            servidor_actual.var_reservadas[var] = transaccion_actual.nombre
        # Cambiar estado
        transaccion_actual.estado = "EN_PREPARACION"

    condicion_forward = (not validacion1 and tipo_validacion == "forward")
    condicion_2PC = (not validacion2)
    if(condicion_forward or condicion_2PC):
        return
    else:
        abortar(servidores_activos, transaccion_actual) """

""" def abort():
    if(transaccion not in transacciones_activas):
        return
    print(f" - [{transaccion}] Comando: ABORT")
    transaccion_actual = transacciones_activas[transaccion]
    abortar_transaccion(servidores_activos, transaccion_actual) """

""" def commit(transaccion: str, transacciones_activas: dict, servidores_activos: dict)->None:
    if(transaccion not in transacciones_activas):
        # Salto, no está iniciado
        return
    transaccion_actual = transacciones_activas[transaccion]
    if(transaccion_actual.estado == "ABORTADA"):
        return
    print(f" - [{transaccion}] Comando: {comando}")

    contador = 0
    for s_name in servidores_activos:
        servidor = servidores_activos[s_name]
        estado = servidor.transacciones[transaccion]
        if(estado == "EN_PREPARACION"):
            contador+=1
    v1 = (contador >= len(servidores_activos)//2 + 1)
    v2 = (transaccion_actual.estado != "INVALIDA")
    v3 = backwards(transaccion_actual, transacciones_activas)
    
    if(v3 == False):
        abortar(servidores_activos, transaccion_actual)
    if(v1 == True and v2 == True and v3 == True):
        for s_name in servidores_activos:
            servidor = servidores_activos[s_name]
            servidor.transacciones[transaccion] = "CONFIRMADA"
            aplicar_cambios_locales(transaccion_actual, servidor)
            for t_name in servidor.transacciones:
                if(servidor.transacciones[t_name] == "EN_PREPARACION"):
                    otro = transacciones_activas[t_name]
                    vars_T_write = obtener_var_W(transaccion_actual)
                    vars_otro_read = obtener_var_R(otro)
                    for var in vars_otro_read:
                        if(var in vars_T_write):
                            abortar(servidores_activos, transaccion_actual)
                            break

            # Ahora libero variables
            vars_T = obtener_vars(transaccion_actual)
            for var in vars_T:
                servidor.var_reservadas.pop(var)
        transaccion_actual.estado = "CONFIRMADA"
        aplicar_cambios_globales(transaccion_actual, base_datos) """

if __name__ == "__main__":
    test = argv[1]
    instrucciones = procesar_input(test)

    tipo_validacion = instrucciones["VALIDATION"]
    servers = instrucciones["SERVERS"]
    base_datos = instrucciones["DATA"]
    operaciones = instrucciones["TRANSACTIONS"]

    transacciones_activas = {}
    servidores_activos = {}
    
    """ test1 = Transaccion({}, "test", "aaaa")
    dicion = {f"{test}": test1.nombre, "estado": "EN_PROC"}
    for servidor in servers:
        servidores_activos[servidor] = Servidor(servidor, {}, {})
        
        servidores_activos[servidor].transacciones["test"] = json.loads(json.dumps(dicion))
    dicion["estado"] = "AAAA"
    servidores_activos["R2"].transacciones["test"]["estado"] = "NEOOOO"
    for servidor in servidores_activos:
        print(servidores_activos[servidor].transacciones) 
        


    Ver si esto funciona o no
        """
    
    
    tiempo = 0
    

    for servidor in servers:
        servidores_activos[servidor] = Servidor(
            nombre=servidor, 
            transacciones={}, 
            var_reservadas={},
            bd=json.loads(json.dumps(base_datos))
            )


    for operacion in operaciones:
        tiempo += 1
        operacion = operacion.split(";")
        # print(operacion)
        tipo_operacion = operacion[0]
        comando = operacion[1]
        if("C" in tipo_operacion):
            # Consulta
            nombre_var = operacion[2]
            if(comando == "READ_POSSIBLE_VALUES"):
                # TODO
                print(f" > Consulta: {comando} {nombre_var}")
            elif(comando == "READ_COMMIT"):
                # TODO
                print(f" > Consulta: {comando} {nombre_var}")
        
        elif("T" in tipo_operacion):
            transaccion = tipo_operacion
            # Comandos
            if(comando == "BEGIN"):
                print(f" - [{transaccion}] Comando: {comando}")
                begin(transacciones_activas, transaccion, servidores_activos, base_datos, tiempo)
            elif(comando == "WRITE"):
                write(operacion, transacciones_activas, transaccion)
            elif(comando == "READ"):
                read(operacion, transacciones_activas, transaccion)
            elif(comando == "CAN_COMMIT"):
                can_commit(transaccion, transacciones_activas, servidores_activos, tipo_operacion)
            elif(comando == "ABORT"):
                abort(transaccion, transacciones_activas, servidores_activos)
            elif(comando == "COMMIT"):
                commit(transaccion, transacciones_activas, servidores_activos)


                        
