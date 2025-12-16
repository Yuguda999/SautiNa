import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from services.search_service import search_service

def verify_search_only():
    print("Testing Search Service Only...")
    
    query = "Market price of rice in Lagos Nigeria 2024"
    print(f"Searching for: {query}")
    
    results = search_service.search(query)
    
    if results:
        print("\n[SUCCESS] Search returned results:")
        print(results)
    else:
        print("\n[FAILURE] Search returned no results.")

if __name__ == "__main__":
    verify_search_only()
