"""
Script to test database connection and create sample menu data
"""
import sys
sys.path.insert(0, 'app')

from db import SessionLocal, engine, Base
from models.menu import Menu
from datetime import datetime


def test_connection():
    """Test database connection"""
    try:
        from sqlalchemy import text
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def create_tables():
    """Create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False


def insert_sample_data():
    """Insert sample menu data"""
    sample_menus = [
        {
            "name": "Es Kopi Susu",
            "category": "drinks",
            "calories": 180,
            "price": 25000.00,
            "ingredients": ["coffee", "milk", "ice", "sugar"],
            "description": "Classic iced coffee with milk"
        },
        {
            "name": "Nasi Goreng",
            "category": "food",
            "calories": 450,
            "price": 35000.00,
            "ingredients": ["rice", "egg", "chicken", "vegetables", "soy_sauce"],
            "description": "Indonesian fried rice with chicken"
        },
        {
            "name": "Cappuccino",
            "category": "drinks",
            "calories": 120,
            "price": 30000.00,
            "ingredients": ["espresso", "steamed_milk", "milk_foam"],
            "description": "Classic Italian coffee with steamed milk"
        },
        {
            "name": "Salad Caesar",
            "category": "food",
            "calories": 280,
            "price": 45000.00,
            "ingredients": ["lettuce", "chicken", "croutons", "parmesan", "caesar_dressing"],
            "description": "Fresh Caesar salad with grilled chicken"
        },
        {
            "name": "Jus Jeruk",
            "category": "drinks",
            "calories": 110,
            "price": 20000.00,
            "ingredients": ["orange", "water", "sugar"],
            "description": "Fresh orange juice"
        },
        {
            "name": "Mie Goreng",
            "category": "food",
            "calories": 420,
            "price": 32000.00,
            "ingredients": ["noodles", "vegetables", "egg", "soy_sauce", "chili"],
            "description": "Indonesian fried noodles"
        },
        {
            "name": "Green Tea Latte",
            "category": "drinks",
            "calories": 150,
            "price": 28000.00,
            "ingredients": ["green_tea", "milk", "sugar"],
            "description": "Japanese green tea with milk"
        },
        {
            "name": "Sandwich Club",
            "category": "food",
            "calories": 380,
            "price": 40000.00,
            "ingredients": ["bread", "chicken", "bacon", "lettuce", "tomato", "mayonnaise"],
            "description": "Classic club sandwich"
        },
    ]
    
    try:
        with SessionLocal() as db:
            # Check if data already exists
            existing_count = db.query(Menu).count()
            if existing_count > 0:
                print(f"ℹ️  Database already has {existing_count} menu items. Skipping sample data.")
                return True
            
            # Insert sample data
            for menu_data in sample_menus:
                menu = Menu(**menu_data)
                db.add(menu)
            
            db.commit()
            print(f"✅ Inserted {len(sample_menus)} sample menu items!")
            return True
    except Exception as e:
        print(f"❌ Failed to insert sample data: {e}")
        return False


def main():
    print("=" * 50)
    print("Database Setup & Test Script")
    print("=" * 50)
    print()
    
    print("1. Testing database connection...")
    if not test_connection():
        print("\n❌ Setup failed. Please check your DATABASE_URL in .env file")
        return
    
    print("\n2. Creating tables...")
    if not create_tables():
        print("\n❌ Setup failed. Could not create tables")
        return
    
    print("\n3. Inserting sample data...")
    if not insert_sample_data():
        print("\n⚠️  Warning: Could not insert sample data, but tables are ready")
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("=" * 50)
    print("\nYou can now start the application:")
    print("  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080")
    print("\nAPI Documentation:")
    print("  http://localhost:8080/docs")


if __name__ == "__main__":
    main()
