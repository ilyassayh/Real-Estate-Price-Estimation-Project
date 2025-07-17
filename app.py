import streamlit as st
import numpy as np
import pandas as pd
import joblib

# --- City mapping (from notebook) ---
CITY_MAPPING = {
    'Agadir': 0, 'Agadir Melloul': 1, 'Ain Aouda': 2, 'Ain Attig': 3, 'Asilah': 4, 'Benslimane': 5, 'Berkane': 6, 'Berrechid': 7, 'Biougra': 8, 'Bouskoura': 9, 'Bouznika': 10, 'Béni Mellal': 11, 'Cabo Negro': 12, 'Casablanca': 13, 'Dakhla': 14, 'Dar Bouazza': 15, 'Dcheira': 16, 'Dcheïra El Jihadia': 17, 'Deroua': 18, 'El Jadida': 19, 'El Ksiba': 20, 'El Mansouria': 21, 'El Menzeh': 22, 'Essaouira': 23, 'Fnideq': 24, 'Fès': 25, 'Had Soualem': 26, 'Ifrane': 27, 'Inzegan': 28, 'Khemisset': 29, 'Khouribga': 30, 'Kénitra': 31, 'Marrakech': 32, 'Martil': 33, 'Mdiq': 34, 'Mehdia': 35, 'Meknès': 36, 'Mers El Kheir': 37, 'Mohammedia': 38, 'Nador': 39, 'Nouaceur': 40, 'Oued Laou': 41, 'Oued Zem': 42, 'Oujda': 43, 'Rabat': 44, 'Safi': 45, 'Saidia': 46, 'Salé': 47, 'Sefrou': 48, 'Selouane': 49, 'Settat': 50, 'Sidi Allal El Bahraoui': 51, 'Sidi Bennour': 52, 'Sidi Bouknadel': 53, 'Sidi Rahal': 54, 'Skhirat': 55, 'Taghazout': 56, 'Tamaris': 57, 'Tamesna': 58, 'Tanger': 59, 'Taounate': 60, 'Taza': 61, 'Temara': 62, 'Tit Mellil': 63, 'Tiznit': 64, 'Tétouan': 65, 'Unknown': 66
}

# --- Equipment and keyword features ---
EQUIPMENTS = [
    'Ascenseur', 'Balcon', 'Chauffage', 'Climatisation', 'Concierge',
    'Cuisine Équipée', 'Duplex', 'Meublé', 'Parking', 'Sécurité', 'Terrasse'
]
KEYWORDS = ['luxe', 'neuf', 'meublé', 'piscine', 'terrasse']

# --- Load model ---
@st.cache(allow_output_mutation=True)
def load_model():
    return joblib.load('final_modele.joblib')
model = load_model()

# --- Title ---
st.title('Estimation Immobilière Avito (XGBoost)')
st.write('Remplissez les informations pour estimer le prix de votre bien immobilier.')

# --- Form ---
with st.form('prediction_form'):
    col1, col2 = st.columns(2)
    with col1:
        salon = st.number_input('Nombre de salons', min_value=0, max_value=8, value=1)
        nb_rooms = st.number_input('Nombre de chambres', min_value=1, max_value=10, value=2)
        nb_baths = st.number_input('Nombre de salles de bain', min_value=0, max_value=10, value=1)
        surface_area = st.number_input('Surface (m²)', min_value=10, max_value=1000, value=80)
    with col2:
        city = st.selectbox('Ville', list(CITY_MAPPING.keys()), index=0)
        price = st.number_input('Prix (DH)', min_value=10000, max_value=10000000, value=1000000)
    st.markdown('---')
    st.write('**Équipements**')
    equipment_selected = [st.checkbox(eq) for eq in EQUIPMENTS]
    st.markdown('---')
    st.write('**Mots-clés du titre** (cochez si le mot apparaît dans le titre de votre annonce)')
    keyword_selected = [st.checkbox(f"Mot-clé: {kw}") for kw in KEYWORDS]
    st.markdown('---')
    submitted = st.form_submit_button('Estimer le prix')

if submitted:
    # --- Prepare features ---
    city_encoded = CITY_MAPPING[city]
    # For city_target_enc, in real app, you would use the mean price for the city from training data. Here, we use the input price as a proxy.
    city_target_enc = price  # Approximation, since we don't have the mapping here
    price_per_m2 = price / surface_area if surface_area > 0 else 0
    # Build feature vector in the right order
    features = [
        salon, nb_rooms, nb_baths, surface_area, price_per_m2,
        city_encoded, city_target_enc
    ]
    features += [int(k) for k in keyword_selected]
    features += [int(e) for e in equipment_selected]
    # Convert to DataFrame for model
    input_df = pd.DataFrame([features], columns=[
        'salon', 'nb_rooms', 'nb_baths', 'surface_area', 'price_per_m2',
        'city_encoded', 'city_target_enc',
        'kw_luxe', 'kw_neuf', 'kw_meublé', 'kw_piscine', 'kw_terrasse',
        'Ascenseur', 'Balcon', 'Chauffage', 'Climatisation', 'Concierge',
        'Cuisine Équipée', 'Duplex', 'Meublé', 'Parking', 'Sécurité', 'Terrasse'
    ])
    # --- Predict ---
    prediction = model.predict(input_df)[0]
    st.success(f"Prix estimé : {prediction:,.0f} DH") 