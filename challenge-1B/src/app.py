import streamlit as st
import sys
import os
import json
import time
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from processor import PersonaDrivenProcessor
from heatmap import HeatMapGenerator
from validator import SchemaValidator
from utils import format_file_size, format_duration

# Page configuration
st.set_page_config(
    page_title="Adobe Challenge 1B - Persona-Driven Document Intelligence",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .persona-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
    }
    .heatmap-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .results-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .metric-highlight {
        background: linear-gradient(45deg, #ff6b6b, #ffa726);
        color: white;
        padding: 0.5rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

PERSONAS = {
    "🍳 Food Contractor": {
        "description": "Menu planning, nutrition analysis, cost optimization",
        "keywords": ["food", "menu", "nutrition", "recipe", "ingredient", "cooking", "meal", "diet", "calorie", "restaurant"]
    },
    "✈️ Travel Planner": {
        "description": "Itinerary creation, location insights, budget planning",
        "keywords": ["travel", "destination", "hotel", "flight", "itinerary", "tourism", "vacation", "trip", "location", "budget"]
    },
    "📚 Academic Researcher": {
        "description": "Literature review, citation analysis, methodology extraction",
        "keywords": ["research", "study", "analysis", "methodology", "academic", "paper", "citation", "literature", "theory", "data"]
    },
    "💼 Business Analyst": {
        "description": "Market insights, financial data, strategic planning",
        "keywords": ["business", "market", "finance", "strategy", "revenue", "profit", "analysis", "growth", "investment", "planning"]
    },
    "🏥 Healthcare Professional": {
        "description": "Medical information, treatment protocols, research findings",
        "keywords": ["health", "medical", "treatment", "patient", "diagnosis", "therapy", "clinical", "medicine", "care", "protocol"]
    }
}

def initialize_session_state():
    """Initialize session state variables"""
    if 'processed_results' not in st.session_state:
        st.session_state.processed_results = None
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'selected_persona' not in st.session_state:
        st.session_state.selected_persona = None
    if 'heatmap_data' not in st.session_state:
        st.session_state.heatmap_data = None

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.title("🎭 Adobe Challenge 1B")
    st.subheader("Persona-Driven Document Intelligence with Heat Map Visualization")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Persona Selection")
        
        # Persona selection
        selected_persona = st.selectbox(
            "Choose your persona:",
            list(PERSONAS.keys()),
            index=0 if not st.session_state.selected_persona else list(PERSONAS.keys()).index(st.session_state.selected_persona)
        )
        
        if selected_persona:
            st.session_state.selected_persona = selected_persona
            persona_info = PERSONAS[selected_persona]
            
            st.markdown(f"""
            <div class="persona-card">
                <h4>{selected_persona}</h4>
                <p>{persona_info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🔍 Keywords & Focus Areas"):
                st.write("**Key Terms:**")
                for keyword in persona_info['keywords']:
                    st.write(f"• {keyword}")
        
        st.markdown("---")
        
        # Processing settings
        st.header("⚙️ Processing Settings")
        max_docs = st.slider("Max Documents", 3, 10, 5)
        max_pages = st.slider("Max Pages per Doc", 10, 100, 50)
        relevance_threshold = st.slider("Relevance Threshold", 0.0, 1.0, 0.3, 0.1)
        
        # Heat map settings
        st.subheader("🔥 Heat Map Options")
        show_heatmap = st.checkbox("Generate Heat Map", value=True)
        color_scheme = st.selectbox("Color Scheme", ["RdYlGn_r", "Viridis", "Plasma", "RdBu_r"])
        
        st.markdown("---")
        
        # System info
        st.subheader("📊 System Info")
        st.info(f"""
        **Performance Targets:**
        - Processing: <60 seconds
        - Max Documents: {max_docs}
        - Memory: <1GB
        - Architecture: CPU-only
        """)
    
    # Main content
    if not st.session_state.selected_persona:
        st.warning("👆 Please select a persona from the sidebar to begin.")
        return
    
    # Document upload section
    st.header("📁 Upload Documents for Analysis")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files (3-10 documents recommended)",
        type=['pdf'],
        accept_multiple_files=True,
        help=f"Upload 3-{max_docs} PDF documents for persona-driven analysis"
    )
    
    if uploaded_files:
        if len(uploaded_files) > max_docs:
            st.error(f"❌ Too many files. Maximum allowed: {max_docs}")
            return
        
        # Display uploaded files
        st.success(f"✅ {len(uploaded_files)} files uploaded successfully")
        
        for i, file in enumerate(uploaded_files, 1):
            file_size = len(file.read())
            file.seek(0)  # Reset file pointer
            st.write(f"**{i}.** {file.name} - {format_file_size(file_size)}")
        
        st.session_state.uploaded_files = uploaded_files
        
        # Process button
        if st.button("🚀 Analyze Documents with Persona Intelligence", type="primary"):
            process_documents(uploaded_files, selected_persona, max_pages, relevance_threshold, show_heatmap, color_scheme)
    
    # Results section
    if st.session_state.processing_complete and st.session_state.processed_results:
        display_results()

def process_documents(uploaded_files, persona, max_pages, relevance_threshold, show_heatmap, color_scheme):
    """Process uploaded documents with persona intelligence"""
    with st.spinner("🧠 Analyzing documents with persona intelligence..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize processor
            status_text.text("Initializing persona-driven processor...")
            progress_bar.progress(10)
            
            processor = PersonaDrivenProcessor(persona, PERSONAS[persona])
            
            # Save uploaded files temporarily
            temp_files = []
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Saving document {i+1}/{len(uploaded_files)}...")
                progress_bar.progress(20 + (i * 10))
                
                temp_path = f"temp_{file.name}"
                with open(temp_path, "wb") as f:
                    f.write(file.read())
                temp_files.append(temp_path)
            
            # Process documents
            status_text.text("Performing persona-driven analysis...")
            progress_bar.progress(50)
            
            start_time = time.time()
            
            processing_config = {
                'max_pages': max_pages,
                'relevance_threshold': relevance_threshold,
                'generate_heatmap': show_heatmap
            }
            
            results = processor.analyze_documents(temp_files, config=processing_config)
            
            progress_bar.progress(70)
            
            # Generate heat map if requested
            if show_heatmap:
                status_text.text("Generating interactive heat map...")
                heatmap_generator = HeatMapGenerator()
                heatmap_data = heatmap_generator.create_heatmap(results, color_scheme)
                st.session_state.heatmap_data = heatmap_data
            
            progress_bar.progress(90)
            status_text.text("Validating results...")
            
            # Validate schema
            validator = SchemaValidator()
            is_valid, validation_errors = validator.validate_challenge1b_output(results)
            
            if not is_valid:
                st.error(f"❌ Schema validation failed: {', '.join(validation_errors)}")
                return
            
            # Store results
            st.session_state.processed_results = results
            st.session_state.processing_complete = True
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Clean up temporary files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            # Display success message
            processing_time = time.time() - start_time
            st.success(f"🎉 {len(uploaded_files)} documents analyzed successfully in {processing_time:.2f} seconds!")
            
        except Exception as e:
            st.error(f"❌ Error analyzing documents: {str(e)}")
            # Clean up on error
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

def display_results():
    """Display analysis results with heat maps"""
    st.header("🎯 Persona-Driven Analysis Results")
    
    results = st.session_state.processed_results
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    analysis_meta = results.get('analysis_metadata', {})
    
    with col1:
        st.markdown('<div class="metric-highlight">', unsafe_allow_html=True)
        st.metric("Documents Analyzed", analysis_meta.get('documents_processed', 0))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-highlight">', unsafe_allow_html=True)
        st.metric("Processing Time", f"{analysis_meta.get('total_processing_time', 0):.1f}s")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-highlight">', unsafe_allow_html=True)
        avg_relevance = calculate_average_relevance(results)
        st.metric("Avg Relevance", f"{avg_relevance:.1%}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-highlight">', unsafe_allow_html=True)
        st.metric("Persona", analysis_meta.get('persona', 'N/A').split(' ')[1] if ' ' in analysis_meta.get('persona', '') else analysis_meta.get('persona', 'N/A'))
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Heat map visualization
    if st.session_state.heatmap_data:
        display_heatmap()
    
    # Document analysis tabs
    st.header("📊 Document Analysis")
    
    document_analyses = results.get('document_analyses', [])
    
    if document_analyses:
        # Create tabs for each document
        tab_names = [f"📄 Doc {i+1}" for i in range(len(document_analyses))]
        tabs = st.tabs(tab_names)
        
        for i, (tab, doc_analysis) in enumerate(zip(tabs, document_analyses)):
            with tab:
                display_document_analysis(doc_analysis, i+1)
    
    # Comparative analysis
    if len(document_analyses) > 1:
        st.header("🔍 Comparative Analysis")
        display_comparative_analysis(results.get('comparative_analysis', {}))
    
    # Export options
    st.header("💾 Export Results")
    export_results(results)

def display_heatmap():
    """Display interactive heat map visualization"""
    st.header("🔥 Document Relevance Heat Map")
    
    heatmap_data = st.session_state.heatmap_data
    
    if heatmap_data:
        # Document overview heat map
        st.subheader("📊 Document Relevance Overview")
        
        doc_scores = heatmap_data.get('document_scores', [])
        if doc_scores:
            fig = px.bar(
                x=[f"Doc {i+1}" for i in range(len(doc_scores))],
                y=doc_scores,
                title="Document Relevance Scores",
                color=doc_scores,
                color_continuous_scale="RdYlGn"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Page-level heat map
        st.subheader("📑 Page-Level Relevance")
        
        page_data = heatmap_data.get('page_heatmap', {})
        if page_data:
            # Create heatmap matrix
            docs = list(page_data.keys())
            max_pages = max(len(pages) for pages in page_data.values()) if page_data else 0
            
            if max_pages > 0:
                # Prepare data for heatmap
                heatmap_matrix = []
                page_labels = []
                
                for doc_name in docs:
                    pages = page_data[doc_name]
                    row = pages + [0] * (max_pages - len(pages))  # Pad with zeros
                    heatmap_matrix.append(row)
                
                page_labels = [f"Page {i+1}" for i in range(max_pages)]
                
                fig = go.Figure(data=go.Heatmap(
                    z=heatmap_matrix,
                    x=page_labels,
                    y=docs,
                    colorscale='RdYlGn',
                    text=[[f"{val:.2f}" for val in row] for row in heatmap_matrix],
                    texttemplate="%{text}",
                    textfont={"size": 10},
                    hoverongaps=False
                ))
                
                fig.update_layout(
                    title="Page Relevance Heat Map",
                    xaxis_title="Pages",
                    yaxis_title="Documents",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Keyword analysis
        st.subheader("🔍 Keyword Frequency Analysis")
        
        keyword_data = heatmap_data.get('keyword_analysis', {})
        if keyword_data:
            df_keywords = pd.DataFrame(list(keyword_data.items()), columns=['Keyword', 'Frequency'])
            df_keywords = df_keywords.sort_values('Frequency', ascending=False).head(20)
            
            fig = px.bar(
                df_keywords,
                x='Frequency',
                y='Keyword',
                orientation='h',
                title="Top 20 Persona-Relevant Keywords",
                color='Frequency',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)

def display_document_analysis(doc_analysis, doc_num):
    """Display analysis for a single document"""
    doc_info = doc_analysis.get('document_info', {})
    relevance = doc_analysis.get('persona_relevance', {})
    content = doc_analysis.get('content_analysis', {})
    
    # Document info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Document Information")
        st.write(f"**Filename:** {doc_info.get('filename', 'N/A')}")
        st.write(f"**Pages:** {doc_info.get('page_count', 0)}")
        st.write(f"**Size:** {format_file_size(doc_info.get('file_size', 0))}")
    
    with col2:
        st.markdown("### 🎯 Relevance Analysis")
        overall_score = relevance.get('overall_score', 0)
        st.metric("Overall Relevance", f"{overall_score:.1%}")
        
        # Relevance breakdown
        st.write("**Key Insights:**")
        for insight in relevance.get('key_insights', []):
            st.write(f"• {insight}")
    
    # Priority sections
    st.markdown("### 📑 Priority Sections")
    priority_sections = relevance.get('priority_sections', [])
    
    if priority_sections:
        for i, section in enumerate(priority_sections[:5], 1):  # Top 5 sections
            with st.expander(f"Section {i}: {section.get('title', 'Untitled')} (Relevance: {section.get('relevance_score', 0):.1%})"):
                st.write(f"**Page:** {section.get('page', 'N/A')}")
                st.write(f"**Content Preview:** {section.get('content_preview', 'No preview available')}")
                
                if 'keywords_found' in section:
                    st.write(f"**Keywords Found:** {', '.join(section['keywords_found'])}")
    else:
        st.info("No priority sections identified for this document.")
    
    # Recommendations
    recommendations = content.get('recommendations', [])
    if recommendations:
        st.markdown("### 💡 Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")

def display_comparative_analysis(comparative_data):
    """Display comparative analysis across documents"""
    
    # Document ranking
    ranking = comparative_data.get('document_ranking', [])
    if ranking:
        st.subheader("🏆 Document Relevance Ranking")
        
        ranking_df = pd.DataFrame(ranking)
        ranking_df.index = ranking_df.index + 1  # Start from 1
        
        st.dataframe(
            ranking_df,
            column_config={
                "document": "Document",
                "relevance_score": st.column_config.ProgressColumn(
                    "Relevance Score",
                    help="Overall relevance to selected persona",
                    min_value=0,
                    max_value=1,
                ),
                "key_strength": "Key Strength"
            },
            use_container_width=True
        )
    
    # Cross-document insights
    insights = comparative_data.get('cross_document_insights', [])
    if insights:
        st.subheader("🔍 Cross-Document Insights")
        for insight in insights:
            st.info(f"💡 {insight}")
    
    # Aggregated recommendations
    agg_recommendations = comparative_data.get('aggregated_recommendations', [])
    if agg_recommendations:
        st.subheader("📋 Aggregated Recommendations")
        for i, rec in enumerate(agg_recommendations, 1):
            st.write(f"{i}. {rec}")

def export_results(results):
    """Provide export options for results"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download complete JSON
        json_str = json.dumps(results, indent=2)
        st.download_button(
            label="📥 Download Complete Analysis (JSON)",
            data=json_str,
            file_name=f"persona_analysis_{int(time.time())}.json",
            mime="application/json"
        )
    
    with col2:
        # Download summary report
        summary_report = generate_summary_report(results)
        st.download_button(
            label="📄 Download Summary Report",
            data=summary_report,
            file_name=f"analysis_summary_{int(time.time())}.txt",
            mime="text/plain"
        )
    
    with col3:
        # Download heat map data
        if st.session_state.heatmap_data:
            heatmap_json = json.dumps(st.session_state.heatmap_data, indent=2)
            st.download_button(
                label="🔥 Download Heat Map Data",
                data=heatmap_json,
                file_name=f"heatmap_data_{int(time.time())}.json",
                mime="application/json"
            )

def calculate_average_relevance(results):
    """Calculate average relevance across all documents"""
    document_analyses = results.get('document_analyses', [])
    if not document_analyses:
        return 0.0
    
    total_relevance = sum(
        doc.get('persona_relevance', {}).get('overall_score', 0)
        for doc in document_analyses
    )
    
    return total_relevance / len(document_analyses)

def generate_summary_report(results):
    """Generate a comprehensive text summary report"""
    analysis_meta = results.get('analysis_metadata', {})
    document_analyses = results.get('document_analyses', [])
    comparative = results.get('comparative_analysis', {})
    
    report = f"""Adobe Challenge 1B - Persona-Driven Document Intelligence Report
================================================================

Analysis Overview:
- Persona: {analysis_meta.get('persona', 'N/A')}
- Documents Processed: {analysis_meta.get('documents_processed', 0)}
- Total Processing Time: {analysis_meta.get('total_processing_time', 0):.2f} seconds
- Analysis Timestamp: {analysis_meta.get('analysis_timestamp', 'N/A')}

Document Analysis Results:
==========================

"""
    
    for i, doc in enumerate(document_analyses, 1):
        doc_info = doc.get('document_info', {})
        relevance = doc.get('persona_relevance', {})
        
        report += f"""Document {i}: {doc_info.get('filename', 'N/A')}
----------------------------------------------
- Pages: {doc_info.get('page_count', 0)}
- Overall Relevance: {relevance.get('overall_score', 0):.1%}
- Relevance Percentage: {relevance.get('relevance_percentage', 0)}%

Key Insights:
"""
        
        for insight in relevance.get('key_insights', []):
            report += f"• {insight}\n"
        
        report += "\nPriority Sections:\n"
        for j, section in enumerate(relevance.get('priority_sections', [])[:3], 1):
            report += f"{j}. {section.get('title', 'Untitled')} (Page {section.get('page', 'N/A')}, Relevance: {section.get('relevance_score', 0):.1%})\n"
        
        report += "\n"
    
    # Add comparative analysis
    if comparative:
        report += """Comparative Analysis:
====================

Document Ranking:
"""
        for i, doc in enumerate(comparative.get('document_ranking', []), 1):
            report += f"{i}. {doc.get('document', 'N/A')} - {doc.get('relevance_score', 0):.1%}\n"
        
        report += "\nCross-Document Insights:\n"
        for insight in comparative.get('cross_document_insights', []):
            report += f"• {insight}\n"
        
        report += "\nAggregated Recommendations:\n"
        for i, rec in enumerate(comparative.get('aggregated_recommendations', []), 1):
            report += f"{i}. {rec}\n"
    
    report += f"\n\nReport generated on: {analysis_meta.get('analysis_timestamp', 'N/A')}"
    
    return report

if __name__ == "__main__":
    main()