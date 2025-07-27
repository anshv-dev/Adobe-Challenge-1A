# 🚀 Adobe Hackathon PDF Processor - Streamlit Cloud Deployment Guide

## Quick Deployment Steps

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Adobe Hackathon PDF Processor with Heat Map"
   git remote add origin https://github.com/YOUR_USERNAME/adobe-pdf-processor
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository
   - Set main file path: `app.py`
   - Click "Deploy!"

3. **Deployment Configuration**
   - Main file: `app.py`
   - Requirements: `streamlit_requirements.txt`
   - Python version: 3.9+
   - Advanced settings: Use `packages.txt` for system dependencies

### Option 2: Replit Deployment (Current Environment)

Since you're already on Replit, you can deploy directly:

1. **Use Replit Deployments**
   - Click the "Deploy" button in your Replit workspace
   - The app will be automatically deployed to a `.replit.app` domain
   - All dependencies are already configured

### Option 3: Local Deployment

1. **Install Dependencies**
   ```bash
   pip install -r streamlit_requirements.txt
   ```

2. **Run Locally**
   ```bash
   streamlit run app.py --server.port 8501
   ```

## 📁 Required Files for Deployment

✅ **Core Application Files:**
- `app.py` - Main Streamlit application
- `challenge_processor.py` - Challenge 1A processor
- `challenge1b_processor.py` - Challenge 1B processor
- `utils.py` - Utility functions

✅ **Schema Files:**
- `challenge_schema.json` - Challenge 1A output schema
- `challenge1b_output_schema.json` - Challenge 1B output schema

✅ **Deployment Configuration:**
- `streamlit_requirements.txt` - Python dependencies
- `packages.txt` - System dependencies
- `.streamlit/config.toml` - Streamlit configuration

✅ **Documentation:**
- `README.md` - Project documentation
- `approach_explanation.md` - Technical approach
- `replit.md` - Project architecture

## 🔧 Environment Variables (Optional)

No API keys required! The application works completely offline.

## 🎯 Deployment Features

### Challenge 1A: PDF Title & Heading Extraction
- Extract titles and headings (H1, H2, H3)
- Process documents in <10 seconds
- Adobe-compliant JSON output schema
- Drag-and-drop file upload

### Challenge 1B: Persona-Driven Document Intelligence
- Interactive persona selection
- Multi-document analysis (3-10 PDFs)
- Real-time relevance heat map visualization
- Keyword frequency analysis
- Comprehensive output with subsection analysis

### Interactive Visualizations
- Document relevance heat maps using Plotly
- Section importance ranking charts
- Keyword frequency analysis
- Persona-specific insights

## 📊 Performance Specifications

- **CPU Only**: No GPU dependencies
- **Model Size**: <200MB (lightweight processing)
- **Processing Time**: 
  - Challenge 1A: <10 seconds (50-page PDFs)
  - Challenge 1B: <60 seconds (3-5 documents)
- **Memory Usage**: <1GB
- **Offline Operation**: Zero internet dependencies

## 🚨 Troubleshooting

### Common Issues:

1. **PyMuPDF Installation**
   - Ensure `packages.txt` includes system dependencies
   - Use `PyMuPDF>=1.23.0` in requirements

2. **Plotly Charts Not Displaying**
   - Check Streamlit version >= 1.28.0
   - Verify plotly>=5.17.0 installed

3. **File Upload Errors**
   - Max file size: 200MB per PDF
   - Supported formats: PDF only
   - Check browser file size limits

### Error Recovery:
- Clear browser cache
- Restart Streamlit app
- Check deployment logs

## 🎉 Deployment Success

Once deployed, your application will feature:
- Professional UI with challenge selection
- Real-time document processing
- Interactive heat map visualizations
- Comprehensive analysis results
- Export capabilities (JSON/TXT)

## 📞 Support

For deployment issues:
1. Check Streamlit Cloud logs
2. Verify all required files are present
3. Ensure GitHub repository is public
4. Test locally first with `streamlit run app.py`

---

**Note**: This application is designed for the Adobe India Hackathon 2025 and meets all specified performance constraints for both Challenge 1A and 1B.