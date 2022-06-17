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

The developed code is divided in the following folders/classes:
-	The “bot” folder contains all the classes related to the AI as well as the heuristic and α-β pruning search. In particular, it contains:
    -	alpha_beta_pruning.py implementing α-β pruning algorithm
    -	BotGomoku.py implementing the AI
    -	constants_ai.py that contains some constants used for the AI
    -	patterns.py that contains all patterns considered by the AI
-	The “graphic” folder contains all the classes related to the board of the game as well as the update of the GUI. In particular, it contains: 
    -	BoardGomoku.py implementing the board of the game
    -	ButtonHome.py displaying and show animations of home page’s buttons
    -	constants_graphics.py that contains some constants used for the board internal structure
-	The “data” folder contains wav file to reproduce audio effect
-	The “utility” folder contains all the classes related to the AI and the board. In particular, it contains:
    -	Chronometer.py implementing the chronometer in order to take in consideration both the elapsed time for each AI move and the match’s total elapsed time
    -	utils.py that contains csv function in order to make the matches’ log, which will be saved in the “log” folder
-	The class main.py which allows to start the match initializing both the home and its modalities.

# How to run
1.	Run the main.py
2.	2.	From the Main page, use the buttons to chose the modality

<p align="center">
  <img src="https://user-images.githubusercontent.com/75745078/173242570-79df3e93-f49e-4613-b366-2829b1505f5e.png" />
</p>
 
## Player VS PC
Initially the system asks if the player desires to be the first one to place the stones:

<p align="center">
  <img src="https://user-images.githubusercontent.com/75745078/174127184-ccd1cb80-2e4b-459b-8db0-cd072c738a9e.png" />
</p>

After pressing yes, you are able to place: 1 black stone, 1 white stone and 1 black stones in this order. So, the bot, basing on his utility function, will be able to choose among:
-	Playing with black stones
-	Playing with withe stones
-   Placing one black stone and one white stone so that the player has to choose its own colour.


<p align="center">
  <img src="https://user-images.githubusercontent.com/75745078/173242611-35a697cd-9de8-4c91-881c-72520772e1fc.png" />
</p>

After pressing no, the bot is able to place: 1 black stone, 1 white stone and 1 black stone in this order. Hence, the player can choose among the followings:
-	Playing with black stones
-	Playing with withe stones
-	Placing one black stone and one white stone so that the bot has to choose its own colour.


<p align="center">
  <img src="https://user-images.githubusercontent.com/75745078/173242620-18b7f43d-5028-40cb-8378-520a09c9ccd5.png" />
</p>

## Player VS Player
It is a free table which can be used by two players utilizing the same computer.

## PC VS PC
It has been used to compare different heuristics.
Its Swap 2 consist in:
1.	Choosing randomly whose heuristics starts the match
2.	Random first move for each player.

