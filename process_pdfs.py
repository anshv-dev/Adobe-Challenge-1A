#!/usr/bin/env python3
"""
Adobe Hackathon Challenge 1a - PDF Processing Solution
Processes all PDFs from /app/input directory and outputs JSON files to /app/output directory
"""

import os
import json
import time
import fitz  # PyMuPDF
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFProcessor:
    """Enhanced PDF processor for Adobe Hackathon Challenge 1a"""
    
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process a PDF file and extract structured data according to challenge requirements
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing structured data conforming to output schema
        """
        start_time = time.time()
        
        try:
            # Open PDF document
            doc = fitz.open(pdf_path)
            
            # Extract document metadata
            metadata = doc.metadata
            
            # Process all pages (optimized for performance)
            content = self._extract_content_optimized(doc)
            
            # Structure output according to Adobe challenge schema
            result = {
                "document_info": {
                    "filename": Path(pdf_path).name,
                    "page_count": len(doc),
                    "total_pages": len(doc),
                    "processing_timestamp": datetime.now().isoformat(),
                    "metadata": {
                        "title": metadata.get("title", ""),
                        "author": metadata.get("author", ""),
                        "subject": metadata.get("subject", ""),
                        "creator": metadata.get("creator", ""),
                        "producer": metadata.get("producer", ""),
                        "creation_date": metadata.get("creationDate", ""),
                        "modification_date": metadata.get("modDate", "")
                    }
                },
                "content": content,
                "extraction_summary": {
                    "total_text_blocks": len(content.get("text_blocks", [])),
                    "total_images": len(content.get("images", [])),
                    "total_tables": len(content.get("tables", [])),
                    "processing_complete": True,
                    "processing_time_seconds": time.time() - start_time
                }
            }
            
            processing_time = time.time() - start_time
            page_count = len(doc)
            
            logger.info(f"Processed {Path(pdf_path).name} in {processing_time:.2f}s - {page_count} pages")
            
            doc.close()
            return result
            
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {str(e)}")
            raise Exception(f"PDF processing failed: {str(e)}")
    
    def _extract_content_optimized(self, doc: fitz.Document) -> Dict[str, Any]:
        """Extract content with optimizations for performance"""
        content = {
            "text_blocks": [],
            "images": [],
            "tables": [],
            "page_structure": []
        }
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Extract text blocks with positioning
            text_blocks = self._extract_text_blocks_fast(page, page_num)
            content["text_blocks"].extend(text_blocks)
            
            # Extract images efficiently
            images = self._extract_images_fast(page, page_num)
            content["images"].extend(images)
            
            # Detect tables (simplified for performance)
            tables = self._detect_tables_fast(page, page_num)
            content["tables"].extend(tables)
            
            # Page structure analysis
            page_structure = self._analyze_page_structure_fast(page, page_num)
            content["page_structure"].append(page_structure)
        
        return content
    
    def _extract_text_blocks_fast(self, page: fitz.Page, page_num: int) -> List[Dict[str, Any]]:
        """Fast text extraction optimized for performance"""
        text_blocks = []
        
        # Use get_text("dict") for detailed formatting
        blocks = page.get_text("dict")
        
        block_id = 0
        for block in blocks.get("blocks", []):
            if "lines" in block:  # Text block
                block_text = []
                fonts = set()
                sizes = set()
                
                for line in block["lines"]:
                    line_text = []
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        if text:
                            line_text.append(text)
                            fonts.add(span.get("font", ""))
                            sizes.add(span.get("size", 0))
                    
                    if line_text:
                        block_text.append(" ".join(line_text))
                
                if block_text:
                    # Classify block type
                    block_type = self._classify_text_block_fast(block_text, fonts, sizes)
                    
                    text_blocks.append({
                        "page": page_num + 1,
                        "block_id": f"page_{page_num + 1}_block_{block_id}",
                        "type": block_type,
                        "text": "\n".join(block_text),
                        "position": {
                            "x0": block.get("bbox", [0, 0, 0, 0])[0],
                            "y0": block.get("bbox", [0, 0, 0, 0])[1],
                            "x1": block.get("bbox", [0, 0, 0, 0])[2],
                            "y1": block.get("bbox", [0, 0, 0, 0])[3]
                        },
                        "fonts": list(fonts),
                        "font_sizes": list(sizes)
                    })
                    block_id += 1
        
        return text_blocks
    
    def _classify_text_block_fast(self, text_lines: List[str], fonts: set, sizes: set) -> str:
        """Fast text block classification"""
        if not text_lines:
            return "unknown"
        
        full_text = " ".join(text_lines).strip()
        
        # Quick classification based on text patterns
        if len(text_lines) == 1 and len(full_text) < 100 and sizes and max(sizes) > 14:
            return "header"
        elif any(line.strip().startswith(("•", "-", "*", "1.", "2.", "3.")) for line in text_lines):
            return "list"
        elif any(keyword in full_text.lower() for keyword in ["figure", "table", "chart"]):
            return "caption"
        else:
            return "paragraph"
    
    def _extract_images_fast(self, page: fitz.Page, page_num: int) -> List[Dict[str, Any]]:
        """Fast image extraction"""
        images = []
        image_list = page.get_images()
        
        for img_num, img in enumerate(image_list):
            try:
                xref = img[0]
                pix = fitz.Pixmap(page.parent, xref)
                
                images.append({
                    "page": page_num + 1,
                    "image_id": f"page_{page_num + 1}_img_{img_num}",
                    "width": pix.width,
                    "height": pix.height,
                    "colorspace": pix.colorspace.name if pix.colorspace else "unknown",
                    "format": "image"
                })
                
                pix = None  # Clean up
                
            except Exception:
                # Skip problematic images for performance
                continue
        
        return images
    
    def _detect_tables_fast(self, page: fitz.Page, page_num: int) -> List[Dict[str, Any]]:
        """Fast table detection"""
        tables = []
        
        # Simple table detection for performance
        text_dict = page.get_text("dict")
        blocks = text_dict.get("blocks", [])
        
        table_id = 0
        for block in blocks:
            if "lines" in block and len(block["lines"]) > 2:
                lines = block["lines"]
                
                # Check for table-like structure
                span_counts = [len(line.get("spans", [])) for line in lines]
                if len(set(span_counts)) <= 2 and max(span_counts) > 1:
                    # Extract table data
                    table_data = []
                    for line in lines:
                        row_data = []
                        for span in line.get("spans", []):
                            text = span.get("text", "").strip()
                            if text:
                                row_data.append(text)
                        if row_data:
                            table_data.append(row_data)
                    
                    if table_data:
                        tables.append({
                            "page": page_num + 1,
                            "table_id": f"page_{page_num + 1}_table_{table_id}",
                            "type": "table",
                            "rows": len(table_data),
                            "columns": max(len(row) for row in table_data),
                            "position": block.get("bbox", {}),
                            "data": table_data
                        })
                        table_id += 1
        
        return tables
    
    def _analyze_page_structure_fast(self, page: fitz.Page, page_num: int) -> Dict[str, Any]:
        """Fast page structure analysis"""
        rect = page.rect
        
        # Count elements quickly
        text_blocks = page.get_text("dict").get("blocks", [])
        text_block_count = len([b for b in text_blocks if "lines" in b])
        image_count = len(page.get_images())
        
        # Calculate text coverage (simplified)
        total_text_area = sum((b["bbox"][2] - b["bbox"][0]) * (b["bbox"][3] - b["bbox"][1]) 
                             for b in text_blocks if "lines" in b and "bbox" in b)
        page_area = rect.width * rect.height
        text_coverage = (total_text_area / page_area) * 100 if page_area > 0 else 0
        
        # Determine layout type
        if image_count > text_block_count:
            layout_type = "image_heavy"
        elif text_block_count > 10:
            layout_type = "text_heavy"
        elif image_count > 0 and text_block_count > 0:
            layout_type = "mixed"
        else:
            layout_type = "standard"
        
        return {
            "page": page_num + 1,
            "dimensions": {
                "width": rect.width,
                "height": rect.height
            },
            "text_coverage": text_coverage,
            "element_counts": {
                "text_blocks": text_block_count,
                "images": image_count
            },
            "layout_type": layout_type
        }

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
    
    processor = PDFProcessor()
    
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
            
            # Process PDF
            result = processor.process_pdf(str(pdf_file))
            
            # Generate output filename
            output_filename = f"{pdf_file.stem}.json"
            output_path = output_dir / output_filename
            
            # Save JSON output
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            processor.processed_count += 1
            logger.info(f"Saved: {output_filename}")
            
        except Exception as e:
            logger.error(f"Failed to process {pdf_file.name}: {str(e)}")
            processor.error_count += 1
    
    total_time = time.time() - total_start_time
    
    # Final summary
    logger.info("=" * 50)
    logger.info("PROCESSING COMPLETE")
    logger.info(f"Total files processed: {processor.processed_count}")
    logger.info(f"Total errors: {processor.error_count}")
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