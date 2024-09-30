from model import *

prod_models = ['User', 'Team']

models_to_load = [cls for cls in Base.__subclasses__() \
                  if (cls.__name__ != "Base" \
                      and cls.__name__ in prod_models)]