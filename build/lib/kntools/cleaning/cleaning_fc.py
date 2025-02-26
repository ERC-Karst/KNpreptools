import networkx as nx
import numpy as np
# import kntools as kt



def add_edges(G,additional_edges, dict_address=None, flag = 'add'):
    """Add edges to a networkx cave graph, based on a list of edges
    Parameters
    ----------
    G : networkx graph 
        Graph produced with the function kn.from_therion_sql_enhanced

    additional_edges : list of tuple or list of lists
        list of edges to add to the graph. The edges will be created between already existing nodes, and a flag add will be added. 

        example:
        -----------
        in the case that use_fulladdress == True: additional_edges = [['full_address.0','full_address.1],['full_address.3','full_address.10]]
        if the current networkx key is used: additional_edges = [[67,2],[110,232]]

    dict_address : dict, optional
        by default this function takes the current networkx keys of the graph G. 
        When dict_address is not None, then it uses other node identifiers (for example, it can be the original node name)
        The dictionnary 
        stored in the graph attributes G.nodes('fulladdress').
        This attribute is created with the therion import function.

        example:
        --------
        Each current node id can be associated to a series of older ids, in the case that stations where regrouped because they were at the same positions.
        dict_address = {id_0:['old_id_20','old_id_1','old_id_200'], id_1:['old_id_3']}

        When the cave is processed created with the import function therion, then the original node name is stored in the 
        graph attributes G.nodes('fulladdress'), in the form of a full path from the main folder. This is a therion standard:
        dict_address = {id_0:['full_address.0','full_address.1','full_address.4'], id_1:['full_address.0']}

    """
    
    #create dictionnary to find current id based on the fulladdress
    if dict_address is not None:
        inverse_dict_address = { v: k for k, l in dict_address.items() for v in l }

    for edge in additional_edges:
        #check if there is flags already attached to the edges
        if dict_address is not None:
            #find node id based on the full address and attach the edge
            edge_from = inverse_dict_address[edge[0]]
            edge_to = inverse_dict_address[edge[1]]
            # edges[i][0] = [key for key, value in dict_address.items() if edge[0] in value ][0]
            # edges[i][1] = [key for key, value in dict_address.items() if edge[1] in value ][0]  
            # create a new edge with the flag value
            G.add_edge(edge_from,edge_to,flags=[flag])
        else: 
            # create a new edge with the flag value
            G.add_edge(edge[0],edge[1],flags=[flag])   


                
            


def flag_nodes(G,flagged_nodes, dict_address=None):
    
    """Add a string in the node attribute 'flag' of the networkx cave graph.

    Parameters
    ----------
    G : networkx graph 
        Graph produced with the function kn.from_therion_sql_enhanced
    
    flagged_nodes : dictionnary of list, optional
        list of nodes to be flagged, with associated flag.
        The dictionnary key is the flag, and the values associated with the key is the list of node ids to flag.

        Example of dictionnary: 
        -----------------------
        flagged_nodes = {'ent':['full_address.0','full_address.1','full_address.4']}
        flagged_nodes = {'ent':[old_id_1,old_id_4,old_id_400]}
        or 
        flagged_nodes = {'ent':[8,45,201]}

    dict_address : dict, optional
        by default this function takes the current networkx keys of the graph G. 
        When dict_address is not None, then it uses other node identifiers (for example, it can be the original node name)
        The dictionnary 
        stored in the graph attributes G.nodes('fulladdress').
        This attribute is created with the therion import function.
        
        example:
        --------
        Each current node id can be associated to a series of older ids, in the case that stations where regrouped because they were at the same positions.
        dict_address = {id_0:['old_id_20','old_id_1','old_id_200'], id_1:['old_id_3']}

        When the cave is processed created with the import function therion, then the original node name is stored in the 
        graph attributes G.nodes('fulladdress'), in the form of a full path from the main folder. This is a therion standard:
        dict_address = {id_0:['full_address.0','full_address.1','full_address.4'], id_1:['full_address.0']}


    """

    print(f'Therion Import - adding manual node flags: {flagged_nodes.keys()}')

    #create dictionnary to find current id based on the fulladdress
    if dict_address is not None:
        inverse_dict_address = { v: k for k, l in dict_address.items() for v in l }

        
    for flag in flagged_nodes.keys():
        #loop throught the flags
        for node in flagged_nodes[flag]:
            if dict_address is not None:
                id_node = inverse_dict_address[node]   
            else:
                id_node = node                   
            #check if node already has a flag
            #if not, create a new list of flag(s) attached to the node
            if G.nodes('flags')[id_node] is None:
                # pass
                #create flag on node
                nx.set_node_attributes(G, {id_node:[flag]}, name='flags')
            #if yes, append the new flag to the list
            elif G.nodes('flags')[id_node] is not None:
                #print(flag,id_node, fulladdress)
                G.nodes[id_node]['flags'].append(flag)



