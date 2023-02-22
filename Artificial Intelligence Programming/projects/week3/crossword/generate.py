import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # check for variable in self. domains
        for variable in self.crossword.variables:
            # create copy of variables as words
            words = self.crossword.words
            # check if variable copy is in words
            for word in words:
                #  confirm length of word 
                if len(word) != variable.length:
                    # remove values that are inconsistent with a variable's unary constraints
                    self.domains[variable].remove(word)
                    
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # define overlaps
        overlap = self.crossword.overlaps[x,y]
        # list for incorrects
        incorrect = []
        # check if any overlap
        if overlap != None:
            # loop though words in x
            for word_x in self.domains[x]:
                revise = False
                # loop though words in y
                for word_y in self.domains[y]:
                    #check if oveerlap at start of x or y but not the same word
                    if word_x[overlap[0]] == word_y[overlap[1]]:
                    # initialize correct
                        revise = True
                        break
                # check if correct and add word if not correct to incorrect list
                if not revise:
                    return True
            #check if word in incorrect and remove from domain if incorrect
            for word in incorrect:
                self.domains[x].remove(word)
            if incorrect:
                return True
            else:
                return False
        else:
            return False
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # confirm arcs is none
        if arcs is None:
            # create list for arcs
            arcs = []
        # loop through x and y for arcs
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    # make sure the arcs not identical and append to arcs lis
                    if x != y:
                        arcs.append((x,y))
        # confirm len of arcs to make sure arc is there and remove arc combo for list
        while len(arcs) != 0:
            (x, y) = arcs.pop(0)
            if self.revise(x,y):#
                # once out of moves for x return false
                if len(self.domains[x]) == 0:
                    return False
                # check for potential neibor moves and confirm not same as y
                for z in self.crossword.neighbors(x):
                    if z != y:
                        arcs.append((z,x))
        return True
            

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # loop through variable in crossword
        for variable in self.crossword.variables:
            # confirm var in assignment
            if variable not in assignment.keys():
                return False
            # confirm var in assignemt is not in words
            elif assignment[variable] not in self.crossword.words:
                return False
            else:
                return True
            
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # loop through x axis and confirm lenght of word
        for x in assignment:
            word_x = assignment[x]
            if len(word_x) != x.length:
                return False
            # loop through y axis and confirm lenght of word
            for y in assignment:
                word_y = assignment[y]
                # confirm not same
                if x != y:
                    if word_x == word_y:
                        return False
                    # define overlaps
                    overlap = self.crossword.overlaps[x,y]
                    # check if any overlap
                    if overlap != None:
                        if word_x[overlap[0]] != word_y[overlap[1]]:
                            return False                
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # define words
        words = self.domains[var]
        #define neighbors
        neighbors = self.crossword.neighbors(var)
        #define counter
        counter = []
        # loop through words txt
        for word in words:
            # initialize count to 0
            count = 0
            #loop through neighbors
            for neighbor in neighbors:
                # if neighbor not used yet and word is in words, add to counter
                if neighbor not in assignment and word in self.domains[neighbor]:
                    count += 1
            counter.append(count)
        # sort words
        sort_words = list(zip(words,counter))
        sort_words.sort(key=lambda x: x[1])
        # return  next word    
        return [word[0] for word in sort_words]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        #define unnassigned variable
        un_var = set(self.domains.keys()) - set(assignment.keys())
        #define result
        result= [var for var in un_var]
        #sort result and return new result
        result.sort(key = lambda x: (len(self.domains[x]), -len(self.crossword.neighbors(x))))
        
        return result[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # confirm if assignment completed
        if len(assignment) == len(self.crossword.variables):
            return assignment
        #define var for selected un_var
        var = self.select_unassigned_variable(assignment)
        # define words
        words = self.domains[var]
        #loop through words
        for word in words:
            assignment[var] = word
            # confirm if consistent and backtrack to result
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None: 
                    return result
        # or no result    
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
