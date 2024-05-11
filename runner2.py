from sim import Cube,TurnSequence, countChanges

A = TurnSequence("U2")
Aprime = A.reverse()
XL = TurnSequence("R4 D R4 D' R4")

seq = A + XL + Aprime + XL
seq = TurnSequence("R2 U3 R'2 U3'")

cube = Cube()
cube.executeSequence(seq)

print(cube)
print("Corner changes: ",end='')
print(countChanges(Cube().corners,cube.corners))
print("Gear changes: ",end='')
print(countChanges(Cube().gears,cube.gears))