def flag_edges(G, flagged_edges, dict_address = None):
    """Add a string in the edge attribute 'flag' of the networkx cave graph.

    Parameters
    ----------
    G : networkx graph 
        Graph produced with the function kn.from_therion_sql_enhanced

    flagged_edges : dictionnary of list of tuple or list of lists, optional
        lists of edges to be flagged with corresponding flag to add. Any flag can be added. by default None
        However, for the duplicate edges and surface edges to be removed, it is necessary to use the correct flags.
        It is also possible to use the add edges with this dictionnary instead of using the 'add_edges' option.
        List of flagged edge that will be removed by default:  'dpl', 'srf', 'art', 'rmv', 'spl'

    use_fulladdress : bolean, default False
        by default this function takes the current networkx keys of the graph G. 
        When True, then it uses the "fulladdress" string stored in the graph attributes G.nodes('fulladdress').
        This attribute is created with the therion import function.

    Example of dictionnary: 
    ----------------------
    if use_fulladdress == True:
    flagged_edges = {'dpl':[['full_address.0','full_address.1],['full_address.3','full_address.10]], 'srf':[[full_address.3,full_address.2]]}   

    if we use the networkx key:
    flagged_edges = {'dpl':[[1,3],[11,5]], 'srf':[[5,11]]}   
    """
    print(f'Therion Import - adding manual edges flags: {flagged_edges.keys()}')

    #create dictionnary to find current id based on the fulladdress
    if dict_address is not None:
        inverse_dict_address = { v: k for k, l in dict_address.items() for v in l }

    
    #loop through all the flags
    for flag in flagged_edges.keys():
        print(flag)
        #loop through all the edges for each flag
        for edge in flagged_edges[flag]:
            if dict_address is not None:
                edge_from = inverse_dict_address[edge[0]]
                edge_to = inverse_dict_address[edge[1]]
            else:
                edge_from = edge[0]
                edge_to = edge[1]
            #check if edge exists already (for example to add a duplicate flag on an exisiting edge)
            if G.has_edge(edge_from,edge_to):
            #check if there is flags already attached to the edges
            #if not, create a new edge with the dictionnary 'flags' and the flag value
                if 'flags' not in G[edge_from][edge_to]:
                    # print(f'adding {flag} to edge {edge_from}-{edge_to}')
                    nx.set_edge_attributes(G,{(edge_from,edge_to):{'flags':[flag]}})
                    
                #if yes, append the flag to the list
                elif 'flags' in G[edge_from][edge_to]:
                    # print(f'appending {flag} to edge {edge_from}-{edge_to}')
                    G[edge_from][edge_to]['flags'].append(flag)
            #if edge does not exist yet, then just create a new edge with the appropriate flag name            
            else:
                # add the flag add by default?? if yes, implement this feature (20 fev 2025)
                # print(f'creating edge and adding {flag} to edge {edge_from}-{edge_to}')
                G.add_edge(edge_from,edge_to,flags=[flag])
                # print(f'graph length: {len(G)}')


# def remove_edges()

