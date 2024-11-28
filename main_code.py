#bounding block height maximum of max height of blocks and the average height when 2 blocks are kept one over the other
import time 
import sys
startime=time.time()
input_file=open("input.txt","r")
output_file=open("output.txt","w")

def calc_wire_len(l):  
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
        ans+=((maxx-minx)+(maxy-miny))
    return(ans)
        
def compute(avght,cluster_div_final_part,cluster_start):#a cluster is input
    def compute_cluster(avght,gwh_part,start_x):#an int_div length gates are input-they are sorted by width
        gates_temp={}
        fg=[]
        visited=[0]*(len(gwh_part))
        i=0
        bbheight2=avght
        
        while(i<len(gwh_part)):
            if (visited[i]==1):
                i+=1
                continue

            x=list([gwh_part[i]])
       
            visited[i]=1
          
            for j in range(i+1,len(gwh_part)):
              
                if((gwh_part[j][2]+gwh_part[i][2])<=avght and visited[j]!=1):
        
                    x=list([gwh_part[j]+["t"]])+x
                
                    visited[j]=1
                 
                    present_th=x[1][2]+x[0][2]
                    present_rh=x[1][2]
                    l=1
                    lb=0
                    p=1
                    for h in range(j+1,len(gwh_part)):
                        if(lb>=0 and ((x[l][1]-x[lb][1])>=gwh_part[h][1]) and ((gwh_part[h][2]+present_rh)<=avght) and p!=0 and visited[h]!=1):
                            present_rh+=x[l][2]
                            x.append(gwh_part[h]+["r"])
                    
                            l-=1
                            lb-=1
                            visited[h]=1
                            p-=1
                        elif((gwh_part[h][2]+present_th)<=avght and visited[h]==0 ):
                            x=list([gwh_part[h]+["t"]])+x
                          
                            p+=1
                            l+=1
                            lb+=1
                            present_th+=gwh_part[h][2]
                            visited[h]=1
                    break
                
            fg.append(x)

        k=start_x 
        
        for i in fg:
            if(len(i)>=2):
                for d in range(len(i)):
                    if(len(i[d])==3):
                        break
                gates_temp[i[d][0]]=(k,0)
                p=1
         
                while((d-p)>=0 or (d+p)<len(i) ):
                    if  (d-p)>=0:
                        gates_temp[i[d-p][0]]=(k,gates_temp[i[d-p+1][0]][1]+i[d-p+1][2])
                    if((d+p)<len(i)):
                        gates_temp[i[d+p][0]]=(gates_temp[i[d-p][0]][0]+i[d-p][1],gates_temp[i[d-p][0]][1])
                    p+=1
                k+=i[d][1]
                
            elif(len(i)==2):
                gates_temp[i[1][0]]=(k,0)
                gates_temp[i[0][0]]=(k,i[1][2])
                k+=i[1][1]
            else:
                gates_temp[i[0][0]]=(k,0)
                k+=i[0][1]

        return ([k,gates_temp])

    
    #calling inside function
    gates2={}
    start_x=cluster_start
    for c in cluster_div_final_part:
        r=(compute_cluster(avght,c,start_x))
        start_x=r[0]
        
        gates2.update(r[1])

    bbwidth2=start_x
    final_pin_coord=[]

    for i in wire_con:
        k=[]
        for j in i:
            t=[]
            jj=j.split(".")
            if jj[0] not in gates2:
                break
            else:
                r=pin_coord[int(jj[0][1:])-1][int(jj[1][1:])-1]
                t.append(r[0]+gates2[jj[0]][0])
                t.append(r[1]+gates2[jj[0]][1])
                k.append(t)
        if((len(k))!=0):
            final_pin_coord.append(k)
    
    wire_len=calc_wire_len(final_pin_coord)

    res=[wire_len,bbwidth2,avght,gates2]
    print(gates2)
def calc_wire_len(l):  
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
        ans+=((maxx-minx)+(maxy-miny))
    return(ans)
    return(res)




