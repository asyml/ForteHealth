import yaml


with open('main.yml') as f:
    my_dict = yaml.safe_load(f)

print(my_dict)