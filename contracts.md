# AI Tools Directory - Backend Integration Contracts

## API Endpoints

### Authentication APIs
- **POST /api/auth/register** - Register new user
  - Input: `{ name, email, password }`
  - Output: `{ user, token }`
  
- **POST /api/auth/login** - User login
  - Input: `{ email, password }`
  - Output: `{ user, token }`
  
- **GET /api/auth/me** - Get current user (requires auth)
  - Headers: `Authorization: Bearer <token>`
  - Output: `{ user }`

### Tools APIs
- **GET /api/tools** - Get all tools with optional filters
  - Query params: `search`, `category`, `pricing`
  - Output: `{ tools: [...] }`
  
- **GET /api/tools/:id** - Get single tool by ID
  - Output: `{ tool }`
  
- **POST /api/tools** - Create new tool (admin only, requires auth)
  - Input: Tool object
  - Output: `{ tool }`
  
- **PUT /api/tools/:id** - Update tool (admin only, requires auth)
  - Input: Tool object
  - Output: `{ tool }`
  
- **DELETE /api/tools/:id** - Delete tool (admin only, requires auth)
  - Output: `{ message }`

### Tool Submissions APIs
- **POST /api/submissions** - Submit a tool for review
  - Input: Tool submission object
  - Output: `{ submission }`
  
- **GET /api/submissions** - Get all submissions (admin only, requires auth)
  - Output: `{ submissions: [...] }`
  
- **PUT /api/submissions/:id/approve** - Approve submission and create tool (admin only)
  - Output: `{ tool }`

### Favorites APIs
- **GET /api/favorites** - Get user's favorite tools (requires auth)
  - Output: `{ favorites: [...] }`
  
- **POST /api/favorites/:toolId** - Add tool to favorites (requires auth)
  - Output: `{ message }`
  
- **DELETE /api/favorites/:toolId** - Remove from favorites (requires auth)
  - Output: `{ message }`

### Categories APIs
- **GET /api/categories** - Get all categories
  - Output: `{ categories: [...] }`

## Database Models

### User
```python
{
  _id: ObjectId,
  name: str,
  email: str,
  password: str (hashed),
  isAdmin: bool,
  createdAt: datetime,
  updatedAt: datetime
}
```

### Tool
```python
{
  _id: ObjectId,
  name: str,
  description: str,
  longDescription: str,
  category: str,
  pricing: str (Free/Paid/Freemium),
  tags: List[str],
  image: str (URL),
  url: str,
  featured: bool,
  createdAt: datetime,
  updatedAt: datetime
}
```

### ToolSubmission
```python
{
  _id: ObjectId,
  name: str,
  description: str,
  longDescription: str,
  category: str,
  pricing: str,
  tags: List[str],
  imageUrl: str,
  url: str,
  submitterEmail: str,
  status: str (pending/approved/rejected),
  createdAt: datetime,
  updatedAt: datetime
}
```

### Favorite
```python
{
  _id: ObjectId,
  userId: ObjectId,
  toolId: ObjectId,
  createdAt: datetime
}
```

## Mock Data to Replace

In `mockData.js`:
- `mockTools` array - Replace with API call to `/api/tools`
- `categories` array - Replace with API call to `/api/categories`
- `featuredTools` - Filter tools where featured=true from API

## Frontend Integration Changes

### Home.jsx
- Replace `mockTools` import with API call to `/api/tools`
- Add loading and error states
- Implement real-time search/filter with API

### ToolDetail.jsx
- Replace `mockTools.find()` with API call to `/api/tools/:id`
- Add loading state

### AdminDashboard.jsx
- Replace local state management with API calls
- Implement real CRUD operations
- Add authentication check

### SubmitTool.jsx
- Replace mock submission with POST to `/api/submissions`

### Profile.jsx
- Fetch user data from `/api/auth/me`
- Fetch favorites from `/api/favorites`
- Implement real favorite toggle functionality

### Login/Signup
- Implement real authentication with JWT tokens
- Store token in localStorage
- Add protected route wrapper

## Authentication Flow

1. User logs in → JWT token returned
2. Token stored in localStorage
3. Protected routes check for token
4. Token sent in Authorization header for protected endpoints
5. Admin routes check isAdmin flag

## Implementation Steps

1. ✅ Create backend models (User, Tool, ToolSubmission, Favorite)
2. ✅ Implement authentication endpoints with JWT
3. ✅ Implement Tools CRUD endpoints
4. ✅ Implement Submissions endpoints
5. ✅ Implement Favorites endpoints
6. ✅ Implement Categories endpoint
7. ✅ Update frontend to use real API calls
8. ✅ Add loading and error handling
9. ✅ Test all functionality
