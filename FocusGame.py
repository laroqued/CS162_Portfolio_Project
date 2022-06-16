# Author: Donnyves Laroque
# Date: 12/03/2020
# Description: This project simulates the board game Focus/Domination.

import math


class SpecialMoves:
    """ This class represents moves needed to play the Focus game.
     This class contains methods that handles single and multiple
     game piece moves in the game."""

    def __init__(self):
        """ This method initializes the data members for the SpecialMoves class.
         """
        self._game_player = None
        self._end = None
        self._start = None
        self._num_pieces = None
        self._location = None

    def is_a_winner(self, game_player):
        """
        This method return True if a player captures 6 game pieces.
        """
        self._game_player = game_player
        if game_player.get_captured_game_piece() > 7:
            return True
        else:
            return False

    def multiple_move(self, start, end, num_pieces):
        """
        This method moves the game piece(s) depending on how many pieces are stacked.
        """
        self._end = end
        self._start = start
        self._num_pieces = num_pieces
        moves = start.remove_top_piece(num_pieces)
        move = 0
        while move < len(moves):
            end.add_game_piece(moves[len(moves) - 1 - move])
            move += 1

    def reserve_or_capture_game_piece(self, end, game_player):
        """
        This method checks the piece at the bottom of the stack. The piece is captured or reserved
        depending on color of the player of whose turn it is.
        """
        self._end = end
        self._game_player = game_player
        extra_pieces = end.remove_bottom_piece()
        piece = 0
        while piece < extra_pieces:
            if piece == game_player.get_piece_color():
                game_player.increment_reserved_piece()
                piece += 1
            else:
                game_player.increment_captured_piece()
                piece += 1

    def has_five_pieces_on_stack(self, end, game_player):
        """
        This method check to see if their are more than 5 pieces on the stack
        and calls a method to capture or reserve a game piece.
        """
        self._end = end
        self._game_player = game_player
        fancy_moves = SpecialMoves()
        if end.get_stack_length() >= 4:
            fancy_moves.reserve_or_capture_game_piece(end, game_player)

    def check_number_of_pieces(self, start, num_pieces):
        """
        This method makes sure their are valid number of
        pieces stacked to make a legitimate amount of moves.
        """
        self._start = start
        self._num_pieces = num_pieces
        if num_pieces > start.get_stack_length():
            return False
        else:
            return True

    def is_valid_position(self, location):
        """
        This method makes sure that the pieces remain
        at the bounds of the board.
        """
        self._location = location
        if location[0] < 0:
            return False
        elif location[1] < 0:
            return False
        elif location[1] > 5:
            return False
        else:
            return True


class Gamer:
    """
    This class represents the players and the game pieces in the game.
    """

    def __init__(self, player_name, piece_color):
        """
        This method has the data members for the Gamer class.
        """
        self._captured_piece = 0
        self._reserved_piece = 0
        self._player_name = player_name.upper()
        self._piece_color = piece_color.upper()

    def get_piece_color(self):
        """
        This method returns the color of the game piece.
        """
        return self._piece_color

    def get_player_name(self):
        """
        This method returns the players name.
        """
        return self._player_name

    def get_captured_game_piece(self):
        """
        This method returns the amount of captured game pieces.
        """
        return self._captured_piece

    def get_reserved_game_piece(self):
        """
        This method returns the amount or returned game pieces
        """
        return self._reserved_piece

    def use_reserved_pieces(self):
        """
        This method subtracts 1 piece from the reserved pieces collections.
        """
        self._reserved_piece -= 1

    def increment_reserved_piece(self):
        """
        This method adds 1 piece from the reserved pieces collection.
        """
        self._reserved_piece += 1

    def increment_captured_piece(self):
        """
        This method adds 1 piece from the captured pieces collection.
        """
        self._captured_piece += 1


