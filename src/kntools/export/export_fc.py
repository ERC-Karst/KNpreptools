# import os
# import networkx as nx
# import numpy as np
# import pandas as pd
# from shapely.geometry import Point, LineString
# import kntools as kt



# def to_shp(positions,
#            links,
#            crs,
#            type,
#            outputdir='',
#            name=''):
#     """_Export nodes and edges to two separate shapefiles for Gis visualization. 
#     Requires the field 'pos' as an attribute of the graph. pos must be a list of three values x,y,z, or at least x,y

#     Parameters
#     ----------
#     positions : _type_
#         _description_
#     links : _type_
#         _description_
#     crs : _type_
#         _description_
#     type : str
#         'nodes' or 'edges'
#     outputdir : str, optional
#         _description_, by default ''
#     name : str, optional
#         _description_, by default ''

#     """
#     '''
#     Transform graph data into an esri shapefile. Function written by Ana Tanaka
#     crs OxBelHa: 'EPSG:32616'

#     positions: dict (id:[x,y,z])

#     links: list of list of links id
#     '''
#     import geopandas as gpd
    
#     if type == 'nodes':
#         node_data = {'id': list(positions.keys()), 'geometry': [Point(pos) for pos in positions.values()]}
#         node_gdf = gpd.GeoDataFrame(node_data, crs=crs)
#         node_gdf.to_file(os.path.join(outputdir,f'{name}nodes.shp'))

#     if type == 'edges':
#         edge_data = []
#         for u, v in links:
#             edge_data.append({'geometry': LineString([positions[u], positions[v]]), 'source': u, 'target': v})

#         edge_gdf = gpd.GeoDataFrame(edge_data, crs=crs)   
#         edge_gdf.to_file(os.path.join(outputdir,f'{name}edges.shp'))


# def graph_to_branches(G):
#     """Breaks down networkx graph into individual branches, by creating new points with unique value index at interesections.
#     This was conceived by Nina. for the purpose of the gocad export, which requires to loop through each branch.
#     This creates as many connected components as there is branches.
#     What it does is that it looks at each intersection (node degree >2) and disconnect (randomly) at the intersection.
#     To disconnect, it take randomly a segment, remove it and recreate a segment at the same spot but with a different name
#     For example, at an intersection of degree 3, it will only keep 2 segments attached and detach one segement. 

#     Args:
#         G (networkx Graph): 
#             a graph containing values of position, connected_component_number, and intersection

#     Returns:
#         networkx Graph: separated in branches. 
#     """    
#     def add_cc_attribute(G):
#         """_summary_

#         Parameters
#         ----------
#         G : networkx graph
#             adds a number as an attribute for all the connected components, from 0 to i (i is the number of connected components)
#             This is useful for gocad plotting for example
#         """
#         id_cc = []
#         value_cc = []
        
#         for i,cc in enumerate(nx.connected_components(G)):
#             id_cc += list(cc)
#             value_cc += [i] * len(cc)
        
#         cc_number = dict(zip(id_cc, value_cc))
#         nx.set_node_attributes(G, cc_number, 'connected_component_number') 

#     #!!!here we should find a way to add any attrtibutes to the new create node number!!!
#     #and create atoms to link points at branches intersection
#     #BREAK THE GRAPH IN SINGLE BRANCHES
#     max_value = max(G.nodes) 
#     H = G.copy()

#     # add connected component number to the graph
#     add_cc_attribute(H)

#     #loop through all nodes with degree larger than 2
#     for intersection in [node for node,degree in dict(H.degree()).items() if degree >2]:
#         #loop through all the neighbours minus the first two
#         for node in [n for n in H.neighbors(intersection)][2:]:
#             #set the new id for the new node
#             max_value += 1  
#             #create a new node at the intersection
#             H.add_node(max_value,   pos=H.nodes('pos')[intersection], 
#                                     connected_component_number=H.nodes('connected_component_number')[intersection],
#                                     intersection=intersection)  
#             #create an edge that connects the new node
#             H.add_edge(max_value,node) 
#             #remove the old ege
#             H.remove_edge(intersection,node)      
#     return H



