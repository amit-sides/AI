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
        return a != b
    s_arc1 = lambda b, a: arc1(a,b)
    
    def arc2(a, b):
        return b != a + 1
    s_arc2 = lambda b, a: arc2(a,b)
    
    def arc3(a, c):
        return c != a + 1
    s_arc3 = lambda c, a: arc3(a, c)
    
    def arc4(a, c):
        return c != a + 2
    s_arc4 = lambda c, a: arc4(a, c)
    
    def arc5(b, c):
        return b != c + 1
    s_arc5 = lambda c, a: arc5(a, c)
    
    def arc6(a, c):
        return a != c
    s_arc6 = lambda c, a: arc6(a, c)
    
    def arc7(b, c):
        return b != c
    s_arc7 = lambda c, b: arc7(b, c)
    
    arcs = [(0, 1, arc1), (1, 0, s_arc1),
            (0, 1, arc2), (1, 0, s_arc2),
            (0, 2, arc3), (2, 0, s_arc3),
            (0, 2, arc4), (2, 0, s_arc4),
            (1, 2, arc5), (2, 1, s_arc5),
            (0, 2, arc6), (2, 0, s_arc6),
            (1, 2, arc7), (2, 1, s_arc7)]
    
    csp = (domains, arcs)
    print csp[0]
    ac3(csp)
    print csp[0]

if __name__ == "__main__":
    main()
                        