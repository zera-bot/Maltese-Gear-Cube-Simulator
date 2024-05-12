# Maltese Gear Cube Simulator
Now it is easier to simulate algorithms on the Maltese Gear Cube without actually scrambling your puzzle. These are the main parts of each python file.

Note: This is actually a rewrite of a piece of code where I tried to do the same before; however, I accidentally deleted the old code. Thankfully, I have become a greater Python programmer, so this implementation of the Maltese Gear Cube should be easier to read and work with.
 
## sim.py
sim.py includes the core classes and functions that make the Maltese Gear Cube simulator function. 

`class Turn(name, amount)`
This class represents a single turn on the cube. The `name` property is the name of the turn, such as "R" or "L" and the `amount` property is the amount as an integer.

`class TurnSequence(sequence)`
This class represents a sequence of turns on the cube. `sequence` can be represented as a list of `Turn`s or a string which will be converted to such a list. The `TurnSequence.sequence` property contains the sequence. It is possible to add two `TurnSequence`s together.

`TurnSequence.reverse()` reverses the entire sequence as a new `TurnSequence`.

`TurnSequence.mirror()` mirrors the entire sequence about the X axis.


`class Gear(initialPosition,rotation)` represents a single gear of the puzzle. It contains information about that gear.

`class Piece(initialPosition,rotation)` represents a single piece of the puzzle. A "piece" is any non-gear, non-corner component of the puzzle. The class contains information about that piece.

`class Corner(initialPosition)` represents a single corner of the puzzle. It contains information about that corner. The rotation of the corner is not stored.

`class Cube()` initializes a new cube.
Properties of the cube include `Cube.corners`, `Cube.pieces`, and `Cube.gears`, which are all dictionaries with the values being the pieces in their respective keys' positions. 

To execute single turns on the cube, use `Cube.executeTurn(turn:Turn)`.

To execute sequences of turns on the cube, use `Cube.executeSequence(seq)`, which takes in either a `str` or a `TurnSequence`.

Another function is `countChanges(origin,prime)` which takes in two dictionaries and returns the number of components of that type that have been displaced. It does not account for rotations.

## runner.py
runner.py includes the code for simulating sequences and printing out one that meets a specific condition.
## runner2.py
runner2.py includes the code for simulating a single algorithm. It is another example on how to use this.
## sequence_testing.py
sequence_testing.py includes some code for more easily displaying what some algorithms do. It will print these algorithm summaries in the file summary.txt.