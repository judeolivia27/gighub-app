# main.py
# Admission Number: C027-01-1352/2024
# Categories: "Development", "Design", "Writing"
# Currency: USD
# Number of initial gigs: 7

from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

app = FastAPI(
    title="GigHub API",
    description="A backend API for managing freelance gig listings in Nairobi",
    version="1.0.0"
)

# ---------------------------------------------------------
# CONSTANTS & IN-MEMORY DATABASE
# ---------------------------------------------------------

ALLOWED_CATEGORIES = {"Development", "Design", "Writing"}
CURRENCY = "USD"

# 7 initial gigs generated based on the admission number rules
gigs_db = [
    {
        "id": 1,
        "title": "Build a React Dashboard",
        "description": "Build a responsive React dashboard for an e-commerce platform.",
        "category": "Development",
        "budget": 1200.0,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": "Jane Muthoni"
    },
    {
        "id": 2,
        "title": "Logo Design for Fintech Startup",
        "description": "Create a clean, modern minimalist logo design package for a brand new fintech startup.",
        "category": "Design",
        "budget": 350.0,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": "David Otieno"
    },
    {
        "id": 3,
        "title": "Technical Article Writing",
        "description": "Write three deep-dive technical blog posts about FastAPI and Pydantic validation.",
        "category": "Writing",
        "budget": 450.0,
        "currency": CURRENCY,
        "status": "In Progress",
        "client_name": "Alice Kamau"
    },
    {
        "id": 4,
        "title": "Develop REST API with Django",
        "description": "Develop a highly scalable secure REST API utilizing Django REST Framework.",
        "category": "Development",
        "budget": 1800.0,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": "John Ndwiga"
    },
    {
        "id": 5,
        "title": "UI/UX Mobile App Screens",
        "description": "Figma UI/UX high fidelity prototype screens design for a food delivery mobile application.",
        "category": "Design",
        "budget": 950.0,
        "currency": CURRENCY,
        "status": "Closed",
        "client_name": "Mercy Mwangi"
    },
    {
        "id": 6,
        "title": "Copywriting for Landing Page",
        "description": "High-converting sales copywriting for an upcoming SaaS landing page launch.",
        "category": "Writing",
        "budget": 200.0,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": "Peter Kiprop"
    },
    {
        "id": 7,
        "title": "E-Commerce Website Deployment",
        "description": "Deploy an existing WooCommerce website onto an AWS EC2 instance with custom configuration.",
        "category": "Development",
        "budget": 600.0,
        "currency": CURRENCY,
        "status": "In Progress",
        "client_name": "Sarah Hassan"
    }
]


# ---------------------------------------------------------
# PYDANTIC VALIDATION MODELS
# ---------------------------------------------------------

class GigCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100, description="Title of the gig")
    description: str = Field(min_length=20, max_length=500, description="Detailed description of the gig")
    category: str = Field(description="Must be 'Development', 'Design', or 'Writing'")
    budget: float = Field(gt=0, description="Budget must be greater than zero")
    client_name: str = Field(min_length=2, max_length=50, description="Name of the client posting the gig")

    # Custom validator to restrict categories
    @field_validator('category')
    @classmethod
    def validate_category(cls, value: str) -> str:
        if value not in ALLOWED_CATEGORIES:
            raise ValueError(f"Category must be one of: {list(ALLOWED_CATEGORIES)}")
        return value


class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0, description="New budget (must be greater than zero)")
    status: Optional[str] = Field(None, description="Must be 'Open', 'In Progress', or 'Closed'")

    # Custom validator to restrict status options
    @field_validator('status')
    @classmethod
    def validate_status(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and value not in {"Open", "In Progress", "Closed"}:
            raise ValueError("Status must be one of: 'Open', 'In Progress', 'Closed'")
        return value


# ---------------------------------------------------------
# API ENDPOINTS (ROUTES)
# ---------------------------------------------------------

# 1. GET /gigs - Retrieve all gigs with optional filtering
@app.get("/gigs", tags=["Gigs"])
def get_gigs(
    category: Optional[str] = Query(None, description="Filter by category"),
    min_budget: Optional[float] = Query(None, gt=0, description="Minimum budget filter"),
    max_budget: Optional[float] = Query(None, gt=0, description="Maximum budget filter")
):
    results = gigs_db
    
    # Apply category filter if provided
    if category:
        results = [g for g in results if g["category"].lower() == category.lower()]
        
    # Apply minimum budget filter if provided
    if min_budget is not None:
        results = [g for g in results if g["budget"] >= min_budget]
        
    # Apply maximum budget filter if provided
    if max_budget is not None:
        results = [g for g in results if g["budget"] <= max_budget]
        
    return results


# 2. GET /gigs/search - Search gigs by title (Query parameter)
@app.get("/gigs/search", tags=["Gigs"])
def search_gigs(q: str = Query(..., min_length=1, description="Search term for the gig title")):
    results = []
    for gig in gigs_db:
        if q.lower() in gig["title"].lower():
            results.append(gig)
    return results


# 3. GET /gigs/{gig_id} - Retrieve a specific gig by its ID
@app.get("/gigs/{gig_id}", tags=["Gigs"])
def get_gig_by_id(gig_id: int = Path(..., description="The ID of the gig to retrieve")):
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig
    raise HTTPException(status_code=404, detail="Gig not found")


# 4. POST /gigs - Create a new gig
@app.post("/gigs", status_code=210, tags=["Gigs"])  # Created status
def create_gig(gig: GigCreate):
    # Auto-incrementing ID generation
    new_id = max([g["id"] for g in gigs_db]) + 1 if gigs_db else 1
    
    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": CURRENCY,      # Enforced currency based on admission number rules
        "status": "Open",          # Default status for any newly created gig
        "client_name": gig.client_name
    }
    
    gigs_db.append(new_gig)
    return {"message": "Gig created successfully", "gig": new_gig}


# 5. PUT /gigs/{gig_id} - Update an existing gig's budget or status
@app.put("/gigs/{gig_id}", tags=["Gigs"])
def update_gig(
    gig_id: int = Path(..., description="The ID of the gig to update"),
    gig_update: GigUpdate = ...
):
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            # Update only fields that were provided in the request
            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget
            if gig_update.status is not None:
                gigs_db[index]["status"] = gig_update.status
                
            return {"message": "Gig updated successfully", "gig": gigs_db[index]}
            
    raise HTTPException(status_code=404, detail="Gig not found")


# 6. DELETE /gigs/{gig_id} - Remove a gig from the database
@app.delete("/gigs/{gig_id}", tags=["Gigs"])
def delete_gig(gig_id: int = Path(..., description="The ID of the gig to delete")):
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            deleted_gig = gigs_db.pop(index)
            return {"message": "Gig deleted successfully", "deleted_gig": deleted_gig}
            
    raise HTTPException(status_code=404, detail="Gig not found")