# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from collections import namedtuple
import random
import copy
#from utils import argmax

infinity = float('inf')
GameState = namedtuple('GameState', 'to_move, utility, board, moves,prev_move')

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)



class Checkers(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""


    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move,score_array):
        if move not in state.moves:
            return state  # Illegal move has no effect
        elif move == 'pass':
            board_current =copy.deepcopy(state.board)
            star_list,circle_list = self.list_generator(board_current)
            return GameState(to_move=('Star' if state.to_move == 'Circle' else 'Circle'),
                         utility=self.compute_utility(board_current, state.to_move,score_array),
                         board=board_current, moves=self.move_generator(board_current,
                                                                    ('Star' if state.to_move == 'Circle'
                                                                     else 'Circle'),
                                                                     star_list,circle_list),
                                                                     prev_move = move)
        else:
            board_current = copy.deepcopy(state.board)
            player = state.to_move
            new_board = self.update_board(board_current,move,player)
            star_list,circle_list = self.list_generator(new_board)
            return GameState(to_move=('Star' if state.to_move == 'Circle' else 'Circle'),
                         utility=self.compute_utility(new_board, state.to_move,score_array),
                         board=new_board, moves=self.move_generator(new_board,
                                                                    ('Star' if state.to_move == 'Circle'
                                                                     else 'Circle'),
                                                                     star_list,circle_list),
                                                                     prev_move = move)

    def utility(self, state, player,score_array):
        board = copy.deepcopy(state.board)
        return self.compute_utility(board, player,score_array)

    def terminal_test(self, state,player):
        """CASE 1: NO STAR OR CIRCLE REMAINING"""
        
        star_list,circle_list = self.list_generator(state.board)
        
        if len(star_list) == 0 or len(circle_list) == 0:
            return True
        
        """CASE 2: Consecutive pass"""
        if state.moves[0] == state.prev_move and state.prev_move == 'pass' and state.to_move == player:
            return True
        
        return False     

    def display(self, state):
        board = copy.deepcopy(state.board)
        #for x in range(0, 8):
        #    for y in range(0, 8):
        #        print(board[x][y] + "."),
        #    print
        s = [[str(e) for e in row] for row in board]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print '\n'.join(table)
        print
        

    def compute_utility(self, board, player,score_array):
        
        score_array_rev = score_array[::-1]
        
        star_list,circle_list = self.list_generator(board)
        
        current_player_utility = 0
        opposite_player_utility = 0
        if player == 'Star':
            for star in star_list:
                current_player_utility += int(score_array_rev[star[0]]) 
            for circle in circle_list:
                opposite_player_utility += int(score_array[circle[0]])
                
            total_utility = current_player_utility - opposite_player_utility
            
        else:
            for circle in circle_list:
                current_player_utility += int(score_array[circle[0]]) 
            for star in star_list:
                opposite_player_utility += int(score_array_rev[star[0]])
                
            total_utility = current_player_utility - opposite_player_utility
            
            
        return total_utility
        
        
    def update_board(self,cur_board,move,player):
        
        
        cur_board = copy.deepcopy(cur_board)
        
        if player == 'Star':
            source = move[0]
            destination = move[1]
            
            #Handle non jump case
            
            if source[0] - destination[0] == 1:
                if cur_board[destination[0]][destination[1]] == '0':
                    cur_board[destination[0]][destination[1]] = 'S1'
                    cur_board[source[0]][source[1]] = '0'
                else:
                    current_string = cur_board[destination[0]][destination[1]]
                    times = int(filter(str.isdigit, current_string))
                    times = times + 1
                    cur_board[destination[0]][destination[1]] = 'S'+str(times)
                    cur_board[source[0]][source[1]] = '0'
                    
            else:
                if cur_board[destination[0]][destination[1]] == '0':
                    cur_board[destination[0]][destination[1]] = 'S1'
                    cur_board[source[0]][source[1]] = '0'
                    
                    
                else:
                    current_string = cur_board[destination[0]][destination[1]]
                    times = int(filter(str.isdigit, current_string))
                    times = times + 1
                    cur_board[destination[0]][destination[1]] = 'S'+str(times)
                    cur_board[source[0]][source[1]] = '0'
                  
                #kill the piecw
                if source[1] - destination[1] > 0:
                    cur_board[source[0]-1][source[1]-1] = '0'
                else:
                    cur_board[source[0]-1][source[1]+1] = '0'
                    
        else:
            source = move[0]
            destination = move[1]
            
            #Handle non jump case
            
            if source[0] - destination[0] == -1:
                if cur_board[destination[0]][destination[1]] == '0':
                    cur_board[destination[0]][destination[1]] = 'C1'
                    cur_board[source[0]][source[1]] = '0'
                else:
                    current_string = cur_board[destination[0]][destination[1]]
                    times = int(filter(str.isdigit, current_string))
                    times = times + 1
                    cur_board[destination[0]][destination[1]] = 'C'+str(times)
                    cur_board[source[0]][source[1]] = '0'
                    
            else:
                if cur_board[destination[0]][destination[1]] == '0':
                    cur_board[destination[0]][destination[1]] = 'C1'
                    cur_board[source[0]][source[1]] = '0'
                    
                    
                else:
                    current_string = cur_board[destination[0]][destination[1]]
                    times = int(filter(str.isdigit, current_string))
                    times = times + 1
                    cur_board[destination[0]][destination[1]] = 'C'+str(times)
                    cur_board[source[0]][source[1]] = '0'
                  
                #kill the piecw
                if source[1] - destination[1] > 0:
                    cur_board[source[0]+1][source[1]-1] = '0'
                else:
                    cur_board[source[0]-1][source[1]+1] = '0'
                    
                    
        return cur_board
                    
                        
    def move_generator(self,board,next_to_move,star_list,circle_list):
        
        """ This function generates list of valid moves"""
        moves = []
        # Regular move
        if next_to_move == 'Star':
            #remove the pieces on the top row
            star_list_temp = [i for i in star_list if i[0] > 0]
            pos_moves = [(-1,-1),(-1,1)]
            for piece in star_list_temp:
                for pos in pos_moves:
                    targetx = piece[0] + pos[0]
                    targety = piece[1] + pos[1]
                    if targetx < 0 or targetx > 7 or targety < 0 or targety > 7:
                        continue
                    target = (targetx, targety)
                    # Check that there is nothing in the way of moving to the target
                    circle = target in circle_list
                    star = target in star_list_temp
                    if not circle and not star:
                        moves.append((piece,target))
                        # There was something in the way, can we jump it?
                    else:
                        # It has to be of the opposing color to jump
                        if  star:
                            continue
                        # Jump proceeds by adding the same movement in order to jump over the opposing 
                        # piece on the checkerboard
                        jumpx = target[0] + pos[0] 
                        jumpy = target[1] + pos[1]
                        # If the jump is going to be out of bounds don't do it.
                        if jumpx < 0 or jumpx > 7 or jumpy < 0 or jumpy > 7:
                            continue
                        jump = (jumpx, jumpy)
                        # Check that there is nothing in the jumpzone
                        circle = jump in circle_list
                        star = jump in star_list_temp
                        if not star and not circle:
                            moves.append((piece,jump))
                            
        if next_to_move == 'Circle':
            circle_list_temp = [i for i in circle_list if i[0] < 7]
            pos_moves = [(1,-1),(1,1)]
            for piece in circle_list_temp:
                for pos in pos_moves:
                    targetx = piece[0] + pos[0]
                    targety = piece[1] + pos[1]
                    if targetx < 0 or targetx > 7 or targety < 0 or targety > 7:
                        continue
                    target = (targetx, targety)
                    # Check that there is nothing in the way of moving to the target
                    circle = target in circle_list_temp
                    star = target in star_list
                    if not circle and not star:
                        moves.append((piece,target))
                        # There was something in the way, can we jump it?
                    else:
                        # It has to be of the opposing color to jump
                        if  circle:
                            continue
                        # Jump proceeds by adding the same movement in order to jump over the opposing 
                        # piece on the checkerboard
                        jumpx = target[0] + pos[0] 
                        jumpy = target[1] + pos[1]
                        # If the jump is going to be out of bounds don't do it.
                        if jumpx < 0 or jumpx > 7 or jumpy < 0 or jumpy > 7:
                            continue
                        jump = (jumpx, jumpy)
                        # Check that there is nothing in the jumpzone
                        circle = jump in circle_list_temp
                        star = jump in star_list
                        if not star and not circle:
                            moves.append((piece,jump))
                            
        if len(moves) == 0:
            moves.append('pass')
                            
        return moves    



    def list_generator(self,board):
        star_list = []
        circle_list = []
        
        for row_index, row in enumerate(board):
            for col_index, item in enumerate(row):
                if item.find("S") != -1:
                    times = int(filter(str.isdigit, item))
                    for i in range(0,times):
                        star_list.append((row_index,col_index))
                if item.find("C") != -1:
                    times = int(filter(str.isdigit, item))
                    for i in range(0,times):
                        circle_list.append((row_index,col_index))
            
                
        return star_list,circle_list
    




