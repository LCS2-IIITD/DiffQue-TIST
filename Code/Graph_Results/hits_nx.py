import networkx as nx
from networkx.exception import NetworkXError

def hits_nx(G,max_iter=100,tol=1.0e-8,nstart=None,normalized=True):
    print "HERE !!"
    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise Exception("hits() not defined for graphs with multiedges.")
    if len(G) == 0:
        return {},{}
    # choose fixed starting vector if not given
    if nstart is None:
        h=dict.fromkeys(G,1.0/G.number_of_nodes())
    else:
        h=nstart
        # normalize starting vector
        s=1.0/sum(h.values())
        for k in h:
            h[k]*=s
    i=0
    while True: # power iteration: make up to max_iter iterations
        print i
        hlast=h
        h=dict.fromkeys(hlast.keys(),0)
        a=dict.fromkeys(hlast.keys(),0)
        # this "matrix multiply" looks odd because it is
        # doing a left multiply a^T=hlast^T*G
        for n in h:
            for nbr in G[n]:
                a[nbr]+=hlast[n]*G[n][nbr].get('weight',1)
        # now multiply h=Ga
        for n in h:
            for nbr in G[n]:
                h[n]+=a[nbr]*G[n][nbr].get('weight',1)
        # normalize vector
        s=1.0/max(h.values())
        for n in h: h[n]*=s
        # normalize vector
        s=1.0/max(a.values())
        for n in a: a[n]*=s
        # check convergence, l1 norm
        err=sum([abs(h[n]-hlast[n]) for n in h])
        if err < tol:
            break
        if i>max_iter:
            if normalized:
                s = 1.0/sum(a.values())
                for n in a:
                    a[n] *= s
                s = 1.0/sum(h.values())
                for n in h:
                    h[n] *= s
            return h,a
            # raise NetworkXError("HITS: power iteration failed to converge in %d iterations."%(i+1))
            # break
        i+=1
    if normalized:
        s = 1.0/sum(a.values())
        for n in a:
            a[n] *= s
        s = 1.0/sum(h.values())
        for n in h:
            h[n] *= s
    return h,a