Genetric AI Tetris
=================
Michael Germano
August, 2016
Written in Python3.5

Python AI that can continually clear lines in the arcade game Tetris
Built using the tetris terminal game from Eric Pai

### Requirements
- pyinput
- numpy


### Project Breakdown
- `ai.py`:
    - analyzes gameboard, calculating all possible moves and subsequent moves based off of the current and next game piece.
    - calculates the score of each possible move based off of
        - lines formed
        - aggregate height
        - the number of holes
        - overall bumpiness
    - executes the best move
- `runAI.py`:
   - script to start the game and AI
- `scoreConstants.py`:
   - constants used to calculate the each move's score. These were found using the genetic algorithm.
- `geneticAlg`:
   - Algorithm that continually improves a population of AI. Each organism in the population contains a list of 4 scoring constants. These constants are intially found randomly using a normal distribution. Every round, the best 50% of the AI breed randomly. Their offspring replace the worst 25% and the algorithm continues on.
- `tetris` dir:
    - terminal tetris game created by Eric Pai