def remove_flagged_edges(G, flags_to_remove=['srf','dpl','rmv','art','spl'], attribute_name = 'flags'):
    """Remove edges flagged with certain strings.

    Parameters
    ----------
    G : networkx graph 
        Graph produced with the function kn.from_therion_sql_enhanced

    flags_to_remove : list of strings, optional
        list of the flags for which edges should be removed, by default ['srf','dpl','rmv','art','spl']
        - 'dpl' : duplicate
        - 'srf' : surface
        - 'art' : artificial
        - 'rmv' : remove
        - 'spl' : splay (for example when a shot is made in a large room, star shots, ...)
    attribute_name : string
        name of the attribute attached to the graph 


    """
    #edges_to_remove = list(dict(nx.get_edge_attributes(G,'flags')).keys()) 
    #extract flag unique values into a list
    flags = {x for l in list(nx.get_edge_attributes(G,attribute_name).values()) for x in l}
    #loop through the unique flags and 


    for flag in flags:
        #only remove edges with flag surface, duplicate, or remove
        if flag in flags_to_remove:
            
            list_edges = [edge for edge, action in nx.get_edge_attributes(G,attribute_name).items() if flag in action]
            #print('remove ', flag, list_edges)
            #remove edges    
            G.remove_edges_from(list_edges)
            #remove nodes that were isolated when removing the edges
            G.remove_nodes_from(list(nx.isolates(G)))
        else:
            pass
            #print('not removed', flag)



    # print(f'Initial Graph size: {len(G)}, Graph size after removing flagged edges: {len(H)}')
    # return H




# ----------------------------------------------------------------------------
def get_potential_connection(
        G,
        dist_horiz_max,
        dist_vert_max,
        node_deg=1,
        exclude_neighbors_up_to_edge=3,
        pos_attr='pos',
        return_dist=False,
        return_angle=False):
    """
    Retrieves list of potential new edges for a graph.

    For every node `u` of given degree `node_deg`:

    1. the nodes within a cylindrical box of horizontal radius `dist_horiz_max`
    and height `dist_vert_max` centered at `u` are retrieved in a list

    2. The nodes of this list at a distance in number of edges less than or
    equal to `exclude_neighbors_up_to_edge` are excluded.

    3. Then, the nearst node `v` to `u` (checking horizontal Euclidean distance)
    in this list is identified, and the tuple `(u, v)` is considered as a potential
    edge to be added to the graph (new connection)

    Parameters
    ----------
    G : networkx.Graph
        graph

    dist_horiz_max : float (positive)
        maximal horizontal distance (radius of the cylinder around checked nodes)

    dist_vert_max : float (positive)
        maximal vertical distance (height of the cylinder around checked nodes)

    exclude_neighbors_up_to_edge : int, default: 3
        distance in number of edges, nodes to a distance from a checked node at
        distance smaller than or equal to `exclude_neighbors_up_to_edge` are excluded
        from potential edge with the checked node

    node_deg : int, default: 1
        degree of the nodes to be checked as an extremity for
        potential new edge

    return_dist : bool, default: False
        if `True`, the length of the potential new edges (distance between the
        two extremities) are returned

    return_angle : bool, default: False
        if `True`, xxxxthe length of the potential new edges (distance between the
        two extremities) are returned

    Returns
    -------
    edges_list : list of 2-tuples
        list of potential new edges, each element is a 2-tuple (u, v), where
        u and v are the node ids of the two extremities of a potential new edge

    dist_list : list of floats, optional
        returned if `return_dist=True`, list of same length as `edges_list`, of the
        lengths of the potential new edges (distance between the two extremities)

    angle_list : list of lists of float(s), optional
        returned if `return_angle=True`, list of same length as `edges_list`, where
        `angle_list[i]` is the list of angles between the potential new edge `edge_list[i]`
        and the existing edge(s) whose one extremity is the node ``edge_list[i][0]`;
        each angle is in degree in the interval [0, 180]
    """
    # Set dictionary to convert node label (id) to node index, and vice versa
    node_label2index = {u:i for i, u in enumerate(G.nodes())}
    node_index2label = {i:u for i, u in enumerate(G.nodes())}

    pos = nx.get_node_attributes(G, pos_attr)
    pos = {k:np.asarray(v) for k, v in pos.items()} # convert tuple to array

    # Matrix of all positions
    pos_arr = np.asarray(list(pos.values()))

    rh2 = dist_horiz_max**2
    rv = dist_vert_max

    edges_list = []
    for u in G.nodes():
        if G.degree(u) != node_deg:
            continue

        # Get array (sel_ind_arr) of index of nodes within the cylindrical box centered at u:
        ind = node_label2index[u]
        lag = pos_arr - pos_arr[ind]
        disth2 = np.sum(lag[:,:2]**2, axis=1)
        distv = np.abs(lag[:,2])
        sel = np.all((disth2 <= rh2, distv <= rv), axis=0) # True at least for node u (at index ind)
        sel_ind_arr = np.where(sel)[0]
        if sel_ind_arr.size <= 1:
            continue

        # Get array (neigh_to_exclude_ind_arr) of neighbors index to exclude
        neigh_to_exclude_ind_arr = np.asarray([node_label2index[v] for v in list(nx.single_source_shortest_path_length(G, u, cutoff=exclude_neighbors_up_to_edge).keys())])

        # Update sel_ind_array
        sel_ind_arr = np.setdiff1d(sel_ind_arr, neigh_to_exclude_ind_arr)

        if sel_ind_arr.size == 0:
            continue

        # Get v the nearest node to u : potential edge (u, v)
        min_ind = sel_ind_arr[np.argmin(disth2[sel_ind_arr])]
        v = node_index2label[min_ind]
        edges_list.append((u, v))

    out = [edges_list]

    if return_dist:
        if len(edges_list):
            dist_list = [pos_arr[node_label2index[u]] - pos_arr[node_label2index[v]] for u, v in edges_list]
            dist_list = list(np.sqrt(np.sum(np.asarray(dist_list)**2, axis=1)))
        else:
            dist_list = []
        out.append(dist_list)

    if return_angle:
        angle_list = []
        for u, v in edges_list:
            pos_u = pos_arr[node_label2index[u]]
            pos_v = pos_arr[node_label2index[v]]
            uv = pos_v - pos_u
            uv_norm = np.sqrt(np.sum(uv**2))
            a = []
            for _, vi in G.edges(u):
                pos_vi = pos_arr[node_label2index[vi]]
                uvi = pos_vi - pos_u
                uvi_norm = np.sqrt(np.sum(uvi**2))
                a.append(np.rad2deg(np.arccos(np.sum(uv*uvi)/(uv_norm*uvi_norm))))
            angle_list.append(a)
        out.append(angle_list)

    if len(out) == 1:
        out = out[0]
    else:
        out = tuple(out)

    return out
