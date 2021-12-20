import yaml


class Config:
    """This is just a simple yaml object converter"""

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            vars(self)[k] = v

    @classmethod
    def read(cls):
        stream = open("config.yaml", 'r')
        data = yaml.safe_load(stream)
        return cls(**data)


config = Config.read()

if __name__ == "__main__":
    print(dir(config))
    print(config.keywords)