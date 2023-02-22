import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # confirm count of cells and mines and confirm it is not 0, 0 means no mines
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        # empty set
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # confirm count of mines around, if 0 then no mines
        if self.count == 0:
            return self.cells
        # empty set
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # check cell and remove cell AND if mine update count of total mines remaining
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # check cell and remove cell if NOT mine
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # add selected cell to moves_made
        self.moves_made.add(cell)
        # mark cell safe if safe
        self.mark_safe(cell)
        # var for all available cells
        avail_cells = []
        # var for mines counted
        mines_counted = 0
        
        #loop through surrounding cells for mines
        for i in range(cell[0] - 1,cell[0] +2):
            for j in range(cell[1] - 1,cell[1] +2):
                # if (i,j) pair for cell is mine, then add to mines_counted
                if (i,j) in self.mines:
                    mines_counted += 1
                # make sure cell is valid and add to avail_cells to see what cells are remaiining 
                # and not confirmed safe or mine
                if 0 <= i < self.height and 0 <= j < self.width and (i,j) not in self.safes and (i,j) not in self.mines:
                    avail_cells.append((i,j))
        
        # add new sentence for value of `cell` and `count`
        add_sentence = Sentence(avail_cells, count - mines_counted)
        # add new sentence to existing knowledge
        self.knowledge.append(add_sentence)
        # loop through existing knowledge for sentence
        for sentence in self.knowledge:
            # check if sentence is already known_mine
            if sentence.known_mines():
                # loop through cells for known_mines via copied version of board for
                # updated cells and mines
                for cell in sentence.known_mines().copy():
                    # mark cell as mine if known_mine
                    self.mark_mine(cell)
            # check if sentence is already known_safe
            if sentence.known_safes():
                # loop through cells for known_safe via copied version of board for
                # updated cells and mines
                for cell in sentence.known_safes().copy():
                    # mark cell as safe if known_safe
                    self.mark_safe(cell)
        # loop through existing knowledge for sentence
        for sentence in self.knowledge:
            # check if added sentence is a subset of sentence, confirm count is > 0, and confirm added sentece is different from sentece
            if add_sentence.cells.issubset(sentence.cells) and sentence.count > 0 and add_sentence.count > 0 and add_sentence != sentence:
                # add new subset with only differences from initial set
                add_subset = sentence.cells.difference(add_sentence.cells)
                # add new subset for added sentence to count differences
                add_sentence_subset = Sentence(list(add_subset), sentence.count - add_sentence.count)
                # add new sentence subset to existing knowledge
                self.knowledge.append(add_sentence_subset)  

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # check if cell is safe
        for cell in self.safes:
            # confirm if move has already been made
            if cell not in self.moves_made:
                # show cell
                return cell
        # if not safe, disregard
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # var for all available moves
        avail_moves = []
        # loop through and find location of cell based on (i,j) pair
        for i in range(self.height):
            for j in range(self.width):
                # check if (i,j) pair is a move that has been made or is already a mine
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    # add possibility to available moves
                    avail_moves.append((i,j))
        # check to make sure there is an avail move left and choose randomly
        if len(avail_moves) != 0:
            return random.choice(avail_moves)
        else: 
            return None
