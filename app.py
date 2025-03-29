import streamlit as st
from omni_python_sdk import OmniAPI
from dotenv import load_dotenv
# from st_aggrid import AgGrid, GridOptionsBuilder
import os
import pandas as pd
import json
import requests
import random

# Load API key and base url from .env
load_dotenv()
api_key = os.getenv("OMNI_API_KEY")
base_url = os.getenv("OMNI_BASE_URL")

# Define blob names for the title
BLOB_NAMES = [
    "Bloberta",
    "Blobby",
    "Bloberton",
    "Blobsworth",
    "Sir Blobsalot",
    "Blobzilla",
    "Professor Blob",
    "Blobinator",
    "Captain Blob",
    "Blob Ross",  # A happy little blob
    "Blobastian",
    "Bloberto",
    "Lady Blobington",
    "Dr. Blob, PhD",
    "Blob Marley"
]

# Initialize session state for blob name
if "blob_name" not in st.session_state:
    st.session_state.blob_name = random.choice(BLOB_NAMES)

# Page config
st.set_page_config(
    page_title=f"Ask {st.session_state.blob_name}",
    page_icon="🤖",
    layout="wide"
)

# Define available datasets
DATASETS = {
    "eCommerce Store Sales": {
        "topic": "orders_ai",
        "model_id": "8b776a55-748b-455c-a9fc-d54791301e95",
        "description": "Ask questions about sales, orders, and revenue",
        "example_prompts": [
            "Show me total revenue by month",
            "What are the top 10 products by sales?",
            "How many users signed up this month?",
            "Which state has the most orders?",
            "Show me all our open orders",
            "Top users",
            "Highest margin products",
            "Lowest margin products",
            "Worst selling products past 30 days",
            "Best selling products past 30 days",
            "Total orders on the east coast by state",
            "Total orders on the west coast by state",
            "What is the meaning of life?",
            "Performance by channel"
        ]
    },
    "World Happiness Data": {
        "topic": "world_happiness_data",
        "model_id": "4132be68-3537-4089-9ae4-bbbaec65cc30",
        "description": "Explore measures of world happiness",
        "example_prompts": [
            "What is the happiest country?",
            "What country has the highest crime rate?",
            "Show countries by population and GDP",
            "How has happiness trended in the US over time?",
            "Show countries by happiness score",
            "Which country has the best work life balance?",
            "Which country has the worst work life balance?",
            "What is the meaning of life?"   
        ]
    },
    "Consumer Complaints": {
        "topic": "consumer_complaints",
        "model_id": "713b9178-fd14-4e1d-be56-fdbf8f57b33c",
        "description": "Analyze customer demographics and behavior",
        "example_prompts": [
            "How many complaints have there been?",
            "Show me complaints by product",
            "Which company has the most complaints?",
            "Which company is the fastest to resolve complaints?",
            "How many complaints against equifax by year?",
            "Which state complains the most?"
        ]
    }
}

# Initialize session state
if "selected_dataset" not in st.session_state:
    st.session_state.selected_dataset = "eCommerce Store Sales"

if "prompt_text" not in st.session_state:
    st.session_state["prompt_text"] = ""

if "lucky_clicked" not in st.session_state:
    st.session_state["lucky_clicked"] = False

if "previous_query" not in st.session_state:
    st.session_state["previous_query"] = None

