import time
from sim import Cube,TurnSequence, countChanges
from itertools import product

def findGearRotations(cube:Cube):
    list90 = []
    list180 = []
    list270 = []
    
    for v in cube.gears.values():
        if v.rotation == 90: list90.append(v.initialPosition)
        elif v.rotation == 180: list180.append(v.initialPosition)
        elif v.rotation == 270: list270.append(v.initialPosition)
        
    return [list90,list180,list270]

W = TurnSequence("R4 U R4 U' R4 U R4 U' R4 U R4 U'")


allMoves = []
for i in ["R","L","U","D","F","B"]:
    allMoves.append(i)
    allMoves.append(i+"2")
    allMoves.append(i+"3")
    allMoves.append(i+"4")
    allMoves.append(i+"'")
    allMoves.append(i+"'2")
    allMoves.append(i+"'3")


defaultCube = Cube()

stop = False
moves = 1
print("checking for an even number of gears")
while not stop:
    print(f"Searching {moves} moves.")
    start_time = time.time()
    for combo in product(allMoves, repeat=moves):
        cube = Cube()
        seq = TurnSequence(' '.join(combo))

        total = seq + W + seq.reverse()
        cube.executeSequence(total)

        pieceChanges = countChanges(defaultCube.pieces,cube.pieces)

        otherCond = None
        for k,v in cube.pieces.items():
            misplacedCenters = 0
            if len(v.initialPosition)==1:
                if v.initialPosition != k: misplacedCenters+=1
            else:
                if v.rotation %180 != 0: otherCond = False

        if otherCond == None:
            otherCond = misplacedCenters == 2


        if pieceChanges == 4 and cube.pieces["FU"].initialPosition == "RU":
            print(seq)

        
    print(f"Took {str(time.time()-start_time)} seconds.")
    moves+=1