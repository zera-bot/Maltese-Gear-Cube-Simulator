import time
from sim import Cube, TurnSequence, countChanges
from itertools import product

def non_repeating_product(allMoves, moves, disallowAdjacentOpposites=False, starting = None):
    # I KNOW this function is REALLY bad, im so sorry :sob: but it should be
    # more optimized to the specific condition you use it in

    opposites = {"R":"L", "L":"R", "U":"D", "D":"U", "F":"B", "B":"F"}
    if starting:
        start = False
        if not disallowAdjacentOpposites:
            for combo in product(allMoves, repeat=moves):
                if all(combo[i][0] != combo[i-1][0] for i in range(1, len(combo))):
                    if not start:
                        if ' '.join(combo).startswith(starting): start = True
                        else: continue
                        
                    yield combo
        else:
            for combo in product(allMoves, repeat=moves):
                if all(combo[i][0] != combo[i-1][0] for i in range(1, len(combo))) and all(opposites[combo[i][0]] != combo[i-1][0] for i in range(1, len(combo))):
                    if not start:
                        if str(combo) == starting: start = True
                        else: continue
                        
                    yield combo
    else:
        if not disallowAdjacentOpposites:
            for combo in product(allMoves, repeat=moves):
                if all(combo[i][0] != combo[i-1][0] for i in range(1, len(combo))):
                    yield combo
        else:
            for combo in product(allMoves, repeat=moves):
                if all(combo[i][0] != combo[i-1][0] for i in range(1, len(combo))) and all(opposites[combo[i][0]] != combo[i-1][0] for i in range(1, len(combo))):
                    yield combo

def findGearRotations(cube:Cube):
    list90 = []
    list180 = []
    list270 = []
    
    for v in cube.gears.values():
        if v.rotation == 90: list90.append(v.initialPosition)
        elif v.rotation == 180: list180.append(v.initialPosition)
        elif v.rotation == 270: list270.append(v.initialPosition)
        
    return [list90,list180,list270]

XL = TurnSequence("R4 D R4 D' R4")
XR = TurnSequence("R4 D' R4 D R4")

YL = TurnSequence("R4")

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
moves = 3

def addToFile(alg, desc=""):
    with open("rgc_algorithms.txt", "a") as f:
        f.write(str(alg) + "; " + desc + "\n")
    with open("rgc_algorithms_raw.txt", "a") as f1:
        f1.write(str(alg)+"\n")

def start(checkpoint = None):
    global defaultCube, stop, moves, allMoves
    while not stop:
        firstMoves = ""

        print(f"Searching {moves} moves.")
        start_time = time.time()
        for combo in non_repeating_product(allMoves, moves, starting=checkpoint, disallowAdjacentOpposites=True): #product(allMoves, repeat=moves):

            k = ' '.join(combo[0])
            if k != firstMoves:
                firstMoves = k
                print(f"Checking sequences with first moves {firstMoves}")

            #if combo[0][0] == "R" or combo[0][0] == "L": continue # just for this one
                

            cube = Cube()
            seq = TurnSequence(' '.join(combo))
            total = seq + YL + seq.reverse() + YL.reverse()
            #total = seq + XL + seq.reverse() + seq.reverse() + XL + seq
            cube.executeSequence(total)

            cornerChanges = countChanges(defaultCube.corners,cube.corners)
            pieceChanges = countChanges(defaultCube.pieces,cube.pieces)
            #gearsChanges = countChanges(defaultCube.gears,cube.gears)

            gearRots = 0
            gearRots90 = 0
            gearsChanged = 0
            noGearsChanged = True
            for k,v in cube.gears.items():
                if v.rotation != 0 and v.rotation != 180: gearRots90+=1
                if v.rotation == 180: gearRots+=1
                if k != v.initialPosition: 
                    noGearsChanged = False
                    gearsChanged+=1

            """# 180-degree Gear Rotations
            if cornerChanges == 0 and gearRots%2==0 and gearRots!=0 and gearRots90 == 0:
                if noGearsChanged:
                    print("-- Pure Gear Rotations Found: ", end="")
                    print(seq, end="")
                    print(" --")

                    addToFile(str(seq), "Pure Gear Rotation")
                elif gearRots <= 2:
                    print("-- Gear Rotations Found: ", end="")
                    print(seq, end="")
                    print(" --")

                    addToFile(str(seq), f"Gear Rotation ({str(gearRots)})")"""

            # 90-degree Gear Rotations
            if cornerChanges == 0 and gearRots90%2==0 and gearRots90 != 0:
                summary = findGearRotations(cube)
                rotatedGearsUnchanged = False
                if len(summary[0])+len(summary[2]) == 2:
                    # rotated gears have unchanged positions?
                    rotatedGearsUnchanged = all(cube.gears[k].initialPosition == k for k in summary[0]+summary[2])
                    
                if noGearsChanged:
                    print("-- Pure 90-degree Gear Rotations Found: ", end="")
                    print(seq, end="")
                    print(" --")

                    addToFile(str(seq), "90-degree Gear Rotation")
                elif gearRots90 == 2 and rotatedGearsUnchanged:
                    print("-- 90-degree Gear Rotations Found: ", end="")
                    print(seq, end="")
                    print(" --")

                    addToFile(str(seq), f"90-degree Gear Rotation ({str(gearRots90)})")

            #if it's a 3 cycle
            """if cornerChanges == 0 and not noGearsChanged and gearsChanged < 4:
                print("-- 3-cycle Found: ", end="")
                print(seq, end="")
                print(" --")
                
                addToFile(str(seq), "Single Gear 3-Cycle")"""
            
            # Other cycles
            if cornerChanges == 0 and noGearsChanged and pieceChanges > 0:
                if pieceChanges %3 == 0:
                    print("-- Piece 3-cycle Found: ", end="")
                    print(f"{seq} ({pieceChanges})", end="")
                    print(" --")

                    addToFile(str(seq), f"Piece 3-Cycle ({pieceChanges})")
                elif pieceChanges == 4: #check if we have a pure swap (center swap + 1 edge swap)
                    for k,v in cube.pieces.items():
                        if len(k) != len(v.initialPosition) and k != v.initialPosition:
                            print("-- Piece Swap Found: ", end="")
                            print(seq, end="")
                            print(" --")

                            addToFile(str(seq), f"Piece Swap")

            if cornerChanges != 0 and gearRots == 0 and noGearsChanged and pieceChanges == 0:
                print("-- Corner Cycle 3-cycle Found (WHAT): ", end="")
                print(seq, end="")
                print(" --")

                addToFile(str(seq), f"Corner 3-Cycle ({cornerChanges})")


        print(f"Took {str(time.time()-start_time)} seconds.")
        moves+=1

start()