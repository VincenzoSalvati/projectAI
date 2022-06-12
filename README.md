# Artificial Intelligenze - Gomoku
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
- _bot_: contains the scripts to implement the AI;
- _data_: contains the audio file for animation;
- _graphics_: contains the scripts to implement graphics regarding home and board Gomoku;
- _log_: contains the matches' log;
- _utility_: contains the useful scripts;
- _main.py_: script to start the game.

# How to use
1.	Run the main.py



![image](https://user-images.githubusercontent.com/75745078/173242564-2a7f98c6-fbfb-462e-8f0a-845200e78dfe.png)
 
 
 
2.	Chose the modality



![image](https://user-images.githubusercontent.com/75745078/173242570-79df3e93-f49e-4613-b366-2829b1505f5e.png)



3.	Let’s play



![image](https://user-images.githubusercontent.com/75745078/173242600-24891413-1738-4724-96cd-cc428bcaceae.png)
 
 
 
## P.S.
### Player vs PC
Initially the system asks you if you want be the first player:



![image](https://user-images.githubusercontent.com/75745078/173242608-bd85ea3d-72b4-40fc-a06d-2c868c0c9a7c.png)



After pressing yes, you are able to dispose: 1 black stone, 1 white sones and 1 black stones in this order. So, the bot, basing on his utility function, will be able to choose among:
-	Play with black stones;
-	Play with withe stones;
-	Place one black stone and one white stone so that the human have to choose the own colours.



![image](https://user-images.githubusercontent.com/75745078/173242611-35a697cd-9de8-4c91-881c-72520772e1fc.png)



After pressing no, the bot is able to dispose: 1 black stone, 1 white sones and 1 black stones in this order. Hance, you have to choose among:
-	Play with black stones;
-	Play with withe stones;
-	Place one black stone and one white stone so that the bot have to choose the own colours.



![image](https://user-images.githubusercontent.com/75745078/173242620-18b7f43d-5028-40cb-8378-520a09c9ccd5.png)



### Player vs Player
It a free table which could be exploit to play alone or against other people.
### PC vs PC
It has been used to compare different heuristics.
Its Swap 2 consist in:
1.	Choosing casually whose heuristics starts the match
2.	Casually first move for each player.

