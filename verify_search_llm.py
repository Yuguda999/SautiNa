import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from services.llm_service import llm_service
from config import SupportedLanguage

async def verify_search():
    print("Testing Search Integration...")
    
    # Test query that should trigger search
    query = "What is the current price of rice in Lagos today?"
    print(f"\nUser Query: {query}")
    
    response = await llm_service.generate_response(
        user_message=query,
        language=SupportedLanguage.ENGLISH
    )
    
    print(f"\nResponse:\n{response}")
    
    # Simple check if response seems to contain specific data (hard to automate perfectly without mock, but good for manual verify)
    if "price" in response.lower() or "naira" in response.lower():
        print("\n[SUCCESS] Response seems relevant to the price query.")
    else:
        print("\n[WARNING] Response might be generic. Check logs for search execution.")

if __name__ == "__main__":
    asyncio.run(verify_search())
