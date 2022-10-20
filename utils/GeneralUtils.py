from configparser import ConfigParser


def getConfig(section, filename='config.ini'):
    parser = ConfigParser()
    parser.read(filename)

    config = None
    if parser.has_section(section):
        config = {}
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return config
