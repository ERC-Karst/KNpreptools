#%% test lrud to splay

import numpy as np

pos = [np.array([3,0,0]),np.array([3,2,0]),np.array([3,2,1])]
dir = [pos[1]-pos[0], pos[2]-pos[0], pos[2]-pos[1]]
lrud = [[1,2,3,4],[1,2,3,4],[1,2,3,4]]

normal_vector_dir = dir[0]
station_coordinates = pos[0]

def calc_splay_from_lrud(station_coordinates, normal_vector_dir,lrud):
    """Transform left-right-up-down caving survey measurements to splays.
    Calculation made by Nina Egli

    This assumes that:
    1. the normal vector corresponds to the main direction of the conduit
    2. the normal vector is pointing in the direction of survey
    3. left and right measurements are always made in the horizontal plan
    4. up and down are made perpendicular to the direction of the conduit and not strait up or down

    Parameters
    ----------
    station_coordinates : array
        x,y,z coordinates of the station in meters or feet. example: np.array([x,y,z])
    normal_vector_dir : array
        direction of the conduit. x,y,z vector calculated with .... in the direction of the survey.
    lrud : list of floats or int
        left, right, up, down measurements in the same unit of measurements as the coordinates.

    Returns
    -------
    list of array
        left, right, up, down splays list of coordinates of the position measured on the wall

    """
    #unit vector pointing north
    unit_vector_z = np.array([0,0,1])
    #we normalize the normal vector by its norm    
    normal_vector_plan_normalized = normal_vector_dir/np.linalg.norm(normal_vector_dir)

    #extract the left right up down scalar values
    left_scalar = lrud[0]
    right_scalar = lrud[1]
    up_scalar = lrud[2]
    down_scalar = lrud[3]

    #calculate the unit vector to the right and down by taking the vectoriel product
    unit_vector_right = np.cross(normal_vector_plan_normalized,unit_vector_z)
    unit_vector_down = np.cross(normal_vector_plan_normalized,unit_vector_right)

    #calculate position
    left_vector = station_coordinates - unit_vector_right * left_scalar
    right_vector = station_coordinates + unit_vector_right * right_scalar
    up_vector = station_coordinates - unit_vector_down * up_scalar
    down_vector = station_coordinates + unit_vector_down * down_scalar

    return [left_vector, right_vector, up_vector, down_vector]

calc_splay_from_lrud(station_coordinates, normal_vector_dir,lrud[0])


# %%
