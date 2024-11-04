import threading as th
import time
import random
import os

params = {
    "m": 10,
    "n": 10,
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
    movimientos[numRoomba].append("U")
    
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
    movimientos[numRoomba].append("R")
    
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
    movimientos[numRoomba].append("D")
    
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
    movimientos[numRoomba].append("L")
    
    return True

def moverRoomba(pos, numRoomba):
    
    # mover arriba
    if not moverArriba(pos, numRoomba):
        # mover derecha
        if not moverDerecha(pos, numRoomba):
            # mover abajo
            if not moverAbajo(pos, numRoomba):
                # mover izquierda
                if not moverIzquierda(pos, numRoomba):
                    return
                
def printHabitacion():
    global habitacion
    
    os.system("clear")
    print("=== HABITACION ===")
    for row in habitacion:
        print(*row)
    
    print("=== HABITACION ===")
    
    print("")
    
def habitacionLimpia():
    global habitacion
    
    for row in habitacion:
        if "x" in row:
            return False
        
    return True
    
                
def roomba(posInicial, numRoomba, timeMax, velRoomba):
    global habitacion
    global limpio
    global endTime
    
    pos = posInicial.copy()
    iter = 0
    maxIter = int(timeMax / velRoomba)
    
    while not limpio:
        iter += 1
        if iter > maxIter:
            return
        
        #? print("{}: Estoy en {}: {}".format(numRoomba, pos, habitacion[pos[0]][pos[1]]))
        habitacion[pos[0]][pos[1]] = numRoomba
        printHabitacion()
        if limpio: break
        limpio = habitacionLimpia()
        
        moverRoomba(pos, numRoomba)
        time.sleep(velRoomba)
        
    if endTime == 0: endTime = time.time()

def roombas(params):
    global habitacion
    global habitacionInicial
    global movimientos
    global limpio
    global startTime
    global endTime
    
    listaRoombas = []
    habitacion = [["_" for _ in range(params["n"])] for _ in range(params["m"])]
    habitacionInicial = [["_" for _ in range(params["n"])] for _ in range(params["m"])]
    movimientos = {}
    limpio = False
    
    for _ in range(params["numSucio"] - 1):
        x, y = random.randint(0, params["m"]-1), random.randint(0, params["n"]-1)
        
        while habitacion[x][y] == "x" or (x == 0 and y == 0):
            x, y = random.randint(0, params["m"]-1), random.randint(0, params["n"]-1)
            
        habitacion[x][y] = "x"
        habitacionInicial[x][y] = "x"
    
    startTime = time.time()
    for k in range(params["numRoombas"]):
        numRoomba = "R" + str(k)
        movimientos[numRoomba] = []
        
        t = th.Thread(target=roomba, args=(params["posInicial"], numRoomba, params["segundosMax"], params["velocidadRoombas"]))
        listaRoombas.append(t)
        t.start()
        
        time.sleep(0.01)
       
def startInput():
    
    # m
    while True:
        m = input("M: ")
        try:
            if int(m) < 2 or int(m) > 10:
                print("Ingresar un valor de 2 a 10.")
            else:
                break
        except ValueError:
            print("Ingresar un valor numerico.")
    params["m"] = int(m)
    
    # n
    while True:
        n = input("N: ")
        try:
            if int(m) < 2 or int(m) > 10:
                print("Ingresar un valor de 2 a 10.")
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
            if int(tiempoMax) < 1 or int(tiempoMax) > 20:
                print("Ingresar un valor de 1 al 20.")
            else:
                break
        except ValueError:
            print("Ingresar un valor numerico.")
    params["segundosMax"] = int(tiempoMax)
        
#* main
startTime = 0
endTime = 0
os.system("clear")
startInput()
roombas(params)

# checar que haya terminado
timeIter = 0
while not limpio and timeIter < params["segundosMax"] + 0.5:
    time.sleep(1)
    timeIter += 1

os.system("clear")
print("=========== ANALISIS ===========")
print("TERMINADO:", limpio)

if limpio == False:
    tiempo = params["segundosMax"]
else:
    tiempo = endTime - startTime
    
print("- TIEMPO EN TERMINAR (s):", tiempo)
print("MOVIMIENTOS:", movimientos)
print("- MOVIMIENTOS EN TOTAL POR {} ROOMBAS: {}".format(params["numRoombas"], sum([len(movimientos[m]) for m in movimientos])))
print("\n=== HABITACION INICIAL ===")
for row in habitacionInicial:
    print(*row)

print("\n=== HABITACION FINAL ===")

for row in habitacion:
    print(*row)
    
