from sim import Cube,Gear,Corner,Piece,Turn,TurnSequence, countChanges
from itertools import product
arrow = "->"


def findGearCycles(cube:Cube):
    pieces = {k:v.initialPosition for k,v in cube.pieces.items()}
    cycles = []
    for after,before in pieces.items():
        if after != before:
            currentCycle = []
            currentKey = after
            currentCycle.append(currentKey)
            currentKey = pieces[currentKey]
            
            while currentKey != after:
                currentCycle.append(currentKey)
                currentKey = pieces[currentKey]
                
            #currentCycle.append(currentKey)
            cycles.append(list(reversed(currentCycle)))
    
    # delete duplicate cycles
    for ind,cycle in enumerate(reversed(cycles)):
        for jind,other in enumerate(cycles):
            if {*cycle} == {*other}:
                cycles.remove(other)
    
    return cycles
    
def cyclesString(cube:Cube):
    cycles = ", ".join([f" {arrow} ".join(k) for k in findGearCycles(cube)])
    cycles+="; "
        
    return cycles

sequences = """R2 U3 R4 U R'2
R2 U3 R4 U3 B2
R2 U3 R4 U' B2
R2 U3 R4 U'3 R'2
R2 U3 L4 U R'2
R2 U3 L4 U3 B2
R2 U3 L4 U' B2
R2 U3 L4 U'3 R'2
R2 U3 F4 U R'2
R2 U3 F4 U3 B2
R2 U3 F4 U' B2
R2 U3 F4 U'3 R'2
R2 U3 B4 U R'2
R2 U3 B4 U3 B2
R2 U3 B4 U' B2
R2 U3 B4 U'3 R'2
R2 U' R4 U R'2
R2 U' R4 U3 B2
R2 U' R4 U' B2
R2 U' R4 U'3 R'2
R2 U' L4 U R'2
R2 U' L4 U3 B2
R2 U' L4 U' B2
R2 U' L4 U'3 R'2
R2 U' F4 U R'2
R2 U' F4 U3 B2
R2 U' F4 U' B2
R2 U' F4 U'3 R'2
R2 U' B4 U R'2
R2 U' B4 U3 B2
R2 U' B4 U' B2
R2 U' B4 U'3 R'2
R2 D3 R4 D R'2
R2 D3 R4 D3 F2
R2 D3 R4 D' F2
R2 D3 R4 D'3 R'2
R2 D3 L4 D R'2
R2 D3 L4 D3 F2
R2 D3 L4 D' F2
R2 D3 L4 D'3 R'2
R2 D3 F4 D R'2
R2 D3 F4 D3 F2
R2 D3 F4 D' F2
R2 D3 F4 D'3 R'2
R2 D3 B4 D R'2
R2 D3 B4 D3 F2
R2 D3 B4 D' F2
R2 D3 B4 D'3 R'2
R2 D' R4 D R'2
R2 D' R4 D3 F2
R2 D' R4 D' F2
R2 D' R4 D'3 R'2
R2 D' L4 D R'2
R2 D' L4 D3 F2
R2 D' L4 D' F2
R2 D' L4 D'3 R'2
R2 D' F4 D R'2
R2 D' F4 D3 F2
R2 D' F4 D' F2
R2 D' F4 D'3 R'2
R2 D' B4 D R'2
R2 D' B4 D3 F2
R2 D' B4 D' F2
R2 D' B4 D'3 R'2
L2 U3 R4 U L'2
L2 U3 R4 U3 F2
L2 U3 R4 U' F2
L2 U3 R4 U'3 L'2
L2 U3 L4 U L'2
L2 U3 L4 U3 F2
L2 U3 L4 U' F2
L2 U3 L4 U'3 L'2
L2 U3 F4 U L'2
L2 U3 F4 U3 F2
L2 U3 F4 U' F2
L2 U3 F4 U'3 L'2
L2 U3 B4 U L'2
L2 U3 B4 U3 F2
L2 U3 B4 U' F2
L2 U3 B4 U'3 L'2
L2 U' R4 U L'2
L2 U' R4 U3 F2
L2 U' R4 U' F2
L2 U' R4 U'3 L'2
L2 U' L4 U L'2
L2 U' L4 U3 F2
L2 U' L4 U' F2
L2 U' L4 U'3 L'2
L2 U' F4 U L'2
L2 U' F4 U3 F2
L2 U' F4 U' F2
L2 U' F4 U'3 L'2
L2 U' B4 U L'2
L2 U' B4 U3 F2
L2 U' B4 U' F2
L2 U' B4 U'3 L'2
L2 D3 R4 D L'2
L2 D3 R4 D3 B2
L2 D3 R4 D' B2
L2 D3 R4 D'3 L'2
L2 D3 L4 D L'2
L2 D3 L4 D3 B2
L2 D3 L4 D' B2
L2 D3 L4 D'3 L'2
L2 D3 F4 D L'2
L2 D3 F4 D3 B2
L2 D3 F4 D' B2
L2 D3 F4 D'3 L'2
L2 D3 B4 D L'2
L2 D3 B4 D3 B2
L2 D3 B4 D' B2
L2 D3 B4 D'3 L'2
L2 D' R4 D L'2
L2 D' R4 D3 B2
L2 D' R4 D' B2
L2 D' R4 D'3 L'2
L2 D' L4 D L'2
L2 D' L4 D3 B2
L2 D' L4 D' B2
L2 D' L4 D'3 L'2
L2 D' F4 D L'2
L2 D' F4 D3 B2
L2 D' F4 D' B2
L2 D' F4 D'3 L'2
L2 D' B4 D L'2
L2 D' B4 D3 B2
L2 D' B4 D' B2
L2 D' B4 D'3 L'2""".split("\n")

final = ""
XL = TurnSequence("R4 D R4 D' R4")
XR = TurnSequence("R4 D' R4 D R4")

YL = TurnSequence("R4 D R4 D' R4")

print(len(sequences))
for mini in sequences:
    A = TurnSequence(mini)
    Aprime = A.reverse()

    seq = A + YL + Aprime + YL.reverse()
    #seq = (A + XL + Aprime + Aprime + XL + A)

    cube = Cube()
    cube.executeSequence(seq)
    
    final+=f"\n{str(A)} {str(YL)} {str(Aprime)} {str(YL.reverse())} -- " + cyclesString(cube)

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