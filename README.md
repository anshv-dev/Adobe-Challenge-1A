# 🏆 Adobe India Hackathon 2025 - PDF Intelligence Solutions

A comprehensive submission for Adobe India Hackathon 2025 featuring two distinct PDF processing challenges with advanced document intelligence capabilities.

## 📋 Challenge Overview

This repository contains complete solutions for both Adobe Hackathon challenges:

- **[Challenge 1A](./challenge-1A/)**: PDF Title & Heading Extraction System

## 🚀 Quick Start

### Challenge 1A: Title & Heading Extraction
```bash
cd challenge-1A/
streamlit run src/app.py --server.port 5000
```

## 🎯 Key Features

### Challenge 1A
- ⚡ Lightning-fast title and heading extraction (<10 seconds for 50-page PDFs)
- 📋 Adobe-compliant JSON schema output
- 🔧 CPU-only processing with zero external dependencies
- 📱 Interactive web interface with drag-and-drop upload

## 🛠 Technical Specifications

| Requirement | Challenge 1A |
|-------------|--------------|
| **Processing Time** | <10 seconds |
| **Document Capacity** | 50-page PDFs |
| **Model Size** | <200MB | 
| **Architecture** | CPU-only AMD64 |
| **Dependencies** | Offline operation  |
| **Memory Usage** | <1GB |

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
└── └── .streamlit/config.toml # Configuration


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

# Run Challenge 1A
cd challenge-1A && streamlit run src/app.py

```

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

## 👥 Team & Contact

**Submission for Adobe India Hackathon 2025**

- **Challenge Focus**: PDF Document Intelligence
- **Technology Stack**: Python, Streamlit, PyMuPDF, Plotly
- **Deployment**: Production-ready with comprehensive documentation

## 📜 License & Usage

This solution is submitted for Adobe India Hackathon 2025. All code is original and developed specifically for this challenge, meeting all specified constraints and requirements.

---

**Adobe Hackathon Challenge 1a - PDF Processing Solution Demo-Photos**  
*Delivering high-performance, schema-compliant PDF to JSON conversion*

<img width="1919" height="950" alt="Screenshot 2025-07-26 150522" src="https://github.com/user-attachments/assets/0f0c3bb3-8273-4ce6-840c-de9cd8f92f40" />
<img width="1643" height="868" alt="Screenshot 2025-07-26 150544" src="https://github.com/user-attachments/assets/8fe73bf8-9ab6-41eb-b1d3-ec7882093690" />
<img width="1919" height="933" alt="Screenshot 2025-07-26 150558" src="https://github.com/user-attachments/assets/bdf08b9e-b1a9-4cd0-8964-f8dbd55ccbb6" />
<img width="1915" height="959" alt="Screenshot 2025-07-26 150623" src="https://github.com/user-attachments/assets/c0ac80cb-b274-43ab-8aee-9a1a7e9e4d33" />


# DEMO VIDEO LINK

[![Watch the video](https://img.youtube.com/vi/qgjAGjISW98/0.jpg)](https://www.youtube.com/watch?v=qgjAGjISW98)
