from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# variable for knowledge base
kb = And(
    # logic for a,b,c are either a knight OR a knave BUT NOT both knight AND knave
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Or(CKnight,CKnave),
    Not(And(AKnight,AKnave)),
    Not(And(BKnight,BKnave)),
    Not(And(CKnight,CKnave)),
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # implement knowledge base from variable
    kb,
    # because of the implication... that A is knight
    Implication(AKnight, And(AKnight, AKnave)),
    #implication that A is a knave because A cannot be both knight AND knave
    Implication(AKnave, Not(And(AKnight,AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    # implement knowledge base from variable
    kb,
    # implication that both are knaves based on A statement from knight
    Implication(AKnight, And(AKnave,BKnave)),
    # implication that both are knaves based on A statement from knave
    Implication(AKnave, Not(And(AKnave,BKnave))),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    # implement knowledge base from variable
    kb,
    # implication that A is knight saying both are either knight OR knave
    Implication(AKnight, Or(And(AKnight,BKnight), And(AKnave,BKnave))),
    # implication that A is knave saying both are either knight OR knave
    Implication(AKnave, Not(Or(And(AKnight,BKnight),And(AKnave,BKnave)))),
    # implication that B is knight saying both are different
    Implication(BKnight, Or(And(AKnave,BKnight),And(AKnight,BKnave))),
    # implication that B is knave saying both are different
    Implication(BKnave, Not(Or(And(AKnave,BKnight),And(AKnight,BKnave)))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    # implement knowledge base from variable
    kb,
    # implication that A is knight saying either knight OR knave
    Implication(AKnight, Or(AKnight,AKnave)),
    # implication that A is knave saying either knight OR knave
    Implication(AKnave, Not(Or(AKnight,AKnave))),
    # implication that B is knight saying C is knave
    Implication(BKnight, CKnave),
    # implication that B is knave saying C is knave
    Implication(BKnave, Not(CKnave)),
    # implication that C is knight saying A is knight
    Implication(CKnight, AKnight),
    # implication that C is knave saying A is knight
    Implication(CKnave, Not(AKnight))
    
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
