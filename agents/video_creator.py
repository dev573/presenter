from typing import Any, List
import os
import pickle

from llama_index.core.workflow import (
    step,
    Context,
    Workflow,
    Event,
    StartEvent,
    StopEvent,
)
from llama_index.core.workflow.retry_policy import ConstantDelayRetryPolicy

from models import PresentationStructure


class NarrationRequestReceived(Event):
    slide_index: int


class SlideNarrated(Event):
    slide_index: int


class SlideClipCreated(Event):
    slide_index: int


class PresenterVideoCreaterWorkflow(Workflow):
    def __init__(
        self,
        *args: Any,
        model: str,
        voice: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.model = model
        self.voice = voice

    @step
    async def start(
        self, ctx: Context, ev: StartEvent
    ) -> NarrationRequestReceived | StopEvent:
        presentation_dir = ev.presentation_dir
        await ctx.set("presentation_dir", presentation_dir)
        structure_file = os.path.join(presentation_dir, "structure.pkl")
        if not os.path.exists(structure_file):
            return StopEvent(result="No structure found")
        with open(structure_file, "rb") as f:
            structure: PresentationStructure = pickle.load(f)
        await ctx.set("structure", structure)
        slides = structure.slides
        await ctx.set("num_slides", len(slides))
        for i in slides:
            ctx.send_event(NarrationRequestReceived(slide_index=i))

    @step(num_workers=5, retry_policy=ConstantDelayRetryPolicy())
    async def narrate_slide(
        self, ctx: Context, ev: NarrationRequestReceived
    ) -> SlideNarrated:
        slide_index = ev.slide_index
        presentation_dir = await ctx.get("presentation_dir")
        slide_dir = os.path.join(presentation_dir, f"slide_{slide_index}")
        narration_file = os.path.join(slide_dir, "narration.txt")
        with open(narration_file, "r") as f:
            narration = f.read()