# def export_to_gocad(G, 
#                     data_type = 'lines', #or 'points'
#                     properties = [], #['cs_height', 'cs_width']
#                     nodata_value = '-999999999',
#                     name = 'graph_gocad_export',
#                     node_id = [], #list of nodes id to export
#                     pos_attr = 'pos'
#                     ):
#     """Export networkx graph data into a format readable by Gocad (.pl).
#     This export requires x,y,z coordinate information attached as an attribute on each node on graph as a list of [x,y,z]
#     It is possible to only give a few points or the entire dataset. It is also possible to add several properties.

#     idea for improvement: 
#     1. instead of having to attached x,y,z to the graph, give a dictionnary into the function??
#     2. 


#     Parameters
#     ----------
#     G : networkx graph
#         Graph with coordinates position
#     data_type : str, optional
#         Choose data type between 'lines' and 'points', by default 'lines'
#     properties : list of string(s)
#         List containing the name of all the graph attributes to add to the Gocad output, by default []
#         For now, the properties have to be a single value per node. 
#     nodata_value : string
#         by default '-999999999'
#     name : str, optional
#         path and name of the file to save. The extension is .pl , by default 'graph_gocad_export'
#     node_id : list of node id, optional
#         List of node id to use for the export, by default []
#         If [] then the entire graph is selected
#     pos_attr : str, optional
#         name of the attribute containing the list of coordinates, by default 'pos'

#     returns:
#     --------
#     saves a .pl file readable in Gocad
#     """
    



#     #the properties have to be a single value per node
#     nodata_string = 'NO_DATA_VALUES ' + " ".join(str(item) for item in [nodata_value] * (len(properties)+3))
    
#     if data_type=='points':
#         header = 'GOCAD VSet 1.0'
#         header_dataset = 'SUBVSET'
        
#         #nodes
#         if node_id == []:
#             nodes = G.nodes
#         else:
#             nodes = node_id

#         dataset = []

#         for node in nodes:               
#             #write coordinate string ex: '-6.53 -10.24 -28.11'
#             # print(G.nodes('pos')[node])
#             string_coordinates = " ".join(str(item) for item in G.nodes('pos_attr')[node])
#             #write attribute string ex: 'att1 att2 atti'
#             string_attribute = ''

#             # string_id = " ".join(str(item) for item in nodes)
            
#             for attribute in properties:
#                 if G.nodes(attribute)[node] is not None:
#                     string_attribute += str(G.nodes(attribute)[node]) + ' '
#                 else:
#                     # in the case there is no data
#                     string_attribute += nodata_value
            
#             #create a list of lines containing the notes attributes  
#             dataset.append('PVRTX '+ str(node) +  ' ' + string_coordinates + ' ' + str(node) + ' ' + string_attribute)

#         #write the lines
#         lines = [   header, 
#                 'HEADER{',
#                 'name:' + name ,
#                 '}',
#                 'GOCAD_ORIGINAL_COORDINATE_SYSTEM',
#                 'ZPOSITIVE Elevation',
#                 'END_ORIGINAL_COORDINATE_SYSTEM',
#                 'PROPERTIES ID ' + " ".join(str(item) for item in properties),  
#                 nodata_string,
#                 header_dataset] + dataset + ['END']
    
#     if data_type=='lines':
#         header = 'GOCAD PLine 1'
#         header_dataset = ''
        
#         H = graph_to_branches(G)
        
#         #write lines containing pline information
#         #Gocad only read the pline right by single branch, with points in the right order
#         dataset = []
#         if nx.is_connected(H) == False:
#             #iterate through the connectec components to find nodes where disconnection occured
#             #search for the nodes that used to be degree >1 and are now degree 1.
#             for i, subgraph_index in enumerate(nx.connected_components(H)):
#                 subgraph = nx.subgraph(H, subgraph_index)
#                 # print(subgraph)
#                 #segments
#                 seg = []
#                 nodes_start_end = [node for node,degree in dict(subgraph.degree()).items() if degree ==1]
#                 # print(nodes_start_end)

