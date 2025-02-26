# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 11:27:05 2024

@author: celia
"""

#graph test


import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt



links = [(0,1),(1,2),(2,3),(3,4),(4,5),(3,6),(2,7),(7,8),(7,9),(9,10),(10,11),(11,7)]

pos = {0:[1.,2.,3.],
       1:[4.,5.,6.],
       2:[6.,10.,1.],
       3:[7.,8.,9.],
       4:[1.,2.,3.],
       5:[4.,5.,6.],
       6:[7.,8.,9.],
       7:[10.,11.,1.2],
       8:[13.,14.,15.],
       9:[16.,17,1.8],
       10:[19.,20,21.],
       11:[2.2,23.,24.]
       }

G = nx.Graph()
G.add_edges_from(links)
nx.set_node_attributes(G, pos, 'pos')   
plt.figure()
nx.draw(G)
#nx.set_node_attributes(G, coord, 'coord')

def nextstep(G, path):
     """
     from karstnet

     Work on self_graph
     Adds the next node to a path of self_graph along a branch.
     Stops when reaches a node of degree different from 2.

     Parameters
     ----------
         path : list
             A list of nodes to explain a path

     Returns:
     --------
     list
         path : A list of nodes to explain a path

     bool
         stopc
     """
     current = path[-1]
     # Checks first if the end of the path is already on an end
     if G.degree(current) != 2:
         stopc = False
         return path, stopc

     # This is a security / it may be removed
     if len(path) > 1:
         old = path[-2]
     else:
         old = current

     # Among the neighbors search for the next one
     for nextn in G.neighbors(current):
         if old != nextn:
             break

     # Add the next node to the path and check stopping criteria
     # noinspection PyUnboundLocalVariable
     path.append(nextn)

     # Test for a closed loop / even if start node has degree = 2
     test_loop = path[0] == path[-1]

     if (G.degree(nextn) != 2) or test_loop:
         stopc = False
     else:
         stopc = True

     return path, stopc



def getallbranches(G):
    """
    NOT PUBLIC
    
    Constructs the list of all branches of the karstic graph self_graph.
    Compute lengths and tortuosities
    """
    # Initialisations
    target = []
    degree_target = []
    
    # Create one subgraph per connected components
    # to get isolated loops as branches
    # Return a list of connected graphs
    list_sub_gr = [G.subgraph(c).copy()
                   for c in nx.connected_components(G)]
    
    for sub_gr in list_sub_gr:
        local_counter = 0
        last_node_index = 0
        # Identifies all the extremeties of the branches (nodes of degree
        # != 2)
        for i in sub_gr.nodes():
            if (sub_gr.degree(i) != 2):
                target.append(i)
                degree_target.append(nx.degree(sub_gr, i))
                local_counter += 1
            last_node_index = i
        # to manage cases where a subgraph is only composed of nodes of
        # degree 2
        if (local_counter == 0):
            target.append(last_node_index)
            degree_target.append(nx.degree(sub_gr, last_node_index))
    
    # Identifies all the neighbors of those nodes,
    # to create all the initial paths
    list_start_branches = []
    for i in target:
        for n in G.neighbors(i):
            list_start_branches.append([i, n])
    
    # Follow all these initial paths to get all the branches
    branches = []
    for path in list_start_branches:
        go = True
        # Check all existing branches to avoid adding a branch twice
        # if starting from other extremity
        for knownbranch in branches:
            if ((path[0] == knownbranch[-1]) &
                    (path[1] == knownbranch[-2])):
                go = False
                break
        if go:
            #get a list for a single branch
            path, stopc = nextstep(G,path)
            while stopc:
                path, stopc = nextstep(G,path)
        
            branches.append(path)
        
    return branches


branches = getallbranches(G)
vertices = list(dict(G.nodes('pos')).values())

import numpy as np
import pyvista as pv
pl = pv.Plotter()
#points = np.array([[0, 1, 0], [1, 0, 0], [1, 1, 0], [2, 0, 0]])
for branch in branches:
    points = np.array([vertices[i] for i in branch])
    pl.add_lines(points, color='purple', width=7, connected=True)
    pl.add_points(points, render_points_as_spheres=True, point_size=15, color='black')
    
    pl.add_point_labels(
        points,
        branch,
        always_visible=True,
        fill_shape=False,
        margin=100,
        shape_opacity=0.0,
        font_size=20)
    

pl.camera_position = 'xy'
pl.show()

#%%


# def PolyLine() -> UnstructuredGrid:
#     """Create a :class:`pyvista.UnstructuredGrid` containing a single poly line.

#     This represents a set of line segments as a single cell.

#     This cell corresponds to the :attr:`pyvista.CellType.POLY_LINE` cell type.

#     Returns
#     -------
#     pyvista.UnstructuredGrid
#         UnstructuredGrid containing a single polyline.

#     Examples
#     --------
#     Create and plot a single polyline.

#     >>> from pyvista import examples
#     >>> grid = examples.cells.PolyLine()
#     >>> examples.plot_cell(grid)

#     List the grid's cells. This could be any number of points.

#     >>> grid.cells
#     array([4, 0, 1, 2, 3])

#     List the grid's points.

