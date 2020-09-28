# Author: Michelle McFarland
# Date: August 13th, 2020
# Description: Portfolio Project, creating a working Black Box Game.


class BlackBoxGame:
    """
    This class will initialize a new Black Box Game.
    The goal of the game is for a player to guess where hidden atoms
    are located on the board, based on how a laser (ray) acts when
    shot from various border spaces around the board.
    A player starts with 25 points, and loses a point for each unique
    entry or exit point used, as well as 5 points for each incorrect
    atom guess.
    The game is lost when a player runs out of points and has not
    correctly guessed the locations of all atoms on the board.
    The game is won when a player can guess all atom locations
    correctly, with a positive point value remaining (more points
    is better!).
    """
    def __init__(self, atom_list):
        """Initializes a new game."""
        self._board = Board(atom_list)
        self._score = 25
        self._status = "UNFINISHED"
        self._guesses = set()
        self._num_incorrect_guesses = 0

    def display_board(self):
        """Prints the current board."""
        for row in self._board.get_board_layout():
            print(row)

    def shoot_ray(self, row, column):
        """
        Shoots a ray from the position specified by row and column parameters.
        Position should be a border square- row 0 or 9 and column 0 or 9.
        If an invalid row and column are passed, the method will return False.
        Will return a tuple of the exit border square, in the form (row, column).
        If there is no exit square (due to a hit), the method will return None.
        """

        # game has already been won or lost, cannot shoot a new ray
        if self._status != "UNFINISHED":
            print("This game has already been completed.")
            return False

        # position is a main grid square
        if row != 0 and row != 9 and column != 0 and column != 9:
            return False

        # position is a corner square
        elif (row == 0 or row == 9) and (column == 0 or column == 9):
            return False

        # valid start position for a ray
        else:
            result = self._board.shoot_ray(row, column)

            if result is not None:
                self._board._border_squares_used.add(result)  # if there was an exit square, add it to the list of used squares

            self.update_score()

            return result

    def guess_atom(self, row, column):
        """
        Takes in parameters of a players guess- row and column.
        If there is an atom in that position, the method will return True.
        If there is not an atom in that position, the method will return False.
        Score, list atom status, and game status will be updated accordingly.
        """
        for atom in self._board.get_atoms():
            # correct guess- check for win
            if atom.get_position() == (row, column):
                atom._status = "FOUND"

                if self.atoms_left() == 0:
                    self._status = "WON"

                self._guesses.add((row, column))  # adds to guesses set if not a repeat

                return True

        for atom in self._board.get_atoms():
            # incorrect guess, increment incorrect guesses number and check if game is lost
            if (row, column) not in self._guesses:
                self._num_incorrect_guesses += 1

                self._guesses.add((row, column))  # adds to guesses set if not a repeat

                self.update_score()  # updates the current score, should decrement by 5

            return False

    def get_atoms_left(self):
        """Returns the number of atoms left to be guessed."""
        count = 0
        for atom in self._board.get_atoms():
            if atom.get_status() == "NOT FOUND":
                count += 1

        return count

    def get_score(self):
        """Returns the current score."""
        self.update_score()
        return self._score

    def update_score(self):
        """
        Is called after a new ray has exited the board or a new incorrect guess was made
        Checks Board object's border_squares_used and number of guesses that are false,
        updates score accordingly.
        -1 point for each unique border square used
        -5 points for each incorrect atom guess
        If updated score is zero or negative, the status of the game will be set to "LOST"
        """
        current_score = 25

        # checks how many unique border squares have been used, -1 each
        current_score -= 1 * len(self._board.get_border_squares_used())

        # checks how many incorrect guesses have been made, -5 each
        current_score -= self._num_incorrect_guesses * 5

        self._score = current_score  # updates score

        # checks if game is lost
        if self._score <= 0:
            self._status = "LOST"