class GameBoard:
    """
    This class represents the locations and movements on the game board.
    """

    def __init__(self, beginning_piece):
        """ This method initializes the data members for the Gameboard class."""
        self._beginning_piece = beginning_piece
        if self._beginning_piece:
            self._game_piece_stack = [self._beginning_piece]
        elif not self._beginning_piece:
            self._game_piece_stack = list()

    def add_game_piece(self, piece):
        """
        This method places a game piece on top of the stack.
        """
        self._game_piece_stack.append(piece)

    def remove_stack_top_piece(self):
        """
        This method removes a game piece that is on top of the stack.
        """
        if self.is_empty():
            return None
        elif not self.is_empty():
            return self._game_piece_stack.pop(len(self._game_piece_stack) - 1)

    def get_top_piece(self):
        """
        This method returns the game piece that was on top of the stack.
        """
        if not self.is_empty():
            return self._game_piece_stack[len(self._game_piece_stack) - 1]
        else:
            return None

    def is_empty(self):
        """
        This method checks if the stack is empty.
        """
        if len(self._game_piece_stack) == 0:
            return True
        else:
            return False

    def remove_bottom_piece(self):
        """
        This method removes a game piece from the bottom of the stack if
        the stack has more than 5 pieces.
        """
        stack_length = len(self._game_piece_stack)
        additional_pieces = list()
        if stack_length >= 5:
            leftover_pieces = len(self._game_piece_stack) - 5
            i = 0
            while i < leftover_pieces:
                additional_pieces.append(self._game_piece_stack.pop(0))
                i += 1
                return additional_pieces

    def remove_top_piece(self, num_pieces):
        """
        This method removes one or more game pieces from the top of stack depend on
        how many moves a player makes.
        """
        piece_stack = list()
        i = 0
        while i < num_pieces:
            piece_stack.append(self._game_piece_stack.pop(0))
            i += 1
            return piece_stack

    def get_stack_length(self):
        """
        This method returns how many pieces
        are in a stack.
        """
        return len(self._game_piece_stack)

    def get_game_piece_stack(self):
        """
        This method returns the game piece stack.
        """
        return self._game_piece_stack


