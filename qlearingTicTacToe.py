import random
class Player(object):
    def __init__(self):
        self.Type = "You"

    def move(self, TicTacToe_board):
        move_input = int(input(" "))
        return move_input

    def initate_play(self, char):
        print("")

    def available_moves(self, TicTacToe_board):

        available_moves_list = []
        for i in range(0,9):
            if TicTacToe_board[i] == ' ':
                available_moves_list.append(i+1)
        return available_moves_list

    def reward(self, value, TicTacToe_board):
        try :
           if self.value == -1:
               print("Computer Wins")
           else:
               print("You Win")
        except:
            pass

class QL(Player):
    def __init__(self, e=0.4, a=0.5, g=0.9):
        self.Type = "Computer"
        self.e = e
        self.g = g
        self.q = {}
        self.a = a

    def initate_play(self, char):
        self.last_TicTacToe_board = (' ',' ',' ',' ',' ',' ',' ',' ',' ')
        self.last_move = None

    def getParameterQ(self, state, action):
        # encourage exploration; "optimistic" 1.0 initial values
        if self.q.get((state, action)) is None:
            self.q[(state, action)] = 1.0
        return self.q.get((state, action))

    def move(self, TicTacToe_board):
        self.last_TicTacToe_board = tuple(TicTacToe_board)
        available_moves_l = self.available_moves(TicTacToe_board)
        if random.random() < self.e: # explore!
            self.last_move = random.choice(available_moves_l)
            return self.last_move

        listofq = []
        for a in available_moves_l:
            getParameterQ = self.getParameterQ(self.last_TicTacToe_board,a)
            listofq.append(getParameterQ)

        maximumParameter = max(listofq)
        if listofq.count(maximumParameter) > 1:
            best_options = []
            for i in range(len(available_moves_l)):
                if listofq[i] == maximumParameter:
                    best_options.append(i)
            i = random.choice(best_options)
        else:
            i = listofq.index(maximumParameter)

        self.last_move = available_moves_l[i]
        return available_moves_l[i]

    def reward(self, value, TicTacToe_board):
        T_board = self.last_TicTacToe_board
        T_last_move = self.last_move
        T_value = value
        T_TicTacToe = tuple(TicTacToe_board)
        if self.last_move:
           self.q_learning(T_board, T_last_move, T_value, T_TicTacToe)

    def q_learning(self, state, action, reward, result_state):
        prev = self.getParameterQ(state, action)
        ## change for loop
        list_newq = []
        for a in self.available_moves(state):
            newq = self.getParameterQ(result_state, a)
            list_newq.append(newq)
        maximumParameternew = max(list_newq)
        reward_q = (reward + self.g * maximumParameternew) - prev
        state_action = prev + self.a * reward_q
        self.q[(state,action)] = state_action

class TicTacToe:
    def __init__(self, player1, player2):
        self.TicTacToe_board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        ## use variable exchange
        self.player1 =  player1
        self.player2 =  player2
        choice = random.choice([0,1])
        if choice == 0:
            self.player1_chance = False
        else:
            self.player1_chance = True


    def check_for_winner(self, char):
        ## change
        ## horizontal 
        ## veritcal_check
        ## diagonal_check
        horizontal_check = [(0,1,2),(3,4,5),(6,7,8)]
        veritical_check = [(0,3,6),(1,4,7),(2,5,8)]
        diagonal_check = [(0,4,8),(2,4,6)]

        for x,y,z in horizontal_check+diagonal_check+veritical_check:
            first  = self.TicTacToe_board[x]
            second = self.TicTacToe_board[y]
            third  = self.TicTacToe_board[z]
            if char == first == second == third:
                return True
        return False

    def TicTacToe_board_full(self):
        ## change
        space_list = []
        for space in self.TicTacToe_board:
            if space == ' ':
                space_list.append(space)
                return not any(space_list)

    def display_TicTacToe_board(self):
        row = "| {} || {} || {} |"+"\n"
        hr =  "="*15+"\n"
        print((hr+row + hr + row + hr + row + hr).format(*self.TicTacToe_board))

    def tictactoe_initate(self):
        self.player1.initate_play('X')
        self.player2.initate_play('O')
        while True:
            if self.player1_chance:
                player = self.player1
                char = 'X'
                other_player = self.player2

            else:
                player = self.player2
                char = 'O'
                other_player = self.player1

            if player.Type == "You":
                self.display_TicTacToe_board()
                print(" PLEASE SELECT YOUR MOVE: ")
            space = player.move(self.TicTacToe_board)

            if self.TicTacToe_board[space-1] != ' ':
                print("ILLEGAL MOVE.. \n Restarting.. Player has been awarded negative score")
                player.reward(-99, self.TicTacToe_board)
                break
            self.TicTacToe_board[space-1] = char
            if self.check_for_winner(char):
                winner = player.Type
                print(" Winner!: " + player.Type)
                player.reward(1, self.TicTacToe_board)
                other_player.reward(-1, self.TicTacToe_board)
                break
            if self.TicTacToe_board_full():
                print(" TIE... ")
                player.reward(0.5, self.TicTacToe_board)
                other_player.reward(0.5, self.TicTacToe_board)
                break

            other_player.reward(0, self.TicTacToe_board)
            self.player1_chance = not self.player1_chance


## Driver Program
if __name__ == '__main__':
    player1 = Player()
    player2 = QL()
    player2.e = 0

    print('''
        WELCOME TO TIC - TAC - TOE !
        PRESS CONTROL + D to STOP
        INSTRUCTIONS:
          PRESS 1 TO 9 TO SELECT THE GRID YOU WANT
              ===============
              | 1 || 2 || 3 |
              ===============
              | 4 || 5 || 6 |
              ===============
              | 7 || 8 || 9 |
              ===============
        ''')

    while True:
        ttt_object = TicTacToe(player1, player2)
        ttt_object.tictactoe_initate()
