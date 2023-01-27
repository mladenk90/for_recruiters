import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # dictionary for paretns
    parents = dict()
    # initialize genes
    genes = 0
    # initialize probablity
    prob = 1
    # loop through people to find person
    for person in people:
        # check if in one-gene,two_genes, or no gene
        if person in one_gene:
            genes = 1
        elif person in two_genes:
            genes = 2
        elif person not in one_gene and person not in two_genes:
            genes = 0
        # defin var for trait using have_trait
        trait = person in have_trait
        # def var for mother
        mother = people[person]["mother"]
        # def var for mother        
        father = people[person]["father"]    
    
        # check if is parent with no parents
        if mother is None and father is None:
            gene_prob = PROBS["gene"][genes]
        else:
            # check for mother
            if mother in one_gene:
                parents["mother"] = (1 - PROBS["mutation"]) * 0.5
            elif mother in two_genes:
                parents["mother"] = 1 - PROBS["mutation"]
            else:
                parents["mother"] = PROBS["mutation"]
            # check for father
            if father in one_gene:
                parents["father"] = (1 - PROBS["mutation"]) * 0.5
            elif father in two_genes:
                parents["father"] = 1 - PROBS["mutation"]
            else:
                parents["father"] = PROBS["mutation"]
            # check for person
            if person in one_gene:
                gene_prob = (parents["mother"] * (1 - parents["father"])) + (parents["father"]) * (1 - parents["mother"])
            elif person in two_genes:
                gene_prob = parents["mother"] * parents["father"]
            else:
                gene_prob = (1 - parents["father"]) * (1 - parents["mother"])
        # check if person has a trait
        if trait:
            gene_trait_prob = PROBS["trait"][genes][True]
        else:
            gene_trait_prob = PROBS["trait"][genes][False]
        # calculate probability
        prob = prob * gene_trait_prob * gene_prob
    return prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # check if person in probabilities
    for person in probabilities:
        # defin var for trait using have_trait
        trait = person in have_trait
        # check prob of each possibiity
        if person in two_genes:
            if trait:
                probabilities[person]["gene"][2] += p
                probabilities[person]["trait"][True] += p
            else:
                probabilities[person]["gene"][2] += p
                probabilities[person]["trait"][False] += p
        elif person in one_gene:
            if trait:
                probabilities[person]["gene"][1] += p
                probabilities[person]["trait"][True] += p
            else:
                probabilities[person]["gene"][1] += p
                probabilities[person]["trait"][False] += p
        else:
            if trait:
                probabilities[person]["gene"][0] += p
                probabilities[person]["trait"][True] += p
            else:
                probabilities[person]["gene"][0] += p
                probabilities[person]["trait"][False] += p

        

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # intitialize var for sum
    sum_values = 0
    # confirm sum of probs is exactly 1
    # check if person in probabilities
    for person in probabilities:
        # check if field im person's probablities
        for field in probabilities[person]:
            # initialize value of prob-total based on sum of probs
            values = probabilities[person][field].values()
            sum_values = sum(values)
            # check that value is in person's field in probablities
            for genes in probabilities[person][field]:
                # update prob total
                probabilities[person][field][genes] = (probabilities[person][field][genes] * 1) / sum_values

if __name__ == "__main__":
    main()
