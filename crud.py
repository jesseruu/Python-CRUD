import psycopg2 as pg 
from datetime import datetime

conn = pg.connect(database = "postgres", user = "postgres", password = "")
enl = conn.cursor()

def create_table():
    sql = '''CREATE TABLE ESTUDIANTES(
        Codigo VARCHAR(15),
        nombre VARCHAR(20),
        Apellido VARCHAR(20),
        Edad INT,
        Programa VARCHAR(20))'''

    try:
        enl.execute(sql)
        enl.execute("ALTER TABLE ESTUDIANTES ADD PRIMARY KEY(codigo)")
        conn.commit()
        print("Tabla creada correctamente")
    except:
        conn.rollback()
        print("La tabla ya ha sido creada")
        
op = 0

def code_generator(program):
    aux = datetime.now()

    if program == "SISTEMAS":
        code = "55"
    elif program == "MECANICA":
        code = "66"
    elif program == "INDUSTRIAL":
        code = "77"
    elif program == "AMBIENTAL":
        code = "88"

    code = code + aux.strftime("%y%H%d%S")
    return code

def pg_read():

    global sql_select, code_search
    option = input('T = Todos \nU= Uno'
                   '\n¿Que registros desea mostrar? [T/u]:')

    if option == 'T' or option =='t':
        sql_select = "SELECT * FROM ESTUDIANTES"
        enl.execute(sql_select)

    elif option == 'U' or option == 'u':
        sql_select = "SELECT * FROM ESTUDIANTES WHERE codigo = %s;"
        code_search = input("Ingrese el codigo del estudiante a consultar:")
        enl.execute(sql_select,(code_search,))


    imprim_regist = enl.fetchall()

    if imprim_regist:
        for i in imprim_regist:
            print(i) 
    if not imprim_regist:
        print("El estudiante no existe")
    
    

def pg_create(name, lastname, age, program):
    sql_insert = '''INSERT INTO ESTUDIANTES (codigo, nombre, apellido, edad, programa)
                    VALUES (%s, %s, %s, %s, %s);'''
    
    codigoG = code_generator(program)

    enl.execute(sql_insert, (codigoG, name,lastname,age,program))
    conn.commit()
    print("Estudiante registrado")

def pg_update():

    global sql_update, modi

    cod = input("Digite el codigo del estudiante:")
    option = input('\nN = Nombre \nA = Apellido \nE= Edad \nPrograma'
                '\nSeleccione el registro que desea actualizar: [N,A,E,P]:')
    
    if option == 'n' or option == 'N':
        sql_update = "UPDATE ESTUDIANTES SET nombre = %s WHERE codigo = %s;"
        modi = input("Actualice el nombre del estudiante:").capitalize()

    elif option == 'A' or option == 'a':
        sql_update = "UPDATE ESTUDIANTES SET apellido = %s WHERE codigo = %s;"
        modi = input("Actualice el apellido de estudiante:").capitalize

    elif option == 'E' or option == 'e':
        sql_update = "UPDATE ESTUDIANTES SET edad = %s WHERE codigo = %s;"
        modi = int(input("Actualice la edad del estudiante:"))

    elif option == 'P' or option == 'p':
        sql_update = "UPDATE ESTUDIANTES SET programa = %s WHERE codigo = %s;"
        modi = input("ACtualice el programa:").upper()

    else:
        print("Opcion no valida")
        pg_update()

    enl.execute(sql_update, (modi, cod,))
    enl.execute("SELECT * FROM ESTUDIANTES WHERE codigo = %s", (cod,))
    
    try:
        enl.fetchone()
        conn.commit()
    except:
        conn.rollback()
        print("El registro no existe")   

def pg_delete():
    sql_select_elim = "DELETE FROM ESTUDIANTES WHERE codigo = %s;"
    select_registro = input("Ingrese el codigo del registro a eliminar:")

    enl.execute(sql_select_elim,(select_registro,))
    
    try:
        enl.fetchone()
        conn.commit()
    except:
        conn.rollback()
        print("El registro no existe")   

while op != 6:

    op = int(input("Seleccione una opcion:"))

    if op == 1:
        create_table()

    elif op == 2:
        name = input("Ingrese el nombre:").capitalize()
        lastname = input("Ingrese el nombre:").capitalize()
        age = int(input("Ingrese el nombre:"))
        program = input("Ingrese el nombre:").upper()
        
        pg_create(name,lastname,age,program)

    elif op == 3:

        #code_search = input("Ingrese el codigo del registro a consultar:")
        pg_read()

    elif op == 4:
        pg_update()

    elif op == 5:
        pg_delete()

    elif op == 6:
        conn.close()
        print("Cerrando conexion con la base de datos...")

    else:
        print("Digite una opcion valida")

