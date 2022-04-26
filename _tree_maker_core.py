# modified from https://sourceforge.net/p/golly/code/ci/master/tree/Scripts/Python/glife/RuleTree.py#l153

from textwrap import dedent

def has_orthagonal(n, s):
    #NW, NE, SW, SE, N, W, E, S, C
    for i in (4, 5, 6, 7):
        if n[i] == s: return True
    return False

def has_diagonal(n, s):
    #NW, NE, SW, SE, N, W, E, S, C
    for i in (0, 1, 2, 3):
        if n[i] == s: return True
    return False

def rotate(t, by=1):
    for i in range(by):
        t = t[1:] + (t[0],)
    return t

def has_orth_seq(n, seq):
    #NW, NE, SW, SE, N, W, E, S, C
    orths = n[4:8]
    for i in range(4):
        if rotate(orths, i) == seq:
            return True
    return False

def has_diag_seq(n, seq):
    #NW, NE, SW, SE, N, W, E, S, C
    raise SystemExit('todo')
    diags = n[0:4]
    for i in range(4):
        if rotate(diags, i) == seq:
            return True
    return False

def has_3side(n, side, c=True, cc=True):
    #0,  1,  2,  3,  4, 5, 6, 7
    #NW, NE, SW, SE, N, W, E, S, C
    sides = tuple()
    clockwise = ( # going clockwise
        (0, 4, 1),
        (1, 6, 3),
        (3, 7, 2),
        (2, 5, 0)
    )
    if c:
        sides += clockwise
    if reflect:
        sides += tuple(*(tuple(*reversed(p)) for p in clockwise))
    for i1, i2, i3 in sides:
        if (n[i1], n[i2], n[i3]) == side:
            return True
    return False


def getfilename(rule):
    return f'Rule:{rule}'
    
def rule(name, numStates, numNeighbors):
    '''
    @rule('Foo', numStates=5, numNeighbors=8)
    def function(n):
        """
        Rule description here.
        @COLORS
        You can include a colors section.
        It will automatically be dedented.
        """
        return something()

    For vonNeumann neighborhood, inputs are: N,W,E,S,C
    For Moore neighborhood, inputs are NW,NE,SW,SE,N,W,E,S,C
    '''
    
    numParams = numNeighbors + 1
    
    world = {}
    seq = []
    params = [0 for i in range(numParams)]
    nodeSeq = 0
    fun = None

    def decorator(f):
        nonlocal fun
        fun = f
        recur(numParams)
        # write out
        with open(getfilename(name), 'w') as f:
            f.write(f'@RULE {name}\n')
            f.write(dedent(fun.__doc__[:fun.__doc__.find('@COLORS')]))
            writeout(f)
            f.write(dedent(fun.__doc__[fun.__doc__.find('@COLORS'):]))

    def getNode(node):
        if node in world:
            return world[node]
        else:
            iNewNode = nodeSeq
            nodeSeq += 1
            seq.append(node)
            world[node] = iNewNode
            return iNewNode

    def recur(at):
        if at == 0:
            return fun(params)
        node = (at,)
        for i in range(numStates):
            params[numParams - at] = i
            node += (recur(at - 1),)
        return getNode(node)

    def writeout(f):
        f.write(f"num_states={numStates}\n")
        f.write(f"num_neighbors={numNeighbors}\n")
        f.write(f"num_nodes={len(seq)}\n")
        for rule in seq:
            f.write(' '.join(map(str,rule))+'\n')
        f.flush()
    
    return decorator
