import logging
import asyncio
from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)

from livekit.agents.multimodal import MultimodalAgent

try:
    from livekit.plugins.google.beta.realtime import RealtimeModel
except ImportError:
    
    from livekit.plugins.google import RealtimeModel

from rag import RAGEngine

load_dotenv()


logger = logging.getLogger("voice-agent")
logger.setLevel(logging.INFO)


rag = RAGEngine("knowledge.txt")


class AssistantFnc(llm.FunctionContext):
    @llm.ai_callable(description="Search the knowledge base for specific information when the user asks a question about the company or technical details.")
    def search_knowledge(self, query: str):
        logger.info(f"🔍 AI is searching RAG for: {query}")
        results = rag.search(query)
        return results

async def entrypoint(ctx: JobContext):
    
    print(f"--- [DEBUG] Connecting to room: {ctx.room.name} ---")
    
   
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    print("--- [DEBUG] Waiting for user to join... ---")
    participant = await ctx.wait_for_participant()
    print(f"--- [DEBUG] User joined: {participant.identity} ---")

    
    model = RealtimeModel(
        model="gemini-2.0-flash-exp", 
        instructions=(
            "You are a helpful voice assistant. "
            "You have access to a knowledge base. "
            "ALWAYS use the 'search_knowledge' tool if the user asks about specific information not in your general training. "
            "Keep your responses concise and natural for voice conversation."
        ),
        modalities=["audio", "text"], 
        voice="Puck", 
    )

    
    agent = MultimodalAgent(
        model=model,
        fnc_ctx=AssistantFnc(), 
    )

    
    await agent.start(ctx.room, participant)
    
    print("--- [DEBUG] Agent is listening via Gemini Live API! ---")
    
   
    agent.generate_reply() 

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))