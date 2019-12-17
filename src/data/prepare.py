import cfg.cfg as cfg


class Prepare:

    def __init__(self):
        variables = cfg.Cfg().variables()
        self.rotations = variables.augmentation.images.rotations
        self.url = variables.source.images.url
        self.ext = variables.source.images.ext
        self.use = variables.source.metadata.use
        self.alt = variables.source.metadata.alt

    def missing(self, inventory):
        """
        Addressing missing values
        :param inventory:
        :return:
        """

        for i in range(len(self.use)):
            inventory[self.use[i]] = inventory[self.use[i]].fillna(value=self.alt[i])
            inventory[self.use[i]] = inventory[self.use[i]].where(inventory[self.use[i]] != '', other=self.alt[i])

        return inventory

    def angles(self, inventory, fields, labels):

        angle_fields = {'A' + str(i).zfill(3):i for i in self.rotations}

        inventory = inventory.assign(**angle_fields)
        inventory = inventory.melt(id_vars=fields + labels,
                                   value_vars=list(angle_fields.keys()),
                                   var_name=['angle_fields_names'],
                                   value_name='angle').drop(columns=['angle_fields_names'])

        return inventory
