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

mock_tools = [
    {
        "id": str(uuid.uuid4()),
        "name": "Sitepaige",
        "description": "AI web developer that generates complete websites with frontend, backend, database, and APIs from natural language descriptions. Free export with full code ownership.",
        "longDescription": "AI web developer that generates complete websites with frontend, backend, database, and APIs from natural language descriptions. Free export with full code ownership. Perfect for rapid prototyping and MVP development.",
        "category": "Website Builder",
        "pricing": "Paid",
        "tags": ["#AIWebsiteBuilder", "#NoCode", "#FullStack"],
        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500&h=300&fit=crop",
        "featured": True,
        "url": "https://sitepaige.com",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Quickads",
        "description": "AI ad generator with a 20M+ ad library, fast image and video creation, and direct publishing tools for small businesses, agencies, and marketing teams.",
        "longDescription": "AI ad generator with a 20M+ ad library, fast image and video creation, and direct publishing tools for small businesses, agencies, and marketing teams. Create professional ads in minutes.",
        "category": "Advertising",
        "pricing": "Paid",
        "tags": ["#AIAdvertising", "#MetaAds", "#AdCreation"],
        "image": "https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=500&h=300&fit=crop",
        "featured": False,
        "url": "https://quickads.ai",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Do It Free",
        "description": "DoItFree.ai turns how to searches into structured learning paths with curated resources, videos, and communities, helping you learn any skill for free, step by step.",
        "longDescription": "DoItFree.ai turns how to searches into structured learning paths with curated resources, videos, and communities, helping you learn any skill for free, step by step. Perfect for self-learners.",
        "category": "Education",
        "pricing": "Free",
        "tags": ["#AILearning", "#LearningTool", "#Education"],
        "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=500&h=300&fit=crop",
        "featured": False,
        "url": "https://doitfree.ai",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Radiant",
        "description": "Radiant captures Mac meetings and executes the follow-up work. Sends emails in Gmail, and updates in Notion without prompts or manual setup.",
        "longDescription": "Radiant captures Mac meetings and executes the follow-up work. Sends emails in Gmail, and updates in Notion without prompts or manual setup. Automate your meeting workflow completely.",
        "category": "Productivity",
        "pricing": "Free",
        "tags": ["#AIAssistant", "#AIMeetings", "#Productivity"],
        "image": "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=500&h=300&fit=crop",
        "featured": False,
        "url": "https://radiant.ai",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Hostinger Horizons",
        "description": "Hostinger Horizons is a no-code builder that uses conversational AI to turn plain-language prompts into web apps, with Supabase integration, hosting, and real-time editing included.",
        "longDescription": "Hostinger Horizons is a no-code builder that uses conversational AI to turn plain-language prompts into web apps, with Supabase integration, hosting, and real-time editing included. Build complex apps without writing code.",
        "category": "NoCode",
        "pricing": "Freemium",
        "tags": ["#AIApps", "#AIWebDevelopment", "#NoCode"],
        "image": "https://images.unsplash.com/photo-1551434678-e076c223a692?w=500&h=300&fit=crop",
        "featured": False,
        "url": "https://hostinger.com",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Higgsfield",
        "description": "AI video platform with precision camera control for filmmakers and creators. Generate cinematic shots using crash zooms, dolly moves, and creative angles.",
        "longDescription": "AI video platform with precision camera control for filmmakers and creators. Generate cinematic shots using crash zooms, dolly moves, and creative angles. Multi-model access including Sora 2 with unlimited generations on paid plans.",
        "category": "Video Generation",
        "pricing": "Freemium",
        "tags": ["#AIVideo", "#GenerativeVideo", "#VideoCreation"],
        "image": "https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=500&h=300&fit=crop",
        "featured": True,
        "url": "https://higgsfield.ai",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "BeFreed",
        "description": "AI learning app that converts book summaries into short audio lessons with flashcards, an AI tutor, and adaptive learning plans for busy schedules.",
        "longDescription": "AI learning app that converts book summaries, podcasts, and articles into short audio lessons with flashcards, an AI tutor, and adaptive learning plans for busy schedules. Learn on the go.",
        "category": "Education",
        "pricing": "Freemium",
        "tags": ["#AILearning", "#microlearning", "#AudioLearning"],
        "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=500&h=300&fit=crop",
        "featured": False,
        "url": "https://befreed.ai",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "CoTester",
        "description": "AI testing agent that auto-generates self-healing test cases from JIRA stories, adapts to UI changes mid-execution, and runs across real browsers.",
        "longDescription": "AI testing agent that auto-generates self-healing test cases from JIRA stories, adapts to UI changes mid-execution, and runs across real browsers with human checkpoints for enterprise control.",
        "category": "Automation",
        "pricing": "Paid",
        "tags": ["#AITesting", "#TestAutomation", "#QA"],
        "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&h=300&fit=crop",
        "featured": False,
        "url": "https://cotester.ai",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "isFake.ai",
        "description": "Multi-modal AI detector that analyzes text, images, video, and audio for synthetic patterns, providing confidence scores and visual explanations.",
        "longDescription": "Multi-modal AI detector that analyzes text, images, video, and audio for synthetic patterns, providing confidence scores and visual explanations for content verification.",
        "category": "AI Detection",
        "pricing": "Freemium",
        "tags": ["#AIDetection", "#ContentVerification", "#DeepFake"],
        "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=500&h=300&fit=crop",
        "featured": False,
        "url": "https://isfake.ai",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "HeyGen",
        "description": "Create high-quality videos with HeyGen AI video generator. Featuring Sora2, a multilingual platform that creates professional content in minutes.",
        "longDescription": "Create high-quality videos with HeyGen AI video generator. Featuring Sora2, a multilingual platform that creates professional, multilingual content in minutes. Now featuring Sora2, for instant scene and B-roll generation.",
        "category": "Text-to-Video",
        "pricing": "Paid",
        "tags": ["#AIavatars", "#UGC", "#Sora2"],
        "image": "https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=500&h=300&fit=crop",
        "featured": False,
        "url": "https://heygen.com",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Galaxy AI",
        "description": "Galaxy.ai combines GPT, Claude, Gemini, Midjourney, Sora 2, Nano Banana, and thousands more into one affordable plan.",
        "longDescription": "Galaxy.ai combines GPT, Claude, Gemini, Midjourney, Sora 2, Nano Banana, and thousands more into one affordable $15 monthly plan. Create text, images, video, audio, and code from a single platform.",
        "category": "Productivity",
        "pricing": "Paid",
        "tags": ["#AIToolsHub", "#AllInOneAI", "#MultiModel"],
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=500&h=300&fit=crop",
        "featured": False,
        "url": "https://galaxy.ai",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Arcads",
        "description": "Arcads uses AI to turn your text scripts into complete video ads. Choose an AI actor and get a finished video with lip sync, music, and captions.",
        "longDescription": "Arcads uses AI to turn your text scripts into complete video ads. Choose an AI actor and get a finished video with lip sync, music, and captions. Perfect for marketing teams.",
        "category": "Video Generation",
        "pricing": "Freemium",
        "tags": ["#UGC", "#AIAds", "#AIMarketing"],
        "image": "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=500&h=300&fit=crop",
        "featured": False,
        "url": "https://arcads.ai",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
]

async def seed_db():
    # Clear existing tools
    await db.tools.delete_many({})
    print("Cleared existing tools")
    
    # Insert new tools
    result = await db.tools.insert_many(mock_tools)
    print(f"Inserted {len(result.inserted_ids)} tools")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_db())
