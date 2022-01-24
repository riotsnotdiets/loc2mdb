import yaml
import os


class Config:
    #yaml_path = os.path.join(os.getcwd(), '..', '')
    #yaml_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yml')

    yaml_file = os.path.join(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0], 'config.yml')
    __conf = yaml.safe_load(open(yaml_file))
    #__conf = yaml.safe_load(open(f'{yaml_path}config.yml'))
    #__conf = yaml.safe_load(open('.\config.yml'))

    @staticmethod
    def get(name):
        return Config.__conf[name]

#yaml_path = os.path.join(os.getcwd(), '..', '')
#conf = yaml.safe_load(open(f'{yaml_path}config.yml'))
#print(conf)


