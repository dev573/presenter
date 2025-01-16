import os
import subprocess
from typing import Any

from llama_index.core.llms.llm import LLM
from llama_index.core.workflow import (
    step,
    Context,
    Workflow,
    Event,
    StartEvent,
    StopEvent,
)

from models import PresentationStructure, StructureFeedback, Slide, SlideInfo
from agents.structure_creater import create_presentation_structure
from agents.structure_validator import validate_presentation_structure
from agents.structure_updater import update_presentation_structure
from agents.slide_maker import compose_slide
from utils import get_presentation_config, get_safe_foldername, sanitize_markdown


class StructureRequestReceived(Event):
    topic: str


class ValidateStructureRequestReceived(Event):
    structure: PresentationStructure


class UpdateStructureRequestReceived(Event):
    structure: PresentationStructure
    feedback: StructureFeedback


class StructureFinalized(Event):
    structure: PresentationStructure


class ComposeSlideRequestReceived(Event):
    slide_index: int
    slide_info: SlideInfo


class SlideCreated(Event):
    slide_index: int
    content: str


class PresenterWorkflow(Workflow):
    def __init__(
        self,
        *args: Any,
        llm: LLM,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.llm = llm

    @step
    async def start(self, ctx: Context, ev: StartEvent) -> StructureRequestReceived:
        topic = ev.query
        await ctx.set("topic", topic)
        presentation_folder = os.path.join("presentations", get_safe_foldername(topic))
        await ctx.set("presentation_folder", presentation_folder)
        if not os.path.exists(presentation_folder):
            os.makedirs(presentation_folder)
        return StructureRequestReceived(topic=topic)

    @step
    async def create_presentation_structure(
        self, ctx: Context, ev: StructureRequestReceived
    ) -> ValidateStructureRequestReceived:
        topic = ev.topic
        initial_structure = create_presentation_structure(topic, self.llm)
        return ValidateStructureRequestReceived(structure=initial_structure)

    @step
    async def validate_presentation_structure(
        self, ctx: Context, ev: ValidateStructureRequestReceived
    ) -> UpdateStructureRequestReceived | StructureFinalized:
        structure = ev.structure
        topic = await ctx.get("topic")
        feedback = validate_presentation_structure(topic, structure, self.llm)
        if feedback.is_perfect:
            return StructureFinalized(structure=structure)
        return UpdateStructureRequestReceived(structure=structure, feedback=feedback)

    @step
    async def update_presentation_structure(
        self, ctx: Context, ev: UpdateStructureRequestReceived
    ) -> StructureFinalized:
        structure = ev.structure
        feedback = ev.feedback
        topic = await ctx.get("topic")
        updated_structure = update_presentation_structure(
            topic, structure, feedback, self.llm
        )
        return StructureFinalized(structure=updated_structure)

    @step
    async def create_slides(
        self, ctx: Context, ev: StructureFinalized
    ) -> ComposeSlideRequestReceived:
        structure = ev.structure
        await ctx.set("structure", structure)
        for slide_index, slide in enumerate(structure.slides):
            ctx.send_event(
                ComposeSlideRequestReceived(slide_index=slide_index, slide_info=slide)
            )

    @step(num_workers=6)
    async def create_one_slide(
        self, ctx: Context, ev: ComposeSlideRequestReceived
    ) -> SlideCreated:
        structure = ev.structure
        topic = await ctx.get("topic")
        return StopEvent(result=structure)
