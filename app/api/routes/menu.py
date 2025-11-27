from typing import Optional, Literal
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy import or_, and_, func, String
from sqlalchemy.orm import Session
from ...db import SessionLocal
from ...models.menu import (
    Menu,
    MenuCreate,
    MenuUpdate,
    MenuResponse,
    MenuListResponse,
    MenuCreateResponse,
    MenuUpdateResponse,
    MenuDeleteResponse,
    MenuGroupByCategoryCount,
    MenuGroupByCategoryList,
)
from ...services.gemini_search import gemini_service
from loguru import logger

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/menu", response_model=MenuCreateResponse, status_code=201)
async def create_menu(menu: MenuCreate):
    """Create a new menu item"""
    try:
        with SessionLocal() as db:
            db_menu = Menu(**menu.model_dump())
            db.add(db_menu)
            db.commit()
            db.refresh(db_menu)
            return MenuCreateResponse(
                message="Menu created successfully",
                data=MenuResponse.model_validate(db_menu)
            )
    except Exception as e:
        logger.exception("Failed to create menu")
        raise HTTPException(status_code=500, detail=f"Failed to create menu: {str(e)}")


@router.get("/menu")
async def list_menu(
    q: Optional[str] = Query(None, description="Search query for name, description, or ingredients"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[str] = Query(None, description="Minimum price"),
    max_price: Optional[str] = Query(None, description="Maximum price"),
    max_cal: Optional[str] = Query(None, description="Maximum calories"),
    page: Optional[str] = Query("1", description="Page number"),
    per_page: Optional[str] = Query("10", description="Items per page"),
    sort: Optional[str] = Query(None, description="Sort by field:order (e.g., price:asc, name:desc)"),
):
    """List all menu items with optional filters and pagination"""
    try:
        # Convert and validate parameters
        q = q.strip() if q and q.strip() else None
        category = category.strip() if category and category.strip() else None
        sort = sort.strip() if sort and sort.strip() else None
        
        # Convert numeric parameters
        min_price_val = None
        max_price_val = None
        max_cal_val = None
        
        if min_price and min_price.strip():
            try:
                min_price_val = float(min_price)
            except ValueError:
                pass
        
        if max_price and max_price.strip():
            try:
                max_price_val = float(max_price)
            except ValueError:
                pass
        
        if max_cal and max_cal.strip():
            try:
                max_cal_val = float(max_cal)
            except ValueError:
                pass
        
        # Parse pagination
        try:
            page_num = int(page) if page and page.strip() else 1
            page_num = max(1, page_num)
        except ValueError:
            page_num = 1
        
        try:
            per_page_num = int(per_page) if per_page and per_page.strip() else 10
            per_page_num = max(1, min(100, per_page_num))
        except ValueError:
            per_page_num = 10
        
        with SessionLocal() as db:
            query = db.query(Menu)
            
            if category:
                query = query.filter(Menu.category == category)
            
            if min_price_val is not None:
                query = query.filter(Menu.price >= min_price_val)
            
            if max_price_val is not None:
                query = query.filter(Menu.price <= max_price_val)
            
            if max_cal_val is not None:
                query = query.filter(Menu.calories <= max_cal_val)
            
            # Apply sorting
            if sort:
                try:
                    field, order = sort.split(":")
                    if hasattr(Menu, field):
                        column = getattr(Menu, field)
                        if order.lower() == "desc":
                            query = query.order_by(column.desc())
                        else:
                            query = query.order_by(column.asc())
                except ValueError:
                    pass  # Invalid sort format, skip sorting
            
            # Get total count
            total = query.count()
            
            # Apply pagination
            offset = (page_num - 1) * per_page_num
            items = query.offset(offset).limit(per_page_num).all()
            
            # Calculate pagination info
            total_pages = (total + per_page_num - 1) // per_page_num
            
            return {
                "data": [MenuResponse.model_validate(item).model_dump() for item in items],
                "pagination": {
                    "total": total,
                    "page": page_num,
                    "per_page": per_page_num,
                    "total_pages": total_pages
                }
            }
    except Exception as e:
        logger.exception("Failed to list menu")
        raise HTTPException(status_code=500, detail=f"Failed to list menu: {str(e)}")


@router.get("/menu/group-by-category")
async def group_by_category(
    mode: Literal["count", "list"] = Query("count", description="Mode: count or list"),
    per_category: int = Query(5, ge=1, le=100, description="Items per category (only for list mode)"),
):
    """Group menu items by category"""
    try:
        with SessionLocal() as db:
            if mode == "count":
                # Return count of items per category
                result = db.query(
                    Menu.category,
                    func.count(Menu.id).label("count")
                ).group_by(Menu.category).all()
                
                data = {row.category: row.count for row in result}
                return {"data": data}
            
            else:  # mode == "list"
                # Return list of items per category
                categories = db.query(Menu.category).distinct().all()
                data = {}
                
                for (cat,) in categories:
                    items = db.query(Menu).filter(Menu.category == cat).limit(per_category).all()
                    data[cat] = [MenuResponse.model_validate(item).model_dump() for item in items]
                
                return {"data": data}
    
    except Exception as e:
        logger.exception("Failed to group by category")
        raise HTTPException(status_code=500, detail=f"Failed to group by category: {str(e)}")


@router.get("/menu/search")
async def search_menu(
    q: str = Query(..., description="Search query"),
    page: Optional[str] = Query("1", description="Page number"),
    per_page: Optional[str] = Query("10", description="Items per page"),
):
    """Search menu items using Gemini AI for natural language queries"""
    try:
        # Parse pagination
        try:
            page_num = int(page) if page and page.strip() else 1
            page_num = max(1, page_num)
        except ValueError:
            page_num = 1
        
        try:
            per_page_num = int(per_page) if per_page and per_page.strip() else 10
            per_page_num = max(1, min(100, per_page_num))
        except ValueError:
            per_page_num = 10
        
        # Get all menu items
        with SessionLocal() as db:
            all_items = db.query(Menu).all()
            menu_items = [MenuResponse.model_validate(item).model_dump() for item in all_items]
        
        # If Gemini is available, use it for semantic search
        if gemini_service.is_available():
            # Parse query with Gemini
            filters = gemini_service.parse_search_query(q, menu_items)
            
            # Apply filters
            filtered_items = gemini_service.filter_menu_items(menu_items, filters)
        else:
            # Fallback to simple keyword search
            q_lower = q.lower()
            filtered_items = [
                item for item in menu_items
                if q_lower in item.get("name", "").lower()
                or q_lower in item.get("description", "").lower()
                or q_lower in " ".join(item.get("ingredients", [])).lower()
            ]
        
        # Apply pagination
        total = len(filtered_items)
        offset = (page_num - 1) * per_page_num
        paginated_items = filtered_items[offset:offset + per_page_num]
        total_pages = (total + per_page_num - 1) // per_page_num
        
        return {
            "data": paginated_items,
            "pagination": {
                "total": total,
                "page": page_num,
                "per_page": per_page_num,
                "total_pages": total_pages
            }
        }
        
    except Exception as e:
        logger.exception("Failed to search menu")
        raise HTTPException(status_code=500, detail=f"Failed to search menu: {str(e)}")


@router.get("/menu/{menu_id}")
async def get_menu(menu_id: int):
    """Get a single menu item by ID"""
    try:
        with SessionLocal() as db:
            menu = db.query(Menu).filter(Menu.id == menu_id).first()
            if not menu:
                return JSONResponse(
                    status_code=404,
                    content={"message": f"Menu with id {menu_id} not found"}
                )
            return {"data": MenuResponse.model_validate(menu).model_dump()}
    except Exception as e:
        logger.exception("Failed to get menu")
        raise HTTPException(status_code=500, detail=f"Failed to get menu: {str(e)}")


@router.put("/menu/{menu_id}", response_model=MenuUpdateResponse)
async def update_menu(menu_id: int, menu: MenuUpdate):
    """Full update of a menu item"""
    try:
        with SessionLocal() as db:
            db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
            if not db_menu:
                raise HTTPException(status_code=404, detail=f"Menu with id {menu_id} not found")
            
            # Update all fields
            for key, value in menu.model_dump().items():
                setattr(db_menu, key, value)
            
            db.commit()
            db.refresh(db_menu)
            
            return MenuUpdateResponse(
                message="Menu updated successfully",
                data=MenuResponse.model_validate(db_menu)
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to update menu")
        raise HTTPException(status_code=500, detail=f"Failed to update menu: {str(e)}")


@router.delete("/menu/{menu_id}", response_model=MenuDeleteResponse)
async def delete_menu(menu_id: int):
    """Delete a menu item"""
    try:
        with SessionLocal() as db:
            db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
            if not db_menu:
                raise HTTPException(status_code=404, detail=f"Menu with id {menu_id} not found")
            
            db.delete(db_menu)
            db.commit()
            
            return MenuDeleteResponse(message=f"Menu with id {menu_id} deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to delete menu")
        raise HTTPException(status_code=500, detail=f"Failed to delete menu: {str(e)}")
