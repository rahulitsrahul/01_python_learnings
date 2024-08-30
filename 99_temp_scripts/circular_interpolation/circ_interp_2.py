import math
import matplotlib.pyplot as plt

def parse_gcode(gcode, prev_gcode_params={'cmd': None, 'x': None, 'y': None , 'i': None, 'j': None, 'r': None, 'f': None}):
    # Initialize the parameters
    command = None
    r = None
    x = prev_gcode_params['x']
    y = prev_gcode_params['y']
    i = prev_gcode_params['i']
    j = prev_gcode_params['j']
    # r = prev_gcode_params['r']
    f = prev_gcode_params['f']

    # Split the gcode string and iterate through the parts
    parts = gcode.split()
    for part in parts:
        if part.startswith('G'):
            command = part
        elif part.startswith('X'):
            x = float(part[1:])
        elif part.startswith('Y'):
            y = float(part[1:])
        elif part.startswith('I'):
            i = float(part[1:])
        elif part.startswith('J'):
            j = float(part[1:])
        elif part.startswith('R'):
            r = float(part[1:])

    return (command, x, y, i, j, r, f)

def cnc_circular_interpolation(command, x, y, i=None, j=None, r=None, resolution=0.1):
    # Start point is at (0, 0)
    start_x, start_y = 0, 0

    if r is not None:  # If radius is given, calculate center using the R parameter
        dx = x - start_x
        dy = y - start_y
        d = math.sqrt(dx**2 + dy**2)
        if d > 2 * abs(r):
            raise ValueError("Distance between start and end points is greater than the diameter of the circle")

        # Calculate midpoint
        mx, my = (start_x + x) / 2, (start_y + y) / 2

        # Calculate distance from midpoint to center
        h = math.sqrt(r**2 - (d/2)**2)

        # Calculate the offset for the center
        if command == 'G02':  # Clockwise
            xc = mx + h * dy / d
            yc = my - h * dx / d
        elif command == 'G03':  # Counterclockwise
            xc = mx - h * dy / d
            yc = my + h * dx / d
        radius = r
    elif i is not None and j is not None:  # Use I and J to determine the circle center
        xc = start_x + i  # X center of the circle
        yc = start_y + j  # Y center of the circle
        radius = math.sqrt(i**2 + j**2)
    else:
        raise ValueError("Invalid G-code: either I/J or R must be provided")

    if radius <= 0:
        raise ValueError("Radius must be positive and non-zero")

    # Calculate start and end angles
    start_angle = math.atan2(start_y - yc, start_x - xc)
    end_angle = math.atan2(y - yc, x - xc)

    # Adjust the end angle based on the direction
    if command == 'G02':  # Clockwise
        if end_angle > start_angle:
            end_angle -= 2 * math.pi
    elif command == 'G03':  # Counterclockwise
        if end_angle < start_angle:
            end_angle += 2 * math.pi

    # Calculate the angular difference
    angular_difference = end_angle - start_angle

    # Ensure the number of points is at least one
    if resolution <= 0:
        raise ValueError("Resolution must be positive and non-zero")
    num_points = max(int(abs(angular_difference) / (resolution / radius)), 1)

    # Generate the points along the arc
    points = []
    for i in range(num_points + 1):
        angle = start_angle + i * angular_difference / num_points
        px = xc + radius * math.cos(angle)
        py = yc + radius * math.sin(angle)
        points.append((px, py))

    # Ensure the last point is exactly the end point
    points[-1] = (x, y)
    
    return points

def plot_circle(points):
    # Separate the x and y coordinates
    x_coords, y_coords = zip(*points)
    
    # Plot the points
    plt.figure(figsize=(6, 6))
    plt.plot(x_coords, y_coords, 'b-')  # Blue line for the arc
    plt.scatter(x_coords, y_coords, color='red', s=10)  # Red dots for the points
    
    # Set equal scaling and labels
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('CNC Circular Interpolation Arc')
    plt.grid(True)
    plt.show()


# # Example G-code using R for radius
# gcode = "G02 X10 Y10 R10"
# gcode = "G03 X10 Y10 R10"
# gcode = "G03 X10 Y10 I0 J0"

# # Parse the G-code
# command, x, y, i, j, r = parse_gcode(gcode)

# # Generate the circular interpolation points
# points = cnc_circular_interpolation(command, x, y, i, j, r)

# # Plot the circle
# plot_circle(points)

if __name__ == "__main__":
    prev_gcode_params = {'cmd': None, 'x': None, 'y': None , 'i': None, 'j': None, 'r': None, 'f': None}
    
    gcode = "G01 X10 Y10"
    command, x, y, i, j, r, f = parse_gcode(gcode=gcode, prev_gcode_params=prev_gcode_params)
    prev_gcode_params = {'cmd': command, 'x': x, 'y': y , 'i': i, 'j': j, 'r': r, 'f': f}
    
    gcode = "G03 X15"
    command, x, y, i, j, r, f = parse_gcode(gcode=gcode, prev_gcode_params=prev_gcode_params)
    prev_gcode_params = {'cmd': command, 'x': x, 'y': y , 'i': i, 'j': j, 'r': r, 'f': f}
    
    gcode = "G03 X10 Y10 I0 J0"
    command, x, y, i, j, r, f = parse_gcode(gcode=gcode, prev_gcode_params=prev_gcode_params)
    prev_gcode_params = {'cmd': command, 'x': x, 'y': y , 'i': i, 'j': j, 'r': r, 'f': f}
    points = cnc_circular_interpolation(command, x, y, i, j, r)

