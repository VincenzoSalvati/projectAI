# Agenti Intelligenti - Gomoku
## Team

Paolo Mansi - 0622701542 - p.mansi5@studenti.unisa.it

Vincenzo Salvati - 0622701550 - v.salvati10@studenti.unisa.it

# Introduction

Implementation of Gomoku game with AI players based on adversarial search: α-β pruning algorithm and heuristic.

## Paths
```.
|-- projectAI
|   |-- bot
|   |   |-- alpha_beta_pruning.py
|   |   |-- BotGomoku.py
|   |   |-- constants.py
|   |-- data
|   |   |-- right_click.wav
|   |   |-- wrong_click.wav
|   |-- graphics
|   |   |-- BoardGomoku.py
|   |   |-- ButtonHome.py
|   |   |-- constants.py
|   |-- log
|   |   |-- PC_VS_PC.csv
|   |   |-- Player_VS_PC.csv
|   |-- utility
|   |   |-- Chronometer.py
|   |   |-- patterns.py
|   |   |-- utils.py
|   |-- main.py
```

The developed code is divided in the following folders manner:
- The “_bot_” folder contains all the classes related to the AI as well as the heuristic and α-β pruning search. In particular, it contains:
    - _alpha_beta_pruning.py_ for implementing α-β pruning algorithm
    - _BotGomoku.py_ for implementing the AI
    - _constants_ai.py_ that contains some constants used for the AI
    - _patterns.py_ that contains all patterns considered by the AI
-	The “_graphic_” folder contains all the classes related to the bare board of the game as well as the update of the GUI. In particular, it contains: 
    -	_BoardGomoku.py_ for implementing the board of the game
    -	_ButtonHome.py_ for displaying buttons in the home page
    -	_constants_graphics.py_ that contains some constants used for the board internal structure
-	The “_data_” folder contains wav file to reproduce audio effect
-	The “_utility_” folder contains all the classes related to the AI and the board. In particular, it contains:
    -	_Chronometer.py_ for implementing the chronometer in order to take in consideration both the elapsed time for each AI move and the match’s total elapsed time
    -	_utils.py_ that contains csv function in order to make the matches’ log
-	The class _main.py_ which allow to start the match initializing both the home and its modalities


# How to run
1.	Run the main.py

<p align="center">
  <img src="https://user-images.githubusercontent.com/75745078/173242564-2a7f98c6-fbfb-462e-8f0a-845200e78dfe.png" />
</p>

2.	Chose the modality

<p align="center">
  <img src="https://user-images.githubusercontent.com/75745078/173242570-79df3e93-f49e-4613-b366-2829b1505f5e.png" />
</p>
 
## Player vs PC
Initially the system asks if you want to be the first player:

<p align="center">
  <img src="https://user-images.githubusercontent.com/75745078/174127184-ccd1cb80-2e4b-459b-8db0-cd072c738a9e.png" />
</p>

After pressing yes, you are able to dispose: 1 black stone, 1 white stone and 1 black stones in this order. So, the bot, basing on his utility function, will be able to choose among:
-	Play with black stones
-	Play with withe stones
-	Place one black stone and one white stone so that the player has to choose the own colours.

<p align="center">
  <img src="https://user-images.githubusercontent.com/75745078/173242611-35a697cd-9de8-4c91-881c-72520772e1fc.png" />
</p>

After pressing no, the bot is able to dispose: 1 black stone, 1 white stone and 1 black stone in this order. Hence, the player can choose among the followings:
-	Play with black stones
-	Play with withe stones
-	Place one black stone and one white stone so that the bot have to choose the own colours.

<p align="center">
  <img src="https://user-images.githubusercontent.com/75745078/173242620-18b7f43d-5028-40cb-8378-520a09c9ccd5.png" />
</p>

## Player vs Player
It’s a free table which could be exploited to play alone or against other people.

## PC vs PC
It has been used to compare different heuristics.
Its Swap 2 consist in:
1.	Choosing randomly whose heuristics starts the match
2.	Random first move for each player.
