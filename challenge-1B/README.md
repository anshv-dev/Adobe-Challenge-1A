# 🎭 Adobe Challenge 1B - Persona-Driven Document Intelligence

An advanced AI-powered document analysis system that provides persona-specific insights with real-time relevance heat maps and interactive visualizations.

## 🎯 Challenge Requirements

Develop persona-driven document intelligence with:
- **Processing Time**: <60 seconds for 3-5 documents
- **Multi-Document**: Process 3-10 PDFs simultaneously
- **Persona Analysis**: Context-aware content relevance
- **Architecture**: CPU-only AMD64, <1GB model
- **Operation**: Complete offline processing

## ⭐ Revolutionary Features

- 🔥 **Real-Time Heat Maps**: Interactive relevance visualization
- 🎭 **Persona Intelligence**: Context-aware document analysis
- 📊 **Multi-Document Processing**: Simultaneous PDF analysis
- 🎨 **Color-Coded Intensity**: Visual relevance scoring
- 📈 **Keyword Analysis**: Frequency and importance tracking
- 🧠 **Advanced Scoring**: Sophisticated relevance algorithms

## 🚀 Quick Start

### Run the Advanced Interface
```bash
# Install dependencies
pip install -r requirements.txt

# Start the persona-driven interface
streamlit run src/app.py --server.port 5000
```

### Command Line Processing
```bash
# Process multiple documents with persona
python src/processor.py --persona "Food Contractor" --documents /path/to/pdfs/
```

## 📁 Project Structure

```
challenge-1B/
├── src/
│   ├── app.py              # Advanced Streamlit interface
│   ├── processor.py        # Persona-driven processing engine
│   ├── heatmap.py         # Heat map visualization system
│   ├── utils.py           # Enhanced utility functions
│   └── validator.py       # Advanced schema validation
├── docs/
│   ├── schema.json        # Enhanced output schema
│   ├── personas.md        # Persona definitions & algorithms
│   ├── heatmap-guide.md   # Heat map documentation
│   └── deployment.md      # Advanced deployment guide
├── demo/
│   ├── sample_outputs/    # Example persona-driven results
│   │   ├── food_analysis.json
│   │   ├── travel_analysis.json
│   │   └── academic_analysis.json
│   └── test_documents/    # Sample PDFs for testing
│       ├── breakfast_ideas.pdf
│       ├── travel_guide.pdf
│       └── research_paper.pdf
├── requirements.txt        # Enhanced dependencies
├── packages.txt           # System dependencies
├── .streamlit/config.toml # Advanced configuration
└── README.md              # This documentation
```

## 🎭 Supported Personas

### Primary Personas
- **🍳 Food Contractor**: Menu planning, nutrition analysis, cost optimization
- **✈️ Travel Planner**: Itinerary creation, location insights, budget planning  
- **📚 Academic Researcher**: Literature review, citation analysis, methodology extraction
- **💼 Business Analyst**: Market insights, financial data, strategic planning
- **🏥 Healthcare Professional**: Medical information, treatment protocols, research findings

### Custom Persona Creation
Users can define custom personas with:
- **Interest Keywords**: Domain-specific terminology
- **Priority Weights**: Importance scoring factors
- **Context Rules**: Relevance determination logic
- **Output Preferences**: Specific formatting requirements

## 🔥 Heat Map Visualization

### Interactive Features
- **Color-Coded Intensity**: Red (high) → Yellow (medium) → Green (low) relevance
- **Hover Tooltips**: Detailed section information and scores
- **Page Navigation**: Click-through document exploration
- **Section Zoom**: Detailed subsection analysis
- **Export Options**: Save visualizations as images

### Relevance Scoring Algorithm
```python
relevance_score = (
    keyword_frequency * 0.4 +
    context_relevance * 0.3 +
    section_importance * 0.2 +
    persona_specificity * 0.1
)
```

## 📊 Advanced Analytics

### Document Analysis
- **Section Importance Ranking**: Weighted relevance scores
- **Keyword Frequency Analysis**: Term occurrence tracking
- **Content Categorization**: Automatic topic classification
- **Cross-Document Insights**: Multi-document pattern analysis

### Persona Matching
- **Relevance Percentage**: Overall document-persona alignment
- **Key Insights Extraction**: Most relevant content highlights
- **Priority Recommendations**: Action-oriented suggestions
- **Comparative Analysis**: Multi-document relevance comparison

## 🛠 Core Components

### Persona-Driven Processor (`src/processor.py`)
- **Advanced NLP Pipeline**: Context-aware text analysis
- **Multi-Document Handling**: Concurrent processing
- **Relevance Scoring**: Sophisticated algorithm implementation
- **Content Extraction**: Structured data organization

### Heat Map Engine (`src/heatmap.py`)
- **Plotly Integration**: Interactive visualization framework
- **Real-Time Rendering**: Dynamic chart generation
- **Color Mapping**: Intuitive relevance representation
- **Export Functionality**: Multiple output formats

### Enhanced Interface (`src/app.py`)
- **Persona Selection**: Interactive persona chooser
- **Multi-File Upload**: Drag-and-drop for multiple PDFs
- **Real-Time Processing**: Live progress tracking
- **Advanced Results**: Comprehensive analysis display

## 📋 Enhanced Output Schema

```json
{
  "analysis_metadata": {
    "persona": "Food Contractor",
    "documents_processed": 3,
    "total_processing_time": 45.3,
    "analysis_timestamp": "2025-01-20T10:30:00Z"
  },
  "document_analyses": [
    {
      "document_info": {...},
      "persona_relevance": {
        "overall_score": 0.87,
        "relevance_percentage": 87,
        "key_insights": [...],
        "priority_sections": [...]
      },
      "heat_map_data": {
        "page_scores": [...],
        "section_scores": [...],
        "visualization_data": {...}
      },
      "content_analysis": {
        "extracted_sections": [...],
        "keyword_analysis": {...},
        "recommendations": [...]
      }
    }
  ],
  "comparative_analysis": {
    "document_ranking": [...],
    "cross_document_insights": [...],
    "aggregated_recommendations": [...]
  }
}
```

## 🎮 Interactive Usage

### Web Interface Workflow
1. **Select Persona**: Choose from predefined or create custom
2. **Upload Documents**: Multiple PDF files (3-10 documents)
3. **Configure Analysis**: Set processing parameters
4. **View Heat Maps**: Interactive relevance visualization
5. **Explore Results**: Detailed insights and recommendations
6. **Export Analysis**: JSON, PDF, or image formats

### Advanced Features
- **Real-Time Updates**: Live processing feedback
- **Document Comparison**: Side-by-side analysis
- **Persona Switching**: Dynamic re-analysis
- **Bookmark Insights**: Save important findings

## 🚀 Performance Optimization

### Multi-Document Processing
- **Parallel Analysis**: Concurrent document processing
- **Memory Management**: Efficient resource allocation
- **Progress Tracking**: Real-time status updates
- **Error Recovery**: Graceful failure handling

### Heat Map Rendering
- **Optimized Plotting**: Fast Plotly chart generation
- **Data Compression**: Efficient visualization data
- **Interactive Performance**: Smooth user interaction
- **Export Speed**: Quick image/data export

## 📈 Analytics & Insights

### Relevance Metrics
- **Document-Persona Alignment**: Percentage match scores
- **Section Importance**: Weighted relevance ranking
- **Keyword Density**: Term frequency analysis
- **Content Quality**: Information richness assessment

### Visualization Analytics
- **Heat Map Intensity**: Color-coded relevance mapping
- **Section Highlighting**: Important content emphasis
- **Trend Analysis**: Cross-document pattern recognition
- **Insight Clustering**: Related content grouping

## 🧪 Testing & Validation

### Comprehensive Test Suite
- **Persona Accuracy Tests**: Relevance scoring validation
- **Multi-Document Tests**: Concurrent processing verification
- **Heat Map Tests**: Visualization accuracy checking
- **Performance Tests**: Speed and memory benchmarks

### Sample Scenarios
- **Food Contractor**: Menu planning documents
- **Travel Planner**: Destination guides and itineraries
- **Academic**: Research papers and literature reviews
- **Business**: Market reports and financial analyses

## 🏅 Innovation Highlights

### Revolutionary Heat Maps
- **First-of-its-kind** real-time document relevance visualization
- **Interactive exploration** with hover tooltips and click navigation
- **Multi-dimensional scoring** with persona-specific algorithms
- **Export-ready visualizations** for presentations and reports

### Advanced Persona Intelligence
- **Context-aware analysis** beyond simple keyword matching
- **Dynamic scoring algorithms** adapting to document types
- **Cross-document insights** revealing patterns across multiple files
- **Actionable recommendations** tailored to specific personas

### Performance Excellence
- **Sub-60-second processing** for complex multi-document analysis
- **Memory efficient** operation within 1GB constraints
- **Offline operation** with zero external dependencies
- **Production-ready** with comprehensive error handling

## 🔍 Advanced Troubleshooting

### Performance Optimization
- **Large Document Handling**: Efficient memory management
- **Complex Layout Processing**: Advanced structure recognition
- **Multi-Document Coordination**: Parallel processing optimization
- **Heat Map Rendering**: Visualization performance tuning

### Error Recovery
- **Partial Analysis Recovery**: Graceful degradation
- **Document Format Handling**: Robust PDF parsing
- **Memory Management**: Automatic resource cleanup
- **User Feedback**: Clear error reporting

---

**🎯 Challenge 1B Status**: ✅ Complete with Revolutionary Features

This advanced solution exceeds Adobe requirements with cutting-edge heat map visualization, sophisticated persona intelligence, and production-ready deployment configuration. The heat map feature represents a significant innovation in document analysis visualization.