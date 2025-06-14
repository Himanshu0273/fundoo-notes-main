from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class LabelBase(BaseModel):
    label_name: str


class Label(LabelBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UpdateLabel(LabelBase):
    pass
