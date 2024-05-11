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
moves = 3
print("checking for an even number of gears")
while not stop:
    print(f"Searching {moves} moves.")
    for combo in product(allMoves, repeat=moves):
        cube = Cube()
        seq = TurnSequence(' '.join(combo))

        total = seq + XL + seq.reverse() + XL
        cube.executeSequence(total)

        #cornerChanges = countChanges(defaultCube.corners,cube.corners)
        #gearsChanges = countChanges(defaultCube.gears,cube.gears)
        # check if no gear changes
        #noGearsChanged = all(k==v.initialPosition for k,v in cube.gears.items())
        
        # it's better to check all the conditions in one for loop because it can
        # reduce the time to search by A LOT
        gearRots = 0
        noGearsChanged = True
        for k,v in cube.gears.items():
            #if v.rotation != 0: gearRots+=1
            if v.rotation == 180: gearRots+=1
            if k != v: noGearsChanged = False; break
        
        if (gearRots%2 == 0 and gearRots != 0) and noGearsChanged:
            print(seq)
            print(gearRots)

        # if it's a 3 cycle
        #if cornerChanges==0 and gearsChanges!=0 and gearsChanges<4:
        #    print(seq)

        """
        # if exactly two gears are rotated 90 or 270 degrees
        # and those two gears remain in their initial position
        summary = findGearRotations(cube)
        if len(summary[0])+len(summary[2]) == 2:
            rotatedGearsUnchanged = all(cube.gears[k].initialPosition == k for k in summary[0]+summary[2])

            #rotatedGearsUnchanged = all(k != v.initialPosition for k, v in cube.gears.items() 
            #                            if v.initialPosition in summary[0] or v.initialPosition in summary[2])
            if rotatedGearsUnchanged: print(seq)
        """
    moves+=1