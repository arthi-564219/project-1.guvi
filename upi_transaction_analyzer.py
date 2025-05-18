import fitz  # PyMuPDF
import pandas as pd
import streamlit as st

# Step 1 & 2: PDF Parsing and Data Extraction
def extract_transactions_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    transactions = []

    for page in doc:
        text = page.get_text("text")
        # Simple line split; replace with your actual parsing logic
        lines = text.split('\n')
        for line in lines:
            # Example parsing: adjust regex or logic for your statements
            # Suppose line format: Date Time Amount Receiver Description Category
            parts = line.split()
            if len(parts) >= 6:
                transaction = {
                    "Date": parts[0],
                    "Time": parts[1],
                    "Amount": parts[2],
                    "Receiver": parts[3],
                    "Description": parts[4],
                    "Category": parts[5]
                }
                transactions.append(transaction)

    df = pd.DataFrame(transactions)
    # Clean/normalize dataframe here if needed
    return df

# Step 3 & 4: Placeholder for LLM analysis & recommendations
def analyze_transactions(df):
    # Here, you would call your Langflow or LLM API
    # For example purposes, return dummy summary
    summary = {
        "total_spent": df['Amount'].astype(float).sum(),
        "top_category": df['Category'].mode()[0] if not df.empty else None,
        "recommendation": "Consider reducing expenses on top category."
    }
    return summary

# Step 5: Streamlit UI
def main():
    st.title("UPI Transaction Analyzer")

    uploaded_file = st.file_uploader("Upload UPI PDF statement", type=["pdf"])

    if uploaded_file:
        df = extract_transactions_from_pdf(uploaded_file)
        st.write("Extracted Transactions:")
        st.dataframe(df)

        summary = analyze_transactions(df)
        st.write("Summary & Recommendations:")
        st.json(summary)

if __name__ == "__main__":
    main()
