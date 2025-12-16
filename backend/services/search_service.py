"""
Tavily Search Service
Uses Tavily AI-optimized search with DuckDuckGo fallback.
"""
import logging
from typing import Optional

from config import settings

logger = logging.getLogger(__name__)

# Try to import tavily, fallback to DuckDuckGo if not available
try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False
    logger.warning("Tavily not installed. Using DuckDuckGo as fallback.")

try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    logger.warning("DuckDuckGo search not available.")


class SearchService:
    """Unified search service with Tavily primary and DuckDuckGo fallback"""
    
    def __init__(self):
        self.tavily_client = None
        self.ddgs_client = None
        
        # Initialize Tavily if available and configured
        if TAVILY_AVAILABLE and settings.tavily_api_key and settings.use_tavily:
            try:
                self.tavily_client = TavilyClient(api_key=settings.tavily_api_key)
                logger.info("✅ Tavily search initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Tavily: {e}")
        
        # Initialize DuckDuckGo as fallback
        if DDGS_AVAILABLE:
            try:
                self.ddgs_client = DDGS()
                logger.info("✅ DuckDuckGo search initialized (fallback)")
            except Exception as e:
                logger.error(f"Failed to initialize DuckDuckGo: {e}")
    
    def search(self, query: str, max_results: int = 5) -> str:
        """
        Perform a web search and return formatted results.
        Uses Tavily if available, falls back to DuckDuckGo.
        
        Args:
            query: The search query
            max_results: Maximum number of results
            
        Returns:
            Formatted string of search results
        """
        # Try Tavily first
        if self.tavily_client:
            result = self._search_tavily(query, max_results)
            if result:
                return result
        
        # Fall back to DuckDuckGo
        if self.ddgs_client:
            result = self._search_ddgs(query, max_results)
            if result:
                return result
        
        logger.warning("No search provider available")
        return ""
    
    def _search_tavily(self, query: str, max_results: int) -> str:
        """Search using Tavily AI-optimized search"""
        try:
            logger.info(f"🔍 Tavily search: {query}")
            
            response = self.tavily_client.search(
                query=query,
                search_depth="basic",
                max_results=max_results,
                include_answer=True,  # Get AI-generated answer
            )
            
            # Format results
            formatted = "Web Search Results:\n\n"
            
            # Include AI answer if available
            if response.get("answer"):
                formatted += f"Summary: {response['answer']}\n\n"
            
            # Include individual results
            for i, result in enumerate(response.get("results", [])[:max_results], 1):
                title = result.get("title", "No title")
                content = result.get("content", "")[:300]
                formatted += f"{i}. {title}: {content}\n\n"
            
            logger.info(f"Tavily returned {len(response.get('results', []))} results")
            return formatted
            
        except Exception as e:
            logger.error(f"Tavily search error: {e}")
            return ""
    
    def _search_ddgs(self, query: str, max_results: int) -> str:
        """Search using DuckDuckGo (fallback)"""
        try:
            logger.info(f"🦆 DuckDuckGo search: {query}")
            
            results = self.ddgs_client.text(query, max_results=max_results)
            
            if not results:
                return ""
            
            formatted = "Web Search Results:\n\n"
            for i, result in enumerate(results, 1):
                formatted += f"{i}. {result['title']}: {result['body']}\n\n"
            
            logger.info(f"DuckDuckGo returned {len(results)} results")
            return formatted
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
            return ""


# Singleton instance
search_service = SearchService()
