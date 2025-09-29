from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from search_agent.agent import root_agent as search_agent

root_agent = LlmAgent(
    name="orchestrator",
    model="gemini-2.0-flash",
    description="Agent to answer questions about Versailles Castle and create itineraries.",
    instruction="""You are an agent that can answer questions about Versailles Castle and create itineraries for visitors.
If the user asks a specific question, provide a detailed answer using the search_agent tool.
If the user wants an itinerary and provides their preferences, create a personalized itinerary using the create_itinerary tool.
If the user wants an itinerary but does not provide preferences, ask him questions to understand his preferences and situation (age, mobility, interests, time available, budget, children...).
Answer with the language of the question asked.""",
    tools=[AgentTool(agent=search_agent)]
)