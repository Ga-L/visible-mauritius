import pandas as pd
import streamlit as st
import base64

# Load the dataset
file_path = "datasets/polling_stations_2023.csv"  # Update with the correct file path
df_polling_stations = pd.read_csv(file_path)

# Set favicon
favicon_path = "fav_icon.png"

st.set_page_config(
    page_title="Visible Mauritius",
    layout="wide",
    page_icon=favicon_path  # Set the favicon
)

# Read the SVG image as binary
with open("logo.svg", "rb") as svg_file:
    svg_binary = svg_file.read()

# Convert the binary data to base64
svg_base64 = base64.b64encode(svg_binary).decode()

# Display the logo using HTML
st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/svg+xml;base64,{svg_base64}" width="85">
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

# Create a dictionary mapping constituencies to their polling stations
constituency_polling_stations = {
    "Grand River North West and Port Louis West": [
        "Xavier Christian Barbe Government School",
        "New Pailles Government School",
        "Pailles State Secondary School (Girls)",
        "Richelieu Government School",
        "Pointe Aux Sables Government School",
        "J. M. Frank Richard State Secondary School",
        "New La Tour Koenig Government School",
        "La Tour Koenig Government School",
        "Grand River North West Government School",
        "Residence Vallijee Government School",
        "Dr. James Burty David State Secondary School",
        "Renganaden Seeneevassen Government School",
        "Medco Cassis Secondary School",
        "Dr. Edgar Millien Government School",
    ],
    "Port Louis South and Port Louis Central": [
        "Raoul Rivet Government School",
        "Notre Dame De Bon Secours Roman Catholic Aided School",
        "Renganaden Seeneevassen State Secondary School",
        "Labourdonnais Government School",
        "Guy Rozemont Government School",
        "Surtee Soonnee Government School",
        "G.M.D. Atchia State College",
        "St. Jean Baptiste De La Salle Roman Catholic Aided School",
        "Notre Dame De La Paix Roman Catholic Aided School",
    ],
    "Port Louis Maritime And Port Louis East": [
        "Sir Abdool Razack Mohamed State Secondary School",
        "Villiers Rene Government School",
        "Dr. Idrice A. Goumany Government School",
        "Jean Lebrun Government School",
        "Coeur Sacre De Jesus Roman Catholic Aided School",
        "St. Francois Xavier Roman Catholic Aided School",
        "Emmanuel Anquetil Government School",
        "Abdool Rahman Abdool Government School",
        "La Fourche Community Centre",
        "Sainte Rita Government School",
        "Jacques Le Chartier Government School",
        "Abercrombie Training Centre",
    ],
    # Add other constituencies here
}

# Create a Streamlit selectbox for selecting constituencies
st.markdown("<h2 style='font-size: 25px;'>Find & locate your Polling Station</h2>", unsafe_allow_html=True)

# Create a two-column layout
col1, col2 = st.columns(2)

# Display the "Your Constituency" picker and table in col1
with col1:
    # Create a Streamlit selectbox for selecting constituencies
    selected_constituency = st.selectbox("Your Constituency", list(constituency_polling_stations.keys()))

    if selected_constituency:
        polling_stations = constituency_polling_stations[selected_constituency]
        st.write("Polling Stations:")
        st.table(pd.DataFrame(polling_stations, columns=["Polling Stations"]))

