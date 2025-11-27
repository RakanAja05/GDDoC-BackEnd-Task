"""
Test file for Menu API endpoints
Run with: pytest tests/test_menu_api.py -v
"""
import sys
sys.path.insert(0, 'app')

import pytest
from fastapi.testclient import TestClient
from app.main import app
from db import SessionLocal, Base, engine
from models.menu import Menu

client = TestClient(app)

# Sample menu data
SAMPLE_MENU = {
    "name": "Test Coffee",
    "category": "drinks",
    "calories": 150,
    "price": 25000,
    "ingredients": ["coffee", "milk", "sugar"],
    "description": "Test coffee for testing"
}


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Setup test database"""
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup after tests
    Base.metadata.drop_all(bind=engine)


def test_create_menu():
    """Test POST /api/menu"""
    response = client.post("/api/menu", json=SAMPLE_MENU)
    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert "data" in data
    assert data["data"]["name"] == SAMPLE_MENU["name"]
    assert data["data"]["category"] == SAMPLE_MENU["category"]
    assert "id" in data["data"]
    assert "created_at" in data["data"]


def test_list_menu():
    """Test GET /api/menu"""
    response = client.get("/api/menu")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert "pagination" in data


def test_list_menu_with_filters():
    """Test GET /api/menu with filters"""
    response = client.get("/api/menu?category=drinks&max_price=30000&page=1&per_page=5")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "pagination" in data
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["per_page"] == 5


def test_get_menu_by_id():
    """Test GET /api/menu/{id}"""
    # Create a menu first
    create_response = client.post("/api/menu", json=SAMPLE_MENU)
    menu_id = create_response.json()["data"]["id"]
    
    # Get menu by ID
    response = client.get(f"/api/menu/{menu_id}")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["id"] == menu_id


def test_get_menu_not_found():
    """Test GET /api/menu/{id} with invalid ID"""
    response = client.get("/api/menu/99999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_update_menu():
    """Test PUT /api/menu/{id}"""
    # Create a menu first
    create_response = client.post("/api/menu", json=SAMPLE_MENU)
    menu_id = create_response.json()["data"]["id"]
    
    # Update menu
    updated_data = SAMPLE_MENU.copy()
    updated_data["name"] = "Updated Coffee"
    updated_data["price"] = 30000
    
    response = client.put(f"/api/menu/{menu_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["data"]["name"] == "Updated Coffee"
    assert data["data"]["price"] == 30000


def test_delete_menu():
    """Test DELETE /api/menu/{id}"""
    # Create a menu first
    create_response = client.post("/api/menu", json=SAMPLE_MENU)
    menu_id = create_response.json()["data"]["id"]
    
    # Delete menu
    response = client.delete(f"/api/menu/{menu_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Verify deletion
    get_response = client.get(f"/api/menu/{menu_id}")
    assert get_response.status_code == 404


def test_group_by_category_count():
    """Test GET /api/menu/group-by-category?mode=count"""
    response = client.get("/api/menu/group-by-category?mode=count")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], dict)


def test_group_by_category_list():
    """Test GET /api/menu/group-by-category?mode=list"""
    response = client.get("/api/menu/group-by-category?mode=list&per_category=5")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], dict)


def test_search_menu():
    """Test GET /api/menu/search"""
    # Create a menu with specific name
    search_menu = SAMPLE_MENU.copy()
    search_menu["name"] = "Unique Search Coffee"
    client.post("/api/menu", json=search_menu)
    
    # Search for it
    response = client.get("/api/menu/search?q=Unique")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0


def test_search_with_pagination():
    """Test search with pagination"""
    response = client.get("/api/menu/search?q=coffee&page=1&per_page=3")
    assert response.status_code == 200
    data = response.json()
    assert "pagination" in data
    assert data["pagination"]["per_page"] == 3


def test_sort_menu():
    """Test sorting"""
    response = client.get("/api/menu?sort=price:asc")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    
    # Check if sorted
    if len(data["data"]) > 1:
        prices = [item["price"] for item in data["data"]]
        assert prices == sorted(prices)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
