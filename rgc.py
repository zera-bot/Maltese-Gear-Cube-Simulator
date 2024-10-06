import time
from sim import Cube,TurnSequence, countChanges
from itertools import product

def non_repeating_product(allMoves, moves):
    for combo in product(allMoves, repeat=moves):
        if all(combo[i][0] != combo[i-1][0] for i in range(1, len(combo))):
            yield combo

XL = TurnSequence("R4 D R4 D' R4")

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
moves = 4
#print("checking for an even number of gears")
while not stop:
    firstTwoMoves = ""

    print(f"Searching {moves} moves.")
    start_time = time.time()
    for combo in non_repeating_product(allMoves, moves): #product(allMoves, repeat=moves):
        if combo[0][0] == "R": continue # just for this one which has R at the start

        k = ' '.join(combo[0:2])
        if k != firstTwoMoves:
            firstTwoMoves = k
            print(f"Checking sequences with first two moves {firstTwoMoves}")
            

        cube = Cube()
        seq = TurnSequence("R " + ' '.join(combo))

        total = seq + XL + seq.reverse() + XL
        #total = seq + XL + seq.reverse() + seq.reverse() + XL + seq
        cube.executeSequence(total)

        cornerChanges = countChanges(defaultCube.corners,cube.corners)
        gearsChanges = countChanges(defaultCube.gears,cube.gears)

        gearRots = 0
        noGearsChanged = True
        for k,v in cube.gears.items():
            #if v.rotation != 0: gearRots+=1
            if v.rotation == 180: gearRots+=1
            if k != v: noGearsChanged = False; break # remove break for other conditions


        if cornerChanges == 0 and gearRots%2==0 and gearRots!=0:# and noGearsChanged:
            print("-- Gear Rotations Found: ", end="")
            print(seq, end="")
            print(" --")

        #if it's a 3 cycle
        if cornerChanges==0 and gearsChanges!=0 and gearsChanges<4:
            print("-- 3-cycle Found: ", end="")
            print(seq, end="")
            print(" --")

    print(f"Took {str(time.time()-start_time)} seconds.")
    moves+=1