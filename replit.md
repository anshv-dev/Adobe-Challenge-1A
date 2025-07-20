# PDF to JSON Processor - Adobe Hackathon Challenge 1a

## Overview

This is a comprehensive PDF processing solution built for Adobe Hackathon Challenge 1a that extracts structured data from PDF documents and converts it to JSON format. The solution provides both a command-line interface optimized for the challenge requirements and a Streamlit web interface for testing and validation. It uses PyMuPDF (fitz) for high-performance PDF processing, with built-in schema validation to ensure consistent output format.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (July 20, 2025)

✓ Updated output schema to match exact Adobe Hackathon Challenge 1a requirements
✓ Fixed web application processing flow with progress bars and status updates  
✓ Implemented proper schema validation using the provided JSON schema
✓ Resolved all display issues - results now show immediately after processing
✓ Enhanced error handling and user feedback in Streamlit interface
✓ **EXTENDED TO CHALLENGE 1B**: Added complete persona-driven document intelligence
✓ Built comprehensive web interface supporting both Challenge 1A and 1B
✓ Created sophisticated relevance scoring algorithm for persona-specific analysis
✓ Implemented multi-document processing with advanced section extraction

## System Architecture

The application follows a modular architecture with clear separation of concerns:

### Frontend Architecture
- **Streamlit Web Interface**: Provides an interactive web application for PDF upload and processing
- **Real-time Processing**: Shows live progress updates and processing status
- **Configuration Panel**: Sidebar with performance settings and processing options

### Backend Architecture
- **PDF Processing Engine**: Core module that handles PDF parsing and data extraction
- **Schema Validation**: Ensures all output conforms to predefined JSON schema
- **Utility Functions**: Helper functions for formatting and file operations

## Key Components

### 1. Command-Line Processor (`process_pdfs.py`) - CHALLENGE SUBMISSION
- **Purpose**: Main solution for Adobe Hackathon Challenge 1a
- **Key Features**:
  - Processes all PDFs from `/app/input` directory automatically
  - Outputs JSON files to `/app/output` directory
  - Optimized for 10-second performance constraint (50-page PDFs)
  - Memory efficient (stays within 16GB limit)
  - AMD64 architecture optimized
  - No internet access required
  - Comprehensive logging and performance metrics

### 2. Web Application (`app.py`)
- **Purpose**: Interactive interface for testing and validation
- **Key Features**:
  - File upload handling with size and type validation
  - Real-time processing status updates using session state
  - Configuration options for performance tuning
  - Results display and export functionality

### 2. PDF Processor (`pdf_processor.py`)
- **Purpose**: Core PDF processing logic
- **Key Features**:
  - PyMuPDF integration for PDF parsing
  - Structured data extraction (text blocks, images, tables)
  - Metadata extraction from PDF documents
  - Page-by-page processing with configurable limits

### 3. Schema Validator (`schema_validator.py`)
- **Purpose**: JSON schema validation and compliance
- **Key Features**:
  - Validates output against predefined schema
  - Creates default schema if none exists
  - Provides detailed validation error reporting

### 4. Output Schema (`output_schema.json`)
- **Purpose**: Defines the structure for extracted data
- **Key Sections**:
  - Document information (filename, page count, timestamps)
  - Content structure (text blocks, images, tables, page structure)
  - Extraction summary with statistics

### 5. Utilities (`utils.py`)
- **Purpose**: Common helper functions
- **Key Features**:
  - File size formatting
  - Duration formatting for processing times

## Data Flow

1. **File Upload**: User uploads PDF through Streamlit interface
2. **Validation**: File size and type validation before processing
3. **Processing**: PDF is processed page-by-page using PyMuPDF
4. **Data Extraction**: Text, images, tables, and metadata are extracted
5. **Schema Validation**: Output is validated against JSON schema
6. **Results Display**: Processed data is displayed with download options

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for user interface
- **PyMuPDF (fitz)**: PDF processing and content extraction
- **jsonschema**: JSON schema validation
- **pandas**: Data manipulation and display

### Python Standard Libraries
- **json**: JSON handling and serialization
- **pathlib**: Path operations
- **datetime**: Timestamp generation
- **threading**: Background processing support
- **logging**: Error and debug logging

## Deployment Strategy

### Local Development
- Application designed to run locally with `streamlit run app.py`
- Session state management for handling multiple file processing
- Real-time updates through Streamlit's reactive framework

### Configuration Options
- **Performance Tuning**: Configurable max pages and file size limits
- **Processing Limits**: Built-in safeguards to prevent resource exhaustion
- **Error Handling**: Comprehensive error handling with user-friendly messages

### File Management
- Temporary file handling for uploaded PDFs
- JSON export functionality for processed results
- Session-based result storage to prevent data loss

The architecture prioritizes modularity, making it easy to extend with additional features like batch processing, different output formats, or integration with cloud storage services. The schema-driven approach ensures consistent output structure across all processed documents.