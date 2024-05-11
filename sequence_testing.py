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

sequences = """R U D'3 B
R U3 D3 F
R U' D' F
R U'2 R D
R U'2 R D3
R U'2 R D'
R U'2 R D'3
R U'3 D B
R D U'3 B
R D3 U3 F
R D' U' F
R D'2 L D
R D'2 L D3
R D'2 L D'
R D'2 L D'3
R D'3 U B
R F'2 L D
R F'2 L D3
R F'2 L D'
R F'2 L D'3
R B2 U4 L3
R B2 D4 L3
R B'2 R'3 F4
R B'2 R'3 B4
R4 F'3 L'2 F
R4 B'3 R'2 B
R'3 U4 F'2 L'
R'3 D4 F'2 L'
L U D'3 F
L U3 D3 B
L U' D' B
L U'2 L D
L U'2 L D3
L U'2 L D'
L U'2 L D'3
L U'3 D F
L D U'3 F
L D3 U3 B
L D' U' B
L D'2 R D
L D'2 R D3
L D'2 R D'
L D'2 R D'3
L D'3 U F
L F2 U4 R3
L F2 D4 R3
L F'2 L'3 F4
L F'2 L'3 B4
L B'2 R D
L B'2 R D3
L B'2 R D'
L B'2 R D'3
L4 F'3 L'2 F
L4 B'3 R'2 B
L'3 U4 B'2 R'
L'3 D4 B'2 R'
D R' U2 R'
D R' D2 L'
D R' B2 L'
D L' U2 L'
D L' D2 R'
D L' F2 R'
D F L'2 B
D F U'2 F
D F D'2 B
D B R'2 F
D B U'2 B
D B D'2 F
D3 R' U2 R'
D3 R' D2 L'
D3 R' B2 L'
D3 L' U2 L'
D3 L' D2 R'
D3 L' F2 R'
D3 F L'2 B
D3 F U'2 F
D3 F D'2 B
D3 B R'2 F
D3 B U'2 B
D3 B D'2 F
D' R' U2 R'
D' R' D2 L'
D' R' B2 L'
D' L' U2 L'
D' L' D2 R'
D' L' F2 R'
D' F L'2 B
D' F U'2 F
D' F D'2 B
D' B R'2 F
D' B U'2 B
D' B D'2 F
D'3 R' U2 R'
D'3 R' D2 L'
D'3 R' B2 L'
D'3 L' U2 L'
D'3 L' D2 R'
D'3 L' F2 R'
D'3 F L'2 B
D'3 F U'2 F
D'3 F D'2 B
D'3 B R'2 F
D'3 B U'2 B
D'3 B D'2 F
F3 U4 R2 B
F3 D4 R2 B
F4 R3 B2 R'
F4 L3 F2 L'
F' R2 B' D
F' R2 B' D3
F' R2 B' D'
F' R2 B' D'3
F' U D R'
F' U2 F' D
F' U2 F' D3
F' U2 F' D'
F' U2 F' D'3
F' U3 D' L'
F' U' D3 L'
F' U'3 D'3 R'
F' D U R'
F' D2 B' D
F' D2 B' D3
F' D2 B' D'
F' D2 B' D'3
F' D3 U' L'
F' D' U3 L'
F' D'3 U'3 R'
B3 U4 L2 F
B3 D4 L2 F
B4 R3 B2 R'
B4 L3 F2 L'
B' R2 B3 R4
B' R2 B3 L4
B' R'2 U4 F'3
B' R'2 D4 F'3
B' L2 F' D
B' L2 F' D3
B' L2 F' D'
B' L2 F' D'3
B' U D L'
B' U2 B' D
B' U2 B' D3
B' U2 B' D'
B' U2 B' D'3
B' U3 D' R'
B' U' D3 R'
B' U'3 D'3 L'
B' D U L'
B' D2 F' D
B' D2 F' D3
B' D2 F' D'
B' D2 F' D'3
B' D3 U' R'
B' D' U3 R'
B' D'3 U'3 L'""".split("\n")

sequences = """R3 U3 L
R3 D3 L
R' U3 F'
R' D' B'
L3 U3 R
L3 D3 R
L' U3 B'
L' D' F'
F U'3 R
F D L
F'3 U'3 B'
F'3 D'3 B'
B U'3 L
B D R
B'3 U'3 F'
B'3 D'3 F'""".split("\n")

final = ""
XL = TurnSequence("R4 D R4 D' R4")
XR = TurnSequence("R4 D' R4 D R4")

print(len(sequences))
for mini in sequences:
    A = TurnSequence(mini)
    Aprime = A.reverse()

    seq = (A + XL + Aprime + XL)

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