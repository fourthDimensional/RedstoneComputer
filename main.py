import mcschematic


def custom_range(n):
    if n >= 0:
        return range(n)
    else:
        return range(0, n, -1)


def parse_instructions(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    stripped_lines = [''.join(ch for ch in line if ch in '10\n') for line in lines]

    instructions = [line.strip() for line in stripped_lines]

    return instructions


def schematic_to_binary_string(schematic, corner):
    structure = schematic.getStructure()

    # Get the bounds of the structure
    bounds = structure.getBounds()

    # bounds is a tuple of two tuples, each representing the (x, y, z) coordinates
    # The first tuple is the minimum (x, y, z) and the second is the maximum (x, y, z)
    (x_min, y_min, z_min), (x_max, y_max, z_max) = bounds

    # Calculate the width, height, and length
    width = x_max - x_min + 1
    height = y_max - y_min + 1
    length = z_max - z_min + 1

    # Adjust the signs based on the corner
    if corner == 'NE':
        width, height, length = -width, -height, length
    elif corner == 'NW':
        width, height, length = width, -height, length
    elif corner == 'SE':
        width, height, length = -width, height, length
    elif corner == 'SW':
        width, height, length = width, height, length

    redstone_torches = []
    for x in custom_range(width):
        for y in custom_range(height):
            for z in custom_range(length):
                block_data = schematic.getBlockDataAt((x, y, z))
                if 'redstone_wall_torch' in block_data:
                    redstone_torches.append((x, y, z))

    # Initialize the counts for each dimension
    x_count = set()
    y_count = set()
    z_count = set()

    # Count the occurrences of each dimension
    for x, y, z in redstone_torches:
        x_count.add(x)
        y_count.add(y)
        z_count.add(z)

    x_count = sorted(x_count)
    y_count = sorted(y_count)
    z_count = sorted(z_count)

    bit_points = []
    # The dimension that isn't shared is the one with the most unique values
    if len(x_count) > len(y_count) and len(x_count) > len(z_count):
        unique_dim = 'x'
        for x in range(0, length + 1, 2):
            bit_points.append(x)
        actual_points = x_count
    elif len(y_count) > len(x_count) and len(y_count) > len(z_count):
        unique_dim = 'y'
        for y in range(0, length + 1, 2):
            bit_points.append(y)
        actual_points = y_count
    else:
        unique_dim = 'z'
        for z in range(0, length + 1, 2):
            bit_points.append(z)
        actual_points = z_count

    bit_points = [int(point/2) for point in bit_points]
    actual_points = [int(point/2) for point in actual_points]

    # Initialize the binary string
    binary_string = ''

    # Generate the binary string
    for point in bit_points:
        if point in actual_points:
            binary_string += '1'
        else:
            binary_string += '0'

    return binary_string


def binary_string_to_schematic(binary_string, corner, direction, mcb=True):
    # Initialize an empty schematic
    schematic = mcschematic.MCSchematic()

    if corner == 'NE':
        x, y, z = -1, -1, 1
        torch_face = 'WEST'
    elif corner == 'NW':
        x, y, z = -1, -1, 1
        torch_face = 'EAST'
    elif corner == 'SE':
        x, y, z = -1, -1, -1
        torch_face = 'NORTH'
    else:
        x, y, z = -1, -1, 1
        torch_face = 'SOUTH'

    # Iterate over the binary string
    for i, bit in enumerate(binary_string):
        if bit == '1':
            # Calculate the corresponding coordinates

            if direction == 'x':
                x = i*2
            elif direction == 'y':
                y = i*2
            else:
                z = i*2

            print(x, y, z)
            # Add a redstone torch at the calculated location
            schematic.setBlock((x, y, z), 'minecraft:redstone_wall_torch[facing=' + torch_face + ']')
            print('1')
        else:
            print('0')

    return schematic


schematic = mcschematic.MCSchematic(
    "schematics/calibration.schem")  # Loads a programmable ROM segment with 6 bits and is torch based.

print(schematic_to_binary_string(schematic, 'NE'))

binary_string = '010111111111111100'
schematic = binary_string_to_schematic(binary_string, 'SE', 'x', True)
schematic.save("schematics", "test", mcschematic.Version.JE_1_18_2)


# instructions = parse_instructions('instructions.txt')
#
# print(instructions)
