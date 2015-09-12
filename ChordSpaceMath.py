import pymultihash as MultiHash

import random

MAX_VAL = 2**256

def idToPoint(dim,id):
    """
    We're using a unit space for the position of our nodes.
    The mapping we use is to use the hash ID as the seed to an RNG.
    We should switch to either
    1) A universal RNG
    2) The mapping done by Symphony
    """
    idLong = MultiHash.parseHash(id)

    return (idLong,0)

def distance(p0,p1):
    """Returns the distance from point 1 to point 2?"""
    delta = sum([(a-b)**2.0 for a,b in zip(p0,p1)])**0.5
    if delta > MAX_VAL/2:
        return MAX_VAL-delta
    return delta

def midpoint(p0,p1):
    """Returns the midpoint between two points in a Euclidean Space"""
    a_0 = p0[0]
    b_0 = p1[0]
    sorted_points = sorted([a_0,b_0])
    delta = distance(p0,p1)/2
    m0 = (sorted_points[0]+delta) % MAX_VAL
    m1 = (sorted_points[1]-delta) % MAX_VAL
    return (min([m0,m1],key=lambda x: distance(p0,(x,0))),0)


def getDelaunayPeers(candidates,center):
    """
    This is the Distrubuted Greedy Voronoi Heuristic.

    center is some point in a space (we don't really care which) and the 
    heuristic decides which of the candidates are members of Delaunay 
    Triangulations with the center point.

    This allows a node located at center to quickly figure out its 
    Voronoi region.

    Error rate: Our heuristic overestimates approximately edge per node

    """
    if len(candidates) < 2:
        return candidates
    sortedCandidates = sorted(candidates,key=lambda x: distance(x,center))
    peers = [sortedCandidates[0]] #create a new list, initialized closest peer
    sortedCandidates = sortedCandidates[1:]
    for c in sortedCandidates:
        m = midpoint(c,center)
        accept = True
        for p in peers:
            if distance(m,p) < distance(m,center):  # if occluded by previous peer
                accept = False
                break
        if accept:
            peers.append(c)
    return peers

def getClosest(point,candidates):
    """Returns the candidate clostest to point."""
    return min(candidates,key=lambda x: distance(point,x))


