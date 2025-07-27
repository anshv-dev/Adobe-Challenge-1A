import streamlit as st
import sys
import os
import json
import time
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from processor import PDFProcessor
from validator import SchemaValidator
from utils import format_file_size, format_duration

# Page configuration
st.set_page_config(
    page_title="Adobe Challenge 1A - PDF Title & Heading Extraction",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .upload-section {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .results-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'processed_results' not in st.session_state:
        st.session_state.processed_results = None
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'uploaded_file_name' not in st.session_state:
        st.session_state.uploaded_file_name = None

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.title("📋 Adobe Challenge 1A")
    st.subheader("PDF Title & Heading Extraction System")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Performance settings
        st.subheader("Performance Settings")
        max_pages = st.slider("Max Pages to Process", 1, 100, 50)
        max_file_size = st.slider("Max File Size (MB)", 1, 200, 100)
        
        # Processing options
        st.subheader("Processing Options")
        extract_titles = st.checkbox("Extract Titles", value=True)
        extract_h1 = st.checkbox("Extract H1 Headings", value=True)
        extract_h2 = st.checkbox("Extract H2 Headings", value=True)
        extract_h3 = st.checkbox("Extract H3 Headings", value=True)
        
        # Information
        st.subheader("📊 System Info")
        st.info(f"""
        **Performance Targets:**
        - Processing: <10 seconds
        - Max Pages: {max_pages}
        - Memory: <1GB
        - Architecture: CPU-only
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File upload section
        st.header("📁 Upload PDF Document")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help=f"Maximum file size: {max_file_size}MB, Maximum pages: {max_pages}"
        )
        
        if uploaded_file is not None:
            # File validation
            file_size = len(uploaded_file.read())
            uploaded_file.seek(0)  # Reset file pointer
            
            if file_size > max_file_size * 1024 * 1024:
                st.error(f"❌ File too large: {format_file_size(file_size)}. Maximum allowed: {max_file_size}MB")
                return
            
            # Display file info
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📊 File size: {format_file_size(file_size)}")
            
            # Process button
            if st.button("🚀 Extract Titles & Headings", type="primary"):
                process_document(uploaded_file, max_pages, extract_titles, extract_h1, extract_h2, extract_h3)
    
    with col2:
        # Quick stats
        st.header("📈 Quick Stats")
        
        if st.session_state.processed_results:
            results = st.session_state.processed_results
            extraction_summary = results.get('extraction_summary', {})
            
            st.metric("Total Headings", extraction_summary.get('total_headings', 0))
            st.metric("Processing Time", f"{extraction_summary.get('processing_time_seconds', 0):.2f}s")
            st.metric("Pages Processed", results.get('document_info', {}).get('page_count', 0))
            
            # Success indicator
            if extraction_summary.get('success', False):
                st.success("✅ Processing Complete")
            else:
                st.error("❌ Processing Failed")
    
    # Results section
    if st.session_state.processing_complete and st.session_state.processed_results:
        display_results()

def process_document(uploaded_file, max_pages, extract_titles, extract_h1, extract_h2, extract_h3):
    """Process the uploaded document"""
    with st.spinner("🔄 Processing document..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize processor
            status_text.text("Initializing PDF processor...")
            progress_bar.progress(10)
            
            processor = PDFProcessor()
            
            # Save uploaded file temporarily
            status_text.text("Saving uploaded file...")
            progress_bar.progress(20)
            
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())
            
            # Process document
            status_text.text("Extracting titles and headings...")
            progress_bar.progress(40)
            
            start_time = time.time()
            
            # Configure extraction options
            extraction_config = {
                'extract_titles': extract_titles,
                'extract_h1': extract_h1,
                'extract_h2': extract_h2,
                'extract_h3': extract_h3,
                'max_pages': max_pages
            }
            
            results = processor.extract_headings(temp_path, config=extraction_config)
            
            progress_bar.progress(70)
            status_text.text("Validating results...")
            
            # Validate schema
            validator = SchemaValidator()
            is_valid, validation_errors = validator.validate_output(results)
            
            progress_bar.progress(90)
            
            if not is_valid:
                st.error(f"❌ Schema validation failed: {', '.join(validation_errors)}")
                return
            
            # Store results
            st.session_state.processed_results = results
            st.session_state.processing_complete = True
            st.session_state.uploaded_file_name = uploaded_file.name
            
            progress_bar.progress(100)
            status_text.text("✅ Processing complete!")
            
            # Clean up
            os.remove(temp_path)
            
            # Display success message
            processing_time = time.time() - start_time
            st.success(f"🎉 Document processed successfully in {processing_time:.2f} seconds!")
            
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")
            if os.path.exists(temp_path):
                os.remove(temp_path)

def display_results():
    """Display processing results"""
    st.header("📊 Extraction Results")
    
    results = st.session_state.processed_results
    
    # Results overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📄 Document Info")
        doc_info = results.get('document_info', {})
        st.write(f"**Filename:** {doc_info.get('filename', 'N/A')}")
        st.write(f"**Pages:** {doc_info.get('page_count', 0)}")
        st.write(f"**Processed:** {doc_info.get('processing_timestamp', 'N/A')}")
    
    with col2:
        st.markdown("### 📈 Extraction Summary")
        summary = results.get('extraction_summary', {})
        st.write(f"**Total Headings:** {summary.get('total_headings', 0)}")
        st.write(f"**Processing Time:** {summary.get('processing_time_seconds', 0):.2f}s")
        st.write(f"**Status:** {'✅ Success' if summary.get('success') else '❌ Failed'}")
    
    with col3:
        st.markdown("### 💾 Export Options")
        
        # Download JSON
        json_str = json.dumps(results, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"{st.session_state.uploaded_file_name}_results.json",
            mime="application/json"
        )
        
        # Download TXT summary
        txt_summary = generate_text_summary(results)
        st.download_button(
            label="📄 Download Summary",
            data=txt_summary,
            file_name=f"{st.session_state.uploaded_file_name}_summary.txt",
            mime="text/plain"
        )
    
    # Detailed results
    st.markdown("---")
    
    # Tabs for different content types
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 All Headings", "🏷️ Titles", "📰 H1", "📑 H2", "📝 H3"])
    
    extracted_content = results.get('extracted_content', {})
    
    with tab1:
        display_all_headings(extracted_content)
    
    with tab2:
        display_heading_section("Titles", extracted_content.get('titles', []))
    
    with tab3:
        headings = extracted_content.get('headings', {})
        display_heading_section("H1 Headings", headings.get('h1', []))
    
    with tab4:
        headings = extracted_content.get('headings', {})
        display_heading_section("H2 Headings", headings.get('h2', []))
    
    with tab5:
        headings = extracted_content.get('headings', {})
        display_heading_section("H3 Headings", headings.get('h3', []))
    
    # Raw JSON view
    with st.expander("🔍 View Raw JSON Output"):
        st.json(results)

def display_all_headings(extracted_content):
    """Display all headings in a consolidated view"""
    titles = extracted_content.get('titles', [])
    headings = extracted_content.get('headings', {})
    
    all_headings = []
    
    # Add titles
    for title in titles:
        all_headings.append({"type": "Title", "text": title.get('text', ''), "page": title.get('page', 0)})
    
    # Add headings
    for level in ['h1', 'h2', 'h3']:
        for heading in headings.get(level, []):
            all_headings.append({"type": level.upper(), "text": heading.get('text', ''), "page": heading.get('page', 0)})
    
    if all_headings:
        # Sort by page number
        all_headings.sort(key=lambda x: x['page'])
        
        # Display in table format
        st.dataframe(
            all_headings,
            column_config={
                "type": "Type",
                "text": "Text",
                "page": "Page"
            },
            use_container_width=True
        )
    else:
        st.info("No headings found in the document.")

def display_heading_section(title, headings_list):
    """Display a specific type of headings"""
    st.subheader(title)
    
    if headings_list:
        for i, heading in enumerate(headings_list, 1):
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{i}.** {heading.get('text', 'N/A')}")
                with col2:
                    st.caption(f"Page {heading.get('page', 'N/A')}")
                st.markdown("---")
    else:
        st.info(f"No {title.lower()} found in the document.")

def generate_text_summary(results):
    """Generate a text summary of the results"""
    doc_info = results.get('document_info', {})
    summary = results.get('extraction_summary', {})
    extracted_content = results.get('extracted_content', {})
    
    text_summary = f"""Adobe Challenge 1A - PDF Title & Heading Extraction Results
================================================================

Document Information:
- Filename: {doc_info.get('filename', 'N/A')}
- Page Count: {doc_info.get('page_count', 0)}
- Processing Time: {summary.get('processing_time_seconds', 0):.2f} seconds
- Total Headings Extracted: {summary.get('total_headings', 0)}
- Processing Status: {'Success' if summary.get('success') else 'Failed'}

Extracted Content:
==================

Titles:
-------
"""
    
    titles = extracted_content.get('titles', [])
    if titles:
        for i, title in enumerate(titles, 1):
            text_summary += f"{i}. {title.get('text', 'N/A')} (Page {title.get('page', 'N/A')})\n"
    else:
        text_summary += "No titles found.\n"
    
    # Add headings
    headings = extracted_content.get('headings', {})
    for level in ['h1', 'h2', 'h3']:
        level_headings = headings.get(level, [])
        text_summary += f"\n{level.upper()} Headings:\n" + "-" * 15 + "\n"
        
        if level_headings:
            for i, heading in enumerate(level_headings, 1):
                text_summary += f"{i}. {heading.get('text', 'N/A')} (Page {heading.get('page', 'N/A')})\n"
        else:
            text_summary += f"No {level.upper()} headings found.\n"
    
    text_summary += f"\n\nGenerated on: {doc_info.get('processing_timestamp', 'N/A')}"
    
    return text_summary

if __name__ == "__main__":
    main()