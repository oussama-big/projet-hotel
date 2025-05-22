import streamlit as st
import sqlite3
from datetime import date

# Connexion à la base SQLite
conn = sqlite3.connect('hotel.db', check_same_thread=False)
cursor = conn.cursor()

st.title("🏨 Application de gestion d'hôtel")

menu = st.sidebar.selectbox("Navigation", [
    "Voir les réservations",
    "Voir les clients",
    "Chambres disponibles",
    "Ajouter un client",
    "Ajouter une réservation"
])

# 1. Voir les réservations
if menu == "Voir les réservations":
    st.subheader("📅 Liste des réservations")
    cursor.execute("""
        SELECT r.id, c.nom, r.date_debut, r.date_fin, ch.numero, h.ville
        FROM Reservation r
        JOIN Client c ON r.client_id = c.id
        JOIN Chambre ch ON r.chambre_id = ch.id
        JOIN Hotel h ON ch.hotel_id = h.id
    """)
    rows = cursor.fetchall()
    st.table(rows)

# 2. Voir les clients
elif menu == "Voir les clients":
    st.subheader("👤 Liste des clients")
    cursor.execute("SELECT * FROM Client")
    rows = cursor.fetchall()
    st.table(rows)

# 3. Chambres disponibles
elif menu == "Chambres disponibles":
    st.subheader("🔍 Chambres disponibles")
    d1 = st.date_input("Date d'arrivée", date.today())
    d2 = st.date_input("Date de départ", date.today())
    if d1 < d2:
        query = """
        SELECT * FROM Chambre
        WHERE id NOT IN (
            SELECT chambre_id FROM Reservation
            WHERE NOT (date_fin < ? OR date_debut > ?)
        )
        """
        cursor.execute(query, (d1, d2))
        rows = cursor.fetchall()
        st.table(rows)
    else:
        st.warning("La date d'arrivée doit être avant la date de départ.")

# 4. Ajouter un client
elif menu == "Ajouter un client":
    st.subheader("➕ Ajouter un nouveau client")
    with st.form("form_client"):
        nom = st.text_input("Nom")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code_postal = st.number_input("Code postal", step=1)
        email = st.text_input("Email")
        telephone = st.text_input("Téléphone")
        submitted = st.form_submit_button("Ajouter")
        if submitted:
            cursor.execute("INSERT INTO Client (nom, adresse, ville, code_postal, email, telephone) VALUES (?, ?, ?, ?, ?, ?)",
                           (nom, adresse, ville, code_postal, email, telephone))
            conn.commit()
            st.success("Client ajouté avec succès ✅")

# 5. Ajouter une réservation
elif menu == "Ajouter une réservation":
    st.subheader("📝 Ajouter une réservation")
    cursor.execute("SELECT id, nom FROM Client")
    clients = cursor.fetchall()
    client_map = {f"{nom} (id: {id})": id for id, nom in clients}
    client_choice = st.selectbox("Client", list(client_map.keys()))
    
    cursor.execute("SELECT id, numero FROM Chambre")
    chambres = cursor.fetchall()
    chambre_map = {f"Chambre {num} (id: {id})": id for id, num in chambres}
    chambre_choice = st.selectbox("Chambre", list(chambre_map.keys()))
    
    date_debut = st.date_input("Date d'arrivée")
    date_fin = st.date_input("Date de départ")
    
    if st.button("Réserver"):
        if date_debut < date_fin:
            cursor.execute("INSERT INTO Reservation (date_debut, date_fin, client_id, chambre_id) VALUES (?, ?, ?, ?)",
                           (date_debut, date_fin, client_map[client_choice], chambre_map[chambre_choice]))
            conn.commit()
            st.success("Réservation enregistrée ✅")
        else:
            st.error("Date d'arrivée doit être avant la date de départ.")
