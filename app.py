import streamlit as st
import os
import json
import time
import threading
from pathlib import Path
from datetime import datetime
import pandas as pd
from challenge_processor import PDFHeadingExtractor
# from schema_validator import SchemaValidator
from utils import format_file_size, format_duration

# Initialize session state
if 'processing_results' not in st.session_state:
    st.session_state.processing_results = {}
if 'processing_status' not in st.session_state:
    st.session_state.processing_status = {}

def main():
    st.set_page_config(
        page_title="PDF to JSON Processor - Adobe Hackathon Challenge 1a",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 PDF to JSON Processor")
    st.markdown("**Adobe Hackathon Challenge 1a Solution**")
    st.markdown("Extract structured data from PDF documents and convert to JSON format")
    
    # Initialize processor
    try:
        processor = PDFHeadingExtractor()
    except Exception as e:
        st.error(f"Error initializing PDF processor: {str(e)}")
        st.stop()
    
    # Sidebar for configuration and stats
    with st.sidebar:
        st.header("Configuration")
        
        # Performance settings
        st.subheader("Performance Settings")
        max_pages = st.number_input(
            "Max pages per PDF",
            min_value=1,
            max_value=1000,
            value=50,
            help="Maximum number of pages to process per PDF"
        )
        
        max_file_size = st.number_input(
            "Max file size (MB)",
            min_value=1,
            max_value=100,
            value=50,
            help="Maximum file size in MB"
        )
        
        st.subheader("Processing Stats")
        if st.session_state.processing_results:
            total_files = len(st.session_state.processing_results)
            successful = sum(1 for r in st.session_state.processing_results.values() if r.get('status') == 'success')
            failed = total_files - successful
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Files", total_files)
                st.metric("Successful", successful)
            with col2:
                st.metric("Failed", failed)
                if successful > 0:
                    avg_time = sum(r.get('processing_time', 0) for r in st.session_state.processing_results.values() if r.get('status') == 'success') / successful
                    st.metric("Avg Time", f"{avg_time:.2f}s")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Upload PDF Files")
        
        # File upload section
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more PDF files to process"
        )
        
        if uploaded_files:
            st.subheader("Uploaded Files")
            
            # Display uploaded files info
            files_data = []
            valid_files = []
            
            for file in uploaded_files:
                file_size = len(file.getvalue())
                file_size_mb = file_size / (1024 * 1024)
                
                status = "✅ Valid"
                if file_size_mb > max_file_size:
                    status = f"❌ Too large (>{max_file_size}MB)"
                else:
                    valid_files.append(file)
                
                files_data.append({
                    "Filename": file.name,
                    "Size": format_file_size(file_size),
                    "Status": status
                })
            
            df = pd.DataFrame(files_data)
            st.dataframe(df, use_container_width=True)
            
            # Process button
            if valid_files and st.button("🚀 Process PDFs", type="primary"):
                process_pdfs(valid_files, processor, max_pages)
    
    with col2:
        st.header("Schema Information")
        
        # Display expected output format
        st.markdown("**Expected Output Format:**")
        sample_output = {
            "title": "Document Title",
            "outline": [
                {"level": "H1", "text": "Introduction", "page": 1},
                {"level": "H2", "text": "Overview", "page": 2},
                {"level": "H3", "text": "Details", "page": 3}
            ]
        }
        st.json(sample_output, expanded=False)
    
    # Results section
    if st.session_state.processing_results:
        st.header("Processing Results")
        
        # Display results
        for filename, result in st.session_state.processing_results.items():
            with st.expander(f"📄 {filename}", expanded=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    status = result.get('status', 'unknown')
                    if status == 'success':
                        st.success(f"✅ Processed successfully")
                        st.info(f"⏱️ Processing time: {result.get('processing_time', 0):.2f} seconds")
                        st.info(f"📊 Pages processed: {result.get('pages_processed', 0)}")
                        st.info(f"📋 Headings extracted: {result.get('headings_found', 0)}")
                    elif status == 'error':
                        st.error(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
                    elif status == 'processing':
                        st.info(f"⏳ Processing...")
                
                with col2:
                    if status == 'success' and 'json_data' in result:
                        # Preview JSON structure
                        st.subheader("JSON Preview")
                        preview_data = {k: f"{type(v).__name__}" for k, v in result['json_data'].items()}
                        st.json(preview_data)
                
                with col3:
                    if status == 'success' and 'json_data' in result:
                        # Download button
                        json_str = json.dumps(result['json_data'], indent=2)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_str,
                            file_name=f"{Path(filename).stem}.json",
                            mime="application/json"
                        )
                        
                        # Validation status
                        if result.get('schema_valid'):
                            st.success("✅ Schema Valid")
                        else:
                            st.warning("⚠️ Schema Issues")
                            if 'validation_errors' in result:
                                st.text(result['validation_errors'])

def process_pdfs(files, processor, max_pages):
    """Process uploaded PDF files"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_files = len(files)
    
    for i, file in enumerate(files):
        progress = (i + 1) / total_files
        progress_bar.progress(progress)
        status_text.text(f"Processing {file.name}...")
        
        try:
            start_time = time.time()
            
            # Save uploaded file temporarily
            temp_path = f"/tmp/{file.name}"
            with open(temp_path, "wb") as f:
                f.write(file.getvalue())
            
            # Process PDF - extract title and headings
            result = processor.extract_title_and_headings(temp_path)
            
            # Simple validation for challenge format
            is_valid = 'title' in result and 'outline' in result
            validation_errors = "" if is_valid else "Missing title or outline"
            
            processing_time = time.time() - start_time
            
            # Update results
            st.session_state.processing_results[file.name] = {
                'status': 'success',
                'processing_time': processing_time,
                'json_data': result,
                'schema_valid': is_valid,
                'validation_errors': validation_errors,
                'pages_processed': 1,
                'headings_found': len(result.get('outline', []))
            }
            
            # Clean up temp file
            os.remove(temp_path)
            
            status_text.success(f"✅ {file.name} processed successfully!")
            
        except Exception as e:
            st.session_state.processing_results[file.name] = {
                'status': 'error',
                'error': str(e),
                'processing_time': time.time() - start_time if 'start_time' in locals() else 0
            }
            status_text.error(f"❌ Failed to process {file.name}: {str(e)}")
    
    progress_bar.progress(1.0)
    status_text.success(f"🎉 Processing complete! {total_files} files processed.")
    
    # Force UI update after processing
    st.rerun()

if __name__ == "__main__":
    main()