# ----------------------------------------------------------------------------

def find_disconnected_node(G, H):
    """Identify node of degree one that were initially of degree 2 or more at an earlier stage of the cleaning process

    Parameters
    ----------
    G : networkx graph
        Graph exported from therion, containing all the data
    H : networkx graph
        Graph without the surface and duplicate shots

    Returns
    -------
    list
        list of disconnected node ids
    """    
    # G_raw = load_raw_therion_data(basename)    
    # G = load_therion_without_flagged_edges(basename)
    print( 'There is ', nx.number_connected_components(G), 'connected components in the original graph')
    print( 'There is ', nx.number_connected_components(H), 'connected components in the graph without flagged edges')
    
    closeby_all = []
    keys_disconnected_all =[]
    
    #cc_number = 0
    if nx.is_connected(H) == False:
        #iterate through the connectec components to find nodes where disconnection occured
        #search for the nodes that used to be degree >1 and are now degree 1.
        for i, subgraph_index in enumerate(nx.connected_components(H)):
            #print(i,subgraph_index )
            subgraph = nx.subgraph(H, subgraph_index)

            keys_disconnected_subgraph=[]   
            #find all the nodes where disconnection happened
            #look for all the nodes degree smaller in the cleaned file than in the original file 
            #keys_disconnected_subgraph = [k for k, v in dict(subgraph.degree()).items() if v == 1 and G_raw.degree()[k] >1]   
            for k in subgraph.nodes(): #dict(subgraph.degree()).items():
                #print(k)
                if subgraph.degree()[k]==1 and G.degree()[k] >1:
                    keys_disconnected_subgraph.append(k)

                
            keys_disconnected_all = keys_disconnected_all + keys_disconnected_subgraph
        return keys_disconnected_all
    else:
        print('There is no disconnected components, no need to merge')