class Board:
    """
    This class contains data members and methods related to the board.
    """
    def __init__(self, atom_list):
        """
        Initializes a new board, with a 9 by 9 layout (corners are empty),
        as well as a list of atom objects on the board and a set of the
        border squares that have been used as entry/exit points for rays.
        """
        self._board_layout = [
            [' ', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', ' '],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            [' ', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', ' ']]
        self._atoms = []
        self._border_squares_used = set()

        # adds atoms to the board layout, creates atom objects held in atoms
        for atom in atom_list:
            row = atom[0]
            column = atom[1]
            self._atoms.append(Atom(row, column))
            self._board_layout[row][column] = 'O'

    def get_board_layout(self):
        """Returns the board layout."""
        return self._board_layout

    def get_atoms(self):
        """Returns a list of the atom objects on the board."""
        return self._atoms

    def get_border_squares_used(self):
        """
        Returns set of border_squares_used. This includes tuples in the form (row, column)
        of all entry and exit points for rays so far.
        """
        return self._border_squares_used

    def check_if_border_square(self, position):
        """Checks if the next position is a border square- will return True or False accordingly."""
        if position[0] == 0 or position[0] == 9 or position[1] == 0 or position[1] == 9:
            return True

        else:
            return False

    def check_for_hit(self, next_position):
        """Checks to see if the next position is a hit. Will return True or False accordingly."""
        for atom in self._atoms:

            if next_position == atom.get_position():
                return True

        return False

    def check_for_deflection(self, current_ray, position):
        """
        Will check for a deflection, returning False, "DOUBLE", "LEFT", or "RIGHT"
        Uses the get_deflection_squares() method from the Ray class to determine
        which squares to check. Checks if there are atoms in either potential
        spot.
        """
        deflection_type = []
        for atom in self._atoms:
            # check for deflection
            if atom.get_position() == current_ray.get_deflection_squares(position)[0]:
                deflection_type.append("RIGHT")

            if atom.get_position() == current_ray.get_deflection_squares(position)[1]:
                deflection_type.append("LEFT")

        if len(deflection_type) == 0:
            return False

        if "RIGHT" in deflection_type and "LEFT" in deflection_type:
            return "DOUBLE"

        if "RIGHT" in deflection_type:
            return "RIGHT"

        if "LEFT" in deflection_type:
            return "LEFT"

    def shoot_ray(self, row, column):
        """
        Creates a new ray object, executes path until the ray exits the board.
        Returns exit square location of the ray in the form (row, column)
        If there is no exit location (in the case of a hit), it will return None
        """
        current_ray = Ray(row, column)
        self._border_squares_used.add(current_ray.get_entry_position())  # add start position to set of squares used

        while True:
            next_position = current_ray.get_next_position()
            print(current_ray.get_current_position())

            # check for immediate hit
            for atom in self._atoms:
                if atom.get_position() == next_position and current_ray.get_current_position() == current_ray.get_entry_position():
                    current_ray.set_status("HIT")
                    return None

            # check for immediate deflection
            for atom in self._atoms:
                if atom.get_position() in current_ray.get_deflection_squares(next_position) and current_ray.get_current_position() == current_ray.get_entry_position():
                    current_ray.set_exit_position(current_ray.get_current_position())
                    self._border_squares_used.add(current_ray.get_exit_position())  # add exit position to set of squares used
                    return current_ray.get_exit_position()

            # check for exit at next position
            if self.check_if_border_square(next_position) is True:
                return current_ray.end_ray()

            # check for atom at next position
            if self.check_for_hit(next_position) is True:
                current_ray.set_status("HIT")
                return None

            # check for a deflection at next position
            if self.check_for_deflection(current_ray, next_position) is not False:
                current_ray.deflect(self.check_for_deflection(current_ray, next_position))

            # move to next position or start next iteration with the adjusted next position
            if next_position == current_ray.get_next_position():
                current_ray.set_current_position(next_position)


class Atom:
    """Creates a new atom object that can be added to the board."""
    def __init__(self, row, column):
        """
        Creates a new atom object with a row, column, and status.
        Status is initialized as "NOT FOUND"
        """
        self._row = row
        self._column = column
        self._status = "NOT FOUND"

    def get_row(self):
        """Returns the row where atom is located."""
        return self._row

    def get_column(self):
        """Returns the column where atom is located."""
        return self._column

    def get_position(self):
        """Returns the position of the atom, as a tuple in the form (row, column)."""
        return self._row, self._column

    def get_status(self):
        """Returns the status of the atom- "FOUND" or "NOT FOUND" """
        return self._status


