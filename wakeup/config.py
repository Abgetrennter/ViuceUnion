from pydantic import BaseSettings, Extra


class Config(BaseSettings,extra=Extra.ignore):
    # Your Config Here
    #class Config:
    extra = "ignore"