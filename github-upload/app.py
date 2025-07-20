import streamlit as st
import os
import json
import time
import threading
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from challenge_processor import PDFHeadingExtractor
from challenge1b_processor import PersonaDrivenDocumentAnalyst
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
    
    st.title("📄 Adobe Hackathon PDF Processor")
    
    # Challenge selection
    challenge_type = st.selectbox(
        "Select Challenge:",
        ["Challenge 1A: PDF Title & Heading Extraction", "Challenge 1B: Persona-Driven Document Intelligence"],
        key="challenge_selector"
    )
    
    if "1A" in challenge_type:
        st.markdown("**Extract title and headings (H1, H2, H3) from PDF documents**")
        handle_challenge_1a()
    else:
        st.markdown("**Intelligent document analyst for persona-driven section extraction**")
        handle_challenge_1b()

def handle_challenge_1a():
    """Handle Challenge 1A: PDF Title & Heading Extraction"""
    
    try:
        processor = PDFHeadingExtractor()
    except Exception as e:
        st.error(f"Error initializing PDF processor: {str(e)}")
        return
    
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
            
            # Validate against challenge schema
            from schema_validator import SchemaValidator
            validator = SchemaValidator('challenge_schema.json')
            is_valid, validation_errors = validator.validate(result)
            
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

def handle_challenge_1b():
    """Handle Challenge 1B: Persona-Driven Document Intelligence"""
    
    st.markdown("---")
    
    # Input section for Challenge 1B
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Persona & Job Definition")
        
        # Persona input
        persona_role = st.selectbox(
            "Select Persona:",
            ["Food Contractor", "Academic Researcher", "Investment Analyst", "Business Analyst", 
             "Student", "Journalist", "Sales Representative", "Custom"],
            key="persona_selector"
        )
        
        if persona_role == "Custom":
            persona_role = st.text_input("Enter Custom Persona:", placeholder="e.g., Marketing Manager")
        
        # Job-to-be-done input
        job_task = st.text_area(
            "Job to be Done:",
            placeholder="Describe the specific task this persona needs to accomplish...",
            height=100,
            key="job_input"
        )
        
        # Example jobs for different personas
        if st.button("💡 Show Example Jobs"):
            examples = {
                "Food Contractor": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items.",
                "Academic Researcher": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks",
                "Investment Analyst": "Analyze revenue trends, R&D investments, and market positioning strategies",
                "Student": "Identify key concepts and mechanisms for exam preparation on reaction kinetics"
            }
            if persona_role in examples:
                st.info(f"Example: {examples[persona_role]}")
    
    with col2:
        st.subheader("📄 Document Collection")
        
        # File upload for multiple documents
        uploaded_files = st.file_uploader(
            "Upload PDF Documents (3-10 files recommended):",
            type=["pdf"],
            accept_multiple_files=True,
            key="challenge1b_files"
        )
        
        if uploaded_files:
            st.success(f"📁 {len(uploaded_files)} documents uploaded")
            
            # Show uploaded files
            for i, file in enumerate(uploaded_files):
                st.text(f"{i+1}. {file.name} ({format_file_size(len(file.getvalue()))})")
    
    # Processing section
    if uploaded_files and persona_role and job_task:
        st.markdown("---")
        
        if st.button("🔍 Analyze Documents", type="primary", key="process_1b"):
            
            # Prepare input data
            input_data = {
                "challenge_info": {
                    "challenge_id": "round_1b_001",
                    "test_case_name": "document_analysis",
                    "description": "Persona-driven document intelligence"
                },
                "documents": [{"filename": file.name, "title": file.name.replace('.pdf', '')} 
                             for file in uploaded_files],
                "persona": {"role": persona_role},
                "job_to_be_done": {"task": job_task}
            }
            
            # Save uploaded files temporarily
            temp_files = []
            for file in uploaded_files:
                temp_path = f"/tmp/{file.name}"
                with open(temp_path, "wb") as f:
                    f.write(file.getvalue())
                temp_files.append(temp_path)
            
            try:
                # Initialize analyzer
                analyzer = PersonaDrivenDocumentAnalyst()
                
                # Process documents
                with st.spinner("🔍 Analyzing documents for persona-specific insights..."):
                    result = analyzer.analyze_documents(input_data)
                
                # Display results
                st.success("✅ Analysis completed!")
                
                # Results display with heat map
                display_challenge1b_results_with_heatmap(result, persona_role, job_task)
                
                # Clean up temp files
                for temp_path in temp_files:
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                        
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
    
    elif uploaded_files:
        st.info("👆 Please define the persona and job-to-be-done to start analysis")
    else:
        st.info("👆 Please upload PDF documents to begin")

