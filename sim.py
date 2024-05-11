from turn_data import *

x_rot = ["F","U","B","D"]
y_rot = ["R","F","L","B"]
z_rot = ["U","R","D","L"]

def rotateAxes(origin,axes:list):
    """
    Format of `axes` is something like the following:
    `[["y",1], ["x",-1], ["y",2]]`
    """
    prime = origin
    for i in axes:
        primeList = [*prime]

        l = None
        if i[0] == "x": l = x_rot
        elif i[0] == "y": l = y_rot
        elif i[0] == "z": l = z_rot

        for charInd,char in enumerate(primeList):
            if char not in l: continue
            index = l.index(char)
            new_index = (index + i[1]) % len(l)
            primeList[charInd] = l[new_index]

        prime = "".join(primeList)
    return prime

def countChanges(origin,prime):
    if isinstance(origin,list):
        return sum(1 for ind, val in enumerate(origin) if val.initialPosition != prime[ind].initialPosition)
    elif isinstance(origin,dict):
        return sum(1 for key in origin.keys() if origin[key].initialPosition != prime[key].initialPosition)
    
class Turn:
    def __init__(self,name,amount=1):
        self.name = name
        self.amount = amount

    def __str__(self):
        amount = str(self.amount)
        if self.amount == 1: amount = ""
        elif self.amount == -1: amount = "'"
        return f"{self.name}{amount}".replace("-","'")
    
    def __repr__(self): return str(self)

class TurnSequence:
    def __init__(self,seq=None):
        if isinstance(seq,str):
            newSeq = []
            for i in seq.split(" "):
                turnBase = i[0]
                turnMods = i[1:].replace("'","")
                turnAmount = 1 if turnMods == "" else int(turnMods)
                neg = -1 if "'" in i else 1
                newSeq.append(Turn(turnBase,neg*turnAmount))
            seq = newSeq
        else:
            self.sequence = []
        self.sequence = seq

    def __add__(self,other):
        return TurnSequence(self.sequence+other.sequence)

    def __str__(self):
        return " ".join([str(k) for k in self.sequence])
    
    def __repr__(self): return str(self)

    def reverse(self):
        return TurnSequence([Turn(k.name,-k.amount) for k in list(reversed(self.sequence))])

    def mirror(self): # mirrors on X axis
        newseq = TurnSequence([])
        for turn in self.sequence:
            newturn = Turn(turn.name,-turn.amount)
            if turn.name == "R": newturn.name = "L"
            elif turn.name == "L": newturn.name = "R"
            newseq.sequence.append(newturn)
        return newseq


class Gear:
    def __init__(self,initialPosition,rotation=0):
        self.initialPosition = initialPosition
        self.rotation = rotation % 360
    
    def __str__(self):
        return f"({self.initialPosition},{str(self.rotation)})"
        
    def __repr__(self): return str(self)

class Piece:
    def __init__(self,initialPosition,rotation=0):
        self.initialPosition = initialPosition
        self.rotation = rotation % 360
    
    def __str__(self):
        return f"({self.initialPosition},{str(self.rotation)})"
    
    def __repr__(self): return str(self)
        

class Corner:
    def __init__(self,initialPosition):
        self.initialPosition = initialPosition
    
    def __str__(self): return self.initialPosition
    def __repr__(self): return str(self)
        


