import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fonction de chargement des données avec mise en cache pour une meilleure performance
@st.cache_data
def load_data():
    with st.spinner(text='In progress'):
    
        df = pd.read_excel("Airbnb.xlsx")
    
        City = df["city"].unique()
        Country = df["country"].unique()
        #period = df["Day"].unique()
        Capacity = df["capacity"].unique()
        Price = df["price"].round(2).unique()
        Room_Type = df["room_type"].unique()
        Longi = df["longitude"].unique()
        Lati = df["latitude"].unique()

    return (df, Country, City, Capacity, Price, Room_Type, Longi, Lati)

# Chargement des données et récupération des données en cache
df, Country, City, Capacity, Price, Room_Type, Longi, Lati = load_data() 


#création de la catégorie filtre et des différents filtres interactifs 
st.sidebar.title("Filtres:")

ville = st.sidebar.multiselect("City:", City)
locations = df.query(f"city in @ville")

capacity_sorted = sorted(Capacity)
capacite = st.sidebar.select_slider("Number of guests:", capacity_sorted)
locations = locations.query(f"capacity == {capacite}")

price_sorted = sorted(Price)   
Max= st.sidebar.select_slider("Price:", price_sorted)
locations = locations.query(f"price <= {Max}")

type_location = st.sidebar.multiselect("Type of accomodation:", Room_Type)
locations = locations.query(f"room_type in @type_location")

        #periode = st.sidebar.radio("Période:", period)
        #locations = locations.query(f"Day == '{periode}'")


#vérification si les filtres ont été sélectionnés 
if ville and type_location :
    #création d'un tableau comprenant les données associées aux filtres choisis
    with st.expander("Locations") :
        #vérification nbr de ligne de données
        nbr_L= locations.shape[0]
        
        if nbr_L == 0 :
            st.info('No accomodations match your selection')
        affichage = ["city", "Price", "room_type", "bedrooms", "cleanliness_rating", "guest_satisfaction_overall",\
                     "dist_from_center", "dist_from_metro"]
        st.write(f"Available rental for {capacite} people with selected accomodations types: {type_location}.")
#hauteur max comprise entre nbr de ligne * 40 et 400 (pixels)
        #h_max = min(nbr_L*40, 400)
        st.dataframe(locations[affichage], height = "auto")
        st.write(f"dist_from_center and dist_from_metro represent the distances from the accomodation to the city center\
                 and the nearest metro station, expressed in km.")
        
    st.title("Available accomodation locations")
#vérification si donnée disponnible à afficher
    if nbr_L == 0 :
        st.info('No accomodations match your selection.')
#affichage des logements sur la carte
    st.map(locations)


# Gestion des cas où certaines combinaisons de filtres ne sont pas présentes
#différents Warning et de la carte vierge si ce n'est pas le cas
elif ville and not type_location:
    st.warning("Please select at least one option in 'Type of accomodation'.")
    st.title("Available accomodation locations", anchor="center")
    st.map()

elif type_location and not ville:
    st.warning("Please select at least one option in 'City'.")
    st.title("Available accomodation locations", anchor="center")
    st.map()

else: 
    st.warning("Please select at least one option in both 'City' and 'Type of acoomodation'.")

    st.title("Available accomodation locations", anchor='center')
    st.map()


#vérification si filtre ville sélectionné 
# Affichage du graphique des prix moyens en fonction des types de logements et des villes sélectionnées
if ville: 
    G1 = df.query(f"city== {ville}")
   
#Groupby par 'Room Type' et 'City', puis calculez la moyenne des prix
    grouped_df = G1.groupby(['city', 'room_type'])['price'].mean().unstack()
    # Utilisez pandas pour créer un graphique en barres groupées 
    fig, ax = plt.subplots(figsize=(6.5,5))

# Ajout de titres, légendes et réglages esthétiques 
    couleurs = ['darkcyan', 'olive', 'gold']
    grouped_df.plot(kind='bar', ax=ax, width=0.75, color = couleurs)
#Pour avoir des lignes sur l'axe y, mais pas très beau
    #ax.ticklabel_format(axis="y", style="plain", useLocale=True)
    #ax.grid(axis='y')
    plt.title('Average price by type of accomodation and city', color = 'Navy')
    plt.xlabel('City')
    plt.ylabel('Average price (€)')
    plt.legend(title='Type of accommodation', bbox_to_anchor=(1, 1), loc='upper right')
# Affichez le graphique avec Streamlit
    st.pyplot(fig)


#si condition non remplie, Warning
else:   
    st.warning("Please select at least one option in 'City' to display the average price chart")
