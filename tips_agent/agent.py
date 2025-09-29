from google.adk.agents import LlmAgent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

ask_vertex_retrieval = VertexAiRagRetrieval(
    name="retrieve_versailles_tips",
    description=(
        "Use this tool to retrieve tips for visiting the Château de Versailles."
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus="projects/btel-data-lab-iafactory/locations/us-central1/ragCorpora/5188146770730811392"
        )
    ],
)

root_agent = LlmAgent(
    name="service_agent",
    model="gemini-2.5-flash",
    description="Assists visitors of the Versailles castle in finding and recommending the most suitable tips to their planned visit.",
    instruction=(
        "You are an expert assistant for visitors to the Château de Versailles. "
        "You are gonna get the synthesis of a guided tour for visitors. Your goal is to add tips using the retrieve_versailles_tips tools to complete the synthesis."
        "Keep the texts you receive and add your tips either directly in the given text or in another section named Conseils Supplémentaires (translated in the right language)."
        "Do not repeat already written or similar informations."
        "Use the retrieve_versailles_tips tool to find relevant information and provide accurate answers to complete user queries."
    ),
    tools=[ask_vertex_retrieval],
)
