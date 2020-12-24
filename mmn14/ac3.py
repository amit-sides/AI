import queue

def ac3(csp):
    q = queue.Queue()
    domains = csp[0]
    arcs = csp[1]
    for arc in arcs:
        q.put(arc)
    
    while not q.empty():
        arc = q.get()
        i = arc[0]
        #print "Checking", i
        if remove_inconsistent_values(csp, arc):
            for k in range(len(domains)):
                for temp_arc in arcs:
                    if (k == temp_arc[0] and i == temp_arc[1]) or (k == temp_arc[1] and i == temp_arc[0]):
                        q.put(temp_arc)
    return csp
                        
def remove_inconsistent_values(csp, arc):
    removed =  False
    domains = csp[0]
    arcs = csp[1]
    
    for x in domains[arc[0]]:
        allowed = False
        for y in domains[arc[1]]:
            if arc[2](x, y):
                allowed = True
                break
        if not allowed:
            print "Removing", x, "from", arc[0], "because of", arc[0], "->", arc[1]
            domains[arc[0]].remove(x)
            removed = True
    return removed


def main():
    domains = [[9],[8,9,10],[8,9,10]]
    
    def arc1(a, b):
        if a == b:
            return False
        if b == a + 1:
            return False
        return True
    s_arc1 = lambda b, a: arc1(a,b)
    
    def arc2(a, c):
        if a == c:
            return False
        if c == a + 1:
            return False
        if c == a + 2:
            return False
        return True
    s_arc2 = lambda c, a: arc2(a, c)
    
    def arc3(b, c):
        if b == c:
            return False
        if b == c + 1:
            return False
        return True
    s_arc3 = lambda c, b: arc3(b, c)
    
    arcs = [(0, 1, arc1), 
            (0, 2, arc2),
            (1, 0, s_arc1),
            (1, 2, arc3),
            (2, 0, s_arc2),
            (2, 1, s_arc3)]
    
    csp = (domains, arcs)
    print csp[0]
    ac3(csp)
    print csp[0]

if __name__ == "__main__":
    main()
                        