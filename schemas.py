"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Concrete industry inquiries submitted from the website
class Inquiry(BaseModel):
    """
    Inquiries collection schema
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Contact person name")
    email: EmailStr = Field(..., description="Email for follow-up")
    phone: Optional[str] = Field(None, description="Phone or WhatsApp number")
    company: Optional[str] = Field(None, description="Company name")
    service_interest: Optional[str] = Field(None, description="Primary service of interest")
    message: str = Field(..., description="Inquiry details")
    preferred_contact: Optional[str] = Field("email", description="Preferred contact method: email | phone | whatsapp")
    source: Optional[str] = Field("website", description="Lead source")
