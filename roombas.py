from itertools import chain
import threading as th
import pandas as pd
import time
import random
import os

params = {
    "m": 9,
    "n": 9,
    "numRoombas": 2,
    "numSucio": 5,
    "posInicial": [0, 0],
    "segundosMax": 10,
    "velocidadRoombas": 1,
}

def moverArriba(pos, numRoomba):
    global habitacion
    
    max_x, max_y = len(habitacion) - 1, len(habitacion[0]) - 1
    pos_x, pos_y = pos
    
    # si se encuentra en el borde de arriba, no moverse
    if pos_x == 0:
        return False
    
    # si el siguiente paso esta limpio o hay otra roomba
    if habitacion[pos_x - 1][pos_y] == "o" or habitacion[pos_x - 1][pos_y][0] == "R":
        return False
    
    # hacer movimiento
    habitacion[pos_x][pos_y] = "o"
    habitacion[pos_x - 1][pos_y] = numRoomba
    
    # actualizar posicion
    pos[0] -= 1
    
    # log movimiento
    movimientos[numRoomba].append("Arriba")
    
    return True

def moverDerecha(pos, numRoomba):
    global habitacion
    global movimientos
    
    max_x, max_y = len(habitacion) - 1, len(habitacion[0]) - 1
    pos_x, pos_y = pos
    
    # si se encuentra en el borde de derecha, no moverse
    if pos_y == max_y:
        return False
    
    # si el siguiente paso esta limpio o hay otra roomba
    if habitacion[pos_x][pos_y + 1] == "o" or habitacion[pos_x][pos_y + 1][0] == "R":
        return False
    
    # hacer movimiento
    habitacion[pos_x][pos_y] = "o"
    habitacion[pos_x][pos_y + 1] = numRoomba
    
    # actualizar posicion
    pos[1] += 1
    
    # log movimiento
    movimientos[numRoomba].append("Derecha")
    
    return True

def moverAbajo(pos, numRoomba):
    global habitacion
    
    max_x, max_y = len(habitacion) - 1, len(habitacion[0]) - 1
    pos_x, pos_y = pos
    
    # si se encuentra en el borde de abajo, no moverse
    if pos_x == max_x:
        return False
    
    # si el siguiente paso esta limpio o hay otra roomba
    if habitacion[pos_x + 1][pos_y] == "o" or habitacion[pos_x + 1][pos_y][0] == "R":
        return False
    
    # hacer movimiento
    habitacion[pos_x][pos_y] = "o"
    habitacion[pos_x + 1][pos_y] = numRoomba
    
    # actualizar posicion
    pos[0] += 1
    
    # log movimiento
    movimientos[numRoomba].append("Abajo")
    
    return True

def moverIzquierda(pos, numRoomba):
    global habitacion
    
    max_x, max_y = len(habitacion) - 1, len(habitacion[0]) - 1
    pos_x, pos_y = pos
    
    # si se encuentra en el borde de izquierda, no moverse
    if pos_y == 0:
        return False
    
    # si el siguiente paso esta limpio o hay otra roomba
    if habitacion[pos_x][pos_y - 1] == "o" or habitacion[pos_x][pos_y - 1][0] == "R":
        return False
    
    # hacer movimiento
    habitacion[pos_x][pos_y] = "o"
    habitacion[pos_x][pos_y - 1] = numRoomba
    
    # actualizar posicion
    pos[1] -= 1
    
    # log movimiento
    movimientos[numRoomba].append("Izquierda")
    
    return True

def moverSE(pos, numRoomba):
    global habitacion
    
    max_x, max_y = len(habitacion) - 1, len(habitacion[0]) - 1
    pos_x, pos_y = pos
    
    # si se encuentra en borde derecha o borde abajo, no moverse
    if pos_x == max_x or pos_y == max_y:
        return False
    
    # si el siguiente paso esta limpio o hay otra roomba
    if habitacion[pos_x + 1][pos_y + 1] == "o" or habitacion[pos_x + 1][pos_y + 1][0] == "R":
        return False
    
    # hacer movimiento
    habitacion[pos_x][pos_y] = "o"
    habitacion[pos_x + 1][pos_y + 1] = numRoomba
    
    # actualizar posicion
    pos[0] += 1
    pos[1] += 1
    
    # log movimiento
    movimientos[numRoomba].append("Izquierda")
    
    return True

def moverRoomba(pos, numRoomba, tipoRoomba):
    
    #* clockwise roomba
    if tipoRoomba == "cw":
        if not moverArriba(pos, numRoomba):
            if not moverDerecha(pos, numRoomba):
                if not moverAbajo(pos, numRoomba):
                    if not moverIzquierda(pos, numRoomba):
                        if not moverSE(pos, numRoomba):
                            return
                    
    #* counter-clockwise roomba
    else:
        if not moverArriba(pos, numRoomba):
            if not moverAbajo(pos, numRoomba):
                if not moverDerecha(pos, numRoomba):
                    if not moverIzquierda(pos, numRoomba):
                        if not moverSE(pos, numRoomba):
                            return
                
def printHabitacion():
    global habitacion
    
    os.system("clear")
    print("=== HABITACION ===")
    for row in habitacion:
        for r in row:
            if r[0] == 'R':
                print(r, end=' ')
            else:
                print(r, end='  ')
        print("")
    
    print("")
    
def habitacionLimpia():
    global habitacion
    
    for row in habitacion:
        if "x" in row:
            return False
        
    return True
    
                
