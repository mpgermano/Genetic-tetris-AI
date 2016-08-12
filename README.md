Genetric AI Tetris
=================
Michael Germano
August, 2016
Written in Python3.5

Built using the tetris terminal game from Eric Pai, located at
https://github.com/epai/tetris-terminal-game

### Project Breakdown
- `ai.py`:
     - analyzes gameboard, calculating all possible moves and subsequent moves based off of the current and next game piece.
     - calculate the score of each possible move based off of 
        - lines formed
        - aggregate height
        - the number of holes
        - overall bumpiness
    - execute the best move
- `runAI.py`:
    - script to start the game and AI
- `tetris` dir:
    - terminal tetris game created by Eric Pai
