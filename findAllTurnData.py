import json
from r_turn_data import *
from sim import *

# The purpose of this script is to take the turn_data script 
# (which only contains data on the R turn) and output a lookup dictionary
# that has data for all of the 6 different turns.

finalTurnData = {}

x_rot = ["F","U","B","D"]
y_rot = ["R","F","L","B"]
z_rot = ["U","R","D","L"]

def rotateAxes(origin,axes:list):
    """
    Format of `axes` is something like the following:
    `[["y",1], ["x",-1], ["y",2]]`
    """

    rotations = {"x": x_rot, "y": y_rot, "z": z_rot}

    prime = origin
    for axis, shift in axes:
        primeList = list(prime)
        l = rotations.get(axis)  # Get the corresponding rotation list
        
        if l:  # Only proceed if axis is valid
            l_len = len(l)  # Cache the length of the rotation list
            
            for charInd, char in enumerate(primeList):
                if char in l:
                    index = l.index(char)
                    new_index = (index + shift) % l_len
                    primeList[charInd] = l[new_index]

        prime = "".join(primeList)

    return prime

def generate(turn : Turn, data : dict):
    sampleCube = Cube()

    tCorners = rTurnCorners.copy()
    tPieces = rTurnPieces.copy()
    tGears = rTurnGears.copy()
    tPieceRot = rTurnPieceRotations.copy()
    tGearRot = rTurnGearRotations.copy()

    # transform R lists
    rotAxis = None
    if turn.name == "R":
        # rotate all applicable lists by nothing
        rotAxis = [["x",0]]
    if turn.name == "F": 
        # rotate all applicable lists by the sequence ( y )
        rotAxis = [["y",1]]
    elif turn.name == "B":
        # rotate all applicable lists by the sequence ( y' )
        rotAxis = [["y",-1]]
    elif turn.name == "L":
        # rotate all applicable lists by the sequence ( y2 )
        rotAxis = [["y",2]]
    elif turn.name == "U":
        # rotate all applicable lists by the sequence ( z' )
        rotAxis = [["z",-1]]
    elif turn.name == "D":
        # rotate all applicable lists by the sequence ( z )
        rotAxis = [["z",1]]

    tCorners = [sampleCube.adjust(rotateAxes(k,rotAxis),Corner) for k in tCorners]
    tPieces = [ [sampleCube.adjust(rotateAxes(j,rotAxis),Piece) for j in k] for k in tPieces ]
    tGears = [ [rotateAxes(j,rotAxis) for j in k] for k in tGears ]
    tPieceRot = {key: [sampleCube.adjust(rotateAxes(k,rotAxis),Piece) for k in v] for key,v in tPieceRot.items()}
    tGearRot = {key: [rotateAxes(k, rotAxis) for k in v] for key,v in tGearRot.items()}


    data[turn.name] = {}
    data[turn.name]["corners"] = tCorners
    data[turn.name]["pieces"] = tPieces
    data[turn.name]["gears"] = tGears
    data[turn.name]["pieceRot"] = tPieceRot
    data[turn.name]["gearRot"] = tGearRot 

def export(data):
    with open("allTurnData.json", "w") as f:
        json.dump(data, f, indent=4)

generate(Turn("R"), finalTurnData)
generate(Turn("L"), finalTurnData)
generate(Turn("U"), finalTurnData)
generate(Turn("D"), finalTurnData)
generate(Turn("F"), finalTurnData)
generate(Turn("B"), finalTurnData)
export(finalTurnData)