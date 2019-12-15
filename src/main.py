import configurations.configurations as cfg


def main():

    remnant = cfg.variables['image']['remnant']
    strip = int(remnant/2)
    input_size = (cfg.variables['image']['rows'], cfg.variables['image']['columns'])
    temporary_size = (input_size[0] + remnant, input_size[1] + remnant)
    rows, columns = temporary_size[0], temporary_size[1]
    centre = (columns/2, rows/2)
    rotations = cfg.variables['image']['rotations']

    print(type(rotations[1]))


if __name__ == '__main__':
    main()
