# Ask Blobby 🤖

A natural language interface to your data, powered by Omni's AI. Ask questions in plain English and get instant insights from your datasets.

## ✨ Features

- **Natural Language Queries**: Ask questions about your data in plain English
- **Multiple Datasets**: Switch between different data sources:
  - eCommerce Sales Data: Orders, revenue, and product performance
  - World Happiness Data: World happiness indicators by country and year
  - Consumer Complaints: Complaints filed against financial institutions 
- **Smart Formatting**:
  - Automatic number formatting with thousands separators
  - Currency formatting for financial data
  - Beautiful card displays for single-value results
- **Fun Easter Eggs**:
  - Random blob names that change on each reload
  - Try asking "what is the meaning of life?" 😉
- **Export Features**: Download any query result as CSV

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip
- virtualenv

### Installation

1. Clone the repository:
```bash
git clone git@github.com:apstrong/ask-bloberta.git
cd ask-bloberta
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Omni API credentials
```

### Running the App

1. Activate the virtual environment (if not already activated):
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Start the Streamlit app:
```bash
streamlit run app.py
```

3. Open your browser and navigate to:
```
http://localhost:8502
```

## 💡 Example Queries

### eCommerce Sales Data
- "Show me total revenue by month"
- "What are the top 10 products by sales?"
- "Which state has the most orders?"
- "Show me all our open orders"

### World Happiness Data
- "What is the happiest country?"
- "What country has the highest crime rate?"
- "Show countries by population and GDP"
- "How has happiness trended in the US over time?"

### Consumer Complaints
- "How many complaints have there been?"
- "Show me complaints by product"
- "Which company has the most complaints?"
- "Which company is the fastest to resolve complaints?"

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) - The web framework
- [Omni APIs](https://docs.omni.co/docs/API/overview) - AI-powered data querying
- [Pandas](https://pandas.pydata.org/) - Data manipulation and analysis

## 📝 Environment Variables

The following environment variables are required:

```env
OMNI_API_KEY=your_api_key_here
OMNI_BASE_URL=your_base_url_here
```
