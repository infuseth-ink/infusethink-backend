from pydantic import BaseModel, ConfigDict


class AppBaseSchema(BaseModel):
    """
    Base model for all application schemas.
    """

    model_config = ConfigDict(from_attributes=True, use_attribute_docstrings=True)
