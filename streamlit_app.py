import streamlit as st
import requests

# Configuration de l'application Streamlit
st.set_page_config(page_title="LogiAI - Prédiction de Retard", layout="centered")

st.title("🚚 LogiAI : Prédiction et Analyse des Livraisons")

# URL de l'API FastAPI (assurez-vous qu'elle tourne sur le port 8001)
API_URL = "http://localhost:8001/v1/predict"

st.sidebar.header("Paramètres de la livraison")

# Formulaire de saisie des caractéristiques
distance_km = st.sidebar.number_input("Distance (km)", min_value=1.0, max_value=1000.0, value=120.0)
poids_kg = st.sidebar.number_input("Poids (kg)", min_value=1.0, max_value=5000.0, value=450.0)
heure_depart = st.sidebar.number_input("Heure de départ (0-23)", min_value=0.0, max_value=23.0, value=17.0)
pluie_mm = st.sidebar.number_input("Pluie (mm)", min_value=0.0, max_value=100.0, value=8.0)
trafic_index = st.sidebar.number_input("Index de trafic (0-10)", min_value=0.0, max_value=10.0, value=7.5)
nb_arrets = st.sidebar.number_input("Nombre d'arrêts", min_value=0, max_value=20, value=4)
type_vehicule = st.sidebar.selectbox("Type de véhicule", ["camion", "utilitaire", "moto", "velo"])

# Clé API optionnelle si l'authentification est activée
api_key_input = st.sidebar.text_input("Clé API (X-API-Key)", type="password")

if st.button("Évaluer"):
    # Construction du corps de la requête au format attendu par le schéma Pydantic
    livraison = {
        "distance_km": distance_km,
        "poids_kg": poids_kg,
        "heure_depart": heure_depart,
        "pluie_mm": pluie_mm,
        "trafic_index": trafic_index,
        "nb_arrets": nb_arrets,
        "type_vehicule": type_vehicule
    }
    
    headers = {}
    if api_key_input:
        headers["X-API-Key"] = api_key_input

    try:
        # Appel de l'API FastAPI avec un timeout élargi à 15 secondes pour éviter le ReadTimeout
        with st.spinner("Analyse en cours par le modèle..."):
            r = requests.post(API_URL, json=livraison, headers=headers, timeout=5)
        
        if r.status_code == 200:
            data = r.json()
            st.success("Prédiction effectuée avec succès !")
            
            # Affichage des résultats
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Probabilité de retard", value=f"{data.get('probabilite_retard', 0)*100:.1f}%")
            with col2:
                alerte = data.get('alerte', False)
                if alerte:
                    st.error("⚠️ Alerte : Risque de retard élevé !")
                else:
                    st.success("✅ Trajet stable / Pas d'alerte majeure")
                    
            st.json(data)
        else:
            st.error(f"Erreur API (Code {r.status_code}) : {r.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("Impossible de se connecter à l'API. Vérifiez que Uvicorn est bien lancé sur le port 8001.")
    except requests.exceptions.ReadTimeout:
        st.error("Le serveur a mis trop longtemps à répondre (Délai dépassé). Le modèle est peut-être en train de s'initialiser.")