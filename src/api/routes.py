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
) -> str:
    """
    # Overview
    Retrieves additional context for the prompt, builds role messages for the
    LLM with the additional context, and sends the request to the LLM service 
    for processing.

    ## Args
    * **prompt (str)**: The question or prompt about fishing conditions at a body
                      of water in a specific state from the LLM.

    ## Returns
    * **str**: The response from the LLM service, which includes the answer to
             the user's prompt with the provided context.
    """
    additional_context = get_location_and_weather_context(prompt)

    role_messages = build_role_prompts(prompt, additional_context)

    answer = llm_service.ask_mr_robot(role_messages)

    return answer
