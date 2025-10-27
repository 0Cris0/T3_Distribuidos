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
from f_aux import procesar_input
from comandos import begin, write, read, can_commit, abort, commit
from consultas import read_possible_values, read_commit

    


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

    log_consultas = ["##LOGS##"]
    log_bd = ["##DATABASE##"]
    log_stats = ["##STATS##"]

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
                resultado = read_possible_values(nombre_var, base_datos, transacciones_activas)
                log_consultas.append(resultado)

            elif(comando == "READ_COMMIT"):
                resultado = read_commit(nombre_var, base_datos)
                log_consultas.append(resultado)
        
        elif("T" in tipo_operacion):
            transaccion = tipo_operacion
            # Comandos
            if(comando == "BEGIN"):
                print(f" - [{transaccion}] Comando: {comando}")
                begin(transacciones_activas, transaccion, servidores_activos, base_datos, tiempo)
            elif(comando == "WRITE"):
                write(operacion, transacciones_activas, transaccion, tiempo, servidores_activos)
            elif(comando == "READ"):
                read(operacion, transacciones_activas, transaccion, tiempo, base_datos, servidores_activos)
            elif(comando == "CAN_COMMIT"):
                can_commit(transaccion, transacciones_activas, servidores_activos, tipo_operacion, tiempo, operacion)
            elif(comando == "ABORT"):
                abort(transaccion, transacciones_activas, servidores_activos)
            elif(comando == "COMMIT"):
                commit(transaccion, transacciones_activas, servidores_activos, tiempo, base_datos)
    
    if(len(log_consultas)==1):
        log_consultas.append("No hubo logs")
    for var in base_datos:
        log_bd.append(f"{var}={base_datos[var]}")
    if(len(log_bd)==1):
        log_bd.append("No hay datos")

    n_abierta = []
    n_abortada = []
    n_confirmada = []
    n_en_preparacion = []
    n_invalida = []
    for t_name in transacciones_activas:
        tran = transacciones_activas[t_name]
        if(tran.estado == "ABIERTA"):
            n_abierta.append(t_name)
        elif(tran.estado == "ABORTADA"):
            n_abortada.append(t_name)
        elif(tran.estado == "CONFIRMADA"):
            n_confirmada.append(t_name)
        elif(tran.estado == "EN_PREPARACION"):
            n_en_preparacion.append(t_name)
        elif(tran.estado == "INVALIDA"):
            n_invalida.append(t_name)
    log_stats.append(f"ABIERTA={n_abierta}")
    log_stats.append(f"ABORTADA={n_abortada}")
    log_stats.append(f"CONFIRMADA={n_confirmada}")
    log_stats.append(f"EN_PREPARACION={n_en_preparacion}")
    log_stats.append(f"INVALIDA={n_invalida}")


    ruta_test = argv[1]
    nombre_base = os.path.basename(ruta_test)
    nombre_sin_ext, _ = os.path.splitext(nombre_base)
    nombre_salida = f"{nombre_sin_ext}.txt"

    print(f"Archivo: {ruta_test} v/s Ruta_salida: {nombre_salida}")
    ruta_salida = os.path.join("logs", nombre_salida)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        for linea in log_consultas + log_bd + log_stats:
            f.write(f"{linea}\n")


        
        

                        