def roomba(posInicial, numRoomba, timeMax, velRoomba, tipoRoomba):
    global habitacion
    global limpio
    
    pos = posInicial.copy()
    iter = 0
    maxIter = int(timeMax / velRoomba)
    
    while not limpio:
        iter += 1
        if iter > maxIter:
            break
        
        #? print("{}: Estoy en {}: {}".format(numRoomba, pos, habitacion[pos[0]][pos[1]]))
        habitacion[pos[0]][pos[1]] = numRoomba
        printHabitacion()
        if limpio:
            break
        limpio = habitacionLimpia()
        
        moverRoomba(pos, numRoomba, tipoRoomba)
        time.sleep(velRoomba)
    

def roombas(params):
    global habitacion
    global movimientos
    global limpio
    
    listaRoombas = []
    habitacion = [["_" for _ in range(params["n"])] for _ in range(params["m"])]
    movimientos = {}
    limpio = False
    
    for _ in range(params["numSucio"] - 1):
        x, y = random.randint(0, params["m"]-1), random.randint(0, params["n"]-1)
        
        while habitacion[x][y] == "x" or (x == 0 and y == 0):
            x, y = random.randint(0, params["m"]-1), random.randint(0, params["n"]-1)
            
        habitacion[x][y] = "x"
    
    for k in range(1, params["numRoombas"] + 1):
        numRoomba = "R" + str(k)
        movimientos[numRoomba] = []
        if k % 2 == 0:
            tipoRoomba = 'cw'
        else:
            tipoRoomba = 'ccw'
        
        t = th.Thread(target=roomba,
                      args=(
                          params["posInicial"],
                          numRoomba, 
                          params["segundosMax"],
                          params["velocidadRoombas"],
                          tipoRoomba
                          ))
        listaRoombas.append(t)
        t.start()
        
        time.sleep(0.01)
       
def startInput():
    
    # m
    while True:
        m = input("M: ")
        try:
            if int(m) < 2 or int(m) > 15:
                print("Ingresar un valor de 2 a 15.")
            else:
                break
        except ValueError:
            print("Ingresar un valor numerico.")
    params["m"] = int(m)
    
    # n
    while True:
        n = input("N: ")
        try:
            if int(n) < 2 or int(n) > 15:
                print("Ingresar un valor de 2 a 15.")
            else:
                break
        except ValueError:
            print("Ingresar un valor numerico.")
    params["n"] = int(n)
    
    # numRoombas
    while True:
        numRoombas = input("Numero de agentes: ")
        try:
            if int(numRoombas) < 1 or int(numRoombas) > 10:
                print("Ingresar un valor de 1 a 10.")
            else:
                break
        except ValueError:
            print("Ingresar un valor numerico.")
    params["numRoombas"] = int(numRoombas)
    
    # celdas sucias
    while True:
        sucias = input("Porcentaje de celdas sucias (0-1): ")
        try:
            if float(sucias) < 0 or float(sucias) > 1:
                print("Ingresar un valor de 0 a 1.")
            else:
                break
        except ValueError:
            print("Ingresar un valor numerico.")
    params["numSucio"] = int(params["m"] * params["n"] * float(sucias))
    
    # tiempo maximo
    while True:
        tiempoMax = input("Tiempo máximo de ejecución (s): ")
        try:
            if int(tiempoMax) < 1 or int(tiempoMax) > 60:
                print("Ingresar un valor de 1 al 60.")
            else:
                break
        except ValueError:
            print("Ingresar un valor numerico.")
    params["segundosMax"] = int(tiempoMax)
        
#* main
def main():
    startTime = 0
    endTime = 0
    os.system("clear")
    # startInput()
    startTime = time.time()
    roombas(params)

    # checar que haya terminado
    timeIter = 0
    while not limpio and timeIter < params["segundosMax"]:
        time.sleep(1)
        timeIter += 1

    endTime = time.time()

    print("=========== ANALISIS ===========")

    # analisis tiempo

    if limpio == False:
        tiempo = params["segundosMax"]
    else:
        tiempo = endTime - startTime
        
    print(f"+ Tiempo en terminar: {tiempo:.3f}s")
    print("  - Terminado:", limpio)

    # analisis limpio
    habitacion_plana = list(chain.from_iterable(habitacion))
    celdas_limpias = len([x for x in habitacion_plana if x == 'o'])

    print("+ Celdas limpias: {:.3f}%".format(celdas_limpias / (len(habitacion_plana) - params["numRoombas"]) * 100))

    # analisis movimientos
    print(f"+ Movimientos en total por {params['numRoombas']} roomba{'s:' if params['numRoombas'] != 1 else ':'} {sum([len(movimientos[m]) for m in movimientos])}")
    print("  - Movimientos:")
    for k in movimientos:
        print(f"    {k}: {movimientos[k]}")
    
    return tiempo
        
settings = [
    [3, 3, 1],
    [3, 3, 2],
    [3, 3, 3],
    [4, 4, 1],
    [4, 4, 2],
    [4, 4, 3],
    [5, 5, 1],
    [5, 5, 2],
    [5, 5, 3],
]

times_df = pd.DataFrame(columns=['m', 'n', 'numRoombas', 'tiempo'])

for sett in settings:
    params["m"] = sett[0]
    params["n"] = sett[1]
    params["numRoombas"] = sett[2]
    tiempo = main()
    
    times_df = times_df._append(
        {'m': sett[0],
        'n': sett[1],
        'numRoombas': sett[2],
        'tiempo': tiempo},
        ignore_index=True)
    
times_df.to_csv('times.csv')