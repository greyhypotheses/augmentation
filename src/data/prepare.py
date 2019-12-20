import cfg.cfg as cfg


class Prepare:

    def __init__(self):
        variables = cfg.Cfg().variables()
        self.rotations = variables['augmentation']['images']['rotations']
        self.url = variables['source']['images']['url']
        self.ext = variables['source']['images']['ext']
        self.use = variables['source']['metadata']['use']
        self.if_missing = variables['source']['metadata']['if_missing']
        self.list_of_outliers = variables['augmentation']['images']['outliers']

    def filename(self, data):

        data['filename'] = data['image'].apply(lambda x: self.url + x + self.ext)

        return data

    def outliers(self, data):

        for i in self.list_of_outliers:
            data = data.loc[~eval(i)]
            data.reset_index(inplace=True)

        return data

    def missing(self, data):
        """
        Addressing missing values.
        Erroneous:
            data[self.use[i]] = data[self.use[i]].where(data[self.use[i]] != '', other=self.alt[i])

        :type data: pandas.DataFrame

        :param data:
        :return:
        """

        for i in range(len(self.use)):
            data[self.use[i]] = data[self.use[i]].fillna(value=self.if_missing[i])
            data[self.use[i]] = data[self.use[i]].apply(lambda x: self.if_missing[i] if x == '' else x)

        return data

    def angles(self, data, fields, labels):
        """
        Expands the data frame such that each original image now has a row per rotation required.

        :type data: pandas.DataFrame
        :type fields: list
        :type labels: list

        :param data: A data frame
        :param fields: The columns of data that are not label/class columns
        :param labels: The label/class columns of data
        :return:
        """
        angle_fields = {'A' + str(i).zfill(3): i for i in self.rotations}

        data = data.assign(**angle_fields)
        data = data.melt(id_vars=fields + labels,
                         value_vars=list(angle_fields.keys()),
                         var_name=['angle_fields_names'],
                         value_name='angle').drop(columns=['angle_fields_names'])

        return data
