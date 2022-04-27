from _tree_maker_core import *

@rule('Fusion', 11, 8)
def Fusion(n):
    """
    Fusion is a rule I devised that is a 'fusion' of many different wire-like rules. It steals properties from:
    * Wireworld++ => tiny AND/XOR gates
    * NoTimeAtAll (Moore neighborhood variant) => stagnating signals
    * Digital => diagonal inputs, orthogonal outputs
    * DECA => tiny AND/ANDNOT gates
    
    States:
    
    0. background
    1. strong head
    2. strong tail
    3. strong wire
    4. weak head
    5. weak tail
    6. weak wire
    7. NTAA head 1
    8. NTAA head 0
    9. NTAA tail
    10. NTAA wire
    @COLORS
    0 0 0 0
    1 255 255 0
    2 127 127 0
    3 102 32 0
    4 255 255 255
    5 136 136 136
    6 34 34 34
    7 0 255 0
    8 255 0 0
    9 127 127 127
    10 0 0 127
    """
    
    neighbors, me = n[:-1], n[-1]
    orthneighbors = neighbors[4:8]
    diagneighbors = neighbors[0:4]
    counts = [0] * 11
    orthcounts = [0] * 11
    diagcounts = [0] * 11
    for i in neighbors:
        counts[i] += 1
    for i in orthneighbors:
        orthcounts[i] += 1
    for i in diagneighbors:
        diagcounts[i] += 1

    if me == 0: return 0 # background
    
    elif me == 1: return 2 # strong head
    elif me == 2: return 3 # strong tail
    elif me == 3: # strong wire
        if (counts[7] + counts[8] == 1) and (counts[3] + counts[6] in (1, 2)):
            return 1 if counts[7] == 1 else 2 # change to head or tail if transition from NTAA
        if counts[1] not in (1, 2) and counts[4] != 2: return 3 # wouldn't turn on anyway
        if has_orth_seq(neighbors, [[3, 6], 7, [1, 4], 0]): return 6 # blocked by NTAA cell
        return 1 # yay, can turn on
    elif me == 4: return 5 # weak head
    elif me == 5: return 6 # weak tail
    elif me == 6: # weak wire
        if (counts[7] + counts[8] == 1) and (counts[3] + counts[6] in (1, 2)):
            return 4 if counts[7] == 1 else 5 # change to head or tail if transition from NTAA
        if counts[1] != 1 and counts[4] not in (1, 2): return 6 # wouldn't turn on anyway
        if has_orth_seq(neighbors, [[3, 6], 7, [1, 4], 0]): return 6 # blocked by NTAA cell
        return 4 # yay, can turn on
    elif me == 7 or me == 8: # NTAA head 1 or 0
        if has_any(neighbors, [7, 8, 9, 10]): # behave as wire
            if (has_any(neighbors, [7, 8]) and has_any(neighbors, [9])) or not has_any(neighbors, [10]):
                return 9 # change to tail
            return me # stay the same
        else: # behave as DECA blocker cell
            # swap state if has orth 2, 3, 5
            if has_any(orthneighbors, [2, 3, 5]):
                return 7 if me == 8 else 8
            return me
    elif me == 9: # NTAA tail
        if not (has_any(neighbors, [9]) and has_any(neighbors, [10])):
            return me
        return 10 # stay the same
    elif me == 10: # NTAA wire
        if not has_any(neighbors, [7, 8, 9, 10]): return 8 # make sure something bad doesn't happen: DECA cell
        if has_orth_seq(neighbors, [0, 0, [2, 5, 9], 0]): return 10 # can only turn on if not next to tail
        if sum(orthcounts[i] for i in (2, 3, 5, 6, 9, 10)) == 1 and sum(diagcounts[i] for i in (1, 3, 4, 6, 7, 8, 10)) == 2: # compute function
            return 7 if sum(diagcounts[i] for i in (1, 4, 7)) == 1 else 8
        else: # do nothing
            return 10
            
    
    
    
    
