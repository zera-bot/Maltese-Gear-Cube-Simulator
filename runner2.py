from sim import Cube,TurnSequence, countChanges

A = TurnSequence("R U R' U' R' F R F'")
Aprime = A.reverse()
XL = TurnSequence("R4 D R4 D' R4")
XR = TurnSequence("R4 D' R4 D R4")
W = TurnSequence("R4 U R4 U' R4 U R4 U' R4 U R4 U'")

seq = Aprime + XR + A + A + XR + Aprime
seq = TurnSequence("R")

cube = Cube()
cube.executeSequence(seq)

print(cube)
print("Corner changes: ",end='')
print(countChanges(Cube().corners,cube.corners))
print("Gear changes: ",end='')
print(countChanges(Cube().gears,cube.gears))