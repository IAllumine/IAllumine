from google.adk.agents import ParallelAgent, LlmAgent, SequentialAgent
from event_agent.agent import root_agent as event_agent
from weather_affluence_agent.agent import root_agent as weather_agent
from service_agent.agent import root_agent as service_agent
from visit_agent.agent import root_agent as visit_agent
from tips_agent.agent import root_agent as tips_agent

# Parallel agent that runs several research agents concurrently
research_parallel_agent = ParallelAgent(
     name="research_parallel_agent",
     sub_agents=[event_agent, weather_agent, service_agent, visit_agent],
     description=(
          "Parallel data-collection agent: runs the event, weather/affluence and service agents "
          "concurrently to gather all information required to build a route and plan a visit to "
          "the Palace of Versailles."
     )
)

# Synthesis agent backed by a LLM that organizes and summarizes results
synthesis_agent = LlmAgent(
     name="synthesis_agent",
     model="gemini-2.5-flash-lite",
     instruction=(
          "You are an AI Assistant responsible for combining research findings into a structured report.")
)

# Sequential pipeline: first parallel collection, then synthesis
create_itinerary_agent = SequentialAgent(
     name="create_itinerary_agent",
     # Run parallel collection first, then the synthesis step
     sub_agents=[research_parallel_agent, synthesis_agent, tips_agent],
     description=(
          "Research and synthesis pipeline: collects data in parallel via multiple agents, then "
          "generates a consolidated, structured report to assist visit planning."
     ),
)

# Export root for compatibility with the project's pattern
root_agent = create_itinerary_agent