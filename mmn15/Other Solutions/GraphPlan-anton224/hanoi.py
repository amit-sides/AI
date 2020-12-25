def createDomainFile(domainFileName, n):
    numbers = list(range(n))  # [0,...,n-1]
    pegs = ['a', 'b', 'c']
    domainFile = open(domainFileName, 'w')  # use domainFile.write(str) to write to domainFile
    "*** YOUR CODE HERE ***"

    s = "Propositions:\n"

    for p in pegs:
        s += "clear " + p + " "

    for disk in range(n):
        for p in pegs:
            s += "disk " + str(disk) + "on peg " + p + " "

    for disk in range(n):
        for p in pegs:
            s += "disk " + str(disk) + "on top " + p + " "

    for disk in range(n):
        for p in pegs:
            s += "disk " + str(disk) + "on bottom " + p + " "

    for disk1 in range(n):
        for disk2 in range(n):
            if disk1 < disk2:
                s += "disk " + str(disk1) + "on disk " + str(disk2) + " "

    # The actions
    s += "\nActions:\n"
    for from_peg in pegs:
        for to_peg in pegs:
            for disk1 in range(n):
                for disk2 in range(n):
                    if from_peg != to_peg and disk1 < disk2:
                        s += "Name: move disk " + str(disk1) + " from disk " + str(
                            disk2) + " from peg " + from_peg + " to bottom " + to_peg + "\n"

                        s += "pre: "
                        s += "disk " + str(disk1) + "on disk " + str(disk2) + " "
                        s += "disk " + str(disk1) + "on top " + from_peg + " "
                        s += "disk " + str(disk1) + "on peg " + from_peg + " "
                        s += "disk " + str(disk2) + "on peg " + from_peg + " "
                        s += "clear " + to_peg + "\n"

                        s += "add: "
                        s += "disk " + str(disk1) + "on top " + to_peg + " "
                        s += "disk " + str(disk1) + "on bottom " + to_peg + " "
                        s += "disk " + str(disk1) + "on peg " + to_peg + " "
                        s += "disk " + str(disk2) + "on top " + from_peg + "\n"

                        s += "delete: "
                        s += "disk " + str(disk1) + "on disk " + str(disk2) + " "
                        s += "disk " + str(disk1) + "on top " + from_peg + " "
                        s += "disk " + str(disk1) + "on peg " + from_peg + " "
                        s += "clear " + to_peg + "\n"

    for from_peg in pegs:
        for to_peg in pegs:
            for disk1 in range(n):
                for disk2 in range(n):
                    if from_peg != to_peg and disk1 < disk2:
                        s += "Name: move disk " + str(disk1) + " from bottom " + from_peg + " to disk " + str(
                            disk2) + " on peg " + to_peg + "\n"

                        s += "pre: "
                        s += "disk " + str(disk1) + "on peg " + from_peg + " "
                        s += "disk " + str(disk1) + "on top " + from_peg + " "
                        s += "disk " + str(disk1) + "on bottom " + from_peg + " "
                        s += "disk " + str(disk2) + "on peg " + to_peg + " "
                        s += "disk " + str(disk2) + "on top " + to_peg + "\n"

                        s += "add: "
                        s += "disk " + str(disk1) + "on top " + to_peg + " "
                        s += "disk " + str(disk1) + "on disk " + str(disk2) + " "
                        s += "disk " + str(disk1) + "on peg " + to_peg + " "
                        s += "clear " + from_peg + "\n"

                        s += "delete: "
                        s += "disk " + str(disk1) + "on peg " + from_peg + " "
                        s += "disk " + str(disk1) + "on top " + from_peg + " "
                        s += "disk " + str(disk1) + "on bottom " + from_peg + " "
                        s += "disk " + str(disk2) + "on top " + to_peg + "\n"

    for from_peg in pegs:
        for to_peg in pegs:
            for disk in range(n):
                if from_peg != to_peg:
                    s += "Name: move disk " + str(disk) + " from bottom " + from_peg + " to bottom " + to_peg + "\n"

                    s += "pre: "
                    s += "disk " + str(disk) + "on peg " + from_peg + " "
                    s += "disk " + str(disk) + "on top " + from_peg + " "
                    s += "disk " + str(disk) + "on bottom " + from_peg + " "
                    s += "clear " + to_peg + "\n"

                    s += "add: "
                    s += "disk " + str(disk) + "on peg " + to_peg + " "
                    s += "disk " + str(disk) + "on top " + to_peg + " "
                    s += "disk " + str(disk) + "on bottom " + to_peg + " "
                    s += "clear " + from_peg + "\n"

                    s += "delete: "
                    s += "disk " + str(disk) + "on peg " + from_peg + " "
                    s += "disk " + str(disk) + "on top " + from_peg + " "
                    s += "disk " + str(disk) + "on bottom " + from_peg + " "
                    s += "clear " + to_peg + "\n"

    for from_peg in pegs:
        for to_peg in pegs:
            for disk1 in range(n):
                for disk2 in range(n):
                    for disk3 in range(n):
                        if from_peg != to_peg and disk1 < disk2 and disk1 < disk3:
                            s += "Name: move disk " + str(disk1) + " from disk " + str(
                                disk2) + " from peg " + from_peg + " to disk " + str(disk3) + "on peg " + to_peg + "\n"

                            s += "pre: "
                            s += "disk " + str(disk1) + "on_disk " + str(disk2) + " "
                            s += "disk " + str(disk1) + "on_top " + from_peg + " "
                            s += "disk " + str(disk1) + "on_peg " + from_peg + " "
                            s += "disk " + str(disk2) + "on_peg " + from_peg + " "
                            s += "disk " + str(disk3) + "on_top " + to_peg + " "
                            s += "disk " + str(disk3) + "on peg " + to_peg + "\n"

                            s += "add: "
                            s += "disk_" + str(disk1) + "on_top_" + to_peg + " "
                            s += "disk_" + str(disk1) + "on_peg_" + to_peg + " "
                            s += "disk_" + str(disk1) + "on_disk_" + str(disk3) + " "
                            s += "disk_" + str(disk2) + "on_top_" + from_peg + "\n"

                            s += "delete: "
                            s += "disk_" + str(disk1) + "on_disk_" + str(disk2) + " "
                            s += "disk_" + str(disk1) + "on_top_" + from_peg + " "
                            s += "disk_" + str(disk1) + "on_peg_" + from_peg + " "
                            s += "disk_" + str(disk3) + "on_top_" + to_peg + "\n"
    domainFile.write(s)
    domainFile.close()