def display_challenge1b_results_with_heatmap(result, persona_role, job_task):
    """Display Challenge 1B analysis results with real-time relevance heat map"""
    
    st.header("📊 Analysis Results")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["🔥 Relevance Heat Map", "📋 Analysis Results", "💾 Export Options"])
    
    with tab1:
        # Real-time Document Relevance Heat Map
        create_relevance_heatmap(result, persona_role, job_task)
    
    with tab2:
        # Original results display
        display_traditional_results(result)
    
    with tab3:
        # Export options
        display_export_options(result)

def create_relevance_heatmap(result, persona_role, job_task):
    """Create interactive relevance heat map visualization"""
    
    st.subheader("🔥 Real-time Document Relevance Heat Map")
    st.markdown("Visual representation of document sections ranked by relevance to your persona and job")
    
    extracted_sections = result.get("extracted_sections", [])
    
    if not extracted_sections:
        st.warning("No sections available for heat map visualization")
        return
    
    # Prepare data for heat map
    heatmap_data = []
    documents = list(set([section["document"] for section in extracted_sections]))
    max_pages = max([section["page_number"] for section in extracted_sections])
    
    # Create matrix for heat map
    heat_matrix = []
    doc_labels = []
    page_labels = []
    hover_text = []
    
    for doc in documents:
        doc_sections = [s for s in extracted_sections if s["document"] == doc]
        doc_heat_row = []
        doc_hover_row = []
        
        for page in range(1, max_pages + 1):
            page_sections = [s for s in doc_sections if s["page_number"] == page]
            
            if page_sections:
                # Calculate average relevance for this page
                total_score = sum([s.get("relevance_score", 0) for s in page_sections])
                avg_score = total_score / len(page_sections)
                
                # Get section titles for hover
                section_titles = [s["section_title"] for s in page_sections]
                hover_info = f"Document: {doc}<br>Page: {page}<br>Sections: {', '.join(section_titles)}<br>Relevance: {avg_score:.2f}"
            else:
                avg_score = 0
                hover_info = f"Document: {doc}<br>Page: {page}<br>No relevant sections"
            
            doc_heat_row.append(avg_score)
            doc_hover_row.append(hover_info)
        
        heat_matrix.append(doc_heat_row)
        hover_text.append(doc_hover_row)
        doc_labels.append(doc.replace('.pdf', ''))
    
    page_labels = [f"Page {i}" for i in range(1, max_pages + 1)]
    
    # Create interactive heat map
    fig = go.Figure(data=go.Heatmap(
        z=heat_matrix,
        x=page_labels,
        y=doc_labels,
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=hover_text,
        colorscale='Reds',
        colorbar=dict(title="Relevance Score"),
        zmin=0,
        zmax=max([max(row) for row in heat_matrix]) if heat_matrix else 1
    ))
    
    fig.update_layout(
        title=f"Document Relevance for {persona_role}: {job_task[:50]}...",
        xaxis_title="Pages",
        yaxis_title="Documents",
        height=400,
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Section importance bar chart
    st.subheader("📊 Section Importance Ranking")
    
    if extracted_sections:
        # Prepare data for bar chart
        chart_data = []
        for section in extracted_sections[:10]:  # Top 10 sections
            chart_data.append({
                "Section": section["section_title"][:30] + "..." if len(section["section_title"]) > 30 else section["section_title"],
                "Relevance Score": section.get("relevance_score", 0),
                "Document": section["document"].replace('.pdf', ''),
                "Page": section["page_number"],
                "Rank": section["importance_rank"]
            })
        
        chart_df = pd.DataFrame(chart_data)
        
        # Create bar chart
        fig_bar = px.bar(
            chart_df,
            x="Relevance Score",
            y="Section",
            color="Document",
            orientation='h',
            title="Top 10 Most Relevant Sections",
            hover_data=["Page", "Rank"],
            height=400
        )
        
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Persona keyword relevance
    st.subheader("🎯 Persona Keyword Analysis")
    
    # Create keyword relevance analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Persona keywords found
        persona_keywords = get_persona_keywords(persona_role)
        job_keywords = extract_job_keywords(job_task)
        
        st.markdown(f"**Persona Keywords for {persona_role}:**")
        st.write(", ".join(persona_keywords[:10]))
        
        st.markdown(f"**Job-Specific Keywords:**")
        st.write(", ".join(job_keywords[:10]))
    
    with col2:
        # Keyword frequency in sections
        keyword_freq = analyze_keyword_frequency(extracted_sections, persona_keywords + job_keywords)
        
        if keyword_freq:
            freq_data = list(keyword_freq.items())
            freq_df = pd.DataFrame(freq_data, columns=["Keyword", "Frequency"])
            freq_df = freq_df.sort_values("Frequency", ascending=False).head(8)
            
            fig_freq = px.bar(
                freq_df,
                x="Frequency",
                y="Keyword",
                orientation='h',
                title="Keyword Frequency in Relevant Sections",
                height=300
            )
            fig_freq.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_freq, use_container_width=True)

