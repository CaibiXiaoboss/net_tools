import yaml


def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def write_yaml(data, file_path):
    with open(file_path, 'a+', encoding='utf-8') as file:
        yaml.safe_dump(data, file)
