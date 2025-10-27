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
    logs_output = []
    
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
                resultado = read_possible_values(nombre_var, base_datos, transacciones_activas)
                logs_output.append(str(resultado))
            elif(comando == "READ_COMMIT"):
                resultado = read_commit(nombre_var, base_datos)
                logs_output.append(str(resultado))
        
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
                can_commit(transaccion, transacciones_activas, servidores_activos, tipo_validacion, tiempo, operacion)
            elif(comando == "ABORT"):
                abort(transaccion, transacciones_activas, servidores_activos)
            elif(comando == "COMMIT"):
                commit(transaccion, transacciones_activas, servidores_activos, tiempo, base_datos)

# Escritura de resultados
    nombre_salida = f"{os.path.splitext(os.path.basename(test))[0]}.txt"
    ruta_salida = os.path.join("logs", nombre_salida)

    os.makedirs("logs", exist_ok=True)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        # --- LOGS ---
        f.write("##LOGS##\n")
        if logs_output:
            for log in logs_output:
                f.write(f"{log}\n")
        else:
            f.write("No hay logs\n")
        
        # --- DATABASE ---
        f.write("##DATABASE##\n")
        for var, valor in base_datos.items():
            f.write(f"{var}={valor}\n")
        
        # --- STATS ---
        f.write("##STATS##\n")
        abiertas = []
        abortadas = []
        confirmadas = []
        en_preparacion = []
        invalidas = []

        for t_name, t_obj in transacciones_activas.items():
            estado = getattr(t_obj, "estado", "")
            if estado == "ABIERTA":
                abiertas.append(t_name)
            elif estado == "ABORTADA":
                abortadas.append(t_name)
            elif estado == "CONFIRMADA":
                confirmadas.append(t_name)
            elif estado == "EN_PREPARACION":
                en_preparacion.append(t_name)
            elif estado == "INVALIDA":
                invalidas.append(t_name)

        f.write(f"ABIERTA={json.dumps(abiertas)}\n")
        f.write(f"ABORTADA={json.dumps(abortadas)}\n")
        f.write(f"CONFIRMADA={json.dumps(confirmadas)}\n")
        f.write(f"EN_PREPARACION={json.dumps(en_preparacion)}\n")
        f.write(f"INVALIDA={json.dumps(invalidas)}\n")