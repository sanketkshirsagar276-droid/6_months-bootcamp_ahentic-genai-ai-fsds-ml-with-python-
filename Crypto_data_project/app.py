import streamlit as st
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

# ========================
# Load Model
# ========================
model_path = 'random_forest_model.pkl'
with open(model_path, 'rb') as file:
    model_rf = pickle.load(file)

# ========================
# Prediction Function
# ========================
def predict_btc_price(input_data):
    prediction = model_rf.predict(input_data)
    return prediction[0]

# ========================
# Streamlit App
# ========================
def main():
    st.set_page_config(page_title="BTC Close Price Predictor", page_icon="💰", layout="centered")

    # ---------- Custom Dark Theme CSS ----------
    st.markdown("""
        <style>
        body {
            background-color: #0b0c10;
            color: #ffffff;
        }
        .stApp {
            background: linear-gradient(180deg, #0b0c10 0%, #1f2833 100%);
            color: #ffffff;
        }
        .main-title {
            text-align: center;
            color: #66fcf1;
            font-size: 40px;
            font-weight: 800;
            margin-bottom: 10px;
            text-shadow: 2px 2px 8px #000000;
        }
        .sub-title {
            text-align: center;
            font-size: 18px;
            color: #c5c6c7;
            margin-bottom: 40px;
        }
        .card {
            background: rgba(31, 40, 51, 0.9);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(102, 252, 241, 0.2);
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            background: linear-gradient(90deg, #45a29e, #66fcf1);
            color: black;
            font-weight: bold;
            border: none;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #66fcf1, #45a29e);
            color: #0b0c10;
        }
        .css-1v0mbdj, .css-1v3fvcr {
            color: #fff !important;
        }
        .stSidebar {
            background-color: #1f2833 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---------- Titles ----------
    st.markdown("<h1 class='main-title'>💰 Bitcoin Close Price Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Predict BTC closing price using market indicators</p>", unsafe_allow_html=True)

    # ---------- Sidebar ----------
    st.sidebar.header("📊 Input Market Data")
    usdt_close = st.sidebar.number_input("USDT Close Price", min_value=0.0, format="%.2f")
    usdt_volume = st.sidebar.number_input("USDT Volume", min_value=0.0, format="%.2f")
    bnb_close = st.sidebar.number_input("BNB Close Price", min_value=0.0, format="%.2f")
    bnb_volume = st.sidebar.number_input("BNB Volume", min_value=0.0, format="%.2f")

    # ---------- Input Data ----------
    input_data = pd.DataFrame({
        'USDT_Close': [usdt_close],
        'USDT_Volume': [usdt_volume],
        'BNB_Close': [bnb_close],
        'BNB_Volume': [bnb_volume]
    })

    # ---------- Main Section ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔍 Model Prediction")
    if st.button("🚀 Predict BTC Close Price"):
        with st.spinner("Calculating prediction..."):
            predicted_price = predict_btc_price(input_data)
        st.success("✅ Prediction Complete!")
        st.metric(label="Predicted BTC Close Price", value=f"${predicted_price:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Footer ----------
    st.markdown("""
        <br><hr style='border: 1px solid rgba(255,255,255,0.1)'>
        <p style='text-align: center; color: #c5c6c7;'>Built with ❤️ using Streamlit | Powered by Random Forest</p>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
