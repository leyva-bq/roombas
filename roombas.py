import threading as th
import time
import random

params = {
    "numRoombas": 2,
    "m": 5,
    "n": 5,
    "numSucio": 2,
    "posInicial": [0, 0],
    "segundosMax": 10,
    "velocidadRoombas": 0.5
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
        
        
        print("{}: Estoy en {}: {}".format(numRoomba, pos, habitacion[pos[0]][pos[1]]))
        habitacion[pos[0]][pos[1]] = numRoomba
        printHabitacion()
        if limpio: break
        limpio = habitacionLimpia()
        
        moverRoomba(pos, numRoomba)
        time.sleep(velRoomba)
        
    endTime = time.time()

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
    
    for _ in range(params["numSucio"]):
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
        
        time.sleep(params["velocidadRoombas"] / params["numRoombas"])
        
#* main
startTime = 0
endTime = 0
roombas(params)

time.sleep(params["segundosMax"] + 1)

print("=========== ANALISIS ===========")
print("TERMINADO:", limpio)

if limpio == False:
    tiempo = "N/A"
else:
    tiempo = endTime - startTime
    
print("- TIEMPO EN TERMINAR (s):", tiempo)
print("MOVIMIENTOS:", movimientos)
print("\n=== HABITACION INICIAL ===")
for row in habitacionInicial:
    print(*row)

print("\n=== HABITACION FINAL ===")

for row in habitacion:
    print(*row)
    