#     >>> grid.points
#     pyvista_ndarray([[0. , 0. , 0. ],
#                      [0.5, 0. , 0. ],
#                      [0.5, 1. , 0. ],
#                      [0. , 1. , 0. ]])

#     >>> grid.celltypes  # same as pyvista.CellType.POLY_LINE
#     array([4], dtype=uint8)

#     """
#     points = [
#         [0.0, 0.0, 0.0],
#         [0.5, 0.0, 0.0],
#         [0.5, 1.0, 0.0],
#         [0.0, 1.0, 0.0],
#     ]

#     cells = [len(points)] + list(range(len(points)))
#     return UnstructuredGrid(cells, [CellType.POLY_LINE], points)

import numpy as np
import pyvista as pv

# points = [
#     [0.0, 0.0, 0.0],
#     [0.5, 0.0, 0.0],
#     [0.5, 1.0, 0.0],
#     [0.0, 1.0, 0.0],
# ]

# cells = [len(points)] + list(range(len(points)))
# grid = pv.UnstructuredGrid(cells, [pv.CellType.POLY_LINE], points)

#vertices = np.array([[0, 3,10], [1, 0, 5], [1, 0.5, 0], [4, 0.5, 0]])

vertices = list(dict(G.nodes('pos')).values())
lines=[]
for branch in branches:
    print(branch)
    
    lines = lines + [len(branch)] + branch
#lines = [[3, 0, 1,2],[3, 2, 1,3], [2,3, 2]]
grid = pv.PolyData(vertices, lines=lines)

cpos=None

#def plot_cell(grid, cpos=None, **kwargs):
"""Plot a :class:`pyvista.UnstructuredGrid` while displaying cell indices.

Parameters
----------
grid : pyvista.UnstructuredGrid
    Unstructured grid (ideally) containing a single cell.

cpos : str, optional
    Camera position.

**kwargs : dict, optional
    Additional keyword arguments when showing. See :func:`pyvista.Plotter.show`.

Examples
--------
Create and plot a single hexahedron.

>>> from pyvista import examples
>>> grid = examples.cells.Hexahedron()
>>> examples.plot_cell(grid)

"""


#%%


pl = pv.Plotter()
pl.add_mesh(grid, opacity=1, show_edges=True, edge_color='red')
# edges = grid.extract_all_edges()
# if edges.n_cells:
#     pl.add_mesh(grid.extract_all_edges(), line_width=20, color='r', render_lines_as_tubes=True)
pl.add_points(grid, render_points_as_spheres=True, point_size=30, color='b')

#pl.add_lines(lines, color='purple', width=7, connected=True)

pl.add_point_labels(
    grid.points,
    range(grid.n_points),
    always_visible=True,
    fill_shape=False,
    margin=0,
    shape_opacity=0.0,
    font_size=20)
# #choose initial camera angle
pl.enable_anti_aliasing()
# if cpos is None:
#     pl.camera.azimuth = 20
#     pl.camera.elevation = -20
# else:
#     pl.camera_position = cpos
pl.show()



#%%

import numpy as np
import pyvista as pv
pl = pv.Plotter()
#points = np.array([[0, 1, 0], [1, 0, 0], [1, 1, 0], [2, 0, 0]])
for branch in branches:
    points = np.array([vertices[i] for i in branch])
    pl.add_lines(points, color='purple', width=7, connected=True)
    pl.add_points(points, render_points_as_spheres=True, point_size=15, color='black')
    
    pl.add_point_labels(
        points,
        branch,
        always_visible=True,
        fill_shape=False,
        margin=100,
        shape_opacity=0.0,
        font_size=20)
    

pl.camera_position = 'xy'
pl.show()

# #Adding lines with ``connected=True`` will add a series of connected
# #line segments.

# pl = pv.Plotter()
# points = np.array([[0, 1, 0], [1, 0, 0], [1, 1, 0], [2, 0, 0]])
# actor = pl.add_lines(points, color='purple', width=3, connected=True)
# pl.camera_position = 'xy'
# pl.show()
        
        #    >>> points = np.random.random((10, 3))
        # >>> pl = pv.Plotter()
        # >>> actor = pl.add_points(
        # ...     points, render_points_as_spheres=True, point_size=100.0
        # ... )
        # >>> pl.show()     
        
#%%






    
#plot_cell(polyline)

# import numpy as np

# import pyvista
# vertices = np.array([[0, 0, 0], [1, 0, 0], [1, 0.5, 0], [0, 0.5, 0]])
# lines = np.hstack([[3, 0, 1,2],[3, 2, 1,3], [2,3, 2]])
# mesh = pyvista.PolyData(vertices, lines=lines)

# plotter = pyvista.Plotter()
# actor = plotter.add_mesh(mesh, color='k', line_width=10)
# plotter.camera.azimuth = 45
# plotter.camera.zoom(0.8)
# plotter.show()


# H = G.to_directed()
# plt.figure()
# nx.draw(G)

# #%%

# G = nx.complete_graph(4)

# for path in nx.all_simple_paths(G, source=0, target=3):

#     print(path)
    
    
# plt.figure()
# nx.draw(G)


# # [0, 1, 2, 3]
# # [0, 1, 3]
# # [0, 2, 1, 3]
# # [0, 2, 3]
# # [0, 3]


# #%%


