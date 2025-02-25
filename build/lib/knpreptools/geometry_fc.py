import numpy as np
import knpreptools as pr

def calc_projected_splay(conduit_direction,splay_direction):
    """Projects a splay (disto measurement from a station to the surrounding wall) 
    in the u,v plan perpendicular to the cave conduit direction.


    Args:
        conduit_direction (numpy.ndarray, list): list or array of [x,y,z] values 
            of the direction vector of the conduit at the point of interest.
            vector origins has to be (0,0,0).
            use function ... to determin the right direction of the vector.
        splay_direction (numpy.ndarray, list): list or array of [x,y,z] values 
            of the direction of splay. Splay values - node.
            vector origins has to be (0,0,0).

    Returns:
        numpy.ndarray: projected splay length in the u and v direction. 
            (splay vector projectedin the uv plan)
            array of two values [u,v]. 
            u is in horizontal x,y plane, and v is orthogonal to u in the uv plan.
    """
    #normalize vector w
    w = np.array(conduit_direction)
    w /= np.linalg.norm(w)
    #find normalized vector u in the horizontal plan, orthogonal to vector w
    if ((np.abs(w[0])>np.abs(w[1])) and (np.abs(w[0])!=0)):
        #checks that x is not equal to zero and that its longer than y
        u = np.array([-w[1]/w[0],1,0])
    elif ((np.abs(w[1])>np.abs(w[0])) and (np.abs(w[1])!=0)):
        u = np.array([1,-w[0]/w[1],0])

        u /= np.linalg.norm(u)
        #find normalized vector v, orthogonal to u, in the uv plan
        v = np.cross(u,w)
        #calculate the length of the projected vector w in the u and v direction
        s_u = np.dot(u,splay_direction)
        s_v = np.dot(v,splay_direction)

        return np.array([s_u,s_v])
    
    else:
        print('%s and %s are equal to zero. Normalize vector cannot be calculated'%(w[0],w[1]))
        return np.array([0,0])        



def get_conduit_direction(G):
    keys = list(G.nodes()) #list(dict(G.degree()).keys())
    conduit_directions = {}
    
    # get conduit direction
    
    for i,key in enumerate(keys):
        degree = G.degree()[key]
        # print(i)
        # if i==695:
        #     print(i)
        # calc w at the beginning  and end of a conduit
        if degree == 1:           
            #if node is the start or end of the cave
            neighbors = pr.find_neighbors(G,key)#[n for n in G.neighbors(key)]
            conduit_directions[key] = np.array(G.nodes('pos')[key]) - np.array(G.nodes('pos')[neighbors[0]])   
            if all(v == 0 for v in conduit_directions[key]): print(conduit_directions[key])        

        #calc w in the middle of a conduit
        elif degree == 2:
            #if the node $P_{i}$ is degree 2, $w=P_{i+1}-P_{i-1}$ 
            #conduit_directions[key] = np.array(pos3d[keys[i+1]])-np.array(pos3d[keys[i-1]])
            neighbors = [n for n in G.neighbors(key)]
            #find length of each vector, to transform in unit vector
            pos = np.array(G.nodes('pos')[key])
            pos_before = np.array(G.nodes('pos')[neighbors[0]])
            pos_after = np.array(G.nodes('pos')[neighbors[1]])
            vector_0 = pos - pos_before
            vector_1 = pos_after - pos
            length_0 = np.linalg.norm(vector_0)
            length_1 = np.linalg.norm(vector_1)
            #normalize (to prevent a change in direction)
            conduit_directions[key] = vector_0/length_0 - vector_1/length_1
            #conduit_directions[key] = np.array(G.nodes('pos')[neighbors[0]])/length_0 - np.array(G.nodes('pos')[neighbors[1]])/length_1
            if all(v == 0 for v in conduit_directions[key]): print(conduit_directions[key])
    
        elif degree > 2:
            # no projection for conduit intersections
            conduit_directions[key] = []
        

    return conduit_directions


def get_splay_direction(G):
    splays_direction = {} 
    splays = dict(G.nodes('splays'))
    keys = list(splays.keys())
    pos3d = pr.get_pos3d(G)
    for key in keys:
    #calculate the splay direction relative to its node
        #if the node exists. some nodes were survey duplicate, removed from the main graph
        if key in pos3d.keys():
            list_temp = []
            if splays[key]:
                for j in np.arange(len(splays[key])):
                    list_temp.append(np.array(splays[key][j])-np.array(pos3d[key]))
                splays_direction[key] = list_temp

    return splays_direction

def calc_conduit_dimensions(G, output = 'all'):#conduit_directions,splays_direction):
    '''
    FROM SPLAYS
    #possible outputs: 
        'geometric mean': np.sqrt((cs_width/2)*(cs_height/2))
        'cs_dimensions': {[cs_width, cs_height]}
        'projections': project splay in u, projected splay in v
        'all': geometric mean, cs_width, cs_height, project splay in u, projected splay in v
    
    '''
    
    
    
    conduit_directions = get_conduit_direction(G)
    splays_direction = get_splay_direction(G)

    projected_splays_u = {}
    projected_splays_v = {}

    cs_width = {}
    cs_height = {}
    geommean_radius = {}

    keys = list(splays_direction.keys())
    for key in keys:
    #calculate the projected splay length component in u and v direction
        #sometimes there is splays that were duplicates. 
        if key in conduit_directions:
            su=[]
            sv=[]
            if len(conduit_directions[key])>0:
                for splay_direction in splays_direction[key]:       
                    s = calc_projected_splay(conduit_directions[key],splay_direction)
                    print('s:', s)
                    if s is None:
                        pass
                    else:
                        su.append(s[0])
                        sv.append(s[1])
                # # store su and vs in a dictionnary
                # # this is only interesting for plots...
                projected_splays_u[key] = su
                projected_splays_v[key] = sv   

                # add zero to the array, in case all splays have been taken in the same direction
                su.append(0)
                sv.append(0)
                # print(key, '---', su, sv)
                # # extract the futherst coordinate on each side
                # print(key, '---', max(su), min(su), max(sv), min(sv))
            
                
                cs_width[key]  = np.round(max(su)-min(su),3)
                cs_height[key]  = np.round(max(sv)-min(sv),3)
                geommean_radius[key] = np.sqrt((cs_width[key]/2)*(cs_height[key]/2))
                
            else:
                #for intersections, calculate the mean of the splays, instead of the projections
                for splay_direction in splays_direction[key]: 
                    su.append(np.linalg.norm(splay_direction))
                    sv.append(np.linalg.norm(splay_direction))
                cs_width[key] = np.round(np.mean(su),3)
                cs_height[key] = np.round(np.mean(sv),3)
                geommean_radius[key] = np.sqrt((cs_width[key]/2)*(cs_height[key]/2))
    

    if output=='all':
        return geommean_radius, cs_width, cs_height, projected_splays_u, projected_splays_v
    
    elif output == 'geometric mean':
        return geommean_radius
    
    elif output == 'csdim':
        csdim={}
        for k in cs_width.keys():
            csdim[k] = list(d[k] for d in [cs_width,cs_height])
        return csdim
    
    elif output == 'projections':
        return projected_splays_u, projected_splays_v
    

