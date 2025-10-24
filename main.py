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

@dataclasses.dataclass
class Transaccion:
    bd: dict
    nombre: str
    estado: str

@dataclasses.dataclass
class Servidor:
    nombre: str
    transacciones: dict # Idea de que sea Trans-name, bool_can_commit, abort???
    var_reservadas: dict # Idea de 1resevar variables tal que (var, nombre_tas)
""" Mi idea de momento para servidor, es crear esta Clase Servidor que tiene
    - Nombre
    - Transacciones
    - Variables reservadas: dict
    donde es un dict que tiene como key el nombre de una Tran Activa y su estado
    cosa de poder decir que fue estado_base/abortada/ En_commit 
    
    Variables reservadas tal vez podría ser (var, transaccion_qu_la_reserva_nombre)"""

def procesar_input(test: str) -> dict:
    with open(test, "r", encoding="utf-8") as f:
        lineas = f.read()
    lineas_limpias = re.sub(r"//.*", "", lineas)
    json_instrucciones = json.loads(lineas_limpias)
    # print(json_instrucciones)
    print(" = Instrucciones obtenidas del input: ========")
    for key in json_instrucciones:
        print(f"    <<{key}>>: {json_instrucciones[key]}")
    print(" =========")
    return json_instrucciones


if __name__ == "__main__":
    # Completar con tu implementación o crea más archivos y funciones
    # print(argv)
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
    
    


    for servidor in servers:
        servidores_activos[servidor] = Servidor(
            nombre=servidor, 
            transacciones={}, 
            var_reservadas={})


    for operacion in operaciones:
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
                if(transaccion in transacciones_activas):
                    # Ya estaba iniciado, no hago nada
                    continue
                else:
                    # Lo añado a activos
                    nueva_transaccion = Transaccion(
                        bd=json.loads(json.dumps(base_datos)),
                        nombre=transaccion, 
                        estado="ABIERTO"
                        )
                    """ print(nueva_transaccion.nombre)
                    print(nueva_transaccion.bd) """
                    transacciones_activas[transaccion] = nueva_transaccion

            elif(comando == "WRITE"):
                if(transaccion not in transacciones_activas): # Salto, no está iniciado
                    continue
                if(transaccion_actual.estado == "ABORTADA"):
                    continue
                argumentos = operacion[2].split(",")
                nombre_var = argumentos[0]
                valor_var = argumentos[1]
                print(f" - [{transaccion}] Comando: {comando} {nombre_var} -> {valor_var}")
                transaccion_actual = transacciones_activas[transaccion]
                if(transaccion_actual.estado == "EN_PREPARACION"):
                    transaccion_actual.estado = "INVALIDA"
                    continue
                if(nombre_var == "DELETE"):
                    if(nombre_var in transaccion_actual.bd):
                        transaccion_actual.bd.pop(nombre_var)
                else:
                        transaccion_actual.bd[nombre_var] = valor_var
                # TODO: Lo relacionado a reflejarlo en la BD
            # TODO: Ver si en cada comando hago check si es INVALIDO -> Continue o no
            elif(comando == "READ"):
                if(transaccion not in transacciones_activas): # Salto, no está iniciado
                    continue
                if(transaccion_actual.estado == "ABORTADA"):
                    continue
                nombre_var = operacion[2]
                print(f" - [{transaccion}] Comando: {comando} {nombre_var}")
                transaccion_actual = transacciones_activas[transaccion]
                if(transaccion_actual.estado == "EN_PREPARACION"):
                    transaccion_actual.estado = "INVALIDA"
                    continue
                if(nombre_var in transaccion_actual.bd):
                    valor = transaccion_actual.bd[nombre_var]
                    # TODO: Ver qué hacer acá
                else:
                    if(nombre_var in base_datos):
                        valor = base_datos[nombre_var]
                        # TODO: Ver qué hacer acá
                    else:
                        transaccion_actual.estado = "INVALIDA"

            elif(comando == "CAN_COMMIT"):
                if(transaccion not in transacciones_activas): # Salto, no está iniciado
                    continue
                if(transaccion_actual.estado == "EN_PREPARACION"):
                    continue
                if(transaccion_actual.estado == "ABORTADA"):
                    continue
                # TODO
                transaccion_actual = transacciones_activas[transaccion]
                nombre_servidor = operacion[2]
                print(f" - [{transaccion}] Comando: {comando} servidor {nombre_servidor}")
                # TODO: validacion1 = Control de concurrencia
                validacion1 = True
                # TODO: validacion2 = 2PC
                validacion2 = False
                if(validacion1 and validacion2):
                    # TODO: Proteger las variables
                    print("Proteger vars")
                    transaccion_actual.estado = "EN_PREPARACION"
                condicion_forward = (not validacion1 and tipo_validacion == "forward")
                condicion_2PC = (not validacion2)
                if(condicion_forward or condicion_2PC):
                    # TODO: Ver si esto esta bien
                    continue
                else:
                    # TODO: Abortar Transaccion
                    print("Abortando transaccion")

            elif(comando == "ABORT"):
                if(transaccion not in transacciones_activas):
                    # Salto, no está iniciado
                    continue
                if(transaccion_actual.estado == "ABORTADA"):
                    continue
                # TODO
                transaccion_actual = transacciones_activas[transaccion]
                transaccion_actual.estado = "ABORTADA"
                for servidor in servidores_activos.values():
                    servidor.transacciones[transaccion_actual] = transaccion_actual.estado
                    for var in servidor.var_reservadas:
                        if( servidor.var_reservadas[var]==transaccion_actual.nombre):
                            servidor.var_reservadas.pop(var)
                            # Elimino del reservado
                            # TODO: Ver si funciona
                # Ver si funciona, en especial lo de no considerar, aunque creo que eso
                # va en cCOMMIT


                print(f" - [{transaccion}] Comando: {comando}")

            elif(comando == "COMMIT"):
                if(transaccion not in transacciones_activas):
                    # Salto, no está iniciado
                    continue
                if(transaccion_actual.estado == "ABORTADA"):
                    continue
                # TODO
                print(f" - [{transaccion}] Comando: {comando}")

