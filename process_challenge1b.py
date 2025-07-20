#!/usr/bin/env python3
"""
Adobe Hackathon Challenge 1B - Command Line Processor
Processes multiple PDFs for persona-driven document intelligence
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from challenge1b_processor import PersonaDrivenDocumentAnalyst
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_challenge1b_input(input_file_path: str) -> dict:
    """
    Process Challenge 1B input from JSON file
    
    Args:
        input_file_path: Path to input JSON file containing challenge data
        
    Returns:
        Dictionary containing analysis results
    """
    
    # Read input configuration
    try:
        with open(input_file_path, 'r') as f:
            input_data = json.load(f)
        
        logger.info(f"Loaded input configuration: {len(input_data.get('documents', []))} documents")
        
    except Exception as e:
        logger.error(f"Error reading input file {input_file_path}: {str(e)}")
        raise
    
    # Initialize analyzer
    analyzer = PersonaDrivenDocumentAnalyst()
    
    # Process documents
    start_time = time.time()
    result = analyzer.analyze_documents(input_data)
    processing_time = time.time() - start_time
    
    logger.info(f"Challenge 1B processing completed in {processing_time:.2f}s")
    
    return result

def main():
    """Main function for Challenge 1B command line processing"""
    
    # Directory paths for challenge environment
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # For local testing, use current directory structure
    if not input_dir.exists():
        input_dir = Path(".")
        output_dir = Path("./output")
    
    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)
    
    # Look for input configuration file
    input_config_path = input_dir / "challenge1b_input.json"
    if not input_config_path.exists():
        # Create sample input if none exists
        sample_input = {
            "challenge_info": {
                "challenge_id": "round_1b_001",
                "test_case_name": "document_analysis",
                "description": "Persona-driven document intelligence"
            },
            "documents": [
                {"filename": "file01.pdf", "title": "Document 1"},
                {"filename": "file02.pdf", "title": "Document 2"},
                {"filename": "file03.pdf", "title": "Document 3"}
            ],
            "persona": {
                "role": "Food Contractor"
            },
            "job_to_be_done": {
                "task": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."
            }
        }
        
        with open(input_config_path, 'w') as f:
            json.dump(sample_input, f, indent=2)
        
        logger.info(f"Created sample input configuration at {input_config_path}")
    
    try:
        # Process the challenge
        result = process_challenge1b_input(str(input_config_path))
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"challenge1b_result_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        logger.info(f"Results saved to {output_file}")
        
        # Print summary
        metadata = result.get("metadata", {})
        sections = result.get("extracted_sections", [])
        
        print("\n" + "="*60)
        print("CHALLENGE 1B - PERSONA-DRIVEN DOCUMENT INTELLIGENCE")
        print("="*60)
        print(f"Persona: {metadata.get('persona', 'Unknown')}")
        print(f"Job to be Done: {metadata.get('job_to_be_done', 'Unknown')}")
        print(f"Documents Processed: {len(metadata.get('input_documents', []))}")
        print(f"Relevant Sections Found: {len(sections)}")
        print(f"Processing Time: {metadata.get('processing_timestamp', 'Unknown')}")
        print("\nTop 3 Most Relevant Sections:")
        for i, section in enumerate(sections[:3]):
            print(f"  {i+1}. {section['section_title']} ({section['document']}, Page {section['page_number']})")
        print(f"\nResults saved to: {output_file}")
        print("="*60)
        
        return True
        
    except Exception as e:
        logger.error(f"Challenge 1B processing failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)