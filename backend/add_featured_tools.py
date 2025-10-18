import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

new_featured_tools = [
    {
        "id": str(uuid.uuid4()),
        "name": "Perplexity AI",
        "description": "Perplexity AI is an advanced AI-powered search engine that provides accurate, real-time answers with citations. Get FREE 1 month Pro account at https://pplx.ai/vongocdiem97799",
        "longDescription": "Perplexity AI revolutionizes how you search and discover information online. Unlike traditional search engines, Perplexity uses advanced AI models to understand your questions and provide direct, accurate answers with proper citations. Key features include: Real-time web search with AI-powered summaries, Multi-source citation for transparency, Voice search capabilities, Follow-up question suggestions, and Pro mode with GPT-4 and Claude access. 🎁 Special Offer: Claim your FREE 1 month Pro account at https://pplx.ai/vongocdiem97799 to unlock unlimited Pro searches, advanced AI models, and priority support!",
        "category": "Productivity",
        "pricing": "Freemium",
        "tags": ["#AISearch", "#Research", "#Productivity", "#FreeTrial"],
        "image": "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=500&h=300&fit=crop",
        "featured": True,
        "url": "https://pplx.ai/vongocdiem97799",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Comet Browser",
        "description": "Comet is an AI-native browser that integrates ChatGPT, Claude, and Gemini directly into your browsing experience. Claim FREE 1 month Pro at https://pplx.ai/vongocdiem97799",
        "longDescription": "Comet Browser redefines web browsing by seamlessly integrating powerful AI assistants directly into your browser. No more switching tabs or copying text between windows. Key features include: Built-in ChatGPT, Claude, and Gemini integration, AI-powered summarization of web pages, Smart tab management with AI organization, Privacy-focused browsing with ad-blocking, Real-time translation and content explanation, and Instant answers without leaving your current page. 🎁 Special Launch Offer: Get FREE 1 month Pro access at https://pplx.ai/vongocdiem97799 - Experience the future of AI-powered browsing with unlimited AI queries, advanced models access, and premium features!",
        "category": "Productivity",
        "pricing": "Freemium",
        "tags": ["#AIBrowser", "#Productivity", "#ChatGPT", "#FreeTrial"],
        "image": "https://images.unsplash.com/photo-1547954575-855750c57bd3?w=500&h=300&fit=crop",
        "featured": True,
        "url": "https://pplx.ai/vongocdiem97799",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
]

async def add_featured_tools():
    # Add new featured tools
    result = await db.tools.insert_many(new_featured_tools)
    print(f"✅ Added {len(result.inserted_ids)} featured tools: Perplexity AI & Comet Browser")
    print(f"🎁 Both tools include FREE 1 month Pro claim link!")
    
    # Get current featured tools count
    featured_count = await db.tools.count_documents({"featured": True})
    print(f"📊 Total featured tools in database: {featured_count}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_featured_tools())
