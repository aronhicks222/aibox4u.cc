import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def update_featured_tools():
    # Remove featured status from all tools
    await db.tools.update_many({}, {"$set": {"featured": False}})
    print("✓ Removed featured status from all tools")
    
    # Set featured=True only for Perplexity AI and Comet Browser
    result1 = await db.tools.update_one(
        {"name": "Perplexity AI"},
        {"$set": {"featured": True}}
    )
    
    result2 = await db.tools.update_one(
        {"name": "Comet Browser"},
        {"$set": {"featured": True}}
    )
    
    print(f"✅ Set featured=True for Perplexity AI (modified: {result1.modified_count})")
    print(f"✅ Set featured=True for Comet Browser (modified: {result2.modified_count})")
    
    # Verify
    featured_tools = await db.tools.find({"featured": True}, {"_id": 0, "name": 1}).to_list(10)
    print(f"\n📊 Featured tools in database:")
    for tool in featured_tools:
        print(f"   - {tool['name']}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_featured_tools())