class Ray:
    """
    This object is created when a ray is shot.
    The class includes data members and methods to keep track of the
    ray as it traverses the board, and make changes in direction when
    appropriate (after a hit or deflection, for example).
    """
    def __init__(self, row, column):
        """
        Initializes a ray object.
        Positions should always be tuples in the form (row, column)
        Current direction should be "NORTH", "SOUTH", "EAST", or "WEST"
        """
        self._entry_position = (row, column)
        self._current_position = (row, column)
        self._exit_position = None
        self._status = "IN PROGRESS"

        # determine and set current direction
        if row == 0:
            self._current_direction = "SOUTH"

        if row == 9:
            self._current_direction = "NORTH"

        if column == 0:
            self._current_direction = "EAST"

        if column == 9:
            self._current_direction = "WEST"

    def get_status(self):
        """Returns the current status of this ray- "IN PROGRESS" or "COMPLETED" """
        return self._status

    def get_entry_position(self):
        """Returns the entry position of the ray, as a tuple in the form (row, column) """
        return self._entry_position

    def get_exit_position(self):
        """Returns the exit position of the ray, as a tuple in the form (row, column) """
        return self._exit_position

    def get_current_position(self):
        """Returns current position of ray, as a tuple in the form (row, column)."""
        return self._current_position

    def set_current_position(self, position):
        """Sets the ray's current position to the tuple entered, in the form (row, column)."""
        self._current_position = position

    def set_exit_position(self, position):
        """Sets the ray's exit position to the tuple entered, in the form (row, column)."""
        self._exit_position = position

    def set_status(self, status):
        """
        Sets the ray's status to the argument provided.
        Possible statuses include "HIT", "EXITED", or "IN PROGRESS"
        """
        self._status = status

    def get_next_position(self):
        """
        Returns location of next position as (row, column).
        This is a hypothetical next position, based on the assumption
        that the ray will move one space in the current direction.
        """
        current_row = self._current_position[0]
        current_column = self._current_position[1]

        # move up
        if self._current_direction == "NORTH":
            return current_row-1, current_column

        # move down
        if self._current_direction == "SOUTH":
            return current_row+1, current_column

        # move right
        if self._current_direction == "EAST":
            return current_row, current_column+1

        # move left
        if self._current_direction == "WEST":
            return current_row, current_column-1

    def get_deflection_squares(self, position):
        """
        Returns locations of two squares adjacent to the position given.
        Locations will be a list of two tuples- [(row, column), (row, column)]
        The first location will be the square to the left of the ray, and the second will be the square to the right.
        Left and right are determined by the current direction of the ray.
        """
        row = position[0]
        column = position[1]

        # ray is moving North
        if self._current_direction == "NORTH":
            return (row, column-1), (row, column+1)

        # ray is moving South
        if self._current_direction == "SOUTH":
            return (row, column+1), (row, column-1)

        # ray is moving East
        if self._current_direction == "EAST":
            return (row-1, column), (row+1, column)

        # ray is moving West
        if self._current_direction == "WEST":
            return (row+1, column), (row-1, column)

    def turn(self, direction):
        """Turns ray 90 degrees in the specified direction- "LEFT" or "RIGHT" """

        # North
        if self._current_direction == "NORTH":
            if direction == "LEFT":
                self._current_direction = "WEST"
            if direction == "RIGHT":
                self._current_direction = "EAST"

        # South
        elif self._current_direction == "SOUTH":
            if direction == "LEFT":
                self._current_direction = "EAST"
            if direction == "RIGHT":
                self._current_direction = "WEST"

        # East
        elif self._current_direction == "EAST":
            if direction == "LEFT":
                self._current_direction = "NORTH"
            if direction == "RIGHT":
                self._current_direction = "SOUTH"

        # West
        elif self._current_direction == "WEST":
            if direction == "LEFT":
                self._current_direction = "SOUTH"
            if direction == "RIGHT":
                self._current_direction = "NORTH"

    def reflect(self):
        """Reverses current direction of a ray"""
        if self._current_direction == "NORTH":
            self._current_direction = "SOUTH"

        elif self._current_direction == "SOUTH":
            self._current_direction = "NORTH"

        elif self._current_direction == "EAST":
            self._current_direction = "WEST"

        elif self._current_direction == "WEST":
            self._current_direction = "EAST"

        next_position = self.get_next_position()
        if next_position[0] == 0 or next_position[0] == 9 or next_position[1] == 0 or next_position[1] == 9:
            self.end_ray()

    def deflect(self, deflection_type):
        """
        Turns ray according to the deflection type.
        Deflection can be "LEFT" or "RIGHT" or "DOUBLE"
        Calls the reflect() or turn() method as needed.
        """
        if deflection_type == "DOUBLE":
            self.reflect()

        if deflection_type == "LEFT":
            self.turn("LEFT")

        if deflection_type == "RIGHT":
            self.turn("RIGHT")

    def end_ray(self):
        """
        This method is used when a ray is about to move into a border square.
        Will set ray status to "EXITED", set the exit position to the next position,
        update the current position, and return the exit_position as a tuple in
        the form (row, column).
        """
        self.set_status("EXITED")
        self._exit_position = self.get_next_position()
        return self._exit_position


if __name__ == "__main__":
    """Add code here to play a game"""
