# Persona Definitions and Algorithms

This document describes the personas supported by Challenge 1B and their implementation details.

## Supported Personas

### 🍳 Food Contractor
**Focus**: Menu planning, nutrition analysis, cost optimization
**Keywords**: food, menu, nutrition, recipe, ingredient, cooking, meal, diet, calorie, restaurant

### ✈️ Travel Planner  
**Focus**: Itinerary creation, location insights, budget planning
**Keywords**: travel, destination, hotel, flight, itinerary, tourism, vacation, trip, location, budget

### 📚 Academic Researcher
**Focus**: Literature review, citation analysis, methodology extraction
**Keywords**: research, study, analysis, methodology, academic, paper, citation, literature, theory, data

### 💼 Business Analyst
**Focus**: Market insights, financial data, strategic planning
**Keywords**: business, market, finance, strategy, revenue, profit, analysis, growth, investment, planning

### 🏥 Healthcare Professional
**Focus**: Medical information, treatment protocols, research findings
**Keywords**: health, medical, treatment, patient, diagnosis, therapy, clinical, medicine, care, protocol

## Relevance Scoring Algorithm

The persona-driven relevance scoring uses a multi-dimensional approach:

```
relevance_score = (
    keyword_frequency * 0.4 +
    context_relevance * 0.3 +
    section_importance * 0.2 +
    persona_specificity * 0.1
)
```

### Scoring Components

1. **Keyword Frequency (40%)**: Direct matches with persona keywords
2. **Context Relevance (30%)**: Semantic analysis of surrounding content
3. **Section Importance (20%)**: Document structure and heading analysis
4. **Persona Specificity (10%)**: Domain-specific terminology weights

