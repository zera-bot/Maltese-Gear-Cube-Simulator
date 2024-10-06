from sim import Cube,Gear,Corner,Piece,Turn,TurnSequence, countChanges
from itertools import product
arrow = "->"


def findGearCycles(cube:Cube):
    gears = {k:v.initialPosition for k,v in cube.gears.items()}
    cycles = []
    for after,before in gears.items():
        if after != before:
            currentCycle = []
            currentKey = after
            currentCycle.append(currentKey)
            currentKey = gears[currentKey]
            
            while currentKey != after:
                currentCycle.append(currentKey)
                currentKey = gears[currentKey]
                
            #currentCycle.append(currentKey)
            cycles.append(list(reversed(currentCycle)))
    
    # delete duplicate cycles
    indicesToRemove = []
    for ind,cycle in enumerate(reversed(cycles)):
        for jind,other in enumerate(cycles):
            if {*cycle} == {*other}:
                cycles.remove(other)
    
    return cycles
    
def findGearRotations(cube:Cube):
    list90 = []
    list180 = []
    list270 = []
    
    for v in cube.gears.values():
        if v.rotation == 90: list90.append(v.initialPosition)
        elif v.rotation == 180: list180.append(v.initialPosition)
        elif v.rotation == 270: list270.append(v.initialPosition)
        
    return [list90,list180,list270]
    
def cyclesString(cube:Cube):
    cycles = ", ".join([f" {arrow} ".join(k) for k in findGearCycles(cube)])
    cycles+="; "
    rots = findGearRotations(cube)
    
    if len(rots[0]) > 0:
        r = "" + ",".join(rots[0]) + " rotates 90; "
        cycles+= r
    if len(rots[1]) > 0:
        r = "" + ", ".join(rots[1]) + " rotates 180; "
        cycles+= r
    if len(rots[2]) > 0:
        r = "" + ", ".join(rots[2]) + " rotates -90; "
        cycles+= r
        
    return cycles

sequences = """R F' R4 F R'""".split("\n")

final = ""
XL = TurnSequence("R4 D R4 D' R4")
XR = TurnSequence("R4 D' R4 D R4")

print(len(sequences))
for mini in sequences:
    A = TurnSequence(mini)
    Aprime = A.reverse()

    #seq = (A + XL + Aprime + XL)
    seq = (A + XL + Aprime + Aprime + XL + A)

    cube = Cube()
    cube.executeSequence(seq)
    
    final+=f"\n{str(A)} XL {str(Aprime)} XL -- " + cyclesString(cube)

with open("summary.txt", "w") as f:
    f.write(final)

"""
final+="A XL A' XL"
print("A XL A' XL")
for mini in sequences:
    A = TurnSequence(mini)
    Aprime = A.reverse()

    seq = A + XL + Aprime + XL

    cube = Cube()
    cube.executeSequence(seq)
    
    final+=f"\n{str(A)} XL {str(Aprime)} XL -- " + cyclesString(cube)
    
final+="\n A' XL A XL"
print("A' XL A XL")
for mini in sequences:
    A = TurnSequence(mini)
    Aprime = A.reverse()

    seq = Aprime + XL + A + XL

    cube = Cube()
    cube.executeSequence(seq)
    
    final+=f"\n{str(Aprime)} XL {str(A)} XL -- " + cyclesString(cube)

cube = Cube()
cube.executeSequence(TurnSequence("R2 U2 R4 U2' R2"))
print(cyclesString(cube))

#
#with open("summary.txt", "w") as f:
#    f.write(final)
"""