#                 #make sure its not a loop
#                 #in the case of a segment in the form of a loop, 
#                 # here will be no node of degree 1, so we replace by the first node in the list
#                 if nodes_start_end:
#                     for path in nx.all_simple_edge_paths(subgraph, nodes_start_end[0],nodes_start_end[1]):
#                         for edge in path:   
#                             # print(edge) 
#                             seg.append(" ".join(str(item) for item in edge))              
#                             #nodes
#                 else:
#                     #create a new node at the intersection
#                     #take a random node in the loop:
#                     intersection = list(subgraph.nodes())[0]
#                     max_value = np.array(G.nodes()).max()
#                     subgraph = subgraph.copy()
#                     subgraph.add_node(max_value,   pos=subgraph.nodes(pos_attr)[intersection], 
#                                             connected_component_number=subgraph.nodes('connected_component_number')[intersection],
#                                             intersection=intersection)  
#                     #create an edge that connects the new node
#                     node = list(subgraph.neighbors(intersection))[0]
#                     subgraph.add_edge(max_value,node) 
#                     #remove the old ege
#                     subgraph.remove_edge(intersection,node)  

#                     seg = []
#                     nodes_start_end = [node for node,degree in dict(subgraph.degree()).items() if degree ==1]

#                     for path in nx.all_simple_edge_paths(subgraph, nodes_start_end[0],nodes_start_end[1]):
#                         for edge in path:   
#                             # print(edge) 
#                             seg.append(" ".join(str(item) for item in edge))              
#                             #nodes

                
#                 pvrtx = []
#                 for node in nx.shortest_path(subgraph, source=nodes_start_end[0], target=nodes_start_end[1]):               
#                     #write coordinate string ex: '-6.53 -10.24 -28.11'
#                     string_coordinates = " ".join(str(item) for item in subgraph.nodes(pos_attr)[node])
#                     #write attribute string ex: 'att1 att2 atti'
#                     string_attribute = ''
                    
#                     for attribute in properties:
#                         if subgraph.nodes(attribute)[node] is not None:
#                             string_attribute += str(subgraph.nodes(attribute)[node]) + ' '
#                         else:
#                             # in the case there is no data
#                             print('no properties for node: ', node )
#                             string_attribute += nodata_value
                    
#                     #create a list of lines  
#                     pvrtx.append('PVRTX '+ str(node) +  ' ' + string_coordinates + ' ' + string_attribute)
#                 # create each branch text    
#                 dataset += ['ILINE'] + pvrtx + seg
           
     
#         lines = [   header, 
#                     'HEADER{',
#                     'name:' + name ,
#                     '}',
#                     'GOCAD_ORIGINAL_COORDINATE_SYSTEM',
#                     'ZPOSITIVE Elevation',
#                     'END_ORIGINAL_COORDINATE_SYSTEM',
#                     'PROPERTIES ' + " ".join(str(item) for item in properties),  
#                     nodata_string,
#                     header_dataset] + dataset + ['END']
               
#     with open(name + '.pl', 'w') as f:
#         f.write('\n'.join(lines))






# #EXPORT TO JSON
# def nx2json(G,outputpath):
#     """Export edges to a json file to Gis visualization. Requires the field 'pos' as an attribute of the graph. pos must be a list of three values x,y,z. 

#     Parameters
#     ----------
#     G : netowrkx graph created with therion import
#         _description_
#     outputpath : string
#         full path to folder where the files should be saved. the name of file will be the name of the cave stored in the graph
#     """
    
#     json_text = []
#     #EXPORT TO JSON
#     #create lines of text
#     for i,edge in enumerate(G.edges()):
#         json_text.append('{ "type": "Feature", "properties": { "name": "%s" }, "geometry": { "type": "MultiLineString", "coordinates": [ [ %s, %s ] ] } }'
#                         %(i, G.nodes('pos')[edge[0]], G.nodes('pos')[edge[1]]))

    
#     #write file
#     filepath = (outputpath,'json')
#     with open(filepath + G.graph['cavename'] + '.json', 'w') as f:
#         f.write('\n'.join(json_text))

# #------------------------------------------------------------------
# #function specific to sql import

