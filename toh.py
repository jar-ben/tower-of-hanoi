import argparse

class TOH:
    """A class for computing and printing instructions on solving the Tower of Hanoi problem"""

    def __init__(self, n, sourceRod="rod1", auxRod="rod2", targetRod="rod3"):
        self.n = n # the number of disks
        self.rodNames = {1 : sourceRod, 2 : auxRod, 3 : targetRod}
        self.algorithm = "recursive"
        self.instructions = []

    def setAlgorithm(self, alg):
        """Set the algorithm to be used for computing the moving instructions"""
        assert alg in ["iterative", "recursive"], "only the 'iterative' and 'recursive' algorithms are supported"
        self.algorithm = alg

    def compute_instructions(self):
        """Computes instructions for moving all disks from the source rod to the target rod.
        Either the recursive or the iterative algorithm is used.
        """
        self.instructions = []
        if self.algorithm == "recursive":
            self.instructions = self.compute_recursive(self.n)
        elif self.algorithm == "iterative":
            self.instructions = self.compute_iterative()
        return self.instructions

    def print_instructions(self):
        """Prints the computed instructions for moving the disks"""
        if self.instructions == [] and self.n > 0:
            print("The instructions were not computed yet. Computing...")
            self.compute_instructions()
        print("To move all disks from the source to the target disk, perform the following {} step(s) (one disk per step):".format(len(self.instructions)))
        for ins in self.instructions:
            print("{} --> {}".format(self.rodNames[ins[0]], self.rodNames[ins[1]]))

    def compute_recursive(self, n, source=1, aux=2, target=3):
        """The basic recursive algorithm for the Tower of Hanoi. Due to the recursion,
        the computation is not as efficient as an iterative one. Especially, if the
        (recursion) stack limit is very low. However, on the other hand, the recursive
        version should be easier to understand for the reader.
        """
        if n == 0:
            return []
        elif n == 1:
            return [(source, target)]
        else:
            instructions = self.compute_recursive(n-1, source, target, aux)
            instructions += [(source, target)]
            instructions += self.compute_recursive(n-1, aux, source, target)
            return instructions

    def compute_iterative(self, source=1, aux=2, target=3):
        """Iterative algorithm for solving the Tower of Hanoi problem. The algorithm
        is more efficient than the recursive version (compute_recursive), however,
        it might be harder to understand.
        """
        if self.n % 2 == 0:
            aux, target = target, aux
        rods = {}
        rods[source] = [i for i in range(self.n, 0, -1)]
        rods[aux] = []
        rods[target] = []
        instructions = []

        def move_between(rodA, rodB):
            if len(rods[rodA]) == 0:
                rods[rodA].append(rods[rodB].pop())
                return (rodB, rodA)
            elif len(rods[rodB]) == 0:
                rods[rodB].append(rods[rodA].pop())
                return (rodA, rodB)
            elif rods[rodA][-1] < rods[rodB][-1]:
                rods[rodB].append(rods[rodA].pop())
                return (rodA, rodB)
            else:
                rods[rodA].append(rods[rodB].pop())
                return (rodB, rodA)

        for i in range(1, pow(2, self.n)):
            if i % 3 == 1:
                instructions.append(move_between(source, target))
            elif i % 3 == 2:
                instructions.append(move_between(source, aux))
            else:
                instructions.append(move_between(aux, target))
        return instructions


def verify_instructions(n, instructions, source=1, aux=2, target=3):
    """Verifies whether a given set of instructions moves all n disks from the source rod to the target rod.
    Basically, we simulate the execution of the instructions. Also, we initially check that the the number of
    steps/instructions is optimal, i.e., 2^n - 1.
    """

    assert len(instructions) == pow(2, n) - 1, "got {} instructions but expecting {}".format(len(instructions), pow(2, n) -1)

    # creates virtual rods
    rods = {}
    rods[source] = [i for i in range(n, 0, -1)]
    rods[aux] = []
    rods[target] = []

    # perform one-by-one individual instructions and check that they comply with the TOH rules
    for ins in instructions:
        assert len(ins) == 2, "invalid instruction '{}'".format(ins)
        sourceRod = ins[0]
        targetRod = ins[1]
        assert sourceRod in [source, aux, target], "the source rod '{}' is unknown".format(sourceRod)
        assert targetRod in [source, aux, target], "the target rod '{}' is unknown".format(targetRod)
        assert len(rods[sourceRod]) > 0, "trying to pick a disk from an empty rod"
        assert len(rods[targetRod]) == 0 or rods[targetRod][-1] > rods[sourceRod][-1], "trying to put a disk on a smaller one"
        rods[targetRod].append(rods[sourceRod].pop())

    assert len(rods[source]) == 0, "the source rod is not empty at the end"
    assert len(rods[aux]) == 0, "the auxiliary rod is not empty at the end"
    assert len(rods[target]) == n, "the target rod does not contain all the disks at the end"


def run_tests():
    # verifies the recursive algorithm for 0-9 disks
    for i in range(10):
        instructions = TOH(i).compute_instructions()
        verify_instructions(i, TOH(i).compute_instructions())

    # verifies the iterative algorithm for 0-9 disks
    for i in range(10):
        toh = TOH(i)
        toh.algorithm = "iterative"
        verify_instructions(i, toh.compute_instructions())

if __name__ == "__main__":
    infoMessage = "A simpe tool for solving the Tower of Hanoi problem (see https://en.wikipedia.org/wiki/Tower_of_Hanoi). " \
        "You can run the tool via 'python ./toh -n <k>' where <k> is the number of disks on the source rod. " \
        "Call 'python ./toh --help' to see all available options."
    parser = argparse.ArgumentParser(infoMessage)
    parser.add_argument("--num-of-disks", "-n", type=int, help="Specify the number of disks on the source rod.")
    parser.add_argument("--algorithm", "-a", choices=["recursive", "iterative"], help="Choose an algorithm to be used to compute the instructions.", default="iterative")
    parser.add_argument("--source", help="Specify the name of the source rod.", default="rod1")
    parser.add_argument("--target", help="Specify the name of the target rod.", default="rod3")
    parser.add_argument("--aux", help="Specify the name of the auxiliary rod.", default="rod2")
    parser.add_argument("--tests", action="store_true", help="Run tests to check the tool.")
    args = parser.parse_args()
    if args.tests:
        run_tests()
    elif args.num_of_disks is None:
        print("Please, specify the number of disks, e.g., 'python ./toh -n 5'")
    elif args.num_of_disks < 1:
        print("Please specify a positive number of disks.")
    else:
        toh = TOH(args.num_of_disks, args.source, args.aux, args.target)
        toh.setAlgorithm(args.algorithm)
        toh.compute_instructions()
        toh.print_instructions()
