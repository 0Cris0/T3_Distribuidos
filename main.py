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

    """ print("Un, dos, tres y...")
    print("Mala")
    print("Esta cuenta es mala")
    print("Se cae la ventana")
    print("No cuadra la tabla")
    print("Mala")
    print("Como fila muy larga")
    print("Como clave olvidada")
    print("Esta cuenta es mala")
    print("Mala")
    print("Como tasa muy alta")
    print("Como deuda atrasada")
    print("Como sistema caído")
    print("Mala")
    print("¡Pero es mía!") """

    instrucciones = procesar_input(test)

    tipo_validacion = instrucciones["VALIDATION"]
    servers = instrucciones["SERVERS"]
    base_datos = instrucciones["DATA"]
    operaciones = instrucciones["TRANSACTIONS"]
        
    """ print(tipo_validacion)
    print(servers)
    print(base_datos)
    print(operaciones) """

    transacciones_activas = {}

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
                    nueva_transaccion = Transaccion(json.loads(json.dumps(base_datos)), transaccion, "ABIERTO")
                    """ print(nueva_transaccion.nombre)
                    print(nueva_transaccion.bd) """
                    transacciones_activas[transaccion] = nueva_transaccion

            elif(comando == "WRITE"):
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
                # TODO
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
                # TODO
                nombre_servidor = operacion[2]
                print(f" - [{transaccion}] Comando: {comando} servidor {nombre_servidor}")
            elif(comando == "ABORT"):
                # TODO
                print(f" - [{transaccion}] Comando: {comando}")
            elif(comando == "COMMIT"):
                # TODO
                print(f" - [{transaccion}] Comando: {comando}")

