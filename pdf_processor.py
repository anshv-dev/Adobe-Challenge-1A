import fitz  # PyMuPDF
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
import logging

class PDFProcessor:
    """
    PDF processing engine that extracts structured data from PDF documents
    and converts it to JSON format conforming to the required schema.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def process_pdf(self, pdf_path: str, max_pages: int = 50) -> Dict[str, Any]:
        """
        Process a PDF file and extract structured data
        
        Args:
            pdf_path: Path to the PDF file
            max_pages: Maximum number of pages to process
            
        Returns:
            Dictionary containing structured data
        """
        try:
            # Open PDF document
            doc = fitz.open(pdf_path)
            
            # Basic document information
            pdf_info = {
                "filename": Path(pdf_path).name,
                "page_count": min(len(doc), max_pages),
                "total_pages": len(doc),
                "processing_timestamp": datetime.now().isoformat(),
                "metadata": self._extract_metadata(doc)
            }
            
            # Extract content from pages
            content = self._extract_content(doc, max_pages)
            
            # Structure the output according to schema
            structured_data = {
                "document_info": pdf_info,
                "content": content,
                "extraction_summary": {
                    "total_text_blocks": len(content.get("text_blocks", [])),
                    "total_images": len(content.get("images", [])),
                    "total_tables": len(content.get("tables", [])),
                    "processing_complete": True
                }
            }
            
            doc.close()
            return structured_data
            
        except Exception as e:
            self.logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            raise Exception(f"PDF processing failed: {str(e)}")
    
    def _extract_metadata(self, doc: fitz.Document) -> Dict[str, Any]:
        """Extract document metadata"""
        metadata = doc.metadata
        return {
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "creator": metadata.get("creator", ""),
            "producer": metadata.get("producer", ""),
            "creation_date": metadata.get("creationDate", ""),
            "modification_date": metadata.get("modDate", "")
        }
    
    def _extract_content(self, doc: fitz.Document, max_pages: int) -> Dict[str, Any]:
        """Extract content from PDF pages"""
        content = {
            "text_blocks": [],
            "images": [],
            "tables": [],
            "page_structure": []
        }
        
        for page_num in range(min(len(doc), max_pages)):
            page = doc[page_num]
            
            # Extract text blocks with positioning
            text_blocks = self._extract_text_blocks(page, page_num)
            content["text_blocks"].extend(text_blocks)
            
            # Extract images
            images = self._extract_images(page, page_num)
            content["images"].extend(images)
            
            # Detect and extract tables
            tables = self._detect_tables(page, page_num)
            content["tables"].extend(tables)
            
            # Page structure analysis
            page_structure = self._analyze_page_structure(page, page_num)
            content["page_structure"].append(page_structure)
        
        return content
    
    def _extract_text_blocks(self, page: fitz.Page, page_num: int) -> List[Dict[str, Any]]:
        """Extract text blocks with formatting and positioning information"""
        text_blocks = []
        
        # Get text with detailed formatting
        blocks = page.get_text("dict")
        
        for block_num, block in enumerate(blocks.get("blocks", [])):
            if "lines" in block:  # Text block
                block_text = []
                block_fonts = set()
                block_sizes = set()
                
                for line in block["lines"]:
                    line_text = []
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        if text:
                            line_text.append(text)
                            block_fonts.add(span.get("font", ""))
                            block_sizes.add(span.get("size", 0))
                    
                    if line_text:
                        block_text.append(" ".join(line_text))
                
                if block_text:
                    # Determine block type based on formatting
                    block_type = self._classify_text_block(block_text, block_fonts, block_sizes)
                    
                    text_blocks.append({
                        "page": page_num + 1,
                        "block_id": f"page_{page_num + 1}_block_{block_num}",
                        "type": block_type,
                        "text": "\n".join(block_text),
                        "position": {
                            "x0": block.get("bbox", [0, 0, 0, 0])[0],
                            "y0": block.get("bbox", [0, 0, 0, 0])[1],
                            "x1": block.get("bbox", [0, 0, 0, 0])[2],
                            "y1": block.get("bbox", [0, 0, 0, 0])[3]
                        },
                        "fonts": list(block_fonts),
                        "font_sizes": list(block_sizes)
                    })
        
        return text_blocks
    
    def _classify_text_block(self, text_lines: List[str], fonts: set, sizes: set) -> str:
        """Classify text block type based on content and formatting"""
        if not text_lines:
            return "unknown"
        
        # Join all text for analysis
        full_text = " ".join(text_lines).strip()
        
        # Check for headers (short text, larger fonts)
        if len(text_lines) == 1 and len(full_text) < 100:
            if sizes and max(sizes) > 14:
                return "header"
        
        # Check for bullet points or lists
        if any(line.strip().startswith(("•", "-", "*", "1.", "2.", "3.")) for line in text_lines):
            return "list"
        
        # Check for tables (structured data patterns)
        if self._has_tabular_structure(text_lines):
            return "table_text"
        
        # Check for captions (contains "Figure", "Table", "Chart" etc.)
        caption_keywords = ["figure", "table", "chart", "image", "diagram"]
        if any(keyword in full_text.lower() for keyword in caption_keywords):
            return "caption"
        
        # Default to paragraph
        return "paragraph"
    
    def _has_tabular_structure(self, text_lines: List[str]) -> bool:
        """Check if text has tabular structure"""
        if len(text_lines) < 2:
            return False
        
        # Look for consistent spacing patterns
        tab_patterns = 0
        for line in text_lines:
            if "\t" in line or "  " in line:  # Multiple spaces or tabs
                tab_patterns += 1
        
        return tab_patterns > len(text_lines) * 0.5
    
    def _extract_images(self, page: fitz.Page, page_num: int) -> List[Dict[str, Any]]:
        """Extract image information from page"""
        images = []
        image_list = page.get_images()
        
        for img_num, img in enumerate(image_list):
            try:
                # Get image info
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
                
            except Exception as e:
                self.logger.warning(f"Could not extract image {img_num} from page {page_num + 1}: {str(e)}")
        
        return images
    
    def _detect_tables(self, page: fitz.Page, page_num: int) -> List[Dict[str, Any]]:
        """Detect and extract table structures"""
        tables = []
        
        # Simple table detection based on text alignment and spacing
        text_dict = page.get_text("dict")
        
        # Look for rectangular arrangements of text
        potential_tables = self._find_table_regions(text_dict, page_num)
        
        for table_num, table_region in enumerate(potential_tables):
            tables.append({
                "page": page_num + 1,
                "table_id": f"page_{page_num + 1}_table_{table_num}",
                "type": "table",
                "rows": table_region.get("rows", 0),
                "columns": table_region.get("columns", 0),
                "position": table_region.get("bbox", {}),
                "data": table_region.get("data", [])
            })
        
        return tables
    
    def _find_table_regions(self, text_dict: Dict, page_num: int) -> List[Dict[str, Any]]:
        """Find potential table regions in page text"""
        # Simplified table detection
        # In a production system, this would use more sophisticated algorithms
        
        tables = []
        
        # Look for blocks with consistent vertical alignment
        blocks = text_dict.get("blocks", [])
        
        for block in blocks:
            if "lines" in block and len(block["lines"]) > 2:
                lines = block["lines"]
                
                # Check if lines have similar structure (potential table rows)
                if self._is_table_block(lines):
                    table_data = self._extract_table_data(lines)
                    if table_data:
                        tables.append({
                            "rows": len(table_data),
                            "columns": max(len(row) for row in table_data) if table_data else 0,
                            "bbox": block.get("bbox", {}),
                            "data": table_data
                        })
        
        return tables
    
    def _is_table_block(self, lines: List[Dict]) -> bool:
        """Check if a block of lines represents a table"""
        if len(lines) < 3:
            return False
        
        # Check for consistent span patterns across lines
        span_counts = [len(line.get("spans", [])) for line in lines]
        
        # If most lines have similar number of spans, it might be a table
        if len(set(span_counts)) <= 2 and max(span_counts) > 1:
            return True
        
        return False
    
    def _extract_table_data(self, lines: List[Dict]) -> List[List[str]]:
        """Extract table data from lines"""
        table_data = []
        
        for line in lines:
            row_data = []
            for span in line.get("spans", []):
                text = span.get("text", "").strip()
                if text:
                    row_data.append(text)
            
            if row_data:
                table_data.append(row_data)
        
        return table_data
    
    def _analyze_page_structure(self, page: fitz.Page, page_num: int) -> Dict[str, Any]:
        """Analyze the overall structure of a page"""
        
        # Get page dimensions
        rect = page.rect
        
        # Analyze text distribution
        text_blocks = page.get_text("dict").get("blocks", [])
        text_coverage = self._calculate_text_coverage(text_blocks, rect)
        
        # Count different element types
        image_count = len(page.get_images())
        
        return {
            "page": page_num + 1,
            "dimensions": {
                "width": rect.width,
                "height": rect.height
            },
            "text_coverage": text_coverage,
            "element_counts": {
                "text_blocks": len([b for b in text_blocks if "lines" in b]),
                "images": image_count
            },
            "layout_type": self._determine_layout_type(text_blocks, image_count, rect)
        }
    
    def _calculate_text_coverage(self, text_blocks: List[Dict], page_rect: fitz.Rect) -> float:
        """Calculate what percentage of the page is covered by text"""
        total_text_area = 0
        
        for block in text_blocks:
            if "lines" in block and "bbox" in block:
                bbox = block["bbox"]
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                total_text_area += area
        
        page_area = page_rect.width * page_rect.height
        return (total_text_area / page_area) * 100 if page_area > 0 else 0
    
    def _determine_layout_type(self, text_blocks: List[Dict], image_count: int, rect: fitz.Rect) -> str:
        """Determine the layout type of the page"""
        text_block_count = len([b for b in text_blocks if "lines" in b])
        
        if image_count > text_block_count:
            return "image_heavy"
        elif text_block_count > 10:
            return "text_heavy"
        elif image_count > 0 and text_block_count > 0:
            return "mixed"
        elif text_block_count == 0 and image_count == 0:
            return "empty"
        else:
            return "standard"
