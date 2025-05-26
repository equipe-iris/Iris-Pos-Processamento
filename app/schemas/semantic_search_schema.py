from pydantic import BaseModel, ConfigDict

class SemanticSearchSchema(BaseModel):
    id: int
    score: float

    model_config = ConfigDict(from_attributes=True)