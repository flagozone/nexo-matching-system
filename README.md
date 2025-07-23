# 🤝 NEXO Event Matching System

A sophisticated B2B networking event scheduler for the fitness industry, built for the NEXO 2025 event (September 25-30, 2025).

## 🎯 Overview

This system facilitates business meetings between fitness companies (buyers) and suppliers/vendors (sellers) using an intelligent matching algorithm with three-tier priority system.

## 🚀 Features

- **Smart Matching Algorithm**: Three-tier priority system (Double Matches → Seller Choices → AI Suggestions)
- **Compatibility Scoring**: Multi-factor algorithm (40% interest alignment, 25% investment, 20% company size, etc.)
- **Real-time Analytics**: Interactive dashboards and visualizations
- **Schedule Management**: Automated time slot assignment with conflict resolution
- **Export Functionality**: Generate actionable meeting schedules (CSV)

## 🏗️ Architecture

- **Frontend**: Streamlit (Python web framework)
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Language**: Python 3.13

## 📊 Business Logic

1. **Double Matches** (Priority 1): When both buyer and seller select each other
2. **Seller Choices** (Priority 2): Sellers choose buyers → buyers MUST accept (sponsored obligation)
3. **AI Suggestions** (Priority 3): Algorithm fills remaining slots based on compatibility

## 🎨 User Interface

- **Dashboard**: Overview and key metrics
- **Participants**: Buyer/seller profiles and data
- **Generate Matches**: Run matching algorithm
- **Create Schedule**: Schedule meetings in time slots
- **Match Results**: View and export results
- **Analytics**: Detailed statistics and visualizations

## 🛠️ Installation

```bash
# Clone the repository
git clone <repository-url>
cd nexo-matching-system

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## 📋 Requirements

- Python 3.13+
- Streamlit >= 1.28.0
- Pandas >= 1.5.0
- Plotly >= 5.0.0

## 🌐 Deployment

This application can be deployed on:
- **Streamlit Cloud** (Recommended)
- **Heroku**
- **AWS**
- **Google Cloud Platform**

## 📈 Real Data Integration

Uses real NEXO 2023 event data including:
- 7 Major Buyers (Fitness Group, BIGG, Smart Fit, etc.)
- 11 Sellers/Vendors (Life Fitness, Technogym, etc.)
- Investment amounts ranging from $8M to $200M
- Geographic regions (Latin America, Brazil, Mexico, etc.)
- Sponsorship tiers (Platinum, Gold, Silver)

## 🤝 Contributing

This project was developed for the NEXO 2023 fitness industry event.

## 📄 License

This project is proprietary and confidential. 