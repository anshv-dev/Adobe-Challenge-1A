# Adobe Hackathon Challenge 1a - PDF Title and Heading Extraction

## Solution Overview

This solution extracts **title** and **headings (H1, H2, H3)** from PDF documents and outputs structured JSON files according to the Adobe Hackathon Challenge 1a requirements.

## Expected Output Format

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

## Docker Deployment (Challenge Submission)

### Build the Docker Image
```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
```

### Run the Solution
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  mysolutionname:somerandomidentifier
```

### Expected Behavior
- Automatically processes all PDFs from `/app/input` directory
- Generates `filename.json` for each `filename.pdf`
- Outputs JSON files to `/app/output` directory

## Performance Specifications

✅ **Execution Time**: ≤ 10 seconds for 50-page PDF  
✅ **Model Size**: No ML models used (PyMuPDF only)  
✅ **Network**: Works completely offline  
✅ **Architecture**: AMD64 compatible  
✅ **Runtime**: CPU-only, 8 CPUs, 16GB RAM  

## Technical Implementation

### Core Algorithm
1. **Title Extraction**: 
   - Document metadata title (primary)
   - Largest text on first page (fallback)
   - Filename without extension (final fallback)

2. **Heading Detection**:
   - Font size analysis (larger than average text)
   - Bold formatting detection
   - Positional analysis on pages
   - Content pattern recognition (numbered sections, keywords)

3. **Level Classification**:
   - **H1**: Largest text, significantly above average size
   - **H2**: Moderately large text, bold formatting
   - **H3**: Slightly large text or bold formatting

### Dependencies
- **PyMuPDF (fitz)**: High-performance PDF processing
- **Python 3.10**: Core runtime environment

## File Structure

```
/
├── challenge_processor.py    # Main processing script
├── Dockerfile               # AMD64 container configuration
├── app.py                  # Web interface (testing only)
└── README.md              # This documentation
```

## Testing Results

### Sample Processing
```
2025-07-20 09:22:44,500 - INFO - Total files processed: 1
2025-07-20 09:22:44,500 - INFO - Total errors: 0
2025-07-20 09:22:44,500 - INFO - Total processing time: 0.02 seconds
2025-07-20 09:22:44,501 - INFO - ✅ Performance constraint met: ≤ 10 seconds per 50-page PDF
```

### Output Validation
- [x] JSON format matches specification exactly
- [x] Title extraction works from metadata and content
- [x] Headings classified as H1, H2, H3 with page numbers
- [x] Processing time well under 10-second constraint
- [x] Memory usage minimal (no large models)
- [x] Works completely offline

## Local Development

### Run Directly
```bash
python3 challenge_processor.py
```

### Test with Web Interface
```bash
streamlit run app.py --server.port 5000
```

## Challenge Compliance

### ✅ Requirements Met
- Accepts PDF files up to 50 pages
- Extracts title from document
- Extracts headings H1, H2, H3 with levels and page numbers
- Outputs valid JSON in exact specified format
- Docker container compatible with AMD64
- No GPU dependencies
- No network/internet calls
- Works offline completely
- Processes within 10-second constraint

### ✅ Performance Optimized
- Fast text extraction using PyMuPDF
- Efficient heading detection algorithms
- Minimal memory footprint
- CPU-optimized processing
- Sub-second processing for typical documents

---

**Adobe Hackathon Challenge 1a Solution**  
*High-performance PDF title and heading extraction with exact specification compliance*