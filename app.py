import streamlit as st
import tempfile
from greenwashing_radar_analysis_updated import init_gemini, evaluate_pdf_with_gemini, plot_radar

# Set up Streamlit page
st.set_page_config(page_title="Greenwashing Detection System", layout="centered")
st.title("🌿 Greenwashing Detection & Scoring System")

# Input Gemini API key
api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")

# Upload ESG PDF report
uploaded_file = st.file_uploader("📄 Upload an ESG PDF report", type=["pdf"])

# Initialize Gemini model once API key is entered
if api_key:
    init_gemini(api_key)

    if uploaded_file and st.button("🚀 Run Analysis"):
        with st.spinner("Analyzing document..."):
            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_path = tmp_file.name

            # Call the backend analysis function
            df = evaluate_pdf_with_gemini(temp_path)

            # Calculate average scores for radar chart
            avg_scores = df[["Transparency", "Specificity", "Completeness", "Consistency"]].mean().to_dict()

            # Display radar chart
            st.subheader("📊 ESG Radar Chart")
            fig = plot_radar(avg_scores)
            st.pyplot(fig)

            # Display detailed scoring results
            st.subheader("📋 Detailed Scoring Table")
            st.dataframe(df)
