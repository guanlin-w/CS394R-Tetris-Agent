Description
```
The root directory contains code our initial attempt at learning on Tetris.
Specifically, though both condensed state representations and reward hacking were employed, the lack
of action abstractions rendered the learning task infeasible for the time scale of our project. The
GUI and human interaction environment were sourced from
https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1.

The directory Tetris-DQN contains code relevant to our final report. This includes a base gym environment
and base DQN implementation sourced from https://github.com/michiel-cox/Tetris-DQN. The base actions (Left,
Right, Rotate Left, Rotate Right, Drop) were abstracted over by instead having an 'action' correspond to
dropping a block at a rotation orientation from the top of a column. 
```

Running the code
```
cd Tetris-DQN
pip install -r requirements.txt
python run_evaluation.py [trained model]
 ... where [trained model] is to be replaced with one of the following:
        "blitz" : Only reward-hacked environment of Blitz mode
        "blitz2" : Only true reward environment of Blitz mode
        "blitz-blitz2" : Pretrain on reward-hacked, then train on true reward of Blitz mode
        "forty" : Only reward-hacked environment of Forty-Lines mode
        "forty2" : Only true reward environment of Forty-Lines mode
        "forty-forty2" : Pretrain on reward-hacked, then train on true reward of Forty-Lines mode
        "forty2-blitz2" : Transfer from Forty-Lines to Blitz
        "blitz2-forty2" : Transfer from Blitz to Forty-Lines
```
