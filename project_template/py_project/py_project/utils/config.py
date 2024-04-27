import yaml


class Config:
    def __init__(self):
        with open("./config/config.yaml", "r", encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            self.__config = config
            f.close()

    def get_config(self):
        return self.__config