def display_traditional_results(result):
    """Display traditional analysis results"""
    
    # Metadata section
    metadata = result.get("metadata", {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Documents Analyzed", len(metadata.get("input_documents", [])))
    
    with col2:
        st.metric("Relevant Sections", len(result.get("extracted_sections", [])))
    
    with col3:
        st.metric("Detailed Analysis", len(result.get("subsection_analysis", [])))
    
    # Show metadata
    st.subheader("📋 Analysis Metadata")
    st.json(metadata)
    
    # Extracted sections
    if result.get("extracted_sections"):
        st.subheader("🎯 Most Relevant Sections")
        
        sections_df = pd.DataFrame(result["extracted_sections"])
        st.dataframe(sections_df, use_container_width=True)
        
        # Show top sections in detail
        st.subheader("📖 Detailed Section Analysis")
        
        for i, section in enumerate(result["extracted_sections"][:3]):
            with st.expander(f"#{section['importance_rank']} - {section['section_title']} (Page {section['page_number']})"):
                st.write(f"**Document:** {section['document']}")
                st.write(f"**Page:** {section['page_number']}")
                st.write(f"**Importance Rank:** {section['importance_rank']}")
    
    # Subsection analysis
    if result.get("subsection_analysis"):
        st.subheader("🔍 Content Analysis")
        
        for analysis in result["subsection_analysis"]:
            st.markdown(f"**{analysis['document']}** (Page {analysis['page_number']})")
            st.text_area(
                "Extracted Content:",
                analysis["refined_text"],
                height=100,
                key=f"content_{analysis['document']}_{analysis['page_number']}"
            )
            st.markdown("---")
    
    # Download section
    st.subheader("💾 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON download
        json_str = json.dumps(result, indent=2)
        st.download_button(
            label="📥 Download Full Analysis (JSON)",
            data=json_str,
            file_name=f"challenge1b_analysis_{metadata.get('processing_timestamp', 'unknown').replace(':', '-')}.json",
            mime="application/json"
        )
    
    with col2:
        # Summary download
        summary = f"""
PERSONA-DRIVEN DOCUMENT ANALYSIS SUMMARY

Persona: {metadata.get('persona', 'Unknown')}
Job to be Done: {metadata.get('job_to_be_done', 'Unknown')}
Documents Analyzed: {len(metadata.get('input_documents', []))}
Processing Time: {metadata.get('processing_timestamp', 'Unknown')}

TOP RELEVANT SECTIONS:
{chr(10).join([f"{i+1}. {s['section_title']} ({s['document']}, Page {s['page_number']})" 
               for i, s in enumerate(result.get('extracted_sections', [])[:5])])}

DETAILED CONTENT ANALYSIS:
{chr(10).join([f"- {a['document']} (Page {a['page_number']}): {a['refined_text'][:100]}..." 
               for a in result.get('subsection_analysis', [])[:3]])}
        """
        
        st.download_button(
            label="📄 Download Summary (TXT)",
            data=summary.strip(),
            file_name=f"challenge1b_summary_{metadata.get('processing_timestamp', 'unknown').replace(':', '-')}.txt",
            mime="text/plain"
        )

def display_export_options(result):
    """Display export options for analysis results"""
    
    metadata = result.get("metadata", {})
    
    st.subheader("💾 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON download
        json_str = json.dumps(result, indent=2)
        st.download_button(
            label="📥 Download Full Analysis (JSON)",
            data=json_str,
            file_name=f"challenge1b_analysis_{metadata.get('processing_timestamp', 'unknown').replace(':', '-')}.json",
            mime="application/json"
        )
    
    with col2:
        # Summary download
        summary = f"""
PERSONA-DRIVEN DOCUMENT ANALYSIS SUMMARY

Persona: {metadata.get('persona', 'Unknown')}
Job to be Done: {metadata.get('job_to_be_done', 'Unknown')}
Documents Analyzed: {len(metadata.get('input_documents', []))}
Processing Time: {metadata.get('processing_timestamp', 'Unknown')}

TOP RELEVANT SECTIONS:
{chr(10).join([f"{i+1}. {s['section_title']} ({s['document']}, Page {s['page_number']})" 
               for i, s in enumerate(result.get('extracted_sections', [])[:5])])}

DETAILED CONTENT ANALYSIS:
{chr(10).join([f"- {a['document']} (Page {a['page_number']}): {a['refined_text'][:100]}..." 
               for a in result.get('subsection_analysis', [])[:3]])}
        """
        
        st.download_button(
            label="📄 Download Summary (TXT)",
            data=summary.strip(),
            file_name=f"challenge1b_summary_{metadata.get('processing_timestamp', 'unknown').replace(':', '-')}.txt",
            mime="text/plain"
        )

def get_persona_keywords(persona_role):
    """Get relevant keywords for a persona"""
    
    persona_keywords = {
        "food contractor": ["ingredients", "recipe", "menu", "dietary", "nutrition", "cooking", "preparation", "serving"],
        "travel planner": ["destination", "itinerary", "activities", "accommodation", "transport", "budget", "attractions"],
        "academic researcher": ["methodology", "analysis", "research", "study", "data", "results", "conclusions"],
        "business analyst": ["strategy", "analysis", "metrics", "performance", "trends", "market", "revenue"],
        "student": ["concepts", "definition", "examples", "theory", "practice", "learning", "education"],
        "investment analyst": ["financial", "investment", "portfolio", "risk", "returns", "market", "valuation"],
        "journalist": ["facts", "sources", "investigation", "reporting", "news", "interviews", "story"]
    }
    
    return persona_keywords.get(persona_role.lower(), ["relevant", "important", "key", "essential", "critical"])

def extract_job_keywords(job_task):
    """Extract important keywords from job description"""
    
    # Simple keyword extraction based on common terms
    important_words = []
    words = job_task.lower().split()
    
    # Common important words in job descriptions
    job_related_terms = {
        "plan", "prepare", "create", "develop", "analyze", "research", "investigate", 
        "design", "implement", "manage", "organize", "coordinate", "review", "evaluate",
        "vegetarian", "gluten-free", "buffet", "menu", "corporate", "gathering",
        "trip", "travel", "budget", "group", "college", "friends", "days", "itinerary"
    }
    
    for word in words:
        clean_word = word.strip('.,!?;:').lower()
        if clean_word in job_related_terms and len(clean_word) > 3:
            important_words.append(clean_word)
    
    return list(set(important_words))

def analyze_keyword_frequency(sections, keywords):
    """Analyze frequency of keywords in extracted sections"""
    
    keyword_freq = {keyword: 0 for keyword in keywords}
    
    for section in sections:
        section_text = (section.get("section_title", "") + " " + section.get("content", "")).lower()
        
        for keyword in keywords:
            if keyword.lower() in section_text:
                keyword_freq[keyword] += 1
    
    # Return only keywords that appear at least once
    return {k: v for k, v in keyword_freq.items() if v > 0}

if __name__ == "__main__":
    main()
