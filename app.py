import streamlit as st
st.set_page_config(page_title="Campus Navigator", page_icon="🎓", layout="wide")

import pandas as pd
import networkx as nx
from PIL import Image
import json
import time
import plotly.graph_objects as go
from pages.class_finder import class_finder
from pages.canteen_menu import canteen_menu
from pages.faculty_room import faculty_room
from pages.department_office import department_office
from pages.administration import administration
from pages.parking_info import parking_info

# Building and paths data remains the same as in your original file
BUILDINGS = {
    "Gate": {"location": "Main Entrance", "facilities": ["Security Post", "Information Desk"]},
    "CSE1": {"location": "Near Saraswat Statue", "facilities": ["Labs", "Classrooms", "Faculty Rooms"]},
    "CSE2": {"location": "Adjacent to CSE1", "facilities": ["Labs", "Classrooms"]},
    "ECE1": {"location": "North Wing", "facilities": ["Labs", "Classrooms"]},
    "ECE2": {"location": "Near Admin Block", "facilities": ["Labs", "Classrooms"]},
    "EEE": {"location": "Near Mechanical Block", "facilities": ["Labs", "Classrooms"]},
    "MECH": {"location": "West Wing", "facilities": ["Workshop", "Labs", "Classrooms"]},
    "CIVIL": {"location": "Southwest Wing", "facilities": ["Labs", "Classrooms"]},
    "AIML": {"location": "Near Civil Block", "facilities": ["AI Lab", "Classrooms"]},
    "Administration": {"location": "Central Block", "facilities": ["Office", "Meeting Rooms"]},
    "Polytechnic": {"location": "Near ECE2", "facilities": ["Classrooms", "Labs"]},
    "BSH": {"location": "Near Polytechnic", "facilities": ["Basic Sciences Labs", "Classrooms"]},
    "Placements": {"location": "Near Gate", "facilities": ["Interview Rooms", "Training Hall"]},
    "Pharmacy": {"location": "Near Boys Hostel", "facilities": ["Labs", "Classrooms"]},
    "Boys Hostel": {"location": "East Wing", "facilities": ["Rooms", "Mess"]},
    "Girls Hostel": {"location": "South Wing", "facilities": ["Rooms", "Mess"]},
    "Basketball Court": {"location": "Near Pharmacy", "facilities": ["Court"]},
    "Sports Area": {"location": "Near Boys Hostel", "facilities": ["Grounds", "Equipment Room"]},
    "Canteen": {"location": "Near Bus Area", "facilities": ["Food Court", "Seating Area"]},
    "Bus Area": {"location": "South End", "facilities": ["Parking", "Waiting Area"]},
    "CAI": {"location": "Near Girls Hostel", "facilities": ["Computer Labs"]}
}


PATHS = {
    ("Gate", "Placements"): {"distance": 50, "covered": True},
    ("Gate", "Basketball Court"): {"distance": 30, "covered": False},
    ("CSE1", "CSE2"): {"distance": 20, "covered": True},
    ("CSE1", "EEE"): {"distance": 25, "covered": True},
    ("CSE1", "ECE1"): {"distance": 35, "covered": True},
    ("ECE1", "ECE2"): {"distance": 40, "covered": True},
    ("ECE2", "Administration"): {"distance": 30, "covered": True},
    ("ECE2", "Polytechnic"): {"distance": 25, "covered": True},
    ("EEE", "MECH"): {"distance": 20, "covered": True},
    ("EEE", "AIML"): {"distance": 25, "covered": True},
    ("MECH", "CIVIL"): {"distance": 30, "covered": True},
    ("CIVIL", "AIML"): {"distance": 25, "covered": True},
    ("AIML", "CAI"): {"distance": 40, "covered": True},
    ("CAI", "Girls Hostel"): {"distance": 35, "covered": True},
    ("CAI", "Bus Area"): {"distance": 45, "covered": False},
    ("Polytechnic", "BSH"): {"distance": 20, "covered": True},
    ("BSH", "Placements"): {"distance": 35, "covered": True},
    ("Placements", "Basketball Court"): {"distance": 25, "covered": False},
    ("Basketball Court", "Boys Hostel"): {"distance": 30, "covered": False},
    ("Basketball Court", "Sports Area"): {"distance": 35, "covered": False},
    ("Boys Hostel", "Sports Area"): {"distance": 25, "covered": False},
    ("Boys Hostel", "Pharmacy"): {"distance": 20, "covered": True}
}


