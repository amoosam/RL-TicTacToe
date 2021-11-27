import random

class Board:
    def __init__(self,player1,player2):
        self.spaces = 9
        self._blank = " "
        self.legal_players = [player1,player2]
        self.boardvals = [self._blank]*self.spaces
        self._base = "{}|{}|{} \n" + \
                    "-------- \n" + \
                    "{}|{}|{} \n" + \
                    "-------- \n" + \
                    "{}|{}|{} \n"
        self._winning = [{0,1,2},
                        {3,4,5},
                        {6,7,8},
                        {0,3,6},
                        {1,4,7},
                        {2,5,8},
                        {0,4,8},
                        {2,4,6}]
    def reset(self):
            self.boardvals = [self._blank]*self.spaces

    def __str__(self):
            return self._base.format(*self.boardvals)

    def available_moves(self):
            # returns open spaces on the board
            return [i for i,p in enumerate(self.boardvals) if p == self._blank]

    def is_winner(self):
            
            for win in self._winning:
                p = [self.boardvals[pos] for pos in win]
                if len(set(p)) == 1 and self._blank not in set(p):
                    return p[0]
                elif len(self.available_moves()) == 0:
                    return "Draw"
                else:
                    return None
            
    def game_over(self):
            return len(self.available_moves()) == 0 or self.is_winner() is not None


class Agent:

    def __init__(self,player,learning,episodes,start):
        self.player = player
        self.lossval = -1
        self.learning = learning
        self.values = {}
        self.epsilon = 0.1
        self.alpha = 0.2
        self.prevstate = None
        self.prevscore = 0
        self.episodes = episodes
        self.ismove = start
        self.winval = 0.5

    def move(self,boardvalues,legal_moves,winner):
        if winner == self.player:
            self.winval = 1
        elif winner == None:
            self.winval = 0.5
        else:
            self.winval = self.lossval

        if self.learning == True:
            return self.greedy(boardvalues, legal_moves)
        else:
            return self.random(legal_moves)
    
    def game_over(self, boardvalues, winner):
        if winner == self.player:
            self.winval = 1
        elif winner == None:
            self.winval = 0.5
        else:
            self.winval = self.lossval
        
        self.values[self.state(boardvalues)] = self.winval

        self.winval=0.5
        self.prevstate=None
        self.prevscore=0

    def greedy(self,boardvalues,legal_moves):
        maxval = -10000
        maxmove = None
        for mv in legal_moves:
            boardvalues[mv] = self.player
            val = self.searchvals(self.state(boardvalues))
            boardvalues[mv] = " "
            if val > maxval:
                maxval = val
                maxmove = mv
        self.prevstate=self.state(boardvalues)
        self.prevscore= self.values[self.prevstate] if self.prevstate in self.values.keys() else 0.5
        self.update(maxval)
        return maxmove

    def random(self,legal_moves):
        return random.choice(legal_moves)
        
    def episode_over(self):
        self.update(self.winval)
        self.prevstate = None
        self.prevscore = 0
        self.winval = 0.5

    def state(self,boardvalues):
        return  "".join(boardvalues)

    def update(self,nextscore):
        if self.prevstate is not None and self.learning:
            if self.prevstate not in self.values.keys():
                self.values[self.prevstate] = 0.5
            self.values[self.prevstate] += self.alpha*(nextscore - self.prevscore)
        

    def searchvals(self,state_str):
        if state_str not in self.values:
            self.add(state_str)
        return self.values[state_str]

    def add(self,state_str):
        self.values[state_str] = self.winval
     


def game(player1, player2):
    board = Board(player1.player, player2.player)
    max_moves = board.spaces
    while not board.game_over():
        winner = board.is_winner()
        if player1.ismove:
            m = player1.move(board.boardvals,board.available_moves(),winner)
            board.boardvals[m] = player1.player 
            player1.ismove = False
            player2.ismove = True
        elif player2.ismove:
            m = player2.move(board.boardvals,board.available_moves(),winner)
            board.boardvals[m] = player2.player
            player1.ismove = True
            player2.ismove = False

    winner = board.is_winner()
    player1.game_over(board.boardvals,winner)
    player2.game_over(board.boardvals,winner)
    return winner
            
        
p1 = Agent("x",False,1000,True)           
p2 = Agent("o",True,100,False)

for i in range(p1.episodes):
    w = game(p1,p2)
    #print(f"Winner is {w} \n")
print(p2.values)

