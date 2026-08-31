import streamlit as st
import pandas as pd
import joblib
import os

# ============================================================
# PATHS — built relative to this script's own location,
# so it works no matter which folder you launch Streamlit from
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "cleaned", "master_dataset.xlsx")
SRC_PATH = os.path.join(BASE_DIR, "..", "src")

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="Tourism Experience Analytics", layout="wide")
st.title("🌍 Tourism Experience Analytics")
st.write("Get personalized attraction recommendations, rating predictions, and visit mode predictions.")

# ============================================================
# LOAD DATA + MODELS (all at once, cached so it doesn't reload on every click)
# ============================================================
@st.cache_data
def load_data():
    master = pd.read_excel(DATA_PATH)
    return master

@st.cache_resource
def load_models():
    regression_model = joblib.load(os.path.join(SRC_PATH, "regression_model.pkl"))
    regression_features = joblib.load(os.path.join(SRC_PATH, "regression_features.pkl"))
    classification_model = joblib.load(os.path.join(SRC_PATH, "classification_model.pkl"))
    classification_features = joblib.load(os.path.join(SRC_PATH, "classification_features.pkl"))
    label_encoder = joblib.load(os.path.join(SRC_PATH, "label_encoder.pkl"))
    content_similarity = joblib.load(os.path.join(SRC_PATH, "content_similarity.pkl"))
    attraction_info_full = joblib.load(os.path.join(SRC_PATH, "attraction_info_full.pkl"))
    return (regression_model, regression_features, classification_model,
            classification_features, label_encoder, content_similarity, attraction_info_full)

master = load_data()
(regression_model, regression_features, classification_model,
 classification_features, label_encoder, content_similarity, attraction_info_full) = load_models()

# ============================================================
# SIDEBAR — shared user inputs
# ============================================================
st.sidebar.header("Enter Your Details")

visit_mode_options = ['Business', 'Couples', 'Family', 'Friends', 'Solo']
attraction_type_options = sorted(master['AttractionType'].unique())
continent_options = sorted(master['Continent'].unique())

visit_mode = st.sidebar.selectbox("Visit Mode", visit_mode_options)
attraction_type = st.sidebar.selectbox("Attraction Type", attraction_type_options)
continent = st.sidebar.selectbox("Continent", continent_options)

regions_for_continent = sorted(master[master['Continent'] == continent]['Region'].unique())
region = st.sidebar.selectbox("Region", regions_for_continent)

countries_for_region = sorted(master[master['Region'] == region]['Country'].unique())
country = st.sidebar.selectbox("Country", countries_for_region)

visit_year = st.sidebar.number_input("Visit Year", min_value=2013, max_value=2026, value=2024)
visit_month = st.sidebar.selectbox("Visit Month", list(range(1, 13)))
rating_input = st.sidebar.slider("Your Typical Rating", min_value=1, max_value=5, value=4)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["⭐ Rating Prediction", "🧳 Visit Mode Prediction", "📍 Recommendations"])

# ------------------------------------------------------------
# TAB 1 — Regression: Predict Rating
# ------------------------------------------------------------
with tab1:
    st.write("### Predicted Rating")
    st.write("Based on your visit mode, attraction type, and location.")

    if st.button("Predict Rating"):
        input_df = pd.DataFrame([{
            'VisitMode': visit_mode,
            'AttractionType': attraction_type,
            'Continent': continent,
            'Region': region,
            'Country': country,
            'VisitYear': visit_year,
            'VisitMonth': visit_month
        }])

        input_encoded = pd.get_dummies(input_df, columns=['VisitMode', 'AttractionType', 'Continent', 'Region', 'Country'])
        input_encoded = input_encoded.reindex(columns=regression_features, fill_value=0)

        prediction = regression_model.predict(input_encoded)[0]
        st.success(f"Predicted Rating: {prediction:.2f} / 5")

# ------------------------------------------------------------
# TAB 2 — Classification: Predict Visit Mode
# ------------------------------------------------------------
with tab2:
    st.write("### Predicted Visit Mode")
    st.write("Based on attraction type, location, and your typical rating behavior.")

    if st.button("Predict Visit Mode"):
        input_df = pd.DataFrame([{
            'AttractionType': attraction_type,
            'Continent': continent,
            'Region': region,
            'Country': country,
            'VisitYear': visit_year,
            'VisitMonth': visit_month,
            'Rating': rating_input
        }])

        input_encoded = pd.get_dummies(input_df, columns=['AttractionType', 'Continent', 'Region', 'Country'])
        input_encoded = input_encoded.reindex(columns=classification_features, fill_value=0)
        

        prediction_encoded = classification_model.predict(input_encoded)[0]
        prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

        st.success(f"Predicted Visit Mode: {prediction_label}")

# ------------------------------------------------------------
# TAB 3 — Content-Based Recommendations
# ------------------------------------------------------------
with tab3:
    st.write("### Attraction Recommendations")
    st.write("Pick an attraction you like, and we'll suggest similar ones from our full catalog.")

    attraction_names = sorted(attraction_info_full['Attraction'].unique())
    selected_attraction_name = st.selectbox("Pick an attraction you've enjoyed", attraction_names)

    if st.button("Get Recommendations"):
        selected_id = attraction_info_full[attraction_info_full['Attraction'] == selected_attraction_name]['AttractionId'].iloc[0]

        similar_scores = content_similarity[selected_id].drop(selected_id)
        top_similar = similar_scores.sort_values(ascending=False).head(5)

        result = attraction_info_full[attraction_info_full['AttractionId'].isin(top_similar.index)].copy()
        result = result.drop_duplicates(subset='AttractionId')
        result['SimilarityScore'] = result['AttractionId'].map(top_similar)
        result = result.sort_values('SimilarityScore', ascending=False)

        st.write("#### Recommended Attractions:")
        st.dataframe(result[['Attraction', 'AttractionType', 'SimilarityScore']], hide_index=True)

    