class FocusGame:
    """
    This class represents the game Focus/Domination
    """

    def __init__(self, player_a, player_b):
        """
        This init method will take in two tuples that will initialize the
        two players for the game.  This function will also initialize the
        board for the game the will begin with (0,0) and end with (5,5). This
        will represent the rows and columns of the game
        """
        starting_a_position = Gamer(player_a[0], player_a[1])
        starting_b_position = Gamer(player_b[0], player_b[1])
        self._player_a = starting_a_position
        self._player_b = starting_b_position
        self._current_turn = None
        player_a_game_piece = self._player_a.get_piece_color()
        player_b_game_piece = self._player_b.get_piece_color()
        self._board = [[GameBoard(player_a_game_piece), GameBoard(player_a_game_piece), GameBoard(player_b_game_piece),
                        GameBoard(player_b_game_piece), GameBoard(player_a_game_piece), GameBoard(player_a_game_piece)],
                       [GameBoard(player_b_game_piece), GameBoard(player_b_game_piece), GameBoard(player_a_game_piece),
                        GameBoard(player_a_game_piece), GameBoard(player_b_game_piece), GameBoard(player_b_game_piece)],
                       [GameBoard(player_a_game_piece), GameBoard(player_a_game_piece), GameBoard(player_b_game_piece),
                        GameBoard(player_b_game_piece), GameBoard(player_a_game_piece), GameBoard(player_a_game_piece)],
                       [GameBoard(player_b_game_piece), GameBoard(player_b_game_piece), GameBoard(player_a_game_piece),
                        GameBoard(player_a_game_piece), GameBoard(player_b_game_piece), GameBoard(player_b_game_piece)],
                       [GameBoard(player_a_game_piece), GameBoard(player_a_game_piece), GameBoard(player_b_game_piece),
                        GameBoard(player_b_game_piece), GameBoard(player_a_game_piece), GameBoard(player_a_game_piece)],
                       [GameBoard(player_b_game_piece), GameBoard(player_b_game_piece), GameBoard(player_a_game_piece),
                        GameBoard(player_a_game_piece), GameBoard(player_b_game_piece), GameBoard(player_b_game_piece)]]

    def move_piece(self, player_name, start_coord, end_coord, num_pieces):
        """
        This method will allow players to move around the 6X6 board.  The
        two player will take turns moving the pieces around.  Each player will
        choose a tuple coordinate to represent the direction the player wants to
        move. The integer will represent how many moves the player will make.
        An error message will be display if there is an invalid move, player moves out
        of turn, wrong number of pieces, player wins, more than five pieces, captured piece, or
        player gains a reserve piece.
        """

        if not self.correct_turn_order(self.find_name_of_player(player_name)):
            return "not your turn"
        if not self.is_valid_location(self.find_name_of_player(player_name), start_coord, end_coord, num_pieces):
            return "invalid location"
        fancy_moves = SpecialMoves()
        if not fancy_moves.check_number_of_pieces(self.get_location(start_coord), num_pieces):
            return "invalid number of pieces"
        fancy_moves.multiple_move(self.get_location(start_coord), self.get_location(end_coord), num_pieces)
        fancy_moves.has_five_pieces_on_stack(self.get_location(end_coord), self.find_name_of_player(player_name))
        winner = fancy_moves.is_a_winner(self.find_name_of_player(player_name))
        if winner:
            return player_name + " Wins"
        self.alternate_player(self.find_name_of_player(player_name))
        return "Successfully moved"

    def show_pieces(self, location):
        """
        This method will show a list of all the pieces that are in
        a particular location.  The piece the is at the "bottom" will be at
        the beginning of the list (0th index).
        """
        fancy_moves = SpecialMoves()
        if not fancy_moves.is_valid_position(location):
            return None
        else:
            return self._board[location[0]][location[1]].get_game_piece_stack()

    def show_reserve(self, player_name):
        """
        This method takes in the name of the player and
        will show all the reserved pieces in a list, that are reserve pieces,
        that belong to a  player.  If the are no pieces in the list, return 0.
        """
        if self.find_name_of_player(player_name):
            return self.find_name_of_player(player_name).get_reserved_game_piece()
        else:
            return 0

    def show_captured(self, player_name):
        """
        This method takes in the name of the player and will show
        all the captured pieces in a list, that are captured pieces,
        that belong to a player.  If the are no pieces in the list, return 0.
        """
        if self.find_name_of_player(player_name):
            return self.find_name_of_player(player_name).get_captured_game_piece()
        else:
            return 0

    def reserved_move(self, player_name, location):
        """
        This method takes in the players name and location on the board. The amount
        of reserved moves will be decremented every time the player makes a reserved
        move.  if the there are no pieces, a message of ' no pieces in reserve' will
        be returned.
        """
        fancy_moves = SpecialMoves()
        if not fancy_moves.is_valid_position(location):
            return 0
        if not self.find_name_of_player(player_name) or \
                self.find_name_of_player(player_name).get_reserved_game_piece() == 0:
            return "No pieces in reserve"
        self.get_location(location).add_game_piece(self.find_name_of_player(player_name).get_piece_color())
        self.find_name_of_player(player_name).use_reserved_pieces()
        fancy_moves.has_five_pieces_on_stack(self.get_location(location), self.find_name_of_player(player_name))
        if fancy_moves.is_a_winner(self.find_name_of_player(player_name)):
            return f"{player_name} Wins"
        self.alternate_player(self.find_name_of_player(player_name))

    def get_location(self, location):
        """
        This method returns the location of the on the board.
        """
        return self._board[location[0]][location[1]]

    def find_name_of_player(self, player_name):
        """
        This method returns the name of the player object.
        """
        player_uppercase = player_name.upper()
        if player_uppercase == self._player_a.get_player_name():
            return self._player_a
        elif player_uppercase == self._player_b.get_player_name():
            return self._player_b
        return None

    def alternate_player(self, current_player):
        """
        This method alternates the player after
        the last player completes their move.
        """
        if current_player == self._player_a:
            self._current_turn = self._player_b
        else:
            self._current_turn = self._player_a

    def correct_turn_order(self, game_player):
        """
        This method checks if the player are alternating back and
        forth in the correct order.  Return True or False.
        """
        if self._current_turn is not None and game_player != self._current_turn:
            return False
        else:
            return True

    def is_valid_location(self, player, start_coord, stop_coord, num_pieces):
        """
        This method checks if the location of the of the game piece is valid.
        Return True or False.
        """
        fancy_moves = SpecialMoves()
        if not fancy_moves.is_valid_position(start_coord):
            return False
        if not fancy_moves.is_valid_position(stop_coord):
            return False
        if self.get_location(start_coord).get_top_piece() != player.get_piece_color():
            return False
        check_row = stop_coord[0] - start_coord[0]
        check_column = stop_coord[1] - start_coord[1]
        if check_row != 0 and check_column != 0:
            return False
        if check_row == 0:
            location_changed = math.fabs(check_column)
        else:
            location_changed = math.fabs(check_row)
        if num_pieces != location_changed:
            return False
        else:
            return True
