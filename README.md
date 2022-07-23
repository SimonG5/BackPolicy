# BackPolicy

Policy network in TensorFlow to classify backgammon moves. The purpose of this network is to help a [reinforcement learning model](https://github.com/SimonG5/BackGS) learn to play backgammon. Using a policy network allows us to greatly reduce the branching factor.

## Training

You can train the model by first extracting the datasets.zip file and then running the following command.

```bash
python train.py
```

The network consists of 3 hidden layers with 128 neurons with an output layer consisting of 325 neurons representing each move on a backgammon board.

## Usage

You can retrieve the 10 most interesting moves by running.

```bash
python getMove.py
```

You will be asked to input a board which you can do following this syntax.

```bash
2,0,0,0,0,-5,0,-3,0,0,0,5,-5,0,0,0,3,0,5,0,0,0,0,-2,0,0,0,0,6,3,-1
```

The first 24 inputs are single digit values representing each point in this order. Where black checkers are negative values and white are positive.

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Bg-start.svg/1200px-Bg-start.svg.png" alt="drawing" width="350"/>

The next 4 inputs represent the white bar, black bar, white home and black home in that order.
Then comes 2 inputs being each dice. Lastly we have a value being either 1 or -1 where 1 represent white moving and black being black moving.

The moves are returned in the standard [Backgammon notation](https://thegammonpress.com/backgammon-notation/).

```bash
1: 24/18 : 0.9912969
------------------------
2: 8/2 : 0.00429581
------------------------
3: 13/10 : 0.0018391979
------------------------
4: 8/5 : 0.0006961238
------------------------
5: 24/21 : 0.00068248104
------------------------
6: 24/15 : 0.0006657073
------------------------
7: 13/7 : 0.00033448273
------------------------
8: Cannot/move : 0.00013562273
------------------------
9: 13/8 : 2.0823425e-05
------------------------
10: 8/3 : 2.0705833e-05
```

## Datasets

The datasets contain over 2 million different board positions with the corresponding correct move. All data points were scraped from games between high-level players.

## Result

The network achieves a top 10 accuracy of 99% whilst having a regular accuracy of 52%. The top 10 accuracy is the more important metric in this instance as we will branch over at least 10 moves in the reinforcement learning model.

Feel free to tweak the hyper parameters to improve accuracy.

## Dependencies

Tensorflow > 2.9.1