# Add a search bar next to the picker in col2
with col2:
    search_query = st.text_input("Enter Polling Station Name:", "")
    
    # Check if search_query is not empty
    if search_query:
        # Define a dictionary to map polling station names to Google Maps iframe URLs
        polling_station_urls = {
            #constituency 1
            "Xavier Christian Barbe Government School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3744.6866344775267!2d57.4816887741123!3d-20.188768946416506!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c5012bcbc54a9%3A0x4e29f6d0cfeffe03!2sXavier%20Christian%20Barbe%20Government%20School!5e0!3m2!1sen!2smu!4v1694528582118!5m2!1sen!2smu",
            "New Pailles Government School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.0138911004757!2d57.486214114112045!3d-20.160967486404693!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c9534d8de6a67%3A0x6827c1d2ab3ac04a!2sNew%20Pailles%20Government%20School!5e0!3m2!1sen!2smu!4v1630509055466!5m2!1sen!2smu",
            "Pailles State Secondary School (Girls)": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14978.690315879247!2d57.476212055419886!3d-20.189353799999985!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c506fae859845%3A0x6577709f8e00cce1!2sPailles%20State%20Secondary%20School!5e0!3m2!1sen!2smu!4v1694509356555!5m2!1sen!2smu",
            "Richelieu Government School":"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3744.6518226520825!2d57.45365257411233!3d-20.19021744646213!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c4ff947e59d41%3A0xb091b7b9d3ac18b2!2sRichelieu%20Government%20School!5e0!3m2!1sen!2smu!4v1694509818361!5m2!1sen!2smu",
            "Pointe Aux Sables Government School":"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.0836454020464!2d57.44252848885498!3d-20.172242500000003!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c4fe9ea27b17b%3A0xa7bb14faadec036b!2sPointe%20aux%20Sables%20Government%20School!5e0!3m2!1sen!2smu!4v1694510262698!5m2!1sen!2smu",
            "J. M. Frank Richard State Secondary School":"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.085087499527!2d57.46423757411167!3d-20.17218244589345!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c50210d0803c5%3A0x956305b9059d4d4d!2sFrank%20Richard%20State%20Secondary%20School!5e0!3m2!1sen!2smu!4v1694510402605!5m2!1sen!2smu",
            "New La Tour Koenig Government School":"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.0743137328973!2d57.46043228885499!3d-20.1726311!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c518a416ddc7d%3A0xde43ec2771c452fc!2sNew%20La%20Tour%20Koenig%20Govt%20School!5e0!3m2!1sen!2smu!4v1694510685323!5m2!1sen!2smu",
            "La Tour Koenig Government School":"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.0385308292666!2d57.46430037411168!3d-20.174121145954597!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c5018a9943617%3A0x8b01816b385b80d5!2sOld%20La%20Tour%20Koenig%20Govt%20School!5e0!3m2!1sen!2smu!4v1694511025481!5m2!1sen!2smu",
            "Grand River North West Government School":"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14980.303630852199!2d57.45270744243371!3d-20.172564722170236!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c5022c82a1039%3A0xd60edd6bcc9f291d!2sGRNW%20Government%20School!5e0!3m2!1sen!2smu!4v1694511210162!5m2!1sen!2smu",
            "Residence Vallijee Government School":"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.144495238993!2d57.47657957411152!3d-20.16970834581551!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c503a2c434445%3A0xd0f1693f800fb4e1!2sResidence%20Valijee%20Government%20School!5e0!3m2!1sen!2smu!4v1694511457865!5m2!1sen!2smu",
            "Dr. James Burty David State Secondary School":"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.023751485876!2d57.48118987411178!3d-20.17473654597401!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c503f3fe7f5d7%3A0x3c0288598ac6ab48!2sDr.%20James%20Burty%20David%20SSS!5e0!3m2!1sen!2smu!4v1694511936625!5m2!1sen!2smu",
            "Renganaden Seeneevassen Government School":"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.313750142332!2d57.4857767741113!3d-20.162657945593363!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c504bb5a519d7%3A0xbd5352e3e4d570fc!2sRenganaden%20Seeneevassen%20Government%20School!5e0!3m2!1sen!2smu!4v1694512121839!5m2!1sen!2smu",
            "Medco Cassis Secondary School":"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.2808465752296!2d57.4850798741113!3d-20.164028745636543!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c504987000001%3A0x784f8da91398e349!2sMEDCO%20Cassis%20Secondary%20School!5e0!3m2!1sen!2smu!4v1694512248167!5m2!1sen!2smu",
            "Dr. Edgar Millien Government School":"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.249758079789!2d57.49112367411131!3d-20.165323845677428!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c51df6b3e3b75%3A0x1f4f95234cea726b!2sDr.%20Edgar%20Millien%20Government%20School!5e0!3m2!1sen!2smu!4v1694512670927!5m2!1sen!2smu",
            
            #constituency 2
            "Raoul Rivet Government School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.1640945870918!2d57.50067687411155!3d-20.168892045789747!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c5056c4f87b49%3A0x31f84db68a337a64!2sRaoul%20Rivet%20Government%20School!5e0!3m2!1sen!2smu!4v1694520028301!5m2!1sen!2smu",
            "Notre Dame De Bon Secours Roman Catholic Aided School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.2228520601107!2d57.500551774111344!3d-20.16644464571277!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c511be5b41a23%3A0x6f7f725ee876e153!2sNotre%20Dame%20De%20Bon%20Secours%20RCA!5e0!3m2!1sen!2smu!4v1694519647187!5m2!1sen!2smu",
            "Renganaden Seeneevassen State Secondary School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.0143298492485!2d57.50288097411166!3d-20.175128845986443!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c505856ec3e47%3A0xaa427463fbd14df0!2sRenganaden%20Seeneevassen%20SSS!5e0!3m2!1sen!2smu!4v1694518235633!5m2!1sen!2smu",
            "Labourdonnais Government School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.0098843512756!2d57.503569274111726!3d-20.175313945992247!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c5058593dd5c9%3A0xd08da87269430ffb!2sLabourdonnais%20Government%20School%2C%20Justice%20St%2C%20Port%20Louis!5e0!3m2!1sen!2smu!4v1694520240885!5m2!1sen!2smu",
            "Guy Rozemont Government School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3744.964464060854!2d57.51025317411185!3d-20.177205046051856!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c50f6d99661a7%3A0x922dba025dc16e13!2sGuy%20Rosemont%20Government%20School!5e0!3m2!1sen!2smu!4v1694520391921!5m2!1sen!2smu",
            "Surtee Soonnee Government School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.186437348789!2d57.514342274111456!3d-20.167961445760458!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c50fcf0f2cd33%3A0x32aade100006e6!2sSurtee%20Sunee%20Government%20School!5e0!3m2!1sen!2smu!4v1694520682970!5m2!1sen!2smu",
            "G.M.D. Atchia State College": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.101615562961!2d57.509802074111576!3d-20.171494145871836!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c50f97569d71f%3A0x2081709955e3b2f5!2sG.M.D.%20Atchia%20State%20College!5e0!3m2!1sen!2smu!4v1694520814954!5m2!1sen!2smu",
            "St. Jean Baptiste De La Salle Roman Catholic Aided School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.199276907074!2d57.50535257411153!3d-20.16742664574367!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c5055f92b1cf3%3A0xe409dc288a144f5c!2sSaint-Jean-Baptiste-de-la-Salle%20R.C.A.%20School!5e0!3m2!1sen!2smu!4v1694520962498!5m2!1sen!2smu",
            "Notre Dame De La Paix Roman Catholic Aided School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.3564294130992!2d57.50848777411111!3d-20.16087974553732!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c5100550466d5%3A0xcfd67cffe3725ac3!2sNotre%20Dame%20de%20la%20Paix%20RCA!5e0!3m2!1sen!2smu!4v1694521078373!5m2!1sen!2smu",
            
            #constituency 3
            "Sir Abdool Razack Mohamed State Secondary School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14980.858005025875!2d57.48723051486863!3d-20.16679249554377!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c5055c9294a53%3A0x6613a36472bd9577!2sSir%20Abdool%20Razack%20Mohamed%20State%20Secondary%20School!5e0!3m2!1sen!2smu!4v1694521224790!5m2!1sen!2smu",
            "Villiers Rene Government School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.401917674698!2d57.505681574111115!3d-20.158984345477634!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c51009f400001%3A0xc8e9eb8a89ffb3b3!2sVilliers%20Ren%C3%A9%20Government%20School!5e0!3m2!1sen!2smu!4v1694521383561!5m2!1sen!2smu",
            "Dr. Idrice A. Goumany Government School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14980.748197874836!2d57.50661743333045!3d-20.167935949728964!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c514299653d6b%3A0xcb5858987f05f0be!2sDr%20I.%20A%20Goumany%20Govt%20School!5e0!3m2!1sen!2smu!4v1694521507642!5m2!1sen!2smu",
            "Jean Lebrun Government School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.384739461813!2d57.515143874111224!3d-20.159700145500228!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c51036174f37f%3A0x1f68755567333d1f!2sJean%20Lebrun%20Government%20School!5e0!3m2!1sen!2smu!4v1694521605907!5m2!1sen!2smu",
            "Coeur Sacre De Jesus Roman Catholic Aided School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.433467138838!2d57.51124567411103!3d-20.157669645436247!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c51041c497c27%3A0xd58e9ea669b5f178!2sCoeur%20Sacr%C3%A9%20De%20Jesus%20Rca!5e0!3m2!1sen!2smu!4v1694521856538!5m2!1sen!2smu",
            "St. Francois Xavier Roman Catholic Aided School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.4978017126346!2d57.509717088854984!3d-20.154988499999998!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c51ab44d841d1%3A0xb7d8c2a0c141a1ea!2sSt%20Francois%20Xavier%20Church!5e0!3m2!1sen!2smu!4v1694521986787!5m2!1sen!2smu",
            "Emmanuel Anquetil Government School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.743023328707!2d57.50914427411058!3d-20.14476574503003!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c510b0ed9ba9b%3A0x1683e445a7390c82!2sEmmanuel%20Anquetil%20Government%20School!5e0!3m2!1sen!2smu!4v1694522327087!5m2!1sen!2smu",
            "Abdool Rahman Abdool Government School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.5311171120175!2d57.51346937411083!3d-20.153599945308077!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c510f7c6c4c6d%3A0x483c1c14e735dead!2sAbdool%20Rahman%20Abdool%20Government%20School!5e0!3m2!1sen!2smu!4v1694522493851!5m2!1sen!2smu",
            "Jacques Le Chartier Government School": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14981.540776540836!2d57.48930915541994!3d-20.159681199999998!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c516c92ffaf51%3A0xabc63b0fe8deb107!2sSir%20Edgar%20Laurent%20Govt%20School!5e0!3m2!1sen!2smu!4v1694522633844!5m2!1sen!2smu",
            "Abercrombie Training Centre": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3745.476618582402!2d57.51668397411104!3d-20.155871345379598!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x217c51117228c4eb%3A0xb894b82143584373!2sAbercrombie%20Training%20Centre%2C%20MITD!5e0!3m2!1sen!2smu!4v1694523900499!5m2!1sen!2smu",
            
            
            # Add more polling stations and URLs here
        }
        
        # Check if the search_query exists in the dictionary
        st.write("Your Polling Station location")
        if search_query in polling_station_urls:
            google_maps_url = polling_station_urls[search_query]
            st.markdown(f'<iframe src="{google_maps_url}" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>', unsafe_allow_html=True)
        else:
            st.write("Polling station not found or not on maps.")


# Create a container for the footer
footer_container = st.container()

# Display footer text in the container
with footer_container:
    st.markdown(
        "<div style='text-align: left; width: 80%; margin: 0 auto; font-size: 10px;'>"
        "Disclaimer: While Visible Mauritius endeavors to ensure the information on this website is as current and precise as possible, Visible Mauritius makes no assertions or warranties regarding the accuracy and comprehensiveness of the data on this site and explicitly disclaims responsibility for any errors and omissions in the contents of this site.</div>"
        "<div style='text-align: center; margin-top: 20px; font-size: 12px;'>"
        "2023. Visible Mauritius. Developed with good intentions.</div>",
        
        unsafe_allow_html=True
    )