def createProblemFile(problemFileName, n):
    problemFile = open(problemFileName, 'w')  # use problemFile.write(str) to write to problemFile

    "*** YOUR CODE HERE ***"
    s = "Initial state: "
    for disk in range(n):
        if disk + 1 < n:
            s += "disk " + str(disk) + "on peg a "
            s += "disk " + str(disk) + "on disk " + str(disk + 1) + " "

    s += "clear b "
    s += "clear c "
    s += "disk " + str(n - 1) + "on peg a "
    s += "disk " + str(n - 1) + "on bottom a "
    s += "disk 0 on top a\n"

    s += "Goal state: "
    for disk in range(n):
        if disk + 1 < n:
            s += "disk " + str(disk) + "on peg c "
            s += "disk " + str(disk) + "on disk " + str(disk + 1) + " "
    s += "clear b "
    s += "clear a "
    s += "disk " + str(n - 1) + "on peg c "
    s += "disk " + str(n - 1) + "on bottom c "
    s += "disk 0 on top c\n"

    problemFile.write(s)
    problemFile.close()


import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: hanoi.py n')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    domainFileName = 'hanoi' + str(n) + 'Domain.txt'
    problemFileName = 'hanoi' + str(n) + 'Problem.txt'

    createDomainFile(domainFileName, n)
    createProblemFile(problemFileName, n)