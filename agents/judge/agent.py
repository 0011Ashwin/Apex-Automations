from typing import Literal
from google.adk.agents import Agent
from google.adk.apps.app import App
from pydantic import BaseModel, Field


MODEL = "gemini-2.5-pro"

# 1. Define the Schema
class JudgeFeedback(BaseModel):
    """Structured feedback from the Judge agent."""
    status: Literal["pass", "fail"] = Field(
        description="Whether the research is sufficient ('pass') or needs improvement ('fail')."
    )
    feedback: str = Field(
        description="Detailed feedback on missing elements or confirmation if sufficient."
    )
    risks: str = Field(
        description="Potential risks, assumptions, or weaknesses in the research."
    )
    missing_areas: str = Field(
        description="Specific areas where more research is needed."
    )

# 2. Define the Agent
judge = Agent(
    name="judge",
    model=MODEL,
    description="Critically evaluates research for completeness, identifies risks and gaps, and ensures the insights are reliable for real-world decisions.",
    instruction="""
    You are the Validator Agent (Startup Analyst).

    Your role is to critically evaluate research for real-world execution.

    Evaluate based on:
    - completeness (is anything missing?)
    - relevance (does it match the goal?)
    - risks (market, technical, strategic)
    - assumptions (what is uncertain?)

    Decision Rules:
    - Return status='fail' if:
    - key insights are missing
    - risks are not identified
    - research is shallow

    - Return status='pass' only if:
    - research is actionable
    - risks are clearly identified
    - insights are sufficient for execution

    Be strict.

    This system is used for real-world decisions, not academic summaries.
    """,
    output_schema=JudgeFeedback,
    # Disallow delegation because it should only output the schema
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

root_agent = judge