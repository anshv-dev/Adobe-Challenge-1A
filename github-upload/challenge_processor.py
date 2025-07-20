#!/usr/bin/env python3
"""
Adobe Hackathon Challenge 1a - PDF Title and Heading Extraction
Extracts title and headings (H1, H2, H3) from PDF documents
"""

import os
import json
import time
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List, Any
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFHeadingExtractor:
    """Extract title and headings from PDF documents for Adobe Hackathon Challenge 1a"""
    
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        
    def extract_title_and_headings(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract title and headings from PDF according to challenge requirements
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with title and outline (headings) in required format
        """
        start_time = time.time()
        
        try:
            # Open PDF document
            doc = fitz.open(pdf_path)
            
            # Extract title from document metadata or first page
            title = self._extract_title(doc)
            
            # Extract headings from all pages
            outline = self._extract_headings(doc)
            
            # Structure output according to challenge requirements
            result = {
                "title": title,
                "outline": outline
            }
            
            processing_time = time.time() - start_time
            page_count = len(doc)
            
            logger.info(f"Processed {Path(pdf_path).name} in {processing_time:.2f}s - {page_count} pages, {len(outline)} headings")
            
            doc.close()
            return result
            
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {str(e)}")
            raise Exception(f"PDF processing failed: {str(e)}")
    
    def _extract_title(self, doc: fitz.Document) -> str:
        """Extract document title from metadata or first page"""
        
        # Try to get title from metadata first
        metadata = doc.metadata
        title = metadata.get("title", "").strip()
        
        if title:
            return title
        
        # If no metadata title, extract from first page
        if len(doc) > 0:
            first_page = doc[0]
            
            # Get text blocks with formatting
            blocks = first_page.get_text("dict")
            
            # Find the largest text on the first page (likely the title)
            largest_text = ""
            max_size = 0
            
            for block in blocks.get("blocks", []):
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line.get("spans", []):
                            text = span.get("text", "").strip()
                            size = span.get("size", 0)
                            
                            # Look for title-like text (large, short, on top of page)
                            if (text and size > max_size and len(text) < 200 and 
                                not text.isdigit() and len(text.split()) > 1):
                                largest_text = text
                                max_size = size
            
            if largest_text:
                return largest_text
        
        # Fallback to filename without extension
        return Path(doc.name).stem if doc.name else "Untitled Document"
    
    def _extract_headings(self, doc: fitz.Document) -> List[Dict[str, Any]]:
        """Extract headings (H1, H2, H3) from all pages"""
        
        headings = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_headings = self._extract_headings_from_page(page, page_num + 1)
            headings.extend(page_headings)
        
        return headings
    
    def _extract_headings_from_page(self, page: fitz.Page, page_number: int) -> List[Dict[str, Any]]:
        """Extract headings from a single page"""
        
        headings = []
        
        # Get text blocks with detailed formatting
        blocks = page.get_text("dict")
        
        # Collect all text spans with their properties
        text_spans = []
        for block in blocks.get("blocks", []):
            if "lines" in block:
                for line in block["lines"]:
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        if text and len(text) > 2:  # Ignore very short text
                            text_spans.append({
                                "text": text,
                                "size": span.get("size", 0),
                                "flags": span.get("flags", 0),  # Bold, italic flags
                                "font": span.get("font", ""),
                                "y": span.get("bbox", [0, 0, 0, 0])[1]  # Y position for ordering
                            })
        
        if not text_spans:
            return headings
        
        # Sort by Y position (top to bottom)
        text_spans.sort(key=lambda x: x["y"])
        
        # Calculate font size statistics for heading detection
        sizes = [span["size"] for span in text_spans]
        avg_size = sum(sizes) / len(sizes) if sizes else 12
        max_size = max(sizes) if sizes else 12
        
        # Define thresholds for heading levels
        h1_threshold = max_size * 0.9  # Largest text
        h2_threshold = avg_size * 1.4   # Significantly larger than average
        h3_threshold = avg_size * 1.2   # Moderately larger than average
        
        for span in text_spans:
            text = span["text"]
            size = span["size"]
            flags = span["flags"]
            
            # Skip if text looks like regular content
            if self._is_likely_content(text):
                continue
            
            # Determine heading level based on size and formatting
            level = None
            is_bold = bool(flags & 2**4)  # Bold flag
            
            if size >= h1_threshold or (size >= h2_threshold and is_bold):
                level = "H1"
            elif size >= h2_threshold or (size >= h3_threshold and is_bold):
                level = "H2"
            elif size >= h3_threshold or is_bold:
                level = "H3"
            
            # Additional heuristics for heading detection
            if not level and self._looks_like_heading(text, span):
                if size > avg_size * 1.1:
                    level = "H3"
            
            if level:
                headings.append({
                    "level": level,
                    "text": text,
                    "page": page_number
                })
        
        return headings
    
    def _is_likely_content(self, text: str) -> bool:
        """Check if text is likely regular content, not a heading"""
        
        # Skip very long text (likely paragraphs)
        if len(text) > 150:
            return True
        
        # Skip text that ends with period (likely sentences)
        if text.endswith('.') and len(text) > 20:
            return True
        
        # Skip text with too many common words
        common_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        words = text.lower().split()
        if len(words) > 5 and sum(1 for word in words if word in common_words) > len(words) * 0.4:
            return True
        
        return False
    
    def _looks_like_heading(self, text: str, span: Dict) -> bool:
        """Additional heuristics to identify headings"""
        
        # Check for numbering patterns (1.1, 1.2.3, etc.)
        if re.match(r'^\d+(\.\d+)*\.?\s+', text):
            return True
        
        # Check for chapter/section keywords
        heading_keywords = ['chapter', 'section', 'introduction', 'conclusion', 'summary', 
                           'overview', 'background', 'methodology', 'results', 'discussion']
        
        if any(keyword in text.lower() for keyword in heading_keywords):
            return True
        
        # Check if text is short and likely a heading
        if len(text.split()) <= 6 and text[0].isupper():
            return True
        
        return False

def process_pdfs():
    """
    Main function to process all PDFs from input directory
    Meets Adobe Hackathon Challenge 1a requirements
    """
    
    # Directory paths as per challenge requirements
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # For local testing, use current directory structure
    if not input_dir.exists():
        input_dir = Path("./sample_pdfs")
        output_dir = Path("./output")
        
        # Create output directory if it doesn't exist
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.warning(f"Could not create output directory: {e}")
            output_dir = Path(".")
        
        if not input_dir.exists():
            input_dir = Path(".")
            logger.info("Using current directory for input PDFs")
    else:
        # Create output directory if it doesn't exist
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Could not create output directory: {e}")
            return
    
    extractor = PDFHeadingExtractor()
    
    # Find all PDF files
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {input_dir}")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF file
    total_start_time = time.time()
    
    for pdf_file in pdf_files:
        try:
            logger.info(f"Processing: {pdf_file.name}")
            
            # Extract title and headings
            result = extractor.extract_title_and_headings(str(pdf_file))
            
            # Generate output filename
            output_filename = f"{pdf_file.stem}.json"
            output_path = output_dir / output_filename
            
            # Save JSON output
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            extractor.processed_count += 1
            logger.info(f"Saved: {output_filename}")
            
        except Exception as e:
            logger.error(f"Failed to process {pdf_file.name}: {str(e)}")
            extractor.error_count += 1
    
    total_time = time.time() - total_start_time
    
    # Final summary
    logger.info("=" * 50)
    logger.info("PROCESSING COMPLETE")
    logger.info(f"Total files processed: {extractor.processed_count}")
    logger.info(f"Total errors: {extractor.error_count}")
    logger.info(f"Total processing time: {total_time:.2f} seconds")
    logger.info(f"Average time per file: {total_time/len(pdf_files):.2f} seconds")
    
    # Performance check for 50-page constraint
    if len(pdf_files) > 0:
        avg_time = total_time / len(pdf_files)
        if avg_time <= 10:
            logger.info("✅ Performance constraint met: ≤ 10 seconds per 50-page PDF")
        else:
            logger.warning(f"⚠️  Performance constraint exceeded: {avg_time:.2f}s > 10s")

if __name__ == "__main__":
    # Run the PDF processing
    try:
        process_pdfs()
    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        exit(1)