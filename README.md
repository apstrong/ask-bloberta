# Ask Blobby

A Streamlit application that allows users to query data using natural language through the Omni API.

## Features

- Natural language query interface
- Interactive data visualization
- CSV export functionality
- "I'm Feeling Lucky" feature for example queries
- Clean and modern UI

## Setup

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your Omni API credentials:
```
OMNI_API_KEY=your_api_key_here
OMNI_BASE_URL=your_base_url_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter your question in the text input field
2. Click "✨Let's go✨" to execute the query
3. View the results in the interactive table
4. Download results as CSV if needed

## Example Queries

- Show me total revenue by month
- What are the top 10 products by sales?
- How many users signed up this week?
- Which state has the most orders?
- Show me all our open orders 