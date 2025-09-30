from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from search_agent.agent import root_agent as search_agent
from create_itinerary_agent.agent import root_agent as create_itinerary_agent

root_agent = LlmAgent(
    name="orchestrator_api",
    model="gemini-2.5-flash",
    description="Agent to answer questions about Versailles Castle and create itineraries.",
    instruction="""You are an agent that can answer questions about Versailles Castle and create itineraries for visitors.

If the user asks a specific question, provide a detailed answer using the search_agent tool. After your answer, ask the user if he wants help to plan his visit or create an itinerary.
If the user asks for an itinerary, help planning a visit or preparing his trip at versailles, use the create_itinerary_agent tool to create a itinerary.
Don't be too rigid in your questions, adapt them to the user's previous answers and the context of the conversation.
Use the tool create_itinerary_agent to create a personalized itinerary.

Use the tool search_agent for all other questions about Versailles Castle.

Answer with the language of the question asked.
Reject any request that is not related to Versailles Castle or its surroundings.""",
    tools=[AgentTool(agent=search_agent), AgentTool(agent=create_itinerary_agent)]
)