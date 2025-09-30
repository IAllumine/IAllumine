from google.adk.agents import LlmAgent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

# ask_vertex_retrieval = VertexAiRagRetrieval(
#     name="retrieve_versailles_services",
#     description=(
#         "Use this tool to retrieve documentation and reference materials for any questions related to the services available at the Château de Versailles."
#     ),
#     rag_resources=[
#         rag.RagResource(
#             rag_corpus="projects/btel-data-lab-iafactory/locations/us-central1/ragCorpora/6917529027641081856"
#         )
#     ],
# )

ask_vertex_retrieval_service = VertexAiRagRetrieval(
    name="retrieve_versailles_services",
    description="""Use this tool to retrieve documentation and reference materials for any questions related to the services available at the Château de Versailles such as :
        ===
        - Water fountains
        - Lockers
        - Info points
        - Toilets
        - Audio guides / audio phone
        - Recharge points for phone
        """,
    rag_resources=[
        rag.RagResource(
            rag_corpus="projects/btel-data-lab-iafactory/locations/us-central1/ragCorpora/1866742045545070592"
        )   
    ]
)

ask_vertex_retrieval_restauration = VertexAiRagRetrieval(
    name="retrieve_versailles_restauration",
    description="""Use this tool to retrieve documentation and reference materials for any questions related to the restauration services available at the Château de Versailles such as :
        ===
        - Restaurants
        - Cafes
        - Food trucks
        - Picnic areas
        """,
    rag_resources=[
        rag.RagResource(
            rag_corpus="projects/btel-data-lab-iafactory/locations/us-central1/ragCorpora/137359788634800128"
        )   
    ]
)

ask_vertex_retrieval_loisirs_transports = VertexAiRagRetrieval(
    name="retrieve_versailles_loisirs_transports",
    description="""Use this tool to retrieve documentation and reference materials for any questions related to the leisure activities and transport services available at the Château de Versailles such as :
        ===
        - Bike rentals
        - Boat rentals
        - Electric car rentals
        - Small train tours
        - Marly domains
        - Versailles domains
        """,
    rag_resources=[
        rag.RagResource(
            rag_corpus="projects/btel-data-lab-iafactory/locations/us-central1/ragCorpora/3596124302455341056"
        )
    ]
)

ask_vertex_retrieval_boutique = VertexAiRagRetrieval(
    name="retrieve_versailles_boutique",
    description="""Use this tool to retrieve documentation and reference materials for any questions related to the boutique services available at the Château de Versailles such as :
        ===
        - Gift shops
        - Bookstores
        - Souvenir shops
        """,
    rag_resources=[
        rag.RagResource(
            rag_corpus="projects/btel-data-lab-iafactory/locations/us-central1/ragCorpora/5325506559365611520"
        )
    ]
)

ask_vertex_retrieval_hebergement = VertexAiRagRetrieval(
    name="retrieve_versailles_hebergement",
    description="""Use this tool to retrieve documentation and reference materials for any questions related to the accommodation services available at the Château de Versailles such as :
        ===
        - Hotels
        - Bed and breakfasts
        - Hostels
        - Camping sites
        """,
    rag_resources=[
        rag.RagResource(
            rag_corpus="projects/btel-data-lab-iafactory/locations/us-central1/ragCorpora/7054888816275881984"
        )
    ]
)

root_agent = LlmAgent(
    name="service_agent",
    model="gemini-2.0-flash",
    description="Assists visitors of the Versailles castle in finding and recommending the most suitable services, including restaurants, shops, accommodations, and other amenities, tailored to their planned visit.",
    instruction=(
        "You are an expert assistant for visitors to the Château de Versailles. "
        "Recommend services such as restaurants, shops, accommodations, and amenities that best fit the visitor's needs and preferences. "
        "You have access to several retrieval tools (retrieve_versailles_services, retrieve_versailles_restauration, "
        "retrieve_versailles_loisirs_transports, retrieve_versailles_boutique, retrieve_versailles_hebergement) to look up documentation and reference materials. "
        "Use the most relevant tool(s) to find accurate information for user queries."
    ),
    tools=[
        ask_vertex_retrieval_service,
        ask_vertex_retrieval_restauration,
        ask_vertex_retrieval_loisirs_transports,
        ask_vertex_retrieval_boutique,
        ask_vertex_retrieval_hebergement,
    ],
)
