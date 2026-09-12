from pydantic import BaseModel, Field

class HelloModel(BaseModel):
    name: str = Field(..., description="The name of the user to greet", min_length=1, max_length=50)