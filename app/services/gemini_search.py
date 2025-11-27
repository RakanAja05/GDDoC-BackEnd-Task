import google.generativeai as genai
from typing import List, Dict, Any, Optional
from loguru import logger
from ..core.config import GEMINI_API_KEY


class GeminiSearchService:
    
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
            logger.warning("Gemini API key not configured")
    
    def is_available(self) -> bool:
        return self.model is not None
    
    def parse_search_query(self, query: str, menu_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not self.is_available():
            logger.warning("Gemini API not available, using simple search")
            return self._simple_search(query, menu_items)
        
        try:
            # Create prompt for Gemini
            prompt = f"""Analyze this menu search query and return ONLY a JSON object with these fields:
- category: string or null (valid: "drinks", "food")
- min_price: number or null
- max_price: number or null  
- max_calories: number or null
- keywords: array of strings (for name/description/ingredients matching)

Search query: "{query}"

Example menu data:
{self._get_menu_sample()}

Return ONLY the JSON object, no explanation:"""

            # Call Gemini
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()
            
            # Parse JSON
            import json
            filters = json.loads(result_text)
            
            logger.info(f"Gemini parsed query '{query}' to filters: {filters}")
            return filters
            
        except Exception as e:
            logger.exception(f"Error parsing query with Gemini: {e}")
            return self._simple_search(query, menu_items)
    
    def _simple_search(self, query: str, menu_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "category": None,
            "min_price": None,
            "max_price": None,
            "max_calories": None,
            "keywords": [query.lower()]
        }
    
    def _get_menu_sample(self) -> str:
        return """
- "Es Kopi Susu" (drinks, 180 cal, Rp 25000)
- "Nasi Goreng" (food, 450 cal, Rp 35000)
- "Cappuccino" (drinks, 120 cal, Rp 30000)
"""
    
    def filter_menu_items(self, menu_items: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter menu items based on parsed filters
        """
        results = menu_items
        
        # Filter by category
        if filters.get("category"):
            results = [item for item in results if item.get("category") == filters["category"]]
        
        # Filter by min price
        if filters.get("min_price") is not None:
            results = [item for item in results if item.get("price", 0) >= filters["min_price"]]
        
        # Filter by max price
        if filters.get("max_price") is not None:
            results = [item for item in results if item.get("price", 0) <= filters["max_price"]]
        
        # Filter by max calories
        if filters.get("max_calories") is not None:
            results = [item for item in results if item.get("calories", 0) <= filters["max_calories"]]
        
        # Filter by keywords
        if filters.get("keywords"):
            keywords = [kw.lower() for kw in filters["keywords"]]
            filtered_results = []
            for item in results:
                # Search in name, description, ingredients
                text_to_search = " ".join([
                    item.get("name", "").lower(),
                    item.get("description", "").lower(),
                    " ".join(item.get("ingredients", [])).lower()
                ])
                
                if any(keyword in text_to_search for keyword in keywords):
                    filtered_results.append(item)
            
            results = filtered_results
        
        return results


# Singleton instance
gemini_service = GeminiSearchService()
