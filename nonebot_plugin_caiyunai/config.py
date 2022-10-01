from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    caiyunai_apikey: str = "62c2f1a9cf04bf13e9c512d6"
