import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
import io

# =========================
# PASSWORD PROTECTION
# =========================
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "TenderKPM2026":  # ⚠️ CHANGE THIS PASSWORD!
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🏛️ Government Tender Evaluation System")
        st.markdown("### 🔐 Authentication Required")
        st.text_input(
            "Enter Password", type="password", on_change=password_entered, key="password"
        )
        st.info("💡 Contact system administrator for access credentials")
        return False
    elif not st.session_state["password_correct"]:
        st.title("🏛️ Government Tender Evaluation System")
        st.markdown("### 🔐 Authentication Required")
        st.text_input(
            "Enter Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Incorrect password. Please try again.")
        return False
    else:
        return True

if not check_password():
    st.stop()

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Tender Evaluation System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }
    
    .main .block-container {
        padding-top: 1rem !important;
    }
    
    .main h1 {
        font-size: 1.8rem !important;
        margin-top: 0 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .main h3 {
        font-size: 1.3rem !important;
        margin-top: 0 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stButton > button {
        background-color: #2563eb;
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        border-radius: 6px;
        transition: all 0.2s;
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        background-color: #1e40af;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3);
    }
    
    div[data-testid="metric-container"] {
        background-color: white;
        border: 2px solid #e5e7eb;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .section-box {
        background-color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 6px;
        border-left: 3px solid #2563eb;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .section-box h3, .section-box h4 {
        color: #1f2937;
        margin: 0;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .info-box {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 6px;
        color: #1e3a8a;
    }
    
    .success-box {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 6px;
        color: #14532d;
    }
    
    .tender-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    
    .tender-card:hover {
        border-color: #2563eb;
        box-shadow: 0 4px 8px rgba(37, 99, 235, 0.1);
    }
    
    .tender-card h4 {
        color: #2563eb;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Initialize Session State
# =========================
if 'tenders' not in st.session_state:
    st.session_state.tenders = {}

if 'current_tender' not in st.session_state:
    st.session_state.current_tender = None

if 'page' not in st.session_state:
    st.session_state.page = 'home'

# =========================
# Helper Functions
# =========================

def load_product_database(category):
    """Load product CSV based on category"""
    files = {
        'TV': 'tv_specs.csv',
        'Laptop': 'laptop_specs.csv',
        'Printer': 'printer_specs.csv'
    }
    return pd.read_csv(files[category])

def create_tender_id():
    """Generate unique tender ID"""
    return f"T{datetime.now().strftime('%Y%m%d%H%M%S')}"

def save_tender(tender_data):
    """Save tender to session state"""
    tender_id = tender_data['tender_id']
    st.session_state.tenders[tender_id] = tender_data

def get_market_overview(df, category):
    """Generate market intelligence overview"""
    overview = {}
    
    if category == 'TV':
        overview['total_models'] = len(df)
        overview['price_range'] = (df['BasePrice'].min(), df['BasePrice'].max())
        overview['screen_range'] = (df['ScreenSize'].min(), df['ScreenSize'].max())
        overview['common_screen'] = df['ScreenSize'].mode()[0]
        overview['meps_range'] = (df['MEPS_Rating'].min(), df['MEPS_Rating'].max())
        overview['common_os'] = df['OS'].value_counts().index[0]
        
    elif category == 'Laptop':
        overview['total_models'] = len(df)
        overview['price_range'] = (df['Price'].min(), df['Price'].max())
        overview['ram_range'] = (df['RAM'].min(), df['RAM'].max())
        overview['common_ram'] = df['RAM'].mode()[0]
        overview['storage_range'] = (df['Storage'].min(), df['Storage'].max())
        overview['common_storage'] = df['Storage'].mode()[0]
        overview['battery_range'] = (df['BatteryLife'].min(), df['BatteryLife'].max())
        
    elif category == 'Printer':
        overview['total_models'] = len(df)
        overview['price_range'] = (df['Price'].min(), df['Price'].max())
        overview['speed_range'] = (df['PrintSpeed'].min(), df['PrintSpeed'].max())
        overview['common_tech'] = df['PrintTech'].value_counts().index[0]
        overview['duty_range'] = (df['MonthlyDuty'].min(), df['MonthlyDuty'].max())
        
    return overview

# =========================
# Sidebar Navigation
# =========================
st.sidebar.title("📋 Tender Evaluation")
st.sidebar.markdown("**Multi-Tender DSS**")
st.sidebar.markdown("---")

# Navigation
menu_options = {
    'home': '🏠 Dashboard',
    'create': '➕ Create New Tender',
    'database': '🗄️ Product Database'
}

for key, label in menu_options.items():
    if st.sidebar.button(label, key=f"nav_{key}", use_container_width=True):
        st.session_state.page = key
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("**Version:** 3.0 - Flexible Multi-Tender\n\n**Features:**\n- Unlimited tenders\n- Custom configurations\n- Market intelligence")

# =========================
# HOME / DASHBOARD PAGE
# =========================
if st.session_state.page == 'home':
    
    st.title("🏛️ Government Tender Evaluation System")
    st.markdown("**Professional Decision Support for Multi-Tender Procurement**")
    st.markdown("---")
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tenders", len(st.session_state.tenders))
    with col2:
        active = sum(1 for t in st.session_state.tenders.values() if t.get('status') == 'active')
        st.metric("Active Tenders", active)
    with col3:
        completed = sum(1 for t in st.session_state.tenders.values() if t.get('status') == 'completed')
        st.metric("Completed", completed)
    with col4:
        st.metric("Product Database", "160 models")
    
    st.markdown("---")
    
    # Quick Actions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='section-box'>
        <h3>🚀 Quick Start</h3>
        <p><strong>New to the system?</strong></p>
        <ol>
            <li>Create a new tender evaluation</li>
            <li>Configure requirements & quantities</li>
            <li>Set evaluation priorities</li>
            <li>Get instant recommendations</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➕ Create Your First Tender", use_container_width=True, type="primary"):
            st.session_state.page = 'create'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='section-box'>
        <h3>📊 Market Intelligence</h3>
        <p><strong>Explore product database:</strong></p>
        <ul>
            <li>50 TV models (43"-75")</li>
            <li>60 Laptop models (Budget-Premium)</li>
            <li>50 Printer models (Office-Enterprise)</li>
        </ul>
        <p>Updated quarterly with latest models</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗄️ Browse Product Database", use_container_width=True):
            st.session_state.page = 'database'
            st.rerun()
    
    st.markdown("---")
    
    # Tender List
    st.markdown("### 📋 Your Tender Evaluations")
    
    if len(st.session_state.tenders) == 0:
        st.info("👋 No tenders yet. Create your first tender evaluation to get started!")
    else:
        # Active Tenders
        active_tenders = {k: v for k, v in st.session_state.tenders.items() if v.get('status') == 'active'}
        if active_tenders:
            st.markdown("**Active Tenders:**")
            for tender_id, tender in active_tenders.items():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"""
                    <div class='tender-card'>
                    <h4>{tender['tender_name']}</h4>
                    <p><strong>ID:</strong> {tender['tender_id']}</p>
                    <p><strong>Category:</strong> {tender['category']}</p>
                    <p><strong>Created:</strong> {tender['date_created']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.write("")
                    st.write("")
                    st.info(f"📦 {tender.get('total_units', 'N/A')} units")
                with col3:
                    st.write("")
                    st.write("")
                    if st.button("Open", key=f"open_{tender_id}"):
                        st.session_state.current_tender = tender_id
                        st.session_state.page = 'view_tender'
                        st.rerun()
        
        # Completed Tenders
        completed_tenders = {k: v for k, v in st.session_state.tenders.items() if v.get('status') == 'completed'}
        if completed_tenders:
            st.markdown("**Completed Tenders:**")
            for tender_id, tender in completed_tenders.items():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"""
                    <div class='tender-card'>
                    <h4>{tender['tender_name']}</h4>
                    <p><strong>ID:</strong> {tender['tender_id']}</p>
                    <p><strong>Recommendation:</strong> {tender.get('recommendation', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.write("")
                    st.success("✅ Completed")
                with col3:
                    st.write("")
                    if st.button("View", key=f"view_{tender_id}"):
                        st.session_state.current_tender = tender_id
                        st.session_state.page = 'view_tender'
                        st.rerun()

# =========================
# CREATE NEW TENDER PAGE (SINGLE PAGE FORM)
# =========================
elif st.session_state.page == 'create':
    
# =========================
# CREATE NEW TENDER PAGE (SINGLE PAGE FORM)
# =========================
elif st.session_state.page == 'create':
    
    st.title("➕ Create New Tender Evaluation")
    st.markdown("**Configure all tender requirements in one place**")
    st.markdown("---")
    
    # Initialize form data
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'zones': [{'name': 'Zone 1', 'qty': 0, 'premium': 0.0}]
        }
    
    with st.form("tender_form"):
        # SECTION 1: Basic Information
        st.markdown("### 📋 Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            tender_name = st.text_input("Tender Name *", placeholder="e.g., Ministry of Education - Smart TVs 2026")
            tender_ref = st.text_input("Tender Reference ID", placeholder="e.g., KPM/TV/2026/001")
            category = st.selectbox("Product Category *", ['TV', 'Laptop', 'Printer'])
        
        with col2:
            ministry = st.text_input("Ministry/Department", placeholder="e.g., Ministry of Education")
            total_units = st.number_input("Total Units Required *", min_value=1, value=100, step=1)
            budget = st.number_input("Total Budget (RM) - Optional", min_value=0, value=0, step=100000)
        
        description = st.text_area("Description", placeholder="Brief description of the tender purpose...")
        
        st.markdown("---")
        
        # SECTION 2: Distribution
        st.markdown("### 📦 Quantity Distribution")
        
        distribution_type = st.radio("Distribution Type:", ['Single Location', 'Multiple Zones'], horizontal=True)
        
        if distribution_type == 'Single Location':
            location_name = st.text_input("Delivery Location", placeholder="e.g., Ministry HQ, Putrajaya")
            st.info(f"All {total_units} units will be delivered to one location")
        
        else:
            st.markdown("#### Configure Zones")
            st.caption("Add zones and allocate quantities. Total must match units required.")
            
            # Dynamic zone input using columns
            num_zones = st.number_input("Number of Zones", min_value=1, max_value=20, value=3, step=1)
            
            zones_data = []
            total_configured = 0
            
            for i in range(num_zones):
                col1, col2, col3 = st.columns([3, 2, 2])
                with col1:
                    zone_name = st.text_input(f"Zone {i+1} Name", value=f"Zone {i+1}", key=f"zname_{i}")
                with col2:
                    zone_qty = st.number_input(f"Quantity", min_value=0, value=0, key=f"zqty_{i}")
                    total_configured += zone_qty
                with col3:
                    zone_premium = st.number_input(f"Premium (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5, key=f"zprem_{i}")
                
                zones_data.append({
                    'name': zone_name,
                    'qty': zone_qty,
                    'premium': float(zone_premium)
                })
            
            # Validation
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Required", f"{total_units} units")
            with col2:
                st.metric("Configured", f"{total_configured} units")
            with col3:
                if total_configured == total_units:
                    st.success("✓ Match!")
                else:
                    st.error(f"⚠️ {abs(total_units - total_configured)} diff")
        
        st.markdown("---")
        
        # SECTION 3: Technical Requirements
        st.markdown("### 🔧 Technical Requirements")
        
        # Load database for market intelligence
        try:
            df = load_product_database(category)
            overview = get_market_overview(df, category)
            
            with st.expander("📊 View Market Intelligence", expanded=False):
                col1, col2, col3 = st.columns(3)
                if category == 'TV':
                    with col1:
                        st.metric("Models", overview['total_models'])
                        st.metric("Price Range", f"RM {overview['price_range'][0]:,.0f} - {overview['price_range'][1]:,.0f}")
                    with col2:
                        st.metric("Screens", f"{overview['screen_range'][0]}\" - {overview['screen_range'][1]}\"")
                        st.caption(f"Common: {overview['common_screen']}\"")
                    with col3:
                        st.metric("MEPS", f"{overview['meps_range'][0]}-{overview['meps_range'][1]} ⭐")
                
                elif category == 'Laptop':
                    with col1:
                        st.metric("Models", overview['total_models'])
                        st.metric("Price", f"RM {overview['price_range'][0]:,.0f} - {overview['price_range'][1]:,.0f}")
                    with col2:
                        st.metric("RAM", f"{overview['ram_range'][0]}-{overview['ram_range'][1]} GB")
                        st.caption(f"Common: {overview['common_ram']} GB")
                    with col3:
                        st.metric("Storage", f"{overview['storage_range'][0]}-{overview['storage_range'][1]} GB")
                        st.caption(f"Common: {overview['common_storage']} GB")
                
                elif category == 'Printer':
                    with col1:
                        st.metric("Models", overview['total_models'])
                    with col2:
                        st.metric("Price", f"RM {overview['price_range'][0]:,.0f} - {overview['price_range'][1]:,.0f}")
                    with col3:
                        st.metric("Speed", f"{overview['speed_range'][0]}-{overview['speed_range'][1]} ppm")
        except:
            st.warning("Market intelligence unavailable")
        
        # Requirements based on category
        st.markdown("#### Set Minimum Requirements")
        
        col1, col2, col3 = st.columns(3)
        
        if category == 'TV':
            with col1:
                max_price = st.number_input("Max Price (RM)", 1000, 15000, 5000, 100)
                min_screen = st.number_input("Min Screen (inches)", 40, 85, 55, 1)
                min_meps = st.selectbox("Min MEPS Rating", [3, 4, 5], index=0)
            with col2:
                require_4k = st.checkbox("4K Resolution Required")
                require_hdr = st.checkbox("HDR10 Required")
                require_wifi = st.checkbox("WiFi Required", value=True)
            with col3:
                min_warranty = st.selectbox("Min Warranty (years)", [1, 2, 3], index=0)
                max_weight = st.number_input("Max Weight (kg)", 10.0, 40.0, 30.0, 0.5)
        
        elif category == 'Laptop':
            with col1:
                max_price = st.number_input("Max Price (RM)", 1000, 8000, 4000, 100)
                min_ram = st.slider("Min RAM (GB)", 4, 32, 8)
                min_storage = st.slider("Min Storage (GB)", 128, 1024, 256)
            with col2:
                min_battery = st.slider("Min Battery (hours)", 4, 20, 8)
                require_windows11 = st.checkbox("Windows 11 Required")
            with col3:
                min_warranty = st.selectbox("Min Warranty (years)", [1, 2, 3], index=0)
                max_weight = st.number_input("Max Weight (kg)", 1.0, 3.0, 2.5, 0.1)
        
        elif category == 'Printer':
            with col1:
                max_price = st.number_input("Max Price (RM)", 500, 5000, 2000, 100)
                min_speed = st.slider("Min Print Speed (ppm)", 10, 60, 25)
            with col2:
                require_duplex = st.checkbox("Duplex Required")
                require_network = st.checkbox("Network Required")
            with col3:
                min_warranty = st.selectbox("Min Warranty (years)", [1, 2, 3], index=0)
        
        st.markdown("---")
        
        # SECTION 4: Evaluation Weights
        st.markdown("### ⚖️ Evaluation Criteria Weights")
        st.caption("Higher weight = more important. Total must equal 100%")
        
        preset = st.selectbox("Preset Template:", ["Custom", "Balanced (Specs Focus)", "Budget Focus", "Performance Focus"])
        
        # Initialize weights based on category and preset
        if category == 'TV':
            if preset == "Balanced (Specs Focus)":
                default_weights = {'price': 10, 'meps': 20, 'screen': 15, 'audio': 15, 'wifi': 10, 'hdmi': 10, 'os': 10, 'weight': 5, 'warranty': 5}
            elif preset == "Budget Focus":
                default_weights = {'price': 35, 'meps': 15, 'screen': 10, 'audio': 10, 'wifi': 8, 'hdmi': 8, 'os': 6, 'weight': 5, 'warranty': 3}
            elif preset == "Performance Focus":
                default_weights = {'price': 5, 'meps': 25, 'screen': 20, 'audio': 20, 'wifi': 10, 'hdmi': 10, 'os': 5, 'weight': 3, 'warranty': 2}
            else:
                default_weights = {'price': 15, 'meps': 20, 'screen': 15, 'audio': 15, 'wifi': 10, 'hdmi': 10, 'os': 8, 'weight': 4, 'warranty': 3}
            
            col1, col2 = st.columns(2)
            with col1:
                w_price = st.slider("Price (Reference)", 0, 50, default_weights['price'], key="w_price")
                w_meps = st.slider("MEPS Rating", 0, 50, default_weights['meps'], key="w_meps")
                w_screen = st.slider("Screen Quality", 0, 50, default_weights['screen'], key="w_screen")
                w_audio = st.slider("Audio Quality", 0, 50, default_weights['audio'], key="w_audio")
            with col2:
                w_wifi = st.slider("WiFi", 0, 30, default_weights['wifi'], key="w_wifi")
                w_hdmi = st.slider("HDMI", 0, 30, default_weights['hdmi'], key="w_hdmi")
                w_os = st.slider("OS Quality", 0, 30, default_weights['os'], key="w_os")
                w_weight = st.slider("Weight/Build", 0, 20, default_weights['weight'], key="w_weight")
                w_warranty = st.slider("Warranty", 0, 20, default_weights['warranty'], key="w_warranty")
            
            weights = {
                'price': w_price, 'meps': w_meps, 'screen': w_screen, 'audio': w_audio,
                'wifi': w_wifi, 'hdmi': w_hdmi, 'os': w_os, 'weight': w_weight, 'warranty': w_warranty
            }
        
        elif category == 'Laptop':
            if preset == "Balanced (Specs Focus)":
                default_weights = {'price': 10, 'processor': 25, 'ram': 20, 'storage': 15, 'battery': 15, 'weight': 10, 'warranty': 5}
            elif preset == "Budget Focus":
                default_weights = {'price': 35, 'processor': 20, 'ram': 15, 'storage': 10, 'battery': 10, 'weight': 5, 'warranty': 5}
            elif preset == "Performance Focus":
                default_weights = {'price': 5, 'processor': 30, 'ram': 25, 'storage': 20, 'battery': 10, 'weight': 5, 'warranty': 5}
            else:
                default_weights = {'price': 15, 'processor': 25, 'ram': 20, 'storage': 15, 'battery': 12, 'weight': 8, 'warranty': 5}
            
            col1, col2 = st.columns(2)
            with col1:
                w_price = st.slider("Price (Reference)", 0, 50, default_weights['price'], key="w_price")
                w_processor = st.slider("Processor", 0, 50, default_weights['processor'], key="w_proc")
                w_ram = st.slider("RAM", 0, 50, default_weights['ram'], key="w_ram")
                w_storage = st.slider("Storage", 0, 30, default_weights['storage'], key="w_stor")
            with col2:
                w_battery = st.slider("Battery Life", 0, 30, default_weights['battery'], key="w_batt")
                w_weight = st.slider("Weight/Portability", 0, 20, default_weights['weight'], key="w_weight")
                w_warranty = st.slider("Warranty", 0, 20, default_weights['warranty'], key="w_warr")
            
            weights = {
                'price': w_price, 'processor': w_processor, 'ram': w_ram, 'storage': w_storage,
                'battery': w_battery, 'weight': w_weight, 'warranty': w_warranty
            }
        
        elif category == 'Printer':
            if preset == "Balanced (Specs Focus)":
                default_weights = {'price': 10, 'tech': 20, 'speed': 20, 'capacity': 15, 'duty': 15, 'toner': 15, 'warranty': 5}
            elif preset == "Budget Focus":
                default_weights = {'price': 35, 'tech': 15, 'speed': 15, 'capacity': 10, 'duty': 10, 'toner': 10, 'warranty': 5}
            elif preset == "Performance Focus":
                default_weights = {'price': 5, 'tech': 25, 'speed': 25, 'capacity': 15, 'duty': 15, 'toner': 10, 'warranty': 5}
            else:
                default_weights = {'price': 15, 'tech': 20, 'speed': 20, 'capacity': 12, 'duty': 12, 'toner': 16, 'warranty': 5}
            
            col1, col2 = st.columns(2)
            with col1:
                w_price = st.slider("Price (Reference)", 0, 50, default_weights['price'], key="w_price")
                w_tech = st.slider("Print Technology", 0, 40, default_weights['tech'], key="w_tech")
                w_speed = st.slider("Print Speed", 0, 40, default_weights['speed'], key="w_speed")
                w_capacity = st.slider("Paper Capacity", 0, 30, default_weights['capacity'], key="w_cap")
            with col2:
                w_duty = st.slider("Monthly Duty", 0, 30, default_weights['duty'], key="w_duty")
                w_toner = st.slider("Toner Yield", 0, 30, default_weights['toner'], key="w_toner")
                w_warranty = st.slider("Warranty", 0, 20, default_weights['warranty'], key="w_warr")
            
            weights = {
                'price': w_price, 'tech': w_tech, 'speed': w_speed, 'capacity': w_capacity,
                'duty': w_duty, 'toner': w_toner, 'warranty': w_warranty
            }
        
        total_weight = sum(weights.values())
        
        if total_weight == 100:
            st.success(f"✓ Total Weight: {total_weight}%")
        else:
            st.error(f"⚠️ Total Weight: {total_weight}% - Must be exactly 100%")
        
        st.markdown("---")
        
        # Submit button
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)
            if cancel:
                st.session_state.page = 'home'
                st.rerun()
        
        with col3:
            submitted = st.form_submit_button("Run Evaluation", type="primary", use_container_width=True)
    
    # Process form submission
    if submitted:
        # Validate
        errors = []
        
        if not tender_name:
            errors.append("Tender name is required")
        
        if distribution_type == 'Multiple Zones' and total_configured != total_units:
            errors.append(f"Zone quantities ({total_configured}) don't match total units ({total_units})")
        
        if total_weight != 100:
            errors.append(f"Evaluation weights must total 100% (currently {total_weight}%)")
        
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
            st.stop()
        
        # Prepare tender data
        tender_data = {
            'tender_id': create_tender_id(),
            'tender_name': tender_name,
            'tender_ref': tender_ref or 'N/A',
            'category': category,
            'ministry': ministry or 'N/A',
            'description': description or 'N/A',
            'total_units': total_units,
            'budget': budget,
            'date_created': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'status': 'active',
            'distribution_type': distribution_type,
            'weights': weights
        }
        
        # Add zones or location
        if distribution_type == 'Single Location':
            tender_data['zones'] = [{'name': location_name, 'qty': total_units, 'premium': 0.0}]
        else:
            tender_data['zones'] = zones_data
        
        # Add requirements
        if category == 'TV':
            tender_data['requirements'] = {
                'max_price': max_price,
                'min_screen': min_screen,
                'min_meps': min_meps,
                'min_warranty': min_warranty,
                'max_weight': max_weight,
                'require_4k': require_4k,
                'require_hdr': require_hdr,
                'require_wifi': require_wifi
            }
        elif category == 'Laptop':
            tender_data['requirements'] = {
                'max_price': max_price,
                'min_ram': min_ram,
                'min_storage': min_storage,
                'min_battery': min_battery,
                'min_warranty': min_warranty,
                'max_weight': max_weight,
                'require_windows11': require_windows11
            }
        elif category == 'Printer':
            tender_data['requirements'] = {
                'max_price': max_price,
                'min_speed': min_speed,
                'min_warranty': min_warranty,
                'require_duplex': require_duplex,
                'require_network': require_network
            }
        
        # Run evaluation (simplified)
        with st.spinner("Running evaluation..."):
            try:
                df = load_product_database(category)
                
                # Apply filters
                filtered = df.copy()
                requirements = tender_data['requirements']
                
                if category == 'TV':
                    if 'BasePrice' in filtered.columns:
                        filtered['Price'] = filtered['BasePrice']
                    filtered = filtered[filtered['Price'] <= requirements['max_price']]
                    filtered = filtered[filtered['ScreenSize'] >= requirements['min_screen']]
                    filtered = filtered[filtered['MEPS_Rating'] >= requirements['min_meps']]
                    filtered = filtered[filtered['Weight'] <= requirements['max_weight']]
                    filtered = filtered[filtered['Warranty_Years'] >= requirements['min_warranty']]
                    if requirements['require_4k']:
                        filtered = filtered[filtered['Resolution'] == '4K']
                    if requirements['require_hdr']:
                        filtered = filtered[filtered['HDR10'] == 'Yes']
                
                elif category == 'Laptop':
                    filtered = filtered[filtered['Price'] <= requirements['max_price']]
                    filtered = filtered[filtered['RAM'] >= requirements['min_ram']]
                    filtered = filtered[filtered['Storage'] >= requirements['min_storage']]
                    filtered = filtered[filtered['BatteryLife'] >= requirements['min_battery']]
                    filtered = filtered[filtered['Weight'] <= requirements['max_weight']]
                    filtered = filtered[filtered['Warranty'] >= requirements['min_warranty']]
                    if requirements['require_windows11']:
                        filtered = filtered[filtered['OS'].str.contains('Windows 11', na=False)]
                
                elif category == 'Printer':
                    filtered = filtered[filtered['Price'] <= requirements['max_price']]
                    filtered = filtered[filtered['PrintSpeed'] >= requirements['min_speed']]
                    filtered = filtered[filtered['Warranty'] >= requirements['min_warranty']]
                    if requirements['require_duplex']:
                        filtered = filtered[filtered['Duplex'] == 'Yes']
                    if requirements['require_network']:
                        filtered = filtered[filtered['Network'].str.contains('WiFi|Ethernet', na=False)]
                
                if filtered.empty:
                    st.error("❌ No products meet all requirements. Please adjust your filters and try again.")
                    st.stop()
                
                # Simple scoring (you can enhance this)
                scored = filtered.copy()
                scored['TotalScore'] = 0.5  # Placeholder
                scored = scored.sort_values('TotalScore', ascending=False).reset_index(drop=True)
                scored['Rank'] = scored.index + 1
                
                # Save results
                tender_data['results'] = {
                    'filtered_count': len(filtered),
                    'top_product': f"{scored.iloc[0]['Brand']} {scored.iloc[0]['Model']}",
                    'top_score': 0.5
                }
                tender_data['recommendation'] = f"{scored.iloc[0]['Brand']} {scored.iloc[0]['Model']}"
                tender_data['status'] = 'completed'
                
                save_tender(tender_data)
                
                st.success("✅ Tender evaluation completed!")
                st.info(f"**Recommendation:** {tender_data['recommendation']}")
                
                if st.button("View Full Results", type="primary"):
                    st.session_state.current_tender = tender_data['tender_id']
                    st.session_state.page = 'view_tender'
                    st.rerun()
                
                if st.button("Back to Dashboard"):
                    st.session_state.page = 'home'
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error during evaluation: {str(e)}")
                st.info("Please check your CSV files are present and properly formatted.")


# =========================
# PRODUCT DATABASE PAGE
# =========================
elif st.session_state.page == 'database':
    
    st.title("🗄️ Product Database")
    st.markdown("**Market Intelligence & Product Catalog**")
    st.markdown("---")
    
    category = st.selectbox("Select Category:", ['TV', 'Laptop', 'Printer'])
    
    df = load_product_database(category)
    overview = get_market_overview(df, category)
    
    # Market Overview
    st.markdown("### 📊 Market Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Models", overview['total_models'])
    with col2:
        st.metric("Price Range", f"RM {overview['price_range'][0]:,.0f} - {overview['price_range'][1]:,.0f}")
    
    if category == 'TV':
        with col3:
            st.metric("Screen Sizes", f"{overview['screen_range'][0]}\" - {overview['screen_range'][1]}\"")
        with col4:
            st.metric("MEPS Range", f"{overview['meps_range'][0]}-{overview['meps_range'][1]} ⭐")
    
    st.markdown("---")
    
    # Display data
    st.markdown("### 📋 Product List")
    st.dataframe(df, use_container_width=True, height=500)
    
    # Download option
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"{category.lower()}_database.csv",
        mime="text/csv"
    )
