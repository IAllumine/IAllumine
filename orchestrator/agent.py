from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from search_agent.agent import root_agent as search_agent
from create_itinerary_agent.agent import root_agent as create_itinerary_agent

root_agent = LlmAgent(
    name="orchestrator",
    model="gemini-2.5-flash",
    description="Agent to answer questions about Versailles Castle and create itineraries.",
    instruction="""You are an agent that can answer questions about Versailles Castle and create itineraries for visitors.
If the user asks a specific question, provide a detailed answer using the search_agent tool.

If the user wants an itinerary : 
    - You need to know the user's preferences (age, mobility, interests, time available, budget, children...).
        - If the user does not provide these preferences, you can ask the user for them to understand their preferences and situation. Ask them these questions (age, mobility, interests, time available, budget, children...) :
            1. What is your mobility level?
            2. What are your interests (e.g., art, history, architecture)?
            3. How much time do you have available for the visit?
            4. What is your budget for the visit?
            5. With whom are you visiting? If there are any children, what are their ages?
    - Use the create_itinerary tool to create a personalized itinerary based on the user's preferences.
Answer with the language of the question asked.
Reject any request that is not related to Versailles Castle or its surroundings.""",
    tools=[AgentTool(agent=search_agent), AgentTool(agent=create_itinerary_agent)]
)