# Inject custom CSS
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f8f9fa;
    }
    .stTextInput > div > div > input {
        font-size: 18px;
        padding: 10px;
        border-radius: 8px;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI Layout ---

st.markdown("### built on vibes by cursor")
st.title(f"Ask {st.session_state.blob_name} 🤖")

# Dataset selector using buttons in columns
st.write("#### What do you want to learn about?")
cols = st.columns(len(DATASETS))
for col, (dataset_name, dataset_info) in zip(cols, DATASETS.items()):
    if col.button(
        dataset_name,
        type="primary" if st.session_state.selected_dataset == dataset_name else "secondary",
        use_container_width=True
    ):
        st.session_state.selected_dataset = dataset_name
        # Clear prompt and previous query when switching datasets
        st.session_state["prompt_text"] = ""
        st.session_state["previous_query"] = None
        st.rerun()

# Show current dataset info
current_dataset = DATASETS[st.session_state.selected_dataset]
# st.markdown(f"**Currently exploring:** {st.session_state.selected_dataset} - {current_dataset['description']}")
# st.markdown("---")

# Initialize Omni client
client = OmniAPI(api_key, base_url=base_url)

def query_data(prompt):
    try:
        # Use the current dataset's topic and model_id
        current_dataset = DATASETS[st.session_state.selected_dataset]
        data = {
            "currentTopicName": current_dataset["topic"],
            "modelId": current_dataset["model_id"],
            "prompt": prompt
        }

        # Add contextQuery if we have a previous query
        if st.session_state["previous_query"] is not None:
            # First stringify the query object
            query_json = json.dumps({"query": st.session_state["previous_query"]})
            data["contextQuery"] = query_json

        with st.spinner("thinking..."):
            response = requests.post(f"{base_url}/api/unstable/ai/generate-query", headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json=data)
            response.raise_for_status()
            query_dict = response.json()
            
            # Store only the query part for future context
            if "query" in query_dict and isinstance(query_dict["query"], dict):
                st.session_state["previous_query"] = query_dict["query"]
            else:
                st.session_state["previous_query"] = None

        # Step 2: Run query using SDK
        query_result = client.run_query_blocking(query_dict)

        if query_result is None:
            st.error("❌ Query failed: No result returned from Omni.")
        else:
            result, _ = query_result
            df = result.to_pandas()
            st.session_state["df"] = df

            # Clean up Omni query result DataFrame
            def clean_dataframe(df):
                # 1. Drop columns containing 'raw', 'sort', 'pivot' (case-insensitive)
                df = df.loc[:, ~df.columns.str.contains("raw|pivot|sort", case=False)]

                # 2. Simplify and clean column names:
                new_columns = []
                for col in df.columns:
                    # Keep only the part after the last dot (if exists)
                    cleaned_col = col.split(".")[-1] if "." in col else col
                    # Replace underscores with spaces
                    cleaned_col = cleaned_col.replace("_", " ")
                    new_columns.append(cleaned_col)

                # 3. Apply cleaned column names
                df.columns = new_columns

                return df

            # 💵 Format sale price columns as USD
            def format_currency_columns(df):
                for col in df.columns:
                    col_lower = col.lower().replace(" ", "_")  # Normalize column names for checking
                    if any(keyword in col_lower for keyword in ["sale_price", "margin"]):
                        df[col] = df[col].apply(lambda x: f"${float(str(x).replace(',', '').replace('$', '')):,.2f}" if pd.notnull(x) else x)
                    elif "total_orders" in col_lower or "total_order" in col_lower:  # Handle variations
                        df[col] = df[col].apply(lambda x: f"{int(float(str(x).replace(',', '').replace('$', ''))):,}" if pd.notnull(x) else x)
                return df

            df = clean_dataframe(df)
            df = format_currency_columns(df)

        # Display the results
        if not df.empty:
            df.index = df.index + 1

            # Display active filters and fields
            if "query" in query_dict:
                query = query_dict["query"]
                with st.expander("🔍 Query Details", expanded=False):
                    # Show fields (dimensions and measures)
                    if "fields" in query:
                        fields = query.get("fields", [])
                        if fields:
                            st.markdown("**Fields Used:**")
                            for field in fields:
                                st.write(f"• {field}")
                            st.markdown("---")

                    # Show filters
                    filters = query.get("filters", {})
                    if filters:
                        st.markdown("**Filters Applied:**")
                        for field, filter_info in filters.items():
                            filter_type = filter_info.get("kind", "")
                            values = filter_info.get("values", [])
                            is_negative = filter_info.get("is_negative", False)
                            
                            # Format the filter description
                            operator = "is not" if is_negative else "is"
                            if isinstance(values, list):
                                values_str = ", ".join([str(v) for v in values])
                            else:
                                values_str = str(values)
                            
                            st.write(f"• {field} {operator} {filter_type.lower()} {values_str}")

            # If there's only one row and one column, display it in a card format
            if df.shape == (1, 1):
                value = df.iloc[0, 0]
                column_name = df.columns[0]
                col_lower = column_name.lower().replace(" ", "_")  # Normalize for checking
                
                # Format the value based on column name
                if "total_orders" in col_lower or "total_order" in col_lower:
                    formatted_value = f"{int(float(str(value).replace(',', '').replace('$', ''))):,}" if pd.notnull(value) else value
                elif any(keyword in col_lower for keyword in ["sale_price", "margin"]):
                    formatted_value = f"${float(str(value).replace(',', '').replace('$', '')):,.2f}" if pd.notnull(value) else value
                else:
                    formatted_value = value
                    
                st.markdown(f"""
                    <div style="padding: 2rem; background-color: #f0f2f6; border-radius: 10px; text-align: center;">
                        <h1 style="font-size: 2rem; margin-bottom: 1rem;">{formatted_value}</h1>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.dataframe(df, use_container_width=True)

            # Add vertical spacing
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Export to CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="💾 Download CSV if you must",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv"
            )
        else:
            st.warning("Query ran successfully but returned no data.")
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to generate query: {e}")
    except Exception as e:
        st.error(f"❌ Query failed: {e}")

# --- Prompt Form ---
with st.form("prompt_form"):
    prompt = st.text_input(
        label="",
        placeholder="ask away",
        value=st.session_state["prompt_text"],
        key="prompt_input"
    )

    # Create columns for the buttons, left-aligned
    col1, col2, col3 = st.columns([4, 4, 8])
    with col1:
        submitted = st.form_submit_button("✨Let's go✨", use_container_width=True)
    with col2:
        lucky = st.form_submit_button("🎲 I'm Feeling Lucky", use_container_width=True)
    with col3:
        st.write("")  # Empty space

# If lucky clicked, pick a random prompt from the current dataset
if lucky:
    st.session_state["prompt_text"] = random.choice(current_dataset["example_prompts"])
    st.session_state["lucky_clicked"] = True
    st.rerun()

# --- Advanced Settings ---
# with st.expander("⚙️ Config", expanded=False):
#     col1, col2 = st.columns(2)
#     with col1:
#         topic = st.text_input(label="", placeholder="Topic", value="orders_ai", key="topic_input")
#     with col2:
#         model_id = st.text_input(label="", placeholder="Model ID", value="8b776a55-748b-455c-a9fc-d54791301e95", key="model_id_input")

# --- Query Flow ---
if submitted and prompt.strip():
    # Easter egg for meaning of life
    cleaned_prompt = ''.join(c.lower() for c in prompt if c.isalnum() or c.isspace()).strip()
    cleaned_prompt = ' '.join(cleaned_prompt.split())  # normalize spaces
    if "what" in cleaned_prompt and "meaning" in cleaned_prompt and "life" in cleaned_prompt:
        st.markdown("""
            <div style="padding: 2rem; background-color: #f0f2f6; border-radius: 10px; text-align: center;">
                <h1 style="font-size: 4rem; margin-bottom: 1rem;">42</h1>
                <p style="font-style: italic; color: #666;">The Hitchhiker's Guide to the Galaxy</p>
                <p style="margin-top: 1rem; font-size: 0.9rem;">Confidence: 100% 🎯</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        query_data(prompt)
        