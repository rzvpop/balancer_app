import configparser


def read_ini(section, prop):
    config = configparser.ConfigParser()
    config.read('config.ini')

    if section in config.sections():
        if prop in config[section]:
            return config[section][prop]

    return None


def format_migration_class_name(migration_str):
    return ''.join(item[0].upper() + item[1:] for item in migration_str.split('_')) + 'Migration'
