from google.adk.agents import LlmAgent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

ask_vertex_retrieval = VertexAiRagRetrieval(
    name="retrieve_versailles_visits",
    description=(
        "Use this tool to retrieve documentation and reference materials for any questions related to the visits available at the Château de Versailles."
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus="projects/btel-data-lab-iafactory/locations/us-central1/ragCorpora/3458764513820540928"
        )
    ],
)

root_agent = LlmAgent(
    name="visit_agent",
    model="gemini-2.0-flash",
    description=(
        "Provides personalized guidance and itinerary planning for visitors to the Château de Versailles, "
        "including recommendations for families, visitors with disabilities, and other specific needs. "
        "Also recommends the most suitable ticket options for each visitor."
    ),
    instruction=(
        "You are a knowledgeable assistant specializing in planning visits to the Château de Versailles. "
        "Carefully consider each visitor's profile, such as families with children or individuals with disabilities, "
        "to recommend suitable itineraries, activities, facilities, and the best ticket options adapted to their needs. "
        "Always use the retrieve_versailles_visits tool to access up-to-date documentation and reference materials, "
        "ensuring your answers are accurate, relevant, and tailored to the visitor's requirements."
    ),
    tools=[ask_vertex_retrieval],
)
