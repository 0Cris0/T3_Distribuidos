import dataclasses

@dataclasses.dataclass
class Transaccion:
    bd: dict
    nombre: str
    estado: str
    t_inicio: int
    t_can_commit: int
    t_commit: int
    operaciones: dict


""" ej:
    bd: {
        "Var_1": 1,
    },
    nombre: "T2",
    estado: "EN_PREPARACION",
    t_inico: 1,
    t_can_commit: -1,
    t_commit: -1,
    operaciones: {
        "4": {
            "comando": "WRITE",
            "n_var": "Var_1",
            "valor": 10,
            
        }
    },
} """

@dataclasses.dataclass
class Servidor:
    nombre: str
    transacciones: dict # Idea de que sea Trans-name, bool_can_commit, abort???
    var_reservadas: dict # Idea de 1resevar variables tal que (var, nombre_tas)
    bd: dict

""" ej:
{
    nombre: "S1",
    transacciones: {
        "T1": "ABORTADA",
        "T2": "EN_PREPARACION",
    },
    var_reservadas: {
        "Var_2": "T2"
    },
    bd: {
        "Var_1": 1,
        "Var_2": 4,
    }
} """

estados_saltar = ["ABORTADA", "CONFIRMADA"]