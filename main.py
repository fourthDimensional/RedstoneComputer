import mcschematic

def custom_range(n):
    if n >= 0:
        return range(n)
    else:
        return range(0, n, -1)

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

    print(f"Width: {width}, Height: {height}, Length: {length}")
    print(range(-5)) # Results in range(0, -5) instead of range(0, -1, 2), custom range fixes this

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

schematic = mcschematic.MCSchematic("schematics/6bitsegmentNE.schem") # Loads a programmable ROM segment with 6 bits and is torch based.

print(find_redstone_torches(schematic, 'NE'))