# def save_attribrutes_df_to_csv(G, outputpath, cavename='cavename'):
#     #check and create new directory if necessary
#     filepath = kt.make_filepath(outputpath,'clean_graph_csv')
#     # cavename = G.graph['cavename']
       
#     #save edges and flags
#     # nx.write_edgelist(G, filepath + cavename + '_edges.csv', data=False)
#     pd.DataFrame(G.edges()).to_csv(filepath + cavename + '_edges.csv', index=False, header = ['from_id','to_id'], sep=';')    
#     print('saved edge list to ', filepath , cavename , '_edges.csv')
    
#     #load and save all the existing NODE attribute names for this graph
#     attribute_names = kt.get_nodes_attributes(G)
#     if len(attribute_names)==1:
#         attribute_names = [attribute_names]
#     for attribute_name in attribute_names:        
#         df = kt.attribute_dict_to_df(G,attribute_name, 'node')
#         if attribute_name=='pos' or attribute_name=='splays' or attribute_name=='splaylegs' or attribute_name=='splaylrud' :
#             df.to_csv(filepath + cavename + '_node_' + attribute_name + '.csv', index=False, header=['id','x','y','z'], sep=';')   
#         elif attribute_name=='csdim':
#             df.to_csv(filepath + cavename + '_node_' + attribute_name + '.csv', index=False, header=['id','cswidth','csheight'], sep=';')   
#         elif attribute_name=='flags':
#             df.to_csv(filepath + cavename + '_node_' + attribute_name + '.csv', index=False, header=['id','flag'], sep=';')   
#         elif attribute_name=='comments':
#             df.to_csv(filepath + cavename + '_node_' + attribute_name + '.csv', index=False, header=['id','comment'], sep=';')   
#         elif attribute_name=='idsql':
#             df.to_csv(filepath + cavename + '_node_' + attribute_name + '.csv', index=False, header=['id','idsql'], sep=';')    
#         elif attribute_name=='fulladdress':
#             df.to_csv(filepath + cavename + '_node_' + attribute_name + '.csv', index=False, header=['id','fulladdress'], sep=';')    
#         # print('saved node attribute', attribute_name, ' to ', filepath, cavename, '_node_' , attribute_name , '.csv')
    
#     #load and save all the existing EDGE attribute names for this graph
#     attribute_names = kt.get_edges_attributes(G)
#     for attribute_name in attribute_names:
#         df = kt.attribute_dict_to_df(G,attribute_name, 'edge')
#         if attribute_name=='flags':
#             df.to_csv(filepath + cavename + '_edge_' + attribute_name + '.csv', index=False, header=['from_id','to_id','flag'], sep=';')   
  
#         # print('saved edge attribute', attribute_name, ' to ', filepath, cavename, '_edge_', attribute_name, '.csv')



# #----------------------------
# #not sure this one works

# def write_graph_to_plt(graph: nx.Graph, basename: str, disco_keys=None):
#     """
#     Reads a networkx.Graph object and writes it to a plt file.
#     developped by Tanguy Racine, UNINE
#     """
#     coords = nx.get_node_attributes(graph, "coord")
#     plt_command = """{type} {y} {x} {z} S{station} P -9 -9 -9 -9"""
#     plt_file = """G18S\nNX D 1 1 1 C{name}.plt\n{points}"""
#     plt_lines = []

#     for line in graph.edges:
#         x1, y1, z1 = coords[line[0]]
#         x2, y2, z2 = coords[line[1]]

#         plt_lines.append(plt_command.format(
#             type="M", x=x1, y=y1, z = z1, station=line[0]))

#         plt_lines.append(plt_command.format(
#             type="D", x=x2, y=y2, z = z2, station=line[1]))
        
#     if disco_keys != None:
#         for key in disco_keys:
#             x, y, z = coords[key]

#         plt_lines.append(plt_command.format(
#             type="M", x=x, y=y, z=z, station=key))            

#     with open(f"{basename}.plt", "w+") as f:
#         f.write(
#             plt_file.format(
#                 name=basename,
#                 points="\n".join(plt_lines),
#             )
#         # )