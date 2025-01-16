import sys
import asyncio

from dotenv import load_dotenv

from llama_index.utils.workflow import draw_all_possible_flows
from llama_index.llms.openai import OpenAI

from workflow import PresenterWorkflow


async def main():
    load_dotenv()
    llm = OpenAI(model="gpt-4o-mini")
    workflow = PresenterWorkflow(llm=llm, verbose=False, timeout=240.0)
    # draw_all_possible_flows(workflow, filename="workflow.html")
    topic = sys.argv[1]
    result = await workflow.run(query=topic)
    # for i, slide in enumerate(result.slides):
    #     print(f"{i+1}. Title: {slide.title}\nContent: {slide.atomic_core_idea}\n")


if __name__ == "__main__":
    asyncio.run(main())
