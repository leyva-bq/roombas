import threading as th
import time
import random

params = {
    "numRoombas": 1,
    "m": 3,
    "n": 2,
    "numSucio": 1,
    "posInicial": [0, 0],
    "segundosMax": 5
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
    
    return True

def moverDerecha(pos, numRoomba):
    global habitacion
    
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
    
    return True

def moverRoomba(pos, numRoomba):
    
    # mover arriba
    if not moverArriba(pos, numRoomba):
        # mover derecha
        if not moverDerecha(pos, numRoomba):
            # mover abajo
            if not moverAbajo(pos, numRoomba):
                # mover izquierda
                moverIzquierda(pos, numRoomba)
                
def roomba(posInicial, numRoomba):
    global habitacion
    pos = posInicial
    
    print("Estoy en {}: {}".format(pos, habitacion[pos[0]][pos[1]]))
    
    moverRoomba(pos, numRoomba)
    
    time.sleep(1)
    
    return

def roombas(params):
    
    listaRoombas = []
    global habitacion
    habitacion = [["_" for _ in range(params["n"])] for _ in range(params["m"])]
    
    habitacion[1][1] = "x"
    
    for k in range(params["numRoombas"]):
        t = th.Thread(target=roomba, args=(params["posInicial"], params["numRoombas"]))
        listaRoombas.append(t)
        t.start()
        
roombas(params)