import sys
pin_coord=[[(0, 3), (0, 1), (3, 2), (3, 1)], [(0, 2), (4, 3), (4, 1)], [(0, 1), (0, 2), (0, 3), (2, 2)], [(0, 1), (2, 2), (2, 1)]]
wire_con=[['g1.p1', 'g3.p2'], ['g1.p3', 'g4.p2'], ['g1.p4', 'g2.p1'], ['g4.p1', 'g3.p3'], ['g4.p3', 'g3.p1'], ['g2.p2', 'g3.p4'], ['g2.p3', 'g1.p2']]
def calc_wire_len(l):
    print(232323)
    print(l)
    ans=0
    for i in l:
        minx=sys.maxsize
        maxx=-1
        miny=sys.maxsize
        maxy=-1
        for j in i:
            if(j[0]<minx):
                minx=j[0]
            if(j[0]>maxx):
                maxx=j[0]
            if(j[1]<miny):
                miny=j[1]
            if(j[1]>maxy):
                maxy=j[1]
        print(minx,maxx,miny,maxy)
        ans+=((maxx-minx)+(maxy-miny))
        print(ans)
    return(ans)
gates2={'g2': (0, 0), 'g1': (4, 0), 'g3': (7, 0), 'g4': (9, 0)}
final_pin_coord=[]
for i in wire_con:
    k=[]
    for j in i:
        t=[]
        r=pin_coord[int(j[1])-1][int(j[4])-1]
        t.append(r[0]+gates2[j[0:2]][0])
        t.append(r[1]+gates2[j[0:2]][1])
        k.append(t)
    final_pin_coord.append(k)
print(final_pin_coord)
   
wire_len=calc_wire_len(final_pin_coord)
print(wire_len)
