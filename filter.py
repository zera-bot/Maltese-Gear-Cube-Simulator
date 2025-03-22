from sim import Cube,TurnSequence, countChanges

def findGearRotations(cube:Cube):
    list90 = []
    list180 = []
    list270 = []
    
    for v in cube.gears.values():
        if v.rotation == 90: list90.append(v.initialPosition)
        elif v.rotation == 180: list180.append(v.initialPosition)
        elif v.rotation == 270: list270.append(v.initialPosition)
        
    return [list90,list180,list270]

A = TurnSequence("R U R' U' R' F R F'")
Aprime = A.reverse()
XL = TurnSequence("R4 D R4 D' R4")
XR = TurnSequence("R4 D' R4 D R4")
W = TurnSequence("R4 U R4 U' R4 U R4 U' R4 U R4 U'")

defaultCube = Cube()

with open("rgc_algorithms.txt") as f:
    algs = [TurnSequence(k.split(";")[0]) for k in f.read().split("\n")[:-1]]


for alg in algs:
    cube = Cube()
    cube.executeSequence(alg)

    cornerChanges = countChanges(defaultCube.corners,cube.corners)
    pieceChanges = countChanges(defaultCube.pieces,cube.pieces)

    gearRots = 0
    gearRots90 = 0
    gearsChanged = 0
    noGearsChanged = True
    for k,v in cube.gears.items():
        if v.rotation != 0 and v.rotation != 180: gearRots90+=1
        if v.rotation == 180: gearRots+=1
        if k != v: 
            noGearsChanged = False
            gearsChanged+=1

    if cornerChanges == 0 and gearRots%2==0 and gearRots!=0 and gearRots90 == 0:
        print("Gear Rotation", alg)
    
    if cornerChanges == 0 and gearRots90%2==0:
        summary = findGearRotations(cube)
        allgood = False
        if (len(summary[0])+len(summary[2]))%2==0:
            # rotated gears have unchanged positions?
            allgood = all(cube.gears[k].initialPosition == k for k in summary[0]+summary[2])

        if allgood:
            print('90deg Gear Rotation', alg)
            
    

print(cube)
print("Corner changes: ",end='')
print(countChanges(Cube().corners,cube.corners))
print("Gear changes: ",end='')
print(countChanges(Cube().gears,cube.gears))