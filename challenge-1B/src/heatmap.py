#!/usr/bin/env python3
"""
Real-time Document Relevance Heat Map Demo
Showcases the new interactive visualization feature for Challenge 1B
"""

from challenge1b_processor import PersonaDrivenDocumentAnalyst
import json

def demo_heatmap_feature():
    """Demonstrate the heat map visualization capabilities"""
    
    print("🔥 REAL-TIME DOCUMENT RELEVANCE HEAT MAP DEMO")
    print("=" * 60)
    
    # Test Case 1: Food Contractor with multiple documents
    print("\n📊 Test Case 1: Food Contractor Analysis")
    print("-" * 40)
    
    food_input = {
        "challenge_info": {
            "challenge_id": "heatmap_demo_001",
            "test_case_name": "food_planning_heatmap",
            "description": "Multi-document food planning with heat map"
        },
        "documents": [
            {"filename": "Breakfast Menu.pdf", "title": "Breakfast Menu"},
            {"filename": "Lunch Options.pdf", "title": "Lunch Options"},
            {"filename": "Dinner Recipes.pdf", "title": "Dinner Recipes"},
            {"filename": "Dietary Guidelines.pdf", "title": "Dietary Guidelines"},
            {"filename": "Buffet Setup.pdf", "title": "Buffet Setup"}
        ],
        "persona": {"role": "Food Contractor"},
        "job_to_be_done": {"task": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."}
    }
    
    analyzer = PersonaDrivenDocumentAnalyst()
    food_result = analyzer.analyze_documents(food_input)
    
    # Heat map visualization data
    print(f"✓ Documents for Heat Map: {len(food_result['metadata']['input_documents'])}")
    print(f"✓ Sections for Visualization: {len(food_result['extracted_sections'])}")
    
    # Show heat map data structure
    print("\n🔥 Heat Map Data Preview:")
    for i, section in enumerate(food_result['extracted_sections'][:3]):
        print(f"  {i+1}. Document: {section['document']}")
        print(f"      Section: {section['section_title']}")
        print(f"      Page: {section['page_number']}")
        print(f"      Rank: {section['importance_rank']}")
        print(f"      Relevance Score: {section.get('relevance_score', 0):.2f}")
    
    # Test Case 2: Travel Planner with different document structure
    print("\n📊 Test Case 2: Travel Planner Analysis")
    print("-" * 40)
    
    travel_input = {
        "challenge_info": {
            "challenge_id": "heatmap_demo_002",
            "test_case_name": "travel_planning_heatmap",
            "description": "Multi-document travel planning with heat map"
        },
        "documents": [
            {"filename": "Destinations Guide.pdf", "title": "Destinations Guide"},
            {"filename": "Budget Travel Tips.pdf", "title": "Budget Travel Tips"},
            {"filename": "Group Activities.pdf", "title": "Group Activities"},
            {"filename": "Accommodation Options.pdf", "title": "Accommodation Options"}
        ],
        "persona": {"role": "Travel Planner"},
        "job_to_be_done": {"task": "Plan a trip of 4 days for a group of 10 college friends"}
    }
    
    travel_result = analyzer.analyze_documents(travel_input)
    
    print(f"✓ Documents for Heat Map: {len(travel_result['metadata']['input_documents'])}")
    print(f"✓ Sections for Visualization: {len(travel_result['extracted_sections'])}")
    
    # Show keyword analysis for heat map
    print("\n🎯 Keyword Analysis for Heat Map:")
    
    # Simulate keyword extraction
    persona_keywords = ["destination", "itinerary", "activities", "accommodation", "transport", "budget"]
    job_keywords = ["trip", "group", "college", "friends", "days", "plan"]
    
    print(f"  Persona Keywords: {', '.join(persona_keywords)}")
    print(f"  Job Keywords: {', '.join(job_keywords)}")
    
    # Heat Map Features Summary
    print("\n🔥 HEAT MAP FEATURES AVAILABLE:")
    print("-" * 40)
    print("✓ Interactive document-by-page relevance visualization")
    print("✓ Color-coded relevance intensity (red scale)")
    print("✓ Hover tooltips with section details")
    print("✓ Section importance bar charts")
    print("✓ Keyword frequency analysis")
    print("✓ Persona-specific insights visualization")
    print("✓ Real-time updates as documents are processed")
    print("✓ Export capabilities for visualizations")
    
    # Web Interface Instructions
    print("\n🌐 WEB INTERFACE USAGE:")
    print("-" * 40)
    print("1. Navigate to Challenge 1B in the web app")
    print("2. Select persona and define job-to-be-done")
    print("3. Upload multiple PDF documents (3-10 recommended)")
    print("4. Click 'Analyze Documents' to process")
    print("5. Switch to '🔥 Relevance Heat Map' tab to view visualization")
    print("6. Explore interactive charts and keyword analysis")
    
    print("\n✅ HEAT MAP FEATURE DEMONSTRATION COMPLETE!")
    print("=" * 60)
    
    return food_result, travel_result

if __name__ == "__main__":
    food_result, travel_result = demo_heatmap_feature()
    
    # Save sample heat map data
    with open("heatmap_food_demo.json", "w") as f:
        json.dump(food_result, f, indent=2)
    
    with open("heatmap_travel_demo.json", "w") as f:
        json.dump(travel_result, f, indent=2)
    
    print(f"\n💾 Heat map demo data saved:")
    print(f"   • heatmap_food_demo.json")
    print(f"   • heatmap_travel_demo.json")