def combine_clusters(int_div,n_gates,cluster,gwh_clusters,gwh_clusters_inter,rem_gates,pin_coord,wire_con,totalarea,totalh,totalw,maxh):
    
    gates={}
    #making cluster_div_final
    #part1 -splitting into int_div parts
    cluster_div=[]
    cluster_div_final=[]#divide each group of gwh_clusters_inter into int_div number of partss where each part is sorted based on width their order remains half inc and half dec
   
    for cluster in gwh_clusters_inter:
        cluster_sublists = [] 
        for i in range(0, len(cluster), int_div):
            sublist = cluster[i:i+int_div]  
            cluster_sublists.append(sublist)  
        cluster_div.append(cluster_sublists)
    #part2-sorting each div based on width -dec order    
    for i in cluster_div:
        cluster_div_final_sublists=[]
        for j in i:
            k=sorted(j, key=lambda x: (x[1],x[0]),reverse=True)
            cluster_div_final_sublists.append(k)
        cluster_div_final.append(cluster_div_final_sublists)



    cluster_div_final.append([rem_gates])
 
    if(int_div==1):
        for i in cluster_div_final:#removing pin numbers
            for j in i:
                for k in j:
                    k.pop()
    
    cluster_start=0
    overall_wire_len=0
    bbheight=0
  
    for d in cluster_div_final:
        
        wire_len_min=sys.maxsize
        bbwidth_t=0
        gates_t={}
        for f in range(1,int_div+1):
            avght=max((totalh*f)//n_gates,maxh)
            v=compute(avght,d,cluster_start)
            if(v[0]<wire_len_min):
                wire_len_min=v[0]
                bbwidth_t=v[1]
                bbheight_t=v[2]
                gates_t=v[3]
                #print(len(gates_t))
        overall_wire_len+=wire_len_min
        cluster_start=bbwidth_t#total width
        bbheight=max(bbheight,bbheight_t)#total height
        gates.update(gates_t)
    result=[overall_wire_len,bbheight,cluster_start,gates,int_div]
    return(result)



#main_part
    

gwh=[]
cluster=[]#group of just gate names -list of lists
gwh_clusters=[]#gwh info of gourp of gates-list of lists
gwh_clusters_inter=[]#sorted each cluster in half inc and half dec based on number of pins connected in the gate
rem_gates=[]
pin_coord=[]
wire_con=[]
totalarea=0
totalh=0
totalw=0
maxh=0



while(True):
    y=input_file.readline().split()
    
    if len(y)==0:
        break

    elif(y[0][0]=="g"):
        x=[y[0],int(y[1]),int(y[2]),0]
        gwh.append(x)
        maxh=max(maxh,int(y[2]))
        totalh+=int(y[2])
        totalw+=int(y[1])
        totalarea+=(int(y[1])*int(y[2]))
    elif(y[0][0]=="p"):
        x=[]
        for j in range(2,len(y)-1,2):
            x.append((int(y[j]),int(y[j+1])))
        pin_coord.append(x)
    elif(y[0][0]=="w"):
        
        gate_name=y[1].split(".")
        gate_name_2=y[2].split(".")
        h=[gate_name[0],gate_name_2[0]]
        cluster.append(h)
        x=[y[1],y[2]]
        wire_con.append(x)

print(pin_coord)
#forming cluster
def merge(lsts):
    sets = [set(lst) for lst in lsts if lst]
    merged = True
    while merged:
        merged = False
        results = []
        while sets:
            common, rest = sets[0], sets[1:]
            sets = []
            for x in rest:
                if x.isdisjoint(common):
                    sets.append(x)
                else:
                    merged = True
                    common |= x
            results.append(common)
        sets = results
    return sets

cluster=(merge(cluster))
wire_con=merge(wire_con)
for i in wire_con:
    for j in i:
        jj=j.split(".")
        gwh[int(jj[0][1::])-1][-1]+=1

#list of those gates which have no wire connections are added to cluster_div_final-no need to divide and all,so it is the list with more than 7 gates 
rem_gates = []
for i in gwh:
    found = False
    for j in cluster:
        if i[0] in j:  
            found = True
            break  
    if not found:
        rem_gates.append(i)
rem_gates = sorted(rem_gates, key=lambda x: x[1], reverse=True)


#from gwh making gwh_clusters-all cluster gates in a list forming list of lists
for i in cluster:
    temp=[]
    for j in i:
        for k in gwh:
            if(k[0]==j):
                temp.append(k)
    gwh_clusters.append(temp)



#sorting all clusters in half increasing and half decreasing order
for i in gwh_clusters:
    t=sorted(i, key=lambda x: (x[3],x[0]),reverse=True)
    increasing_half = []
    decreasing_half = []
    for i  in range(len(t)):
        if i % 2 == 0:
            increasing_half.append(t[i]) 
        else:
            decreasing_half.append(t[i])

    increasing_half = increasing_half[::-1]
    t = increasing_half + decreasing_half
    gwh_clusters_inter.append(t)
    


n_gates=len(gwh)
wire_len_final=sys.maxsize
width_final=0
height_final=0
gates_final={}
if(n_gates<=200):
    for s in range(1,n_gates+1):
        int_div=s
        x=combine_clusters(int_div,n_gates,cluster,gwh_clusters,gwh_clusters_inter,rem_gates,pin_coord,wire_con,totalarea,totalh,totalw,maxh)
        if(x[0]<wire_len_final):
            wire_len_final=x[0]
            height_final=x[1]
            width_final=x[2]
            gates_final=x[3]
            best_int_div=x[4]
else:
    for s in range(1,n_gates+1,10):
        int_div=s
        x=combine_clusters(int_div,n_gates,cluster,gwh_clusters,gwh_clusters_inter,rem_gates,pin_coord,wire_con,totalarea,totalh,totalw,maxh)
        if(x[0]<wire_len_final):
            wire_len_final=x[0]
            height_final=x[1]
            width_final=x[2]
            gates_final=x[3]
            best_int_div=x[4]

packing_percent=(totalarea*100/(width_final*height_final))


#output writing
output_file.write("bounding_box"+" "+str(width_final)+" "+str(height_final)+"\n")
for i in gates_final:
    output_file.write(i+" "+str(gates_final[i][0])+" "+str(gates_final[i][1])+"\n")
output_file.write("wire_length"+" "+str(wire_len_final))
output_file.close()
input_file.close()


print(packing_percent)
print(wire_len_final)
endtime=time.time()
print(endtime-startime,"seconds")
