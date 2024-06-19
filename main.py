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


def find_redstone_torches(schematic, corner):
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

    print(f"Width: {width}, Height: {height}, Length: {length}")
    print(range(-5))  # Results in range(0, -5) instead of range(0, -1, 2), custom range fixes this

    redstone_torches = []
    for x in custom_range(width):
        for y in custom_range(height):
            for z in custom_range(length):
                print(f"Checking block at ({x}, {y}, {z})")
                block_data = schematic.getBlockDataAt((x, y, z))
                if 'redstone_wall_torch' in block_data:
                    print(f"Found redstone torch at ({x}, {y}, {z})")
                    redstone_torches.append((x, y, z))

    return redstone_torches


def torches_to_binary(redstone_torches):
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
        for x in range(min(x_count), max(x_count) + 1, 2):
            bit_points.append((x, y_count[0], z_count[0]))
    elif len(y_count) > len(x_count) and len(y_count) > len(z_count):
        unique_dim = 'y'
        for y in range(min(y_count), max(y_count) + 1, 2):
            bit_points.append((x_count[0], y, z_count[0]))
    else:
        unique_dim = 'z'
        for z in range(min(z_count), max(z_count) + 1, 2):
            bit_points.append((x_count[0], y_count[0], z))

    print(f"Unique Dimension: {unique_dim}")
    # Initialize the binary string
    binary_string = ''

    print(bit_points)

    return binary_string


schematic = mcschematic.MCSchematic(
    "schematics/6bitsegmentNE.schem")  # Loads a programmable ROM segment with 6 bits and is torch based.

redstone_torches = find_redstone_torches(schematic, 'NE')
print(f'Redstone Torches: {redstone_torches}')
binary_string = torches_to_binary(redstone_torches)
print(f'String: {binary_string}')

instructions = parse_instructions('instructions.txt')\

print(instructions)
