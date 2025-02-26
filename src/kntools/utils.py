# import numpy as np
import networkx as nx
import pandas as pd
import os


def get_pos2d(G):
    return {key: value[0:2] for key, value in nx.get_node_attributes(G,'pos').items()}


def get_posz(G):
    return {key: value[2] for key, value in nx.get_node_attributes(G,'pos').items()}

def get_pos3d(G):
    return nx.get_node_attributes(G,'pos')

def get_nodes_attributes(G):
    # get list of node keys
    return set([k for n in G.nodes for k in G.nodes[n].keys()])

def get_edges_attributes(G):
    # get list of node keys
    return set([k for n in G.edges for k in G.edges[n].keys()])

def find_neighbors(G,key):   
    return [n for n in G.neighbors(key)]

def find_value_in_node_attribute(G,attribute, value):
    return [i for i in dict(G.nodes(attribute)) if dict(G.nodes(attribute))[i]==value]   

def find_elements(lst1, lst2):
    return list(map(lst1.__getitem__, lst2))

def list2dict(key_list, value_list):
    """Transform list to dictionnary by regouping values in list for identical keys. 
    Using dictionnary comprehension.

    Parameters
    ----------
    key_list : list
        Dictionnary keys. Usually a list of int
    value_list : list
        Dictionnary values. Can be a list of int, flot, array, or list.

    Returns
    -------
    dictionnary

    """
    
    return {key : [value_list[idx] 
            for idx in range(len(value_list)) if key_list[idx]== key]
            for key in set(key_list)}



def make_filepath(outputpath,foldername):
    sep = '' if outputpath.endswith('/') else '/'
    filepath = f'{outputpath}{sep}{foldername}' if foldername.endswith('/') else f'{outputpath}{sep}{foldername}/'
    isExist = os.path.exists(filepath)
    if not isExist:
       os.makedirs(filepath)
    return filepath



def find_key_from_dict(dictionnary, value):
    #issue when the list is returned empty
    inverse = { v: k for k, l in dictionnary.items() for v in l } 
    return inverse[value]
    # [key for key,values in dictionnary.items() if value in values][0]


def find_key_from_fulladdress(G, value):
    fulladdress_dict = nx.get_node_attributes(G,'fulladdress')
    # node_id = [key for key,values in fulladdress_dict.items() if value in values]
    log_key = None
    for key,values in fulladdress_dict.items():

        if value in values:
            #print(value)
            log_key = key
            if log_key is None:
                print(f'{value} is missing in G - fulladdress')
            else:
                return(log_key)
            

#%% ATTRIBUTE TO DICTIONNARY
def attribute_dict_to_df(G, attribute_name, attribute_type):
    list_data = []
    
    if attribute_type == 'node':
        # attribute_name = str(attribute_name) #this prevent issues with idealized networks, where this value is a set
        attribute_dict = G.nodes(str(attribute_name))
        for key, values in attribute_dict:
            # print(key,values)
            if values is not None:
                #print(key)
                #for pos and width_thickness (list of 2 or 3 floats)
                #########################################################
                if attribute_name=='pos' or attribute_name=='csdim':
                    if type(values)==tuple:
                        list_data.append([key]+list(values))
                    else:
                        list_data.append([key]+values)
                #for splays (list of lists of arrays)
                ###########################################################                
                elif attribute_name=='splays':

                    for array in values: #!!! the toporobot export makes a list of list. simplify this in the toporobot to uniformise
                        list_data.append([key] + array)   
                                    
                    # for list_of_arrays in values:
                    #     print(list_of_arrays)
                    #     for array in list_of_arrays:
                    #         list_data.append([key] + array.tolist())
                        
                #for full_address_id, therion_sql_id, flags, ... (list of n strings or int)
                #########################################################  
                else:
                    #if attribute_name=='flags': print(key, values)
                    if type(values)==str or type(values)==int or type(values)==float: 
                        # print(key,'is string or int or float')
                        list_data.append([key,values])
                    elif type(values)==list:
                        for value in values:                           
                            list_data.append([key,value])
                    
    if attribute_type == 'edge':
        attribute_dict = dict(nx.get_edge_attributes(G,attribute_name))
        
        for key, values in attribute_dict.items():
            if values is not None:
                #if attribute_name=='flags': print(key, values)
                if type(values)==str or type(values)==int or type(values)==float: 
                    # print(key,'is string or int or float')
                    list_data.append(list(key) +[values])
                elif type(values)==list:
                    for value in values:                           
                        list_data.append([key[0],key[1],value])
                # if len(values.split(','))==1:
                #     list_data.append(list(key) +[values])
                # else:
                #     for value in values:
                #         list_data.append([key,value])

    return pd.DataFrame(list_data)