from google.adk.agents import LlmAgent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

ask_vertex_retrieval = VertexAiRagRetrieval(
    name="retrieve_versailles_services",
    description=(
        "Use this tool to retrieve documentation and reference materials for any questions related to the services available at the Château de Versailles."
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus="projects/btel-data-lab-iafactory/locations/us-central1/ragCorpora/6917529027641081856"
        )
    ],
)

root_agent = LlmAgent(
    name="service_agent",
    model="gemini-2.0-flash",
    description="Assists visitors of the Versailles castle in finding and recommending the most suitable services, including restaurants, shops, accommodations, and other amenities, tailored to their planned visit.",
    instruction=(
        "You are an expert assistant for visitors to the Château de Versailles. "
        "Recommend services such as restaurants, shops, accommodations, and amenities that best fit the visitor's needs and preferences. "
        "Use the retrieve_versailles_services tool to find relevant information and provide accurate answers to user queries."
    ),
    tools=[ask_vertex_retrieval],
    output_key="services"
)