def alphabeta_cutoff_search(state, game,score_array, d=4, cutoff_test=None,eval_fn=None):
        """Search game to determine best action; use alpha-beta pruning.
        This version cuts off search and uses an evaluation function."""

        player = game.to_move(state)
        global node_counter
        node_counter = 1
    
        # Functions used by alphabeta
        def max_value(state, alpha, beta, depth):
            global node_counter
            if cutoff_test(state, depth,player):
                #print "max"
                node_counter += 1
                #game.display(state)
                return game.utility(state, player,score_array)
            v = -infinity
            loop_counter = 1
            for a in game.actions(state):
                if loop_counter == 1:
                    node_counter += 1
                    loop_counter += 1
                    #print a
                    #game.display(state)
                #print "max loop"
                v = max(v, min_value(game.result(state, a,score_array),
                                     alpha, beta, depth + 1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v
    
        def min_value(state, alpha, beta, depth):
            
            global node_counter
            
            if cutoff_test(state, depth,player):
                #print "min"
                node_counter += 1
                #game.display(state)
                return game.utility(state, player,score_array)
            v = infinity
            loop_counter = 1
            for a in game.actions(state):
                if loop_counter == 1:
                    node_counter += 1
                    loop_counter += 1
                    #print a
                    #game.display(state)
                #print "min loop"
                v = min(v, max_value(game.result(state, a,score_array),
                                     alpha, beta, depth + 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v
    
        # Body of alphabeta_cutoff_search starts here:
        # The default test cuts off at depth d or at a terminal state
        cutoff_test = (cutoff_test or
                       (lambda state, depth,player: depth >= d or
                        game.terminal_test(state,player)))
        eval_fn = eval_fn or (lambda state: game.utility(state, player))
        best_score = -infinity
        beta = infinity
        best_action = None
        for a in game.actions(state):
            v = min_value(game.result(state, a,score_array), best_score, beta, 1)
            if v > best_score:
                best_score = v
                best_action = a
        #print best_score        
        #print best_action
        #print node_counter
        
        return best_action,best_score,node_counter
    
    
def minimax_decision(state, game,score_array,d,cutoff_test=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)
    global node_counter
    node_counter = 1

    def max_value(state,depth):
        global node_counter
        if cutoff_test(state, depth,player):
            #print "max"
            node_counter += 1
            return game.utility(state, player,score_array)
        v = -infinity
        loop_counter = 1
        for a in game.actions(state):
            if loop_counter == 1:
                node_counter += 1
                loop_counter += 1
            #print a
            v = max(v, min_value(game.result(state, a,score_array),depth + 1))
            #print "value of max loop v:" + str(v)
        return v

    def min_value(state, depth):
        global node_counter
        if cutoff_test(state, depth,player):
            #print "min"
            node_counter += 1
            return game.utility(state, player,score_array)
        v = infinity
        loop_counter = 1
        #print game.actions(state)
        for a in game.actions(state):
            if loop_counter == 1:
                node_counter += 1
                loop_counter += 1
            #print a
            v = min(v, max_value(game.result(state, a,score_array),depth + 1))
            #print "value if min loop v:" + str(v)
        return v

    # Body of minimax_decision:
    cutoff_test = (cutoff_test or
                       (lambda state, depth,player: depth >= d or
                        game.terminal_test(state,player)))
    #v = max(game.actions(state),
    #              key=lambda a: min_value(game.result(state, a,score_array),1))
    
    best_action = None
    best_score = -infinity
    #print game.actions(state)
    for a in game.actions(state):
        #print a
        v = min_value(game.result(state, a,score_array), 1)
        if v > best_score:
            best_score = v
            best_action = a

    
    return best_action,best_score,node_counter


""" Reading input from file"""

line_counter = 1
initial_board = []
f = open('input.txt','r')
for line in f:
    if(line_counter == 1):
            next_to_move = line.rstrip()
    elif(line_counter == 2):
            algorithm = line.rstrip()
    elif(line_counter == 3):
            max_depth = int(line.rstrip())
    elif(line_counter > 3 and line_counter < 12):
            nline = line.rstrip()
            arr = nline.split(',')
            initial_board.append(arr)
    elif(line_counter == 12):
            nline = line.rstrip()
            arr = nline.split(',')
            val = arr        
    #print line,
    line_counter += 1
f.close()
#print 
    
checkers = Checkers()
star_list,circle_list = checkers.list_generator(initial_board)
current_state = GameState(
        to_move = next_to_move,
        utility = '0',
        board = copy.deepcopy(initial_board),
        moves = checkers.move_generator(initial_board,next_to_move,star_list,circle_list),
        prev_move = None
    ) 

if algorithm == 'ALPHABETA':   
    best_action,best_score,node_counter = alphabeta_cutoff_search(current_state,checkers,val,max_depth,None,None)
else:   
    best_action,best_score,node_counter = minimax_decision(current_state,checkers,val,max_depth,None)

#calculate myopic utility 
myopic_state = checkers.result(current_state,best_action,val)
myopic_utility =  checkers.utility(myopic_state,current_state.to_move,val)   

if best_action != 'pass':  
    source = best_action[0]
    destination = best_action[1]

    source_alphabet = str(unichr(65 + (7-source[0])))
    source_column = source[1]+1
    
    destination_alphabet = str(unichr(65 + (7-destination[0])))
    destination_column = destination[1]+1
    
    best_action = source_alphabet + str(source_column) + '-'+destination_alphabet+str(destination_column)


f = open('output.txt','w')
f.write(str(best_action)+"\n")  
f.write(str(myopic_utility)+"\n")  
f.write(str(best_score)+"\n")  
f.write(str(node_counter)+"\n")
f.close()   