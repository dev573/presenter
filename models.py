from typing import List, Optional
from pydantic import BaseModel, Field


class SlideInfo(BaseModel):
    title: str = Field(..., title="Title of the slide")
    atomic_core_idea: str = Field(
        ..., title="Atomic core idea for the content of this particular slide"
    )


class PresentationStructure(BaseModel):
    slides: List[SlideInfo] = Field(
        ..., title="List of slides information in the presentation"
    )


class StructureFeedback(BaseModel):
    is_perfect: bool = Field(
        ...,
        title="Whether all the slides represent atomic core ideas and can be narrated in 40-50 seconds",
    )
    feedback: Optional[str] = Field(
        None,
        title="If all the slides are not perfect then feedback on which slides need to be broken down and how",
    )