class Cube:
    def __init__(self):
        self.corners={
            "URF": Corner("URF"),
            "URB": Corner("URB"),
            "ULF": Corner("ULF"),
            "ULB": Corner("ULB"),
            "DRF": Corner("DRF"),
            "DRB": Corner("DRB"),
            "DLF": Corner("DLF"),
            "DLB": Corner("DLB"),
        }

        self.pieces={
            "U": Piece("U"),
            "D": Piece("D"),
            "R": Piece("R"),
            "L": Piece("L"),
            "F": Piece("F"),
            "B": Piece("B"),

            "FU": Piece("FU"),
            "FR": Piece("FR"),
            "FD": Piece("FD"),
            "FL": Piece("FL"),

            "BU": Piece("BU"),
            "BR": Piece("BR"),
            "BD": Piece("BD"),
            "BL": Piece("BL"),

            "RU": Piece("RU"),
            "RD": Piece("RD"),
            "LU": Piece("LU"),
            "LD": Piece("LD"),
        }

        self.gears = {
            "FU": Gear("FU"),
            "FR": Gear("FR"),
            "FD": Gear("FD"),
            "FL": Gear("FL"),

            "BU": Gear("BU"),
            "BR": Gear("BR"),
            "BD": Gear("BD"),
            "BL": Gear("BL"),

            "RU": Gear("RU"),
            "RB": Gear("RB"),
            "RD": Gear("RD"),
            "RF": Gear("RF"),

            "LU": Gear("LU"),
            "LB": Gear("LB"),
            "LD": Gear("LD"),
            "LF": Gear("LF"),

            "UF": Gear("UF"),
            "UB": Gear("UB"),
            "UR": Gear("UR"),
            "UL": Gear("UL"),

            "DF": Gear("DF"),
            "DB": Gear("DB"),
            "DR": Gear("DR"),
            "DL": Gear("DL"),
        }
        
    def __str__(self):
        s = "Corners: "
        for initial, corner in self.corners.items():
            s+=f"\n{initial}: {corner}"
        s+="\nPieces: " 
        for initial, piece in self.pieces.items():
            s+=f"\n{initial}: {piece}"
        s+="\nGears: "
        for initial, gear in self.gears.items():
            s+=f"\n{initial}: {gear}"
        return s
        
    def __repr__(self): return str(self)

    def executeTurn(self,turn):
        tCorners = rTurnCorners.copy()
        tPieces = rTurnPieces.copy()
        tGears = rTurnGears.copy()
        tPieceRot = rTurnPieceRotations.copy()
        tGearRot = rTurnGearRotations.copy()
        
        # transform R lists
        rotAxis = None
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
            
        if rotAxis: 
            tCorners = [self.adjust(rotateAxes(k,rotAxis),Corner) for k in tCorners]
            tPieces = [ [self.adjust(rotateAxes(j,rotAxis),Piece) for j in k] for k in tPieces ]
            tGears = [ [rotateAxes(j,rotAxis) for j in k] for k in tGears ]
            tPieceRot = {key: [self.adjust(rotateAxes(k,rotAxis),Piece) for k in v] for key,v in tPieceRot.items()}
            tGearRot = {key: [rotateAxes(k, rotAxis) for k in v] for key,v in tGearRot.items()}
            
        # execute turn
        #   corners
        res = self.corners.copy()
        for i in range(len(tCorners)):
            res[self.adjust(tCorners[i],Corner)] = self.corners[self.adjust(tCorners[(i - turn.amount)%len(tCorners)],Corner)]
        self.corners = res
        
        #   pieces
        res = self.pieces.copy()
        for l in tPieces:
            for i in range(len(l)):
                res[self.adjust(l[i],Piece)] = self.pieces[self.adjust(l[(i - turn.amount)%len(l)],Piece)]
        self.pieces = res
        
        #   gears
        res = self.gears.copy()
        for l in tGears:
            for i in range(len(l)):
                res[l[i]] = self.gears[l[(i - turn.amount)%len(l)]]
        self.gears = res
        
        #   execute rotations
        #       piece rotation
        for r, pieces in tPieceRot.items():
            for piece in pieces:
                self.pieces[piece].rotation = (self.pieces[piece].rotation + r*turn.amount)%360
        #       gear rotation
        # DO GEAR ROTATIONS CHANGE BETWEEN SOMETHING LIKE L OR R?
        for r, gears in tGearRot.items():
            for gear in gears:
                self.gears[gear].rotation = (self.gears[gear].rotation + r*turn.amount)%360
        
    
    def executeSequence(self,seq):
        if isinstance(seq,TurnSequence):
            for i in seq.sequence:
                self.executeTurn(i)
            return
        
        # format as turn sequence
        seqReplacement = TurnSequence(seq)
        self.executeSequence(seqReplacement)
        
    def adjust(self, s, pieceType):
        if pieceType == Corner:
            letters = {*s}
            for key in self.corners.keys():
                if letters == {*key}: return key
        elif pieceType == Piece:
            if len(s) == 1: return s
            letters = {*s}
            for key in self.pieces.keys():
                if letters == {*key}: return key