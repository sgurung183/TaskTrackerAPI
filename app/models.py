#gives you validation + JSON conversion
from pydantic import BaseModel
#BaseModel = the base class that makes all of this validation actucally happen when data comes in
#allows to mark a field as allowed to be empty
from typing import Optional

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    completed: bool = False