class CampusNavigator:
    def __init__(self):
        self.graph = self._build_graph()
        
    def _build_graph(self):
        G = nx.Graph()
        for (start, end), attrs in PATHS.items():
            G.add_edge(start, end, **attrs)
        return G
    
    def find_path(self, start, end, preference):
        if preference == "Shortest":
            return nx.shortest_path(self.graph, start, end, weight="distance")
        else:  # Covered Pathway
            def covered_weight(u, v, d):
                return 1 if d["covered"] else 2
            return nx.shortest_path(self.graph, start, end, weight=covered_weight)
        


def show_custom_header():
    st.markdown("""
        <div class="custom-header">
            <h1>🎓 Sri Vasavi Engineering College</h1>
            <p style='font-size: 1.2rem;'>Smart Campus Navigator - Your Digital Guide</p>
        </div>
    """, unsafe_allow_html=True)
        

# Add custom CSS for enhanced styling
def add_custom_css():
    st.markdown("""
        <style>
        /* --- General Styling with a Dark Modern Theme --- */
       
        /* --- Animated Gradient Background --- */
  
    /* Smooth Animated Gradient */
body {
    background: linear-gradient(135deg, #1e3c72, #2a5298, #6dd5ed);
    background-size: 400% 400%;
    animation: gradientMove 10s infinite ease-in-out;
    font-family: 'Poppins', sans-serif;
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Text Glow */
h1, h2 {
    color: #fff;
    text-shadow: 2px 2px 10px rgba(255, 255, 255, 0.8);
}


@keyframes gradientAnimation {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* --- 3D Parallax Effect --- */
body::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url("https://source.unsplash.com/1600x900/?galaxy,stars,nebula") no-repeat center center/cover;
    opacity: 0.2;
    z-index: -1;
}

/* --- Subtle Noise Overlay for Texture --- */
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url("https://www.transparenttextures.com/patterns/dark-matter.png");
    opacity: 0.05;
    z-index: -1;
}
                

/* --- Neon Glow Box for Sections --- */
.section {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(255, 255, 255, 0.2);
    transition: 0.4s;
}
.section:hover {
    transform: scale(1.05);
    box-shadow: 0 15px 35px rgba(255, 255, 255, 0.4);
}

/* --- Cool Glowing Header --- */
.header {
    font-size: 2.5rem;
    text-align: center;
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: bold;
}

        /* --- Glassmorphism Card Effect --- */
        .stCard {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 25px rgba(255, 255, 255, 0.1);
            transition: all 0.4s ease-in-out;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        .stCard:hover {
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 12px 30px rgba(255, 255, 255, 0.3);
        }

        /* --- Neumorphic Header --- */
        .custom-header {
            background: linear-gradient(135deg, #4e54c8, #8f94fb);
            color: white;
            padding: 2.5rem;
            border-radius: 15px;
            text-align: center;
            font-size: 2.2rem;
            font-weight: bold;
            box-shadow: 5px 5px 15px rgba(79, 93, 204, 0.5), 
                        -5px -5px 15px rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }
        .custom-header:hover {
            transform: scale(1.03);
            box-shadow: 8px 8px 20px rgba(79, 93, 204, 0.8), 
                        -8px -8px 20px rgba(255, 255, 255, 0.3);
        }

        /* --- Animated Quick Link Buttons --- */
        .quick-link {
            background: linear-gradient(90deg, #ff416c, #ff4b2b);
            color: white;
            padding: 1.2rem;
            border-radius: 12px;
            text-align: center;
            margin: 0.8rem 0;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 6px 18px rgba(255, 64, 108, 0.4);
            transition: all 0.4s ease-in-out;
            transform-origin: center;
            position: relative;
            overflow: hidden;
        }
        .quick-link::before {
            content: "";
            position: absolute;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.3);
            top: 0;
            left: -100%;
            transition: 0.5s;
        }
        .quick-link:hover::before {
            left: 100%;
        }
        .quick-link:hover {
            transform: scale(1.12);
            box-shadow: 0 12px 25px rgba(255, 64, 108, 0.6);
            background: linear-gradient(90deg, #ff4b2b, #ff416c);
        }

        /* --- Animated Emergency Contact Box --- */
        .emergency-contact {
            background: linear-gradient(90deg, #ff512f, #dd2476);
            color: white;
            padding: 1.3rem;
            border-radius: 15px;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 8px 16px rgba(221, 36, 118, 0.5);
            transition: all 0.3s ease-in-out;
        }
        .emergency-contact:hover {
            transform: scale(1.1);
            box-shadow: 0 10px 25px rgba(221, 36, 118, 0.7);
        }

        /* --- Interactive Building Info Cards --- */
        .building-card {
            background: rgba(255, 255, 255, 0.12);
            padding: 1.7rem;
            border-radius: 15px;
            box-shadow: 0 6px 14px rgba(255, 255, 255, 0.15);
            transition: transform 0.3s ease-in-out, box-shadow 0.3s;
            border: 2px solid rgba(255, 255, 255, 0.25);
            position: relative;
        }
        .building-card:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 8px 20px rgba(255, 255, 255, 0.25);
        }
        .building-card::after {
            content: "";
            position: absolute;
            top: -3px;
            left: -3px;
            width: 100%;
            height: 100%;
            border-radius: 15px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .building-card:hover::after {
            opacity: 1;
        }

        /* --- Rotating Loading Animation --- */
        .loading {
            display: inline-block;
            width: 55px;
            height: 55px;
            border: 4px solid rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            border-top-color: #ff416c;
            animation: spin 1.2s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        </style>
    """, unsafe_allow_html=True)




def show_campus_map():
    st.header("📍 Campus Map")
    try:
        image = Image.open("D:\\routingpath\\image.png")
        st.image(image, caption="Sri Vasavi Engineering College Route Map", use_container_width=True)
    except:
        st.error("Campus map image not found. Please ensure the image file is in the correct location.")


def show_loading_animation():
    st.markdown("""
        <div style='text-align: center;'>
            <div class="loading"></div>
            <p>Loading your route...</p>
        </div>
    """, unsafe_allow_html=True)


def show_enhanced_navigation():
    st.markdown("""
        <h2 style='text-align: center; color: #1e3c72;'>🚶‍♂️ Interactive Campus Navigation</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        start = st.selectbox("Where are you now?", list(BUILDINGS.keys()), 
                            format_func=lambda x: f"📍 {x}")
        
    with col2:
        end = st.selectbox("Where do you want to go?", 
                          [b for b in BUILDINGS.keys() if b != start],
                          format_func=lambda x: f"🎯 {x}")
    
    route_preference = st.radio("How would you like to get there?",
                              ["⚡ Shortest Route", "☔ Covered Pathway"],
                              format_func=lambda x: x.split(" ", 1)[1])
    
    if st.button("Find My Way!", type="primary"):
        show_loading_animation()
        time.sleep(1)  # Simulate loading
        
        navigator = CampusNavigator()
        try:
            path = navigator.find_path(start, end, "Shortest" if "Shortest" in route_preference else "Covered")
            
            # Create an animated path visualization
            fig = go.Figure()
            
            # Add building points
            x_coords = list(range(len(path)))
            fig.add_trace(go.Scatter(
                x=x_coords,
                y=[0] * len(path),
                mode='markers+text',
                name='Buildings',
                text=path,
                textposition='top center',
                marker=dict(size=20, symbol='star', color='gold'),
            ))
            
            # Add path line
            fig.add_trace(go.Scatter(
                x=x_coords,
                y=[0] * len(path),
                mode='lines',
                line=dict(width=3, color='royalblue', dash='dot'),
                name='Path'
            ))
            
            fig.update_layout(
                title='Your Route Visualization',
                showlegend=False,
                plot_bgcolor='white',
                height=300,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show step-by-step directions with animation
            st.markdown("### 📝 Step-by-Step Directions")
            total_distance = 0
            
            for i in range(len(path)-1):
                path_details = PATHS.get((path[i], path[i+1])) or PATHS.get((path[i+1], path[i]))
                distance = path_details["distance"]
                covered = path_details["covered"]
                total_distance += distance
                
                with st.container():
                    st.markdown(f"""
                        <div class="building-card">
                            <h4>Step {i+1}</h4>
                            <p>🚶‍♂️ From <b>{path[i]}</b> to <b>{path[i+1]}</b></p>
                            <p>📏 Distance: {distance}m | 🌂 Covered Path: {'Yes' if covered else 'No'}</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.success(f"🎉 Total distance: {total_distance} meters")
            
            # Show destination details
            st.markdown("### 📍 Destination Details")
            dest_details = BUILDINGS[end]
            st.markdown(f"""
                <div class="building-card" style='background: linear-gradient(45deg, #2193b0, #6dd5ed); color: white;'>
                    <h3>{end}</h3>
                    <p>📌 Location: {dest_details['location']}</p>
                    <p>🏢 Facilities: {', '.join(dest_details['facilities'])}</p>
                </div>
            """, unsafe_allow_html=True)
            
        except nx.NetworkXNoPath:
            st.error("😕 No route found between selected locations!")

def show_building_info():
    st.header("🏢 Building Information")
    
    building_types = {
        "Academic Blocks": ["CSE1", "CSE2", "ECE1", "ECE2", "EEE", "MECH", "CIVIL", "AIML", "BSH", "Polytechnic", "Pharmacy"],
        "Administrative": ["Administration", "Placements", "CAI"],
        "Hostels": ["Boys Hostel", "Girls Hostel"],
        "Sports & Recreation": ["Basketball Court", "Sports Area", "Canteen"],
        "Other": ["Gate", "Bus Area"]
    }
    
    for type_name, buildings in building_types.items():
        st.subheader(type_name)
        cols = st.columns(3)
        for i, building in enumerate(buildings):
            with cols[i % 3]:
                st.write(f"**{building}**")
                details = BUILDINGS[building]
                st.write(f"Location: {details['location']}")
                st.write(f"Facilities: {', '.join(details['facilities'])}")

def handle_navigation(user_type):
    """Handle quick links based on user type"""
    if user_type == "Student":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎓 Find My Class", use_container_width=True):
                st.session_state.page = "class_finder"
        with col2:
            if st.button("🍽️ Canteen Menu", use_container_width=True):
                st.session_state.page = "canteen_menu"
    
    elif user_type == "Faculty":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏢 Faculty Room", use_container_width=True):
                st.session_state.page = "faculty_room"
        with col2:
            if st.button("🎓 Department Office", use_container_width=True):
                st.session_state.page = "department_office"
    
    else:  # Visitor
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏛️ Administration", use_container_width=True):
                st.session_state.page = "administration"
        with col2:
            if st.button("🅿️ Parking Area", use_container_width=True):
                st.session_state.page = "parking"

def show_enhanced_building_info():
    st.markdown("""
        <h2 style='text-align: center; color: #1e3c72;'>🏢 Campus Buildings Directory</h2>
    """, unsafe_allow_html=True)
    
    building_types = {
        "Academic Blocks": ["CSE1", "CSE2", "ECE1", "ECE2", "EEE", "MECH", "CIVIL", "AIML", "BSH", "Polytechnic", "Pharmacy"],
        "Administrative": ["Administration", "Placements", "CAI"],
        "Hostels": ["Boys Hostel", "Girls Hostel"],
        "Sports & Recreation": ["Basketball Court", "Sports Area", "Canteen"],
        "Other": ["Gate", "Bus Area"]
    }
    
    for type_name, buildings in building_types.items():
        st.markdown(f"""
            <h3 style='color: #1e3c72; margin-top: 2rem;'>{type_name}</h3>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, building in enumerate(buildings):
            with cols[i % 3]:
                details = BUILDINGS[building]
                st.markdown(f"""
                    <div class="building-card" style='height: 100%;'>
                        <h4>{building}</h4>
                        <p>📍 {details['location']}</p>
                        <p>🏢 {', '.join(details['facilities'])}</p>
                    </div>
                """, unsafe_allow_html=True)


def main():
    # Add custom CSS
    add_custom_css()
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    
    
    # Show custom header
    show_custom_header()
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 1rem;'>
                <h2>Navigation Menu</h2>
            </div>
        """, unsafe_allow_html=True)
        
        user_type = st.radio("I am a:", ["Student", "Faculty", "Visitor"])
        
        st.markdown("<h3>Quick Links</h3>", unsafe_allow_html=True)
        
        if user_type == "Student":
            if st.button("🎓 Find My Class", use_container_width=True):
                st.session_state.page = "class_finder"
            if st.button("🍽️ Canteen Menu", use_container_width=True):
                st.session_state.page = "canteen_menu"
        elif user_type == "Faculty":
            if st.button("🏢 Faculty Room", use_container_width=True):
                st.session_state.page = "faculty_room"
            if st.button("🎓 Department Office", use_container_width=True):
                st.session_state.page = "department_office"
        else:
            if st.button("🏛️ Administration", use_container_width=True):
                st.session_state.page = "administration"
            if st.button("🅿️ Parking Area", use_container_width=True):
                st.session_state.page = "parking"
        
        st.markdown("""
            <div class="emergency-contact">
                <h3>📞 Emergency Contacts</h3>
                <p>🚨 Security: XXXX-XXXXXX</p>
                <p>🏥 Medical: XXXX-XXXXXX</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.page = "home"
    
    # Main content
    if st.session_state.page == "home":
        tab1, tab2, tab3 = st.tabs([
            "📍 Campus Map",
            "🚶‍♂️ Navigation",
            "🏢 Building Info"
        ])
        
        with tab1:
            show_campus_map()
        with tab2:
            show_enhanced_navigation()
        with tab3:
            show_enhanced_building_info()
    
    elif st.session_state.page == "class_finder":
        class_finder()
    elif st.session_state.page == "canteen_menu":
        canteen_menu()
    elif st.session_state.page == "faculty_room":
        faculty_room()
    elif st.session_state.page == "department_office":
        department_office()
    elif st.session_state.page == "administration":
        administration()
    elif st.session_state.page == "parking":
        parking_info()

if __name__ == "__main__":
    main()