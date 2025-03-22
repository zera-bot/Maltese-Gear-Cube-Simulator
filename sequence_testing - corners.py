from sim import Cube,Gear,Corner,Piece,Turn,TurnSequence, countChanges
from itertools import product
arrow = "->"


def findGearCycles(cube:Cube):
    corners = {k:v.initialPosition for k,v in cube.corners.items()}
    cycles = []
    for after,before in corners.items():
        if after != before:
            currentCycle = []
            currentKey = after
            currentCycle.append(currentKey)
            currentKey = corners[currentKey]
            
            while currentKey != after:
                currentCycle.append(currentKey)
                currentKey = corners[currentKey]
                
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

sequences = """R2 U2 F4 U2 L2""".split("\n")

final = ""
XL = TurnSequence("R4 D R4 D' R4")
XR = TurnSequence("R4 D' R4 D R4")

YL = TurnSequence("U")

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