import logging
import asyncio
from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm
)
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins.google import BetaRealtimeModel
from rag import RAGEngine

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger("voice-agent")
logger.setLevel(logging.INFO)

# 1. Initialize the RAG engine once at startup
rag = RAGEngine("knowledge.txt")

# 2. Define the Tool (Function) that Gemini will use
# This class acts as the bridge between the LLM and the database
class AssistantFnc(llm.FunctionContext):
    @llm.ai_callable(description="Search the knowledge base for specific company information, policies, or FAQs.")
    def search_knowledge(self, query: str):
        """
        Called when the user asks a question that requires factual information from the documents.
        """
        logger.info(f"RAG Search Triggered for: {query}")
        results = rag.search(query)
        return results

# 3. Agent Entrypoint
async def entrypoint(ctx: JobContext):
    logger.info(f"Connecting to room {ctx.room.name}")
    
    # Connect to the room and subscribe to audio only
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for a participant to join
    participant = await ctx.wait_for_participant()
    
    # 4. Configure Gemini Live Model
    # We use the BetaRealtimeModel which supports the native audio streaming API
    model = BetaRealtimeModel(
        instructions="""
            You are a helpful voice assistant for our company.
            - Your responses should be concise and conversational.
            - You have access to a knowledge base tool. USE IT whenever the user asks about specific company details.
            - If you use the tool, incorporate the answer naturally into your speech.
            - Speak clearly and friendly.
        """,
        modalities=["audio", "text"], # Enable both audio and text modalities
    )

    # 5. Start the Multimodal Agent
    # We pass the function context (fnc_ctx) so the model knows it can use tools
    agent = MultimodalAgent(
        model=model,
        fnc_ctx=AssistantFnc()
    )

    # Start the agent in the room
    agent.start(ctx.room, participant)
    
    logger.info("Agent started and listening...")

# Run the application
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))