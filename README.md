# 🏆 Adobe India Hackathon 2025 - PDF Intelligence Solutions

A comprehensive submission for Adobe India Hackathon 2025 featuring two distinct PDF processing challenges with advanced document intelligence capabilities.

## 📋 Challenge Overview

This repository contains complete solutions for both Adobe Hackathon challenges:

- **[Challenge 1A](./challenge-1A/)**: PDF Title & Heading Extraction System
- **[Challenge 1B](./challenge-1B/)**: Persona-Driven Document Intelligence with Heat Map Visualization

## 🚀 Quick Start

### Challenge 1A: Title & Heading Extraction
```bash
cd challenge-1A/
streamlit run src/app.py --server.port 5000
```

### Challenge 1B: Persona-Driven Intelligence
```bash
cd challenge-1B/
streamlit run src/app.py --server.port 5000
```

## 🎯 Key Features

### Challenge 1A
- ⚡ Lightning-fast title and heading extraction (<10 seconds for 50-page PDFs)
- 📋 Adobe-compliant JSON schema output
- 🔧 CPU-only processing with zero external dependencies
- 📱 Interactive web interface with drag-and-drop upload

### Challenge 1B ⭐
- 🎭 Advanced persona-driven document analysis
- 🔥 Real-time relevance heat maps with interactive visualization
- 📊 Multi-document processing (3-10 PDFs simultaneously)
- 🎨 Color-coded relevance intensity with Plotly integration
- 📈 Keyword frequency analysis and importance ranking
- 🧠 Sophisticated content scoring algorithms

## 🛠 Technical Specifications

| Requirement | Challenge 1A | Challenge 1B |
|-------------|--------------|--------------|
| **Processing Time** | <10 seconds | <60 seconds |
| **Document Capacity** | 50-page PDFs | 3-10 documents |
| **Model Size** | <200MB | <1GB |
| **Architecture** | CPU-only AMD64 | CPU-only AMD64 |
| **Dependencies** | Offline operation | Offline operation |
| **Memory Usage** | <1GB | <1GB |

## 📁 Repository Structure

```
adobe-challenge/
├── README.md                    # This overview document
├── challenge-1A/               # Title & Heading Extraction
│   ├── README.md               # Challenge 1A documentation
│   ├── src/                    # Source code
│   │   ├── app.py             # Streamlit web application
│   │   ├── processor.py       # Core PDF processing
│   │   ├── utils.py           # Utility functions
│   │   └── validator.py       # Schema validation
│   ├── docs/                   # Documentation
│   │   ├── schema.json        # Output schema definition
│   │   ├── approach.md        # Technical approach
│   │   └── deployment.md      # Deployment guide
│   ├── requirements.txt        # Python dependencies
│   ├── packages.txt           # System dependencies
│   └── .streamlit/config.toml # Configuration
│
└── challenge-1B/              # Persona-Driven Intelligence
    ├── README.md              # Challenge 1B documentation
    ├── src/                   # Source code
    │   ├── app.py            # Advanced Streamlit interface
    │   ├── processor.py      # Persona-driven processing
    │   ├── heatmap.py        # Heat map visualization
    │   ├── utils.py          # Utility functions
    │   └── validator.py      # Schema validation
    ├── docs/                  # Documentation
    │   ├── schema.json       # Output schema definition
    │   ├── personas.md       # Persona definitions
    │   ├── heatmap-guide.md  # Heat map documentation
    │   └── deployment.md     # Deployment guide
    ├── demo/                  # Demonstration files
    │   ├── sample_outputs/   # Example outputs
    │   └── test_documents/   # Test PDFs
    ├── requirements.txt       # Python dependencies
    ├── packages.txt          # System dependencies
    └── .streamlit/config.toml # Configuration
```

## 🎮 Live Demonstrations

Both challenges include:
- **Interactive web interfaces** with real-time processing
- **Sample PDF documents** for immediate testing
- **Example outputs** demonstrating schema compliance
- **Performance benchmarks** validating constraint adherence

## 🚀 Deployment Options

### Streamlit Cloud (Recommended)
1. Fork this repository
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Deploy individual challenges from their respective folders

### Local Development
```bash
# Install dependencies for both challenges
pip install -r challenge-1A/requirements.txt
pip install -r challenge-1B/requirements.txt

# Run Challenge 1A
cd challenge-1A && streamlit run src/app.py

# Run Challenge 1B
cd challenge-1B && streamlit run src/app.py
```

### Replit Deployment
- Each challenge folder is configured for one-click Replit deployment
- Use the provided `.replit` configuration files

## 📊 Performance Validation

Both solutions have been rigorously tested to meet Adobe's specifications:

- ✅ **Processing Speed**: All time constraints validated
- ✅ **Memory Efficiency**: Resource usage within limits
- ✅ **Offline Operation**: Zero internet dependencies
- ✅ **Schema Compliance**: Output validation implemented
- ✅ **Architecture Compatibility**: AMD64 CPU-only operation

## 🏅 Innovation Highlights

### Challenge 1A
- Optimized PDF parsing with PyMuPDF
- Intelligent heading detection algorithms
- Real-time processing feedback
- Error handling and validation

### Challenge 1B ⭐
- **World-class heat map visualization** with Plotly
- **Advanced persona matching algorithms**
- **Multi-dimensional relevance scoring**
- **Interactive document exploration**
- **Real-time keyword analysis**

## 👥 Team & Contact

**Submission for Adobe India Hackathon 2025**

- **Challenge Focus**: PDF Document Intelligence
- **Technology Stack**: Python, Streamlit, PyMuPDF, Plotly
- **Deployment**: Production-ready with comprehensive documentation

## 📜 License & Usage

This solution is submitted for Adobe India Hackathon 2025. All code is original and developed specifically for this challenge, meeting all specified constraints and requirements.

---

**🎯 Ready for Evaluation**: Both challenges are complete, documented, and deployment-ready with comprehensive testing and validation.