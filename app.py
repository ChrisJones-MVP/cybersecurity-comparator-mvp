
import streamlit as st
import pandas as pd
import openai
from reviews import reviews
from nist_mapping import nist_mapping

st.set_page_config(page_title="Cybersecurity Comparator", layout="centered")

# Load product data
df = pd.read_csv("product_data.csv")
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🔐 Cybersecurity Product Comparator")
st.write("Compare XDR/EDR solutions based on features, compliance, reviews and more.")

products = df["Product"].tolist()
product1 = st.selectbox("Select Product 1", products)
product2 = st.selectbox("Select Product 2", [p for p in products if p != product1])

industry = st.text_input("Industry", "Finance")
compliance = st.multiselect("Compliance Needs", ["NIST 2.0", "HIPAA", "GDPR", "ISO 27001"])
priorities = st.multiselect("Your Priorities", ["Detection", "Ease of use", "Automation", "Integration"])

if st.button("Compare Now"):
    p1 = df[df["Product"] == product1].iloc[0]
    p2 = df[df["Product"] == product2].iloc[0]

    st.subheader("🧾 Feature Comparison")
    for col in df.columns[1:]:
        st.markdown(f"**{col}**")
        st.write(f"{product1}: {p1[col]}")
        st.write(f"{product2}: {p2[col]}")
        st.markdown("---")

    st.subheader("📊 NIST 2.0 Mapping")
    for prod in [product1, product2]:
        st.markdown(f"**{prod}**")
        for key, value in nist_mapping[prod].items():
            st.write(f"{key}: {', '.join(value)}")
        st.markdown("---")

    st.subheader("🗣️ Simulated User Feedback")
    for prod in [product1, product2]:
        st.markdown(f"**{prod}**")
        st.write("👍 Pros:", reviews[prod]["Pros"])
        st.write("👎 Cons:", reviews[prod]["Cons"])
        st.markdown("---")

    st.subheader("🤖 AI-Powered Recommendation")
    prompt = f"""
    Compare {product1} and {product2} for a company in the {industry} industry.
    Priorities: {', '.join(priorities)}. Compliance: {', '.join(compliance)}.
    Product 1: {p1.to_dict()}
    Product 2: {p2.to_dict()}
    Provide a short, non-technical recommendation.
    """
    with st.spinner("Generating recommendation..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        recommendation = response.choices[0].message.content
        st.success(recommendation)
