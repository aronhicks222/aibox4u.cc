from fastapi import FastAPI, APIRouter, HTTPException, Depends, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import timedelta

from models import (
    User, UserCreate, UserLogin, UserInDB,
    Tool, ToolCreate, ToolUpdate,
    ToolSubmission, ToolSubmissionCreate,
    Favorite
)
from auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user, get_current_admin_user
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== AUTH ROUTES ====================

@api_router.post("/auth/register")
async def register(user_data: UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user_dict = user_data.dict()
    user_dict["password"] = get_password_hash(user_data.password)
    user = UserInDB(**user_dict)
    
    await db.users.insert_one(user.dict())
    
    # Create token
    token = create_access_token(data={"sub": user.email, "userId": user.id, "isAdmin": user.isAdmin})
    
    return {
        "user": {"id": user.id, "name": user.name, "email": user.email, "isAdmin": user.isAdmin},
        "token": token
    }

@api_router.post("/auth/login")
async def login(credentials: UserLogin):
    user = await db.users.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token(data={"sub": user["email"], "userId": user["id"], "isAdmin": user.get("isAdmin", False)})
    
    return {
        "user": {"id": user["id"], "name": user["name"], "email": user["email"], "isAdmin": user.get("isAdmin", False)},
        "token": token
    }

@api_router.get("/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    user = await db.users.find_one({"email": current_user["sub"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"user": {"id": user["id"], "name": user["name"], "email": user["email"], "isAdmin": user.get("isAdmin", False)}}

# ==================== TOOLS ROUTES ====================

@api_router.get("/tools")
async def get_tools(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    pricing: Optional[str] = Query(None)
):
    query = {}
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"tags": {"$regex": search, "$options": "i"}}
        ]
    
    if category and category != "All":
        query["category"] = category
    
    if pricing and pricing != "All":
        query["pricing"] = pricing
    
    tools = await db.tools.find(query, {"_id": 0}).sort("name", 1).to_list(1000)
    return {"tools": tools}

@api_router.get("/tools/{tool_id}")
async def get_tool(tool_id: str):
    tool = await db.tools.find_one({"id": tool_id}, {"_id": 0})
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"tool": tool}

@api_router.post("/tools")
async def create_tool(tool_data: ToolCreate, current_user: dict = Depends(get_current_admin_user)):
    tool = Tool(**tool_data.dict())
    await db.tools.insert_one(tool.dict())
    return {"tool": tool}

@api_router.put("/tools/{tool_id}")
async def update_tool(tool_id: str, tool_data: ToolUpdate, current_user: dict = Depends(get_current_admin_user)):
    tool = await db.tools.find_one({"id": tool_id})
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    update_data = {k: v for k, v in tool_data.dict().items() if v is not None}
    if update_data:
        await db.tools.update_one({"id": tool_id}, {"$set": update_data})
    
    updated_tool = await db.tools.find_one({"id": tool_id})
    return {"tool": updated_tool}

@api_router.delete("/tools/{tool_id}")
async def delete_tool(tool_id: str, current_user: dict = Depends(get_current_admin_user)):
    result = await db.tools.delete_one({"id": tool_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"message": "Tool deleted successfully"}

# ==================== SUBMISSIONS ROUTES ====================

@api_router.post("/submissions")
async def create_submission(submission_data: ToolSubmissionCreate):
    tags_list = [tag.strip() for tag in submission_data.tags.split(',')]
    
    submission = ToolSubmission(
        name=submission_data.name,
        description=submission_data.description,
        longDescription=submission_data.longDescription,
        category=submission_data.category,
        pricing=submission_data.pricing,
        tags=tags_list,
        imageUrl=submission_data.imageUrl,
        url=submission_data.url,
        submitterEmail=submission_data.submitterEmail
    )
    
    await db.submissions.insert_one(submission.dict())
    return {"submission": submission}

@api_router.get("/submissions")
async def get_submissions(current_user: dict = Depends(get_current_admin_user)):
    submissions = await db.submissions.find().to_list(1000)
    return {"submissions": submissions}

@api_router.put("/submissions/{submission_id}/approve")
async def approve_submission(submission_id: str, current_user: dict = Depends(get_current_admin_user)):
    submission = await db.submissions.find_one({"id": submission_id})
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Create tool from submission
    tool = Tool(
        name=submission["name"],
        description=submission["description"],
        longDescription=submission["longDescription"],
        category=submission["category"],
        pricing=submission["pricing"],
        tags=submission["tags"],
        image=submission["imageUrl"],
        url=submission["url"],
        featured=False
    )
    
    await db.tools.insert_one(tool.dict())
    await db.submissions.update_one({"id": submission_id}, {"$set": {"status": "approved"}})
    
    return {"tool": tool}

# ==================== FAVORITES ROUTES ====================

@api_router.get("/favorites")
async def get_favorites(current_user: dict = Depends(get_current_user)):
    user_id = current_user["userId"]
    favorites = await db.favorites.find({"userId": user_id}).to_list(1000)
    
    # Get tool details for each favorite
    tool_ids = [fav["toolId"] for fav in favorites]
    tools = await db.tools.find({"id": {"$in": tool_ids}}).to_list(1000)
    
    return {"favorites": tools}

@api_router.post("/favorites/{tool_id}")
async def add_favorite(tool_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["userId"]
    
    # Check if already favorited
    existing = await db.favorites.find_one({"userId": user_id, "toolId": tool_id})
    if existing:
        return {"message": "Already in favorites"}
    
    favorite = Favorite(userId=user_id, toolId=tool_id)
    await db.favorites.insert_one(favorite.dict())
    
    return {"message": "Added to favorites"}

@api_router.delete("/favorites/{tool_id}")
async def remove_favorite(tool_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["userId"]
    result = await db.favorites.delete_one({"userId": user_id, "toolId": tool_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    return {"message": "Removed from favorites"}

# ==================== CATEGORIES ROUTE ====================

@api_router.get("/categories")
async def get_categories():
    categories = [
        'All', 'Website Builder', 'Advertising', 'Education',
        'Productivity', 'NoCode', 'Video Generation', 'Automation',
        'AI Detection', 'Text-to-Video', 'Marketing', 'Writing',
        'Image Generation', 'Audio', 'Code Assistant'
    ]
    return {"categories": categories}

# ==================== SEED DATA ROUTE ====================

@api_router.post("/seed")
async def seed_data():
    # Check if data already exists
    existing_tools = await db.tools.count_documents({})
    if existing_tools > 0:
        return {"message": "Data already seeded"}
    
    # Seed tools from mockData
    from datetime import datetime
    import uuid
    
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
        }
    ]
    
    await db.tools.insert_many(mock_tools)
    
    return {"message": f"Seeded {len(mock_tools)} tools successfully"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()