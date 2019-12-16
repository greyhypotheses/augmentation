import cfg.cfg as cfg
import os
import src.data.steps as steps


def main():

    var = cfg.Cfg().variables()
    rows = var.image.rows

    print(rows)
    print(os.getcwd())

    steps.Steps().augment()


if __name__ == '__main__':
    main()
