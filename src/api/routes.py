from fastapi import APIRouter, Query
from ..services.llm_service import llm_service
from ..utils import build_role_prompts, get_location_and_weather_context

router = APIRouter()

@router.get("/ask")
async def ask(
    prompt: str = Query(..., 
                        description="The question or prompt about fishing "
                        "conditions at a body of water in a specific "
                        "state for the LLM to answer.")
):

    additional_context = get_location_and_weather_context(prompt)

    role_messages = build_role_prompts(prompt, additional_context)

    answer = llm_service.ask_mr_robot(role_messages)

    return answer
