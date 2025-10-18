#!/usr/bin/env python3
"""
AI Tools Directory Backend API Test Suite
Tests all backend endpoints with realistic data
"""

import requests
import json
import uuid
from datetime import datetime

# Configuration
BASE_URL = "https://discover-ai-4.preview.emergentagent.com/api"
HEADERS = {"Content-Type": "application/json"}

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def log_success(self, test_name):
        print(f"✅ {test_name}")
        self.passed += 1
        
    def log_failure(self, test_name, error):
        print(f"❌ {test_name}: {error}")
        self.failed += 1
        self.errors.append(f"{test_name}: {error}")
        
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"TEST SUMMARY: {self.passed}/{total} passed")
        if self.errors:
            print("\nFAILED TESTS:")
            for error in self.errors:
                print(f"  - {error}")
        print(f"{'='*50}")

def test_auth_endpoints():
    """Test authentication endpoints"""
    results = TestResults()
    
    # Generate unique test data
    test_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    test_password = "SecurePass123!"
    test_name = "John Doe"
    
    print("\n🔐 Testing Authentication Endpoints")
    print("-" * 40)
    
    # Test 1: Register new user
    try:
        register_data = {
            "name": test_name,
            "email": test_email,
            "password": test_password
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", 
                               json=register_data, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            if "user" in data and "token" in data:
                results.log_success("POST /api/auth/register - User registration")
                user_token = data["token"]
                user_id = data["user"]["id"]
            else:
                results.log_failure("POST /api/auth/register", "Missing user or token in response")
                return results
        else:
            results.log_failure("POST /api/auth/register", f"Status {response.status_code}: {response.text}")
            return results
            
    except Exception as e:
        results.log_failure("POST /api/auth/register", f"Request failed: {str(e)}")
        return results
    
    # Test 2: Login with credentials
    try:
        login_data = {
            "email": test_email,
            "password": test_password
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", 
                               json=login_data, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            if "user" in data and "token" in data:
                results.log_success("POST /api/auth/login - User login")
                login_token = data["token"]
            else:
                results.log_failure("POST /api/auth/login", "Missing user or token in response")
        else:
            results.log_failure("POST /api/auth/login", f"Status {response.status_code}: {response.text}")
            
    except Exception as e:
        results.log_failure("POST /api/auth/login", f"Request failed: {str(e)}")
    
    # Test 3: Get current user info
    try:
        auth_headers = {**HEADERS, "Authorization": f"Bearer {user_token}"}
        
        response = requests.get(f"{BASE_URL}/auth/me", headers=auth_headers)
        
        if response.status_code == 200:
            data = response.json()
            if "user" in data and data["user"]["email"] == test_email:
                results.log_success("GET /api/auth/me - Get current user")
            else:
                results.log_failure("GET /api/auth/me", "User data mismatch")
        else:
            results.log_failure("GET /api/auth/me", f"Status {response.status_code}: {response.text}")
            
    except Exception as e:
        results.log_failure("GET /api/auth/me", f"Request failed: {str(e)}")
    
    return results, user_token

def test_tools_endpoints(auth_token=None):
    """Test tools endpoints"""
    results = TestResults()
    
    print("\n🔧 Testing Tools Endpoints")
    print("-" * 40)
    
    # Test 1: Get all tools (no filters)
    try:
        response = requests.get(f"{BASE_URL}/tools", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            if "tools" in data and isinstance(data["tools"], list):
                results.log_success("GET /api/tools - Get all tools")
                tools_list = data["tools"]
            else:
                results.log_failure("GET /api/tools", "Invalid response format")
                tools_list = []
        else:
            results.log_failure("GET /api/tools", f"Status {response.status_code}: {response.text}")
            tools_list = []
            
    except Exception as e:
        results.log_failure("GET /api/tools", f"Request failed: {str(e)}")
        tools_list = []
    
    # Test 2: Get tools with search filter
    try:
        response = requests.get(f"{BASE_URL}/tools?search=AI", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            if "tools" in data:
                results.log_success("GET /api/tools?search=AI - Search tools")
            else:
                results.log_failure("GET /api/tools?search=AI", "Invalid response format")
        else:
            results.log_failure("GET /api/tools?search=AI", f"Status {response.status_code}: {response.text}")
            
    except Exception as e:
        results.log_failure("GET /api/tools?search=AI", f"Request failed: {str(e)}")
    
    # Test 3: Get tools with category filter
    try:
        response = requests.get(f"{BASE_URL}/tools?category=Website Builder", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            if "tools" in data:
                results.log_success("GET /api/tools?category=Website Builder - Filter by category")
            else:
                results.log_failure("GET /api/tools?category=Website Builder", "Invalid response format")
        else:
            results.log_failure("GET /api/tools?category=Website Builder", f"Status {response.status_code}: {response.text}")
            
    except Exception as e:
        results.log_failure("GET /api/tools?category=Website Builder", f"Request failed: {str(e)}")
    
    # Test 4: Get tools with pricing filter
    try:
        response = requests.get(f"{BASE_URL}/tools?pricing=Paid", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            if "tools" in data:
                results.log_success("GET /api/tools?pricing=Paid - Filter by pricing")
            else:
                results.log_failure("GET /api/tools?pricing=Paid", "Invalid response format")
        else:
            results.log_failure("GET /api/tools?pricing=Paid", f"Status {response.status_code}: {response.text}")
            
    except Exception as e:
        results.log_failure("GET /api/tools?pricing=Paid", f"Request failed: {str(e)}")
    
    # Test 5: Get tool by ID (if we have tools)
    if tools_list:
        try:
            tool_id = tools_list[0]["id"]
            response = requests.get(f"{BASE_URL}/tools/{tool_id}", headers=HEADERS)
            
            if response.status_code == 200:
                data = response.json()
                if "tool" in data and data["tool"]["id"] == tool_id:
                    results.log_success(f"GET /api/tools/{tool_id} - Get tool by ID")
                else:
                    results.log_failure("GET /api/tools/{id}", "Tool data mismatch")
            else:
                results.log_failure("GET /api/tools/{id}", f"Status {response.status_code}: {response.text}")
                
        except Exception as e:
            results.log_failure("GET /api/tools/{id}", f"Request failed: {str(e)}")
    else:
        results.log_failure("GET /api/tools/{id}", "No tools available to test")
    
    # Test 6: Get non-existent tool
    try:
        fake_id = str(uuid.uuid4())
        response = requests.get(f"{BASE_URL}/tools/{fake_id}", headers=HEADERS)
        
        if response.status_code == 404:
            results.log_success("GET /api/tools/{fake_id} - Handle non-existent tool")
        else:
            results.log_failure("GET /api/tools/{fake_id}", f"Expected 404, got {response.status_code}")
            
    except Exception as e:
        results.log_failure("GET /api/tools/{fake_id}", f"Request failed: {str(e)}")
    
    # Admin-only endpoints (POST, PUT, DELETE) - Skip if no admin token
    if auth_token:
        print("\nNote: Skipping admin-only endpoints (POST, PUT, DELETE) - requires admin privileges")
    
    return results

def test_submissions_endpoint():
    """Test submissions endpoint"""
    results = TestResults()
    
    print("\n📝 Testing Submissions Endpoint")
    print("-" * 40)
    
    # Test: Create new submission
    try:
        submission_data = {
            "name": "TestAI Pro",
            "description": "Advanced AI tool for productivity and automation",
            "longDescription": "TestAI Pro is a comprehensive AI-powered platform that helps businesses automate their workflows, generate content, and improve productivity. Features include natural language processing, automated reporting, and intelligent task management.",
            "category": "Productivity",
            "pricing": "Freemium",
            "tags": "AI, Productivity, Automation, NLP",
            "imageUrl": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=500&h=300&fit=crop",
            "url": "https://testai-pro.com",
            "submitterEmail": "developer@testai-pro.com"
        }
        
        response = requests.post(f"{BASE_URL}/submissions", 
                               json=submission_data, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            if "submission" in data and data["submission"]["name"] == submission_data["name"]:
                results.log_success("POST /api/submissions - Create tool submission")
            else:
                results.log_failure("POST /api/submissions", "Submission data mismatch")
        else:
            results.log_failure("POST /api/submissions", f"Status {response.status_code}: {response.text}")
            
    except Exception as e:
        results.log_failure("POST /api/submissions", f"Request failed: {str(e)}")
    
    return results

def test_categories_endpoint():
    """Test categories endpoint"""
    results = TestResults()
    
    print("\n📂 Testing Categories Endpoint")
    print("-" * 40)
    
    # Test: Get all categories
    try:
        response = requests.get(f"{BASE_URL}/categories", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            if "categories" in data and isinstance(data["categories"], list) and len(data["categories"]) > 0:
                results.log_success("GET /api/categories - Get all categories")
                print(f"  Found {len(data['categories'])} categories")
            else:
                results.log_failure("GET /api/categories", "Invalid categories format or empty list")
        else:
            results.log_failure("GET /api/categories", f"Status {response.status_code}: {response.text}")
            
    except Exception as e:
        results.log_failure("GET /api/categories", f"Request failed: {str(e)}")
    
    return results

def test_seed_endpoint():
    """Test seed data endpoint"""
    results = TestResults()
    
    print("\n🌱 Testing Seed Data Endpoint")
    print("-" * 40)
    
    # Test: Seed initial data
    try:
        response = requests.post(f"{BASE_URL}/seed", headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            if "message" in data:
                results.log_success("POST /api/seed - Seed initial data")
                print(f"  {data['message']}")
            else:
                results.log_failure("POST /api/seed", "Invalid response format")
        else:
            results.log_failure("POST /api/seed", f"Status {response.status_code}: {response.text}")
            
    except Exception as e:
        results.log_failure("POST /api/seed", f"Request failed: {str(e)}")
    
    return results

def main():
    """Run all backend API tests"""
    print("🚀 AI Tools Directory Backend API Test Suite")
    print("=" * 50)
    print(f"Testing against: {BASE_URL}")
    
    all_results = TestResults()
    
    # Test 1: Seed data first
    seed_results = test_seed_endpoint()
    all_results.passed += seed_results.passed
    all_results.failed += seed_results.failed
    all_results.errors.extend(seed_results.errors)
    
    # Test 2: Authentication
    auth_results, user_token = test_auth_endpoints()
    all_results.passed += auth_results.passed
    all_results.failed += auth_results.failed
    all_results.errors.extend(auth_results.errors)
    
    # Test 3: Tools endpoints
    tools_results = test_tools_endpoints(user_token)
    all_results.passed += tools_results.passed
    all_results.failed += tools_results.failed
    all_results.errors.extend(tools_results.errors)
    
    # Test 4: Submissions
    submissions_results = test_submissions_endpoint()
    all_results.passed += submissions_results.passed
    all_results.failed += submissions_results.failed
    all_results.errors.extend(submissions_results.errors)
    
    # Test 5: Categories
    categories_results = test_categories_endpoint()
    all_results.passed += categories_results.passed
    all_results.failed += categories_results.failed
    all_results.errors.extend(categories_results.errors)
    
    # Final summary
    all_results.summary()
    
    return all_results.failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)