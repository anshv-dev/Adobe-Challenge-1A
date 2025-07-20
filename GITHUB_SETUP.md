# 📦 GitHub Setup and Deployment Guide

## 🚀 Quick GitHub Upload Instructions

### Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com) and log in
2. Click "New repository" (green button)
3. Repository name: `adobe-hackathon-pdf-processor` (or your choice)
4. Description: `Adobe India Hackathon 2025 - PDF Processor with Heat Map Visualization`
5. Set to **Public** (required for free Streamlit Cloud deployment)
6. ✅ Add README file (we'll replace it)
7. Click "Create repository"

### Step 2: Upload Your Code

**Option A: Web Interface (Recommended for beginners)**

1. In your new GitHub repo, click "uploading an existing file"
2. Drag and drop these key files from your Replit:

```
📁 Core Application Files:
├── app.py                          # Main Streamlit app
├── challenge_processor.py          # Challenge 1A processor  
├── challenge1b_processor.py        # Challenge 1B processor
├── utils.py                        # Utilities
├── schema_validator.py             # Schema validation

📁 Schema Files:
├── challenge_schema.json           # Challenge 1A schema
├── challenge1b_output_schema.json  # Challenge 1B schema

📁 Demo & Documentation:
├── challenge1b_demo.py             # Demo script
├── heatmap_demo.py                 # Heat map demo
├── approach_explanation.md         # Technical approach
├── README.md                       # Project documentation
├── DEPLOYMENT_GUIDE.md             # Deployment instructions

📁 Deployment Configuration:
├── streamlit_requirements.txt      # Python dependencies
├── packages.txt                    # System dependencies
├── .streamlit/config.toml          # Streamlit config
├── .gitignore                      # Git ignore rules

📁 Sample Data (Optional):
├── challenge1b_food_output.json    # Sample output
├── challenge1b_travel_output.json  # Sample output
├── heatmap_food_demo.json          # Heat map demo data
├── heatmap_travel_demo.json        # Heat map demo data
```

3. Commit with message: "Adobe Hackathon PDF Processor with Heat Map"

**Option B: Git Commands (If you have Git installed locally)**

```bash
# Download your Replit code first, then:
git init
git add .
git commit -m "Adobe Hackathon PDF Processor with Heat Map visualization"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. **Repository**: Select your uploaded repository
5. **Branch**: main
6. **Main file path**: `app.py`
7. **App URL**: Choose your subdomain (e.g., `adobe-pdf-processor`)
8. Click "Deploy!"

### Step 4: Verify Deployment

Your app will be available at: `https://YOUR_APP_NAME.streamlit.app`

**Expected Features:**
✅ Challenge 1A: PDF title & heading extraction
✅ Challenge 1B: Persona-driven document intelligence  
✅ Real-time relevance heat maps
✅ Interactive visualizations
✅ Multi-document processing
✅ Export capabilities

## 🔧 Troubleshooting

### Common Issues:

1. **Deployment Fails**
   - Ensure `streamlit_requirements.txt` is in root directory
   - Check that `app.py` is the main file
   - Verify repository is public

2. **Missing Dependencies**
   - Confirm `packages.txt` includes system dependencies
   - Check Python version compatibility (3.8+)

3. **App Doesn't Load**
   - Check Streamlit Cloud logs for errors
   - Verify all import statements work
   - Test locally first with `streamlit run app.py`

### File Checklist Before Upload:

- [ ] `app.py` (main application)
- [ ] `streamlit_requirements.txt` (dependencies)
- [ ] `.streamlit/config.toml` (configuration)
- [ ] All processor files (challenge_processor.py, etc.)
- [ ] Schema files (.json)
- [ ] README.md (documentation)

## 🎯 Repository Structure

Your final GitHub repository should look like:

```
adobe-hackathon-pdf-processor/
├── 📄 app.py                          # Main Streamlit application
├── 📄 challenge_processor.py          # Challenge 1A processor
├── 📄 challenge1b_processor.py        # Challenge 1B with heat map
├── 📄 utils.py                        # Helper functions
├── 📄 schema_validator.py             # JSON schema validation
├── 📁 .streamlit/
│   └── config.toml                    # Streamlit configuration
├── 📄 streamlit_requirements.txt      # Python dependencies
├── 📄 packages.txt                    # System dependencies
├── 📄 README.md                       # Project documentation
├── 📄 DEPLOYMENT_GUIDE.md             # Deployment instructions
└── 📄 .gitignore                      # Git ignore rules
```

## ⚡ Quick Commands for Replit Users

If you want to download your code from Replit:

1. In Replit, open Shell and run:
```bash
zip -r adobe-pdf-processor.zip . -x ".replit" "replit.nix" "uv.lock" "__pycache__/*"
```

2. Download the zip file
3. Extract and upload to GitHub

## 🎉 Success!

Once deployed, share your Streamlit Cloud URL to showcase:
- Professional PDF processing solution
- Interactive heat map visualizations  
- Both Adobe Hackathon challenges
- Production-ready deployment

Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`