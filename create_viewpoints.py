import math

def get_stereoscopic_views(azimuth, elevation, distance, eye_distance):
    # Calculate the left and right viewpoints based on eye distance
    left_azimuth = azimuth - math.radians(eye_distance / 2)
    right_azimuth = azimuth + math.radians(eye_distance / 2)
    
    # Convert back to Cartesian coordinates
    # left_x = distance * math.cos(left_azimuth) * math.cos(elevation)
    # left_y = distance * math.sin(left_azimuth) * math.cos(elevation)
    # left_z = distance * math.sin(elevation)
    
    # right_x = distance * math.cos(right_azimuth) * math.cos(elevation)
    # right_y = distance * math.sin(right_azimuth) * math.cos(elevation)
    # right_z = distance * math.sin(elevation)
    
    # return [(left_x, left_y, left_z), (right_x, right_y, right_z)]
    return [left_azimuth, elevation, 0.0, distance], [right_azimuth, elevation, 0.0, distance]

if __name__ == '__main__':
    phi = (1 + math.sqrt(5)) / 2. # golden_ratio
    circumradius = math.sqrt(3)
    distance = circumradius * 1.2
    eye_distance = 1  # Adjust this value to control the eye separation
    
    dodecahedron = [[-1, -1, -1],
                    [ 1, -1, -1],
                    [ 1,  1, -1],
                    [-1,  1, -1],
                    [-1, -1,  1],
                    [ 1, -1,  1],
                    [ 1,  1,  1],
                    [-1,  1,  1],
                    [0, -phi, -1 / phi],
                    [0, -phi,  1 / phi],
                    [0,  phi, -1 / phi],
                    [0,  phi,  1 / phi],
                    [-1 / phi, 0, -phi],
                    [-1 / phi, 0,  phi],
                    [ 1 / phi, 0, -phi],
                    [ 1 / phi, 0,  phi],
                    [-phi, -1 / phi, 0],
                    [-phi,  1 / phi, 0],
                    [ phi, -1 / phi, 0],
                    [ phi, 1 / phi, 0]]

    # get Azimuth, Elevation angles
    # Azimuth varies from -pi to pi
    # Elevation from -pi/2 to pi/2
    view_points = open('./view_points.txt', 'w+')
    for vertice in dodecahedron:
        elevation = math.asin(vertice[2] / circumradius)
        azimuth = math.atan2(vertice[1], vertice[0])
        
        # Get the left and right stereoscopic views
        left_view, right_view = get_stereoscopic_views(azimuth, elevation, distance, eye_distance)
        
        # Write the left and right viewpoints to the file
        view_points.write('%f %f %f %f\n' % (left_view[0], left_view[1], left_view[2], left_view[3]))
        view_points.write('%f %f %f %f\n' % (right_view[0], right_view[1], right_view[2], right_view[3]))
    
    view_points.close()