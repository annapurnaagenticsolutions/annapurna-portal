"""
Project 07: The Structured Output Enforcer

Hidden Gem: `pydantic` — runtime type validation that turns raw dicts
into validated, typed Python objects with helpful error messages.

What it does: Demonstrates how to parse unstructured data (simulated LLM output)
into strictly typed, validated objects using Pydantic models.
"""
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional
from datetime import datetime
import json


class PersonProfile(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    role: str = Field(..., description="Job role")
    skills: list[str] = Field(default_factory=list, max_length=20)
    active: bool = True
    joined_at: Optional[datetime] = None

    @field_validator('name')
    @classmethod
    def name_must_be_capitalized(cls, v):
        if not v[0].isupper():
            raise ValueError("Name must start with a capital letter")
        return v.strip()


class ApiResponse(BaseModel):
    success: bool
    profile: PersonProfile
    message: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)


def simulate_llm_output():
    """Simulate raw LLM JSON output (potentially messy)."""
    return {
        "success": True,
        "profile": {
            "name": "Alice Chen",
            "age": 28,
            "email": "alice.chen@example.com",
            "role": "Backend Engineer",
            "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
            "active": True,
            "joined_at": "2024-01-15T09:30:00",
        },
        "message": "Profile extracted successfully",
    }


def simulate_bad_output():
    """Simulate invalid data to show validation in action."""
    return {
        "success": True,
        "profile": {
            "name": "",  # Empty name — should fail
            "age": 200,  # Too old — should fail
            "email": "not-an-email",  # Invalid email — should fail
            "role": "Engineer",
            "skills": ["Python"],
        },
        "message": "This should fail validation",
    }


def main():
    print("--- Structured Output Enforcer ---")
    print("Demonstrating Pydantic validation on simulated LLM output\n")

    # Test 1: Valid data
    print("Test 1: Valid LLM output")
    raw = simulate_llm_output()
    print(f"Raw input: {json.dumps(raw, indent=2)[:200]}...")

    try:
        response = ApiResponse(**raw)
        print(f"✓ Validated successfully!")
        print(f"  Name: {response.profile.name}")
        print(f"  Age: {response.profile.age}")
        print(f"  Email: {response.profile.email}")
        print(f"  Skills: {', '.join(response.profile.skills)}")
        print(f"  Joined: {response.profile.joined_at}")
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")

    print()

    # Test 2: Invalid data
    print("Test 2: Invalid LLM output (should fail gracefully)")
    raw = simulate_bad_output()

    try:
        response = ApiResponse(**raw)
        print(f"Unexpectedly passed: {response}")
    except ValidationError as e:
        print(f"✓ Caught {len(e.errors())} validation errors:")
        for err in e.errors():
            loc = " → ".join(str(x) for x in err['loc'])
            print(f"  • {loc}: {err['msg']}")


if __name__ == "__main__":
    main()
