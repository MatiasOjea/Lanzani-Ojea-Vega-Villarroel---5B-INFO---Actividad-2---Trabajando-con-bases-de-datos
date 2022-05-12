import sqlite3
import datetime
from tkinter import CASCADE

"""
datetime.datetime.now().replace(microsecond=0).isoformat()

devuelve fecha hora actual en formato ISO8601 simple

yyyymmddThh:mm:ss

"""

tiempo_actual = datetime.datetime.now().replace(microsecond=0).isoformat()

class Persona:
    def __init__(self, dni, apellido, nombre='', movil=''):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.movil= movil


def ingresa_visita(persona, destino):
    """Guarda los datos de una persona al ingresar"""
    conn = sqlite3.connect('recepcion.db')

    q = f"""SELECT dni FROM personas WHERE dni = '{persona.dni}'"""

    resu = conn.execute(q)

    if resu.fetchone():
        print("ya existe")
    else:
        q = f"""INSERT INTO personas (dni, nombre, apellido, movil)
                VALUES ('{persona.dni}',
                        '{persona.nombre}',
                        '{persona.apellido}',
                        '{persona.movil}');"""
        print(q)
        conn.execute(q)

        global tiempo_actual
        tiempo_actual = datetime.datetime.now().replace(microsecond=0).isoformat()

        q2 = f"""INSERT INTO ingresos_egresos (dni, fechahora_in, fechahora_out, destino)
                VALUES ('{persona.dni}',
                        '{tiempo_actual}',
                        'NULL',
                        '{destino}');"""
        print(q2)
        conn.execute(q2)
        conn.commit()

    conn.close()
    

def egresa_visita(dni):
    """Coloca fecha y hora de egreso al visitante con dni dado"""
    conn = sqlite3.connect('recepcion.db')

    q = f"""SELECT fechahora_out FROM ingresos_egresos WHERE dni = ('{dni}')"""

    resu = conn.execute(q)

    global tiempo_actual
    tiempo_actual = datetime.datetime.now().replace(microsecond=0).isoformat()

    if resu.fetchone():
        q = (f"""UPDATE ingresos_egresos SET fechahora_out = ('{tiempo_actual}') WHERE dni = ('{dni}')""")
        print(q)
        conn.execute(q)
        conn.commit()

    conn.close()


def lista_visitantes_en_institucion():
    """Devuelve una lista de objetos Persona presentes en la institución"""
    
    conn = sqlite3.connect('recepcion.db')
    q = f"""SELECT * FROM personas;"""

    resu = conn.execute(q)
    
    for fila in resu:
        print(fila)
    conn.close()


def busca_vistantes(fecha_desde, fecha_hasta, destino, dni):
    """ busca visitantes segun criterios """
    conn = sqlite3.connect('recepcion.db')

    q = f"""SELECT * 
            FROM ingresos_egresos 
            WHERE fechahora_in LIKE '{fecha_desde}%' AND fechahora_out LIKE '{fecha_hasta}%' AND destino = '{destino}' AND dni = '{dni}'"""

    desde = conn.execute(q)

    for fila in desde:
        print(fila)

    conn.commit()

    conn.close()


def iniciar():
    conn = sqlite3.connect('recepcion.db')

    qry = '''CREATE TABLE IF NOT EXISTS
                            personas
                    (dni TEXT NOT NULL PRIMARY KEY,
                     nombre   TEXT,
                     apellido TEXT  NOT NULL,
                     movil    TEXT  NOT NULL

           );'''

    conn.execute(qry)

    qry = '''CREATE TABLE IF NOT EXISTS
                            ingresos_egresos
                    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                     dni TEXT NOT NULL,
                     fechahora_in TEXT  NOT NULL,
                     fechahora_out TEXT,
                     destino TEXT

           );'''

    conn.execute(qry)


if __name__ == '__main__':
    iniciar()

    """
    p = Persona('28123456', 'Álavarez', 'Ana', '02352-456789')

    ingresa_visita(p)
    """
    
    
    doc = input("Igrese dni> ")
    apellido = input("Igrese apellido> ")
    nombre = input("nombre> ")
    movil = input("móvil > ")

    p = Persona(doc, apellido, nombre, movil)

    destino = input("destino > ")
    
    ingresa_visita(p, destino)
    
    lista_visitantes_en_institucion()

#PRUEBAS DE CÓDIGO:

    #Catalina = Persona(23291834, "Vega", "Catalina", 14933183)
    #ingresa_visita(Catalina, "Mardel")
    #Tiziana = Persona(32131834, "Lanzani", "Tiziana", 92812183)
    #ingresa_visita(Tiziana, "Villa Gesell")
    #egresa_visita(32131834)
    #Pedro = Persona(19284732, "Ramirez", "Pedro", 29188371)
    #ingresa_visita(Pedro, "Narnia")
    #egresa_visita(8271321)
    #egresa_visita(213123)
 
    #busca_vistantes("2022-05-12T19", "NULL", "Narnia", 19284732)

    #conn = sqlite3.connect('recepcion.db')
    #q = f"""SELECT nombre FROM personas"""
    #resu = conn.execute(q)
    #r = resu.fetchall()
    #conn.close()