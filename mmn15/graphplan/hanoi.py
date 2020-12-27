def get_third_peg(pegs, src_peg, dest_peg):
  for peg in pegs:
    if peg == src_peg:
      continue
    if peg == dest_peg:
      continue
    return peg
  return None

def createDomainFile(domainFileName, n):
  numbers = list(range(n)) # [0,...,n-1]
  pegs = ['a','b', 'c']
  domainFile = open(domainFileName, 'w') #use domainFile.write(str) to write to domainFile

  # Writes propositions
  domainFile.write("Propositions:\n")
  for number in numbers:
    for peg in pegs:
      prop = "{}{} ".format(peg, number)
      domainFile.write(prop)

  # Writes actions
  domainFile.write("\nActions:\n")
  for number in numbers:
    for src_peg in pegs:
      for dest_peg in pegs:
        if src_peg == dest_peg:
          continue
        name = "Name: M{}{}{}".format(number, src_peg, dest_peg)
        third_peg = get_third_peg(pegs, src_peg, dest_peg)
        preconditions = ["{}{}".format(third_peg, i) for i in range(number)]
        pre = "pre: {}{} {}".format(src_peg, number, " ".join(preconditions))
        add = "add: {}{}".format(dest_peg, number)
        delete = "delete: {}{}".format(src_peg, number)
        domainFile.write(name + "\n")
        domainFile.write(pre + "\n")
        domainFile.write(add + "\n")
        domainFile.write(delete + "\n")

  domainFile.close()  

def createProblemFile(problemFileName, n):
  numbers = list(range(n)) # [0,...,n-1]
  pegs = ['a','b', 'c']
  problemFile = open(problemFileName, 'w') #use problemFile.write(str) to write to problemFile

  # Writes initial state
  problemFile.write("Initial state: ")
  states = ["{}{}".format(pegs[0], i) for i in numbers]
  problemFile.write(" ".join(states))

  # Writes goal
  problemFile.write("\nGoal state: ")
  states = ["{}{}".format(pegs[-1], i) for i in numbers]
  problemFile.write(" ".join(states))

  problemFile.write("\n")
  problemFile.close()

import sys
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('Usage: hanoi.py n')
    sys.exit(2)
  
  n = int(float(sys.argv[1])) #number of disks
  domainFileName = 'hanoi' + str(n) + 'Domain.txt'
  problemFileName = 'hanoi' + str(n) + 'Problem.txt'
  
  createDomainFile(domainFileName, n)
  createProblemFile(problemFileName, n)