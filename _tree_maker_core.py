# modified from https://sourceforge.net/p/golly/code/ci/master/tree/Scripts/Python/glife/RuleTree.py#l153

def getfilename(rule):
    return f'Rule:{rule}'
    
def rule(name, numStates, numNeighbors):
    '''
    @rule('Foo', numStates=5, numNeighbors=8)
    def function(n):
        """Rule description here.
    @COLORS
    You can include a colors section."""
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
            f.write(fun.__doc__[:fun.__doc__.find('@COLORS')])
            writeout(f)
            f.write(fun.__doc__[fun.__doc__.find('@COLORS'):])

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
