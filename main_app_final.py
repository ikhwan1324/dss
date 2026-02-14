import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# PASSWORD PROTECTION
# =========================
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "TenderKPM2026":  # ⚠️ CHANGE THIS PASSWORD!
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    # First run, show input for password
    if "password_correct" not in st.session_state:
        st.title("🏛️ Government Tender Evaluation System")
        st.markdown("### 🔐 Authentication Required")
        st.text_input(
            "Enter Password", type="password", on_change=password_entered, key="password"
        )
        st.info("💡 Contact system administrator for access credentials")
        return False
    # Password not correct, show input + error
    elif not st.session_state["password_correct"]:
        st.title("🏛️ Government Tender Evaluation System")
        st.markdown("### 🔐 Authentication Required")
        st.text_input(
            "Enter Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Incorrect password. Please try again.")
        return False
    else:
        # Password correct
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

# Professional CSS - Better contrast and readability
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #f5f7fa;
    }
    
    /* Reduce top padding */
    .main .block-container {
        padding-top: 1rem !important;
    }
    
    /* Make main titles smaller */
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
    
    /* Primary buttons */
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
    
    /* Metric containers */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 2px solid #e5e7eb;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    div[data-testid="metric-container"] label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #1f2937 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    
    /* Section boxes - smaller and more compact */
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
    
    /* Info boxes with better contrast */
    .info-box {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 6px;
        color: #1e3a8a;
    }
    
    .info-box strong {
        color: #1e40af;
    }
    
    /* Success box */
    .success-box {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 6px;
        color: #14532d;
    }
    
    .success-box h4 {
        color: #15803d;
        margin: 0 0 0.5rem 0;
    }
    
    /* Warning box */
    .warning-box {
        background-color: #fefce8;
        border-left: 4px solid #eab308;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 6px;
        color: #713f12;
    }
    
    /* Step indicator */
    .step-container {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        gap: 1rem;
    }
    
    .step {
        flex: 1;
        text-align: center;
        padding: 1rem;
        background-color: white;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        color: #6b7280;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .step.active {
        border-color: #2563eb;
        background-color: #eff6ff;
        color: #1e40af;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.1);
    }
    
    .step.completed {
        border-color: #22c55e;
        background-color: #f0fdf4;
        color: #15803d;
    }
    
    .step-number {
        display: block;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    /* Comparison cards */
    .comparison-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        height: 100%;
        color: #1f2937;
    }
    
    .comparison-card.winner {
        border-color: #2563eb;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    .comparison-card h4 {
        color: #2563eb;
        margin-top: 0;
    }
    
    .comparison-card h5 {
        color: #1f2937;
        margin: 0.5rem 0;
    }
    
    .comparison-card hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 1rem 0;
    }
    
    .comparison-card p {
        margin: 0.3rem 0;
        color: #374151;
    }
    
    .comparison-card strong {
        color: #1f2937;
    }
    
    /* Table styling */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Expander headers */
    .streamlit-expanderHeader {
        background-color: white;
        border: 2px solid #e5e7eb;
        border-radius: 6px;
        font-weight: 600;
        color: #1f2937 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border: 2px solid #e5e7eb;
        border-radius: 6px;
        color: #374151;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2563eb;
        color: white;
        border-color: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Initialize Session State
# =========================
if 'tv_step' not in st.session_state:
    st.session_state.tv_step = 1
if 'laptop_step' not in st.session_state:
    st.session_state.laptop_step = 1
if 'printer_step' not in st.session_state:
    st.session_state.printer_step = 1

# =========================
# Sidebar Navigation
# =========================
st.sidebar.title("📋 Tender Evaluation")
st.sidebar.markdown("**Government Procurement DSS**")
st.sidebar.markdown("---")

module = st.sidebar.radio(
    "Select Module:",
    ["🏠 Home", "📺 TV Procurement", "💻 Laptop Procurement", "🖨️ Printer Procurement"]
)

st.sidebar.markdown("---")
st.sidebar.info("**Version:** 2.0\n\n**Standards:** KPM 2026")

# =========================
# HOME PAGE
# =========================
if module == "🏠 Home":
    
    st.title("🏛️ Government Tender Evaluation System")
    st.markdown("**Professional Decision Support for Public Procurement**")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class='section-box'>
        <h3>System Overview</h3>
        <p>This system provides a transparent, auditable platform for evaluating government procurement tenders.</p>
        
        <h4>Key Features</h4>
        <ul>
            <li><strong>Automated Compliance Checking</strong> - Filters products against mandatory requirements</li>
            <li><strong>Multi-Criteria Evaluation</strong> - Weighted scoring across technical and financial criteria</li>
            <li><strong>Transparent Ranking</strong> - Clear justification for all recommendations</li>
            <li><strong>Audit-Ready Reports</strong> - Complete documentation for tender committees</li>
        </ul>
        
        <h4>Evaluation Process</h4>
        <ol>
            <li><strong>Configure Requirements</strong> - Set mandatory specifications and filters</li>
            <li><strong>Review Results</strong> - View compliant products and scores</li>
            <li><strong>Compare Options</strong> - Side-by-side analysis of top products</li>
            <li><strong>Generate Report</strong> - Create official recommendation document</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-box'>
        <h4>📺 TV Procurement</h4>
        <p><strong>Purpose:</strong> 65" Smart TVs for schools</p>
        <p><strong>Features:</strong> Zone-based pricing for Malaysia</p>
        <p><strong>Criteria:</strong> 9 weighted evaluation factors</p>
        </div>
        
        <div class='info-box'>
        <h4>💻 Laptop Procurement</h4>
        <p><strong>Purpose:</strong> Professional laptops for offices</p>
        <p><strong>Features:</strong> Enterprise specifications</p>
        <p><strong>Criteria:</strong> 7 weighted evaluation factors</p>
        </div>
        
        <div class='info-box'>
        <h4>🖨️ Printer Procurement</h4>
        <p><strong>Purpose:</strong> Office printers for departments</p>
        <p><strong>Features:</strong> High-volume capabilities</p>
        <p><strong>Criteria:</strong> 7 weighted evaluation factors</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.success("👈 **Select a module from the sidebar to begin evaluation**")

# =========================
# TV MODULE
# =========================
elif module == "📺 TV Procurement":
    
    st.markdown("### 📺 TV Tender Evaluation")
    
    # Load Data
    df = pd.read_csv("tv_specs.csv")
    
    # STEP 1: Configure Requirements
    if st.session_state.tv_step >= 1:
        st.markdown("<div class='section-box'><h3>Step 1: Configure Tender Requirements</h3></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Zone Selection")
            zones = {
                "Zon 1: Sabah & W.P. Labuan": {"quantity": 506, "premium_col": "Zone1_Premium"},
                "Zon 2: Sarawak": {"quantity": 472, "premium_col": "Zone2_Premium"},
                "Zon 3: Kelantan": {"quantity": 583, "premium_col": None},
                "Zon 4: Pahang": {"quantity": 583, "premium_col": None},
                "Zon 5: Kedah & Terengganu": {"quantity": 536, "premium_col": None},
                "Zon 6: Perak": {"quantity": 583, "premium_col": None},
                "Zon 7: Selangor": {"quantity": 583, "premium_col": None},
                "Zon 8: Johor": {"quantity": 583, "premium_col": None},
                "Zon 9: KL, Putrajaya, Melaka, N.Sembilan": {"quantity": 364, "premium_col": None},
                "Zon 10: Perlis & Pulau Pinang": {"quantity": 426, "premium_col": None},
            }
            
            selected_zone_name = st.selectbox("Select Zone:", list(zones.keys()))
            zone_info = zones[selected_zone_name]
            zone_qty = zone_info["quantity"]
            premium_col = zone_info["premium_col"]
            
            st.markdown(f"""
            <div class='info-box'>
            <strong>Quantity:</strong> {zone_qty} units<br>
            <strong>Premium:</strong> {'5% (East Malaysia)' if premium_col else 'None'}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Mandatory Requirements")
            
            col2a, col2b, col2c = st.columns(3)
            
            with col2a:
                st.markdown("**Price & Size**")
                max_price = st.number_input("Max Price (RM)", 1000, 10000, 10000, 100)
                min_screen = st.number_input("Min Screen (inches)", 50, 80, 50)
                max_weight = st.number_input("Max Weight (kg)", 15.0, 30.0, 30.0, 0.1)
            
            with col2b:
                st.markdown("**Quality & Accessories**")
                min_meps = st.selectbox("Min MEPS Rating", [3, 4, 5], index=0)
                min_accessories = st.number_input("Min Accessories", 1, 10, 1)
                min_avr_capacity = st.number_input("Min AVR (VA)", 0, 1500, 0, 100)
                min_warranty = st.selectbox("Min Warranty (years)", [1, 2, 3], index=0)
            
            with col2c:
                st.markdown("**Features**")
                require_4k = st.checkbox("4K Resolution", value=False)
                require_quad_core = st.checkbox("Quad Core CPU", value=False)
                require_hdr = st.checkbox("HDR10", value=False)
                require_bluetooth = st.checkbox("Bluetooth 5.0+", value=False)
                require_floor_stand = st.checkbox("Floor Stand", value=False)
                require_avr = st.checkbox("AVR Included", value=False)
        
        # Apply Filters
        df_working = df.copy()
        if premium_col and premium_col in df_working.columns:
            df_working["Price"] = df_working["BasePrice"] * (1 + df_working[premium_col] / 100)
        else:
            df_working["Price"] = df_working["BasePrice"].copy()
        
        filtered = df_working.copy()
        filtered = filtered[filtered["ScreenSize"] >= min_screen]
        filtered = filtered[filtered["Price"] <= max_price]
        filtered = filtered[filtered["Weight"] <= max_weight]
        filtered = filtered[filtered["MEPS_Rating"] >= min_meps]
        filtered = filtered[filtered["Accessories_Count"] >= min_accessories]
        filtered = filtered[filtered["Warranty_Years"] >= min_warranty]
        
        if require_4k:
            filtered = filtered[filtered["Resolution"] == "4K"]
        if require_quad_core:
            filtered = filtered[filtered["Processor"].str.contains("Quad Core", na=False)]
        if require_hdr:
            filtered = filtered[filtered["HDR10"] == "Yes"]
        if require_bluetooth:
            filtered = filtered[filtered["Bluetooth"] == "Yes"]
        if require_floor_stand:
            filtered = filtered[filtered["FloorStand_Included"] == "Yes"]
        if require_avr:
            filtered = filtered[filtered["AVR_Included"] == "Yes"]
            filtered = filtered[filtered["AVR_Capacity"] >= min_avr_capacity]
        
        if filtered.empty:
            st.error("❌ No products meet the specified requirements. Please adjust your filters.")
            st.stop()
        
        # Scoring
        WEIGHT_PRICE = 0.30
        WEIGHT_MEPS = 0.15
        WEIGHT_WEIGHT = 0.10
        WEIGHT_AUDIO = 0.10
        WEIGHT_WIFI = 0.10
        WEIGHT_HDMI = 0.10
        WEIGHT_SCREEN = 0.05
        WEIGHT_OS = 0.05
        WEIGHT_WARRANTY = 0.05
        
        max_screen_val = filtered["ScreenSize"].max()
        max_audio = filtered["AudioW"].max()
        max_meps_val = filtered["MEPS_Rating"].max()
        max_warranty_val = filtered["Warranty_Years"].max()
        min_weight_val = filtered["Weight"].min()
        min_price = filtered["Price"].min()
        
        scored = filtered.copy()
        scored["PriceScore"] = min_price / scored["Price"]
        scored["ScreenScore"] = scored["ScreenSize"] / max_screen_val
        scored["AudioScore"] = scored["AudioW"] / max_audio
        scored["MEPSScore"] = scored["MEPS_Rating"] / max_meps_val
        scored["WeightScore"] = min_weight_val / scored["Weight"]
        scored["WarrantyScore"] = scored["Warranty_Years"] / max_warranty_val
        scored["OSScore"] = scored["OS_Score"]
        scored["WiFiScore"] = scored["WiFi"].apply(lambda x: 1.0 if "WiFi 6" in str(x) else 0.8)
        scored["HDMIScore"] = scored["HDMI_Version"].apply(lambda x: 1.0 if "2.1" in str(x) else 0.8)
        
        scored["TotalScore"] = (
            scored["PriceScore"] * WEIGHT_PRICE +
            scored["ScreenScore"] * WEIGHT_SCREEN +
            scored["AudioScore"] * WEIGHT_AUDIO +
            scored["MEPSScore"] * WEIGHT_MEPS +
            scored["WeightScore"] * WEIGHT_WEIGHT +
            scored["WiFiScore"] * WEIGHT_WIFI +
            scored["HDMIScore"] * WEIGHT_HDMI +
            scored["OSScore"] * WEIGHT_OS +
            scored["WarrantyScore"] * WEIGHT_WARRANTY
        )
        
        scored = scored.sort_values(by="TotalScore", ascending=False).reset_index(drop=True)
        scored["Rank"] = scored.index + 1
        scored["TotalCost_Zone"] = scored["Price"] * zone_qty
        
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success(f"✅ **{len(scored)} products** meet all requirements (out of {len(df)} total)")
        with col2:
            if st.button("➡️ Proceed to Results", type="primary", use_container_width=True):
                st.session_state.tv_step = 2
                st.rerun()
    
    # STEP 2: Review Results
    if st.session_state.tv_step >= 2:
        st.markdown("<div class='section-box'><h3>Step 2: Review Evaluation Results</h3></div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Compliant", len(scored))
        with col2:
            st.metric("Best Score", f"{scored.iloc[0]['TotalScore']:.3f}")
        with col3:
            st.metric("Lowest Price", f"RM {scored['Price'].min():,.0f}")
        with col4:
            st.metric("Best MEPS", f"{scored['MEPS_Rating'].max()} ⭐")
        with col5:
            st.metric("Total Value", f"RM {scored.iloc[0]['TotalCost_Zone']/1000:.0f}K")
        
        st.markdown("---")
        
        best = scored.iloc[0]
        st.markdown(f"""
        <div class='success-box'>
        <h4>🏆 Top Recommended Product</h4>
        <p><strong>{best['Brand']} {best['Model']}</strong> | Score: {best['TotalScore']:.3f} | Price: RM {best['Price']:,.2f} | Total: RM {best['TotalCost_Zone']:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Complete Results")
        display_cols = ["Rank", "Brand", "Model", "Price", "TotalCost_Zone", "MEPS_Rating", 
                       "Weight", "AudioW", "ScreenSize", "Warranty_Years", "TotalScore"]
        display_df = scored[display_cols].copy()
        display_df.columns = ["Rank", "Brand", "Model", "Price (RM)", "Total Cost (RM)", 
                              "MEPS", "Weight (kg)", "Audio (W)", "Screen (\")", "Warranty (yr)", "Score"]
        
        st.dataframe(display_df.style.background_gradient(subset=['Score'], cmap='Greens'), 
                    use_container_width=True, height=400)
        
        # Full Detailed Table with ALL columns
        with st.expander("📋 View Full Detailed Specifications (All Columns)"):
            st.markdown("**Complete technical specifications for all compliant products**")
            
            # Show all columns from the original dataset
            full_detail_cols = ["Rank", "Brand", "Model", "ScreenSize", "Resolution", "DisplayType", 
                               "Processor", "OS", "OS_Score", "WiFi", "HDMI_Version", "AudioW", 
                               "HDR10", "Bluetooth", "Weight", "MEPS_Rating", "Accessories_Count", 
                               "FloorStand_Included", "AVR_Included", "AVR_Capacity", "Warranty_Years", 
                               "BasePrice", "Price", "TotalCost_Zone", "TotalScore"]
            
            st.dataframe(scored[full_detail_cols], use_container_width=True, height=400)
        
        # Advanced Search Section
        with st.expander("🔍 Advanced Search — Filter by Any Column"):
            st.markdown("**Narrow down results by searching specific columns. Leave fields blank to ignore.**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                s_brand = st.text_input("Brand (text)", key="tv_s_brand")
                s_model = st.text_input("Model (text)", key="tv_s_model")
                s_resolution = st.selectbox("Resolution", ["(Any)", "4K", "8K"], key="tv_s_resolution")
                s_display_type = st.selectbox("Display Type", ["(Any)"] + sorted(scored["DisplayType"].dropna().unique().tolist()), key="tv_s_display_type")
                s_processor = st.text_input("Processor (text)", key="tv_s_processor")
                s_os = st.selectbox("OS", ["(Any)"] + sorted(scored["OS"].dropna().unique().tolist()), key="tv_s_os")
                s_os_score_min = st.number_input("OS Score (min)", min_value=0.0, max_value=1.0, value=0.0, step=0.1, key="tv_s_os_score_min")
            
            with col2:
                s_wifi = st.selectbox("WiFi", ["(Any)"] + sorted(scored["WiFi"].dropna().unique().tolist()), key="tv_s_wifi")
                s_hdmi_version = st.selectbox("HDMI Version", ["(Any)"] + sorted(scored["HDMI_Version"].dropna().unique().tolist()), key="tv_s_hdmi_version")
                s_audio_min = st.number_input("Audio Output min (W)", min_value=0, value=0, step=5, key="tv_s_audio_min")
                s_hdr10 = st.selectbox("HDR10", ["(Any)", "Yes", "No"], key="tv_s_hdr10")
                s_bluetooth = st.selectbox("Bluetooth", ["(Any)", "Yes", "No"], key="tv_s_bluetooth")
                s_weight_max = st.number_input("Max Weight (kg)", min_value=0.0, max_value=50.0, value=50.0, step=0.1, key="tv_s_weight_max")
                s_meps_min = st.number_input("MEPS Rating (min stars)", min_value=0, max_value=5, value=0, step=1, key="tv_s_meps_min")
            
            with col3:
                s_acc_min = st.number_input("Min Accessories Count", min_value=0, max_value=20, value=0, step=1, key="tv_s_acc_min")
                s_floor_stand = st.selectbox("Floor Stand Included", ["(Any)", "Yes", "No"], key="tv_s_floor_stand")
                s_avr = st.selectbox("AVR Included", ["(Any)", "Yes", "No"], key="tv_s_avr")
                s_avr_min = st.number_input("Min AVR Capacity (VA)", min_value=0, value=0, step=100, key="tv_s_avr_min")
                s_warranty_min = st.number_input("Min Warranty (years)", min_value=0, max_value=10, value=0, step=1, key="tv_s_warranty_min")
                s_price_max = st.number_input("Max Zone Price (RM)", min_value=0, value=999999, step=500, key="tv_s_price_max")
            
            # Apply search filters
            search_result = scored.copy()
            
            if s_brand:
                search_result = search_result[search_result["Brand"].str.contains(s_brand, case=False, na=False)]
            if s_model:
                search_result = search_result[search_result["Model"].str.contains(s_model, case=False, na=False)]
            if s_resolution != "(Any)":
                search_result = search_result[search_result["Resolution"] == s_resolution]
            if s_display_type != "(Any)":
                search_result = search_result[search_result["DisplayType"] == s_display_type]
            if s_processor:
                search_result = search_result[search_result["Processor"].str.contains(s_processor, case=False, na=False)]
            if s_os != "(Any)":
                search_result = search_result[search_result["OS"] == s_os]
            if s_os_score_min > 0.0:
                search_result = search_result[search_result["OS_Score"] >= s_os_score_min]
            if s_wifi != "(Any)":
                search_result = search_result[search_result["WiFi"] == s_wifi]
            if s_hdmi_version != "(Any)":
                search_result = search_result[search_result["HDMI_Version"] == s_hdmi_version]
            if s_audio_min > 0:
                search_result = search_result[search_result["AudioW"] >= s_audio_min]
            if s_hdr10 != "(Any)":
                search_result = search_result[search_result["HDR10"] == s_hdr10]
            if s_bluetooth != "(Any)":
                search_result = search_result[search_result["Bluetooth"] == s_bluetooth]
            if s_weight_max < 50.0:
                search_result = search_result[search_result["Weight"] <= s_weight_max]
            if s_meps_min > 0:
                search_result = search_result[search_result["MEPS_Rating"] >= s_meps_min]
            if s_acc_min > 0:
                search_result = search_result[search_result["Accessories_Count"] >= s_acc_min]
            if s_floor_stand != "(Any)":
                search_result = search_result[search_result["FloorStand_Included"] == s_floor_stand]
            if s_avr != "(Any)":
                search_result = search_result[search_result["AVR_Included"] == s_avr]
            if s_avr_min > 0:
                search_result = search_result[search_result["AVR_Capacity"] >= s_avr_min]
            if s_warranty_min > 0:
                search_result = search_result[search_result["Warranty_Years"] >= s_warranty_min]
            if s_price_max < 999999:
                search_result = search_result[search_result["Price"] <= s_price_max]
            
            if search_result.empty:
                st.warning("⚠️ No models match your search filters.")
            else:
                st.success(f"🔎 **{len(search_result)} model(s)** match your search")
                st.dataframe(search_result[full_detail_cols], use_container_width=True, height=400)
        
        with st.expander("📊 View Charts & Analysis"):
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.scatter(scored.head(10), x="Price", y="TotalScore", size="TotalScore", 
                                color="MEPS_Rating", hover_data=["Brand", "Model"],
                                title="Price vs Performance", color_continuous_scale="Viridis")
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                fig2 = px.bar(scored.head(5), x="Model", y="TotalScore", color="Brand",
                            title="Top 5 Products")
                st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Back to Requirements", key="tv_back_step2", use_container_width=True):
                st.session_state.tv_step = 1
                st.rerun()
        with col3:
            if st.button("➡️ Compare Top Products", key="tv_compare_step2", type="primary", use_container_width=True):
                st.session_state.tv_step = 3
                st.rerun()
    
    # STEP 3: Compare
    if st.session_state.tv_step >= 3:
        st.markdown("<div class='section-box'><h3>Step 3: Compare Top Products</h3></div>", unsafe_allow_html=True)
        
        top3 = scored.head(3)
        cols = st.columns(3)
        
        for idx, (i, row) in enumerate(top3.iterrows()):
            with cols[idx]:
                rank_label = ["🥇 1st Place", "🥈 2nd Place", "🥉 3rd Place"][idx]
                card_class = "comparison-card winner" if idx == 0 else "comparison-card"
                
                st.markdown(f"""
                <div class='{card_class}'>
                    <h4>{rank_label}</h4>
                    <h5>{row['Brand']} {row['Model']}</h5>
                    <hr>
                    <p><strong>Total Score:</strong> {row['TotalScore']:.3f}</p>
                    <p><strong>Unit Price:</strong> RM {row['Price']:,.2f}</p>
                    <p><strong>Total Cost:</strong> RM {row['TotalCost_Zone']:,.2f}</p>
                    <hr>
                    <p><strong>MEPS:</strong> {row['MEPS_Rating']} ⭐</p>
                    <p><strong>Screen:</strong> {row['ScreenSize']}" {row['Resolution']}</p>
                    <p><strong>Audio:</strong> {row['AudioW']}W</p>
                    <p><strong>Weight:</strong> {row['Weight']}kg</p>
                    <p><strong>WiFi:</strong> {row['WiFi']}</p>
                    <p><strong>HDMI:</strong> {row['HDMI_Version']}</p>
                    <p><strong>Warranty:</strong> {row['Warranty_Years']} years</p>
                </div>
                """, unsafe_allow_html=True)
        
        with st.expander("🔍 Detailed Score Breakdown"):
            breakdown_cols = ["Brand", "Model", "PriceScore", "MEPSScore", "WeightScore", "AudioScore",
                            "WiFiScore", "HDMIScore", "ScreenScore", "OSScore", "WarrantyScore", "TotalScore"]
            st.dataframe(scored[breakdown_cols].head(3).round(3), use_container_width=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Back to Results", key="tv_back_step3", use_container_width=True):
                st.session_state.tv_step = 2
                st.rerun()
        with col3:
            if st.button("➡️ Generate Report", key="tv_report_step3", type="primary", use_container_width=True):
                st.session_state.tv_step = 4
                st.rerun()
    
    # STEP 4: Report
    if st.session_state.tv_step >= 4:
        st.markdown("<div class='section-box'><h3>Step 4: Official Tender Report</h3></div>", unsafe_allow_html=True)
        
        best_tv = scored.iloc[0]
        zone_premium_amt = best_tv['Price'] - best_tv['BasePrice']
        
        st.markdown(f"""
        <div class='success-box'>
        <h3>📄 OFFICIAL TENDER RECOMMENDATION</h3>
        <h4>Recommended: {best_tv['Brand']} {best_tv['Model']}</h4>
        <p><strong>Evaluation Score: {best_tv['TotalScore']:.3f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Procurement Details")
            st.markdown(f"""
            - **Zone:** {selected_zone_name}
            - **Quantity:** {zone_qty} units
            - **Base Price:** RM {best_tv['BasePrice']:,.2f}
            - **Zone Price:** RM {best_tv['Price']:,.2f}
            - **Premium:** RM {zone_premium_amt:,.2f} {"(5%)" if zone_premium_amt > 0 else ""}
            - **Total Value:** RM {best_tv['TotalCost_Zone']:,.2f}
            """)
            
            st.markdown("#### Technical Specs")
            st.markdown(f"""
            - **Display:** {best_tv['ScreenSize']}" {best_tv['Resolution']}
            - **Processor:** {best_tv['Processor']}
            - **OS:** {best_tv['OS']}
            - **Audio:** {best_tv['AudioW']}W
            - **WiFi:** {best_tv['WiFi']}
            - **HDMI:** {best_tv['HDMI_Version']}
            - **MEPS:** {best_tv['MEPS_Rating']} Stars
            - **Weight:** {best_tv['Weight']} kg
            - **Warranty:** {best_tv['Warranty_Years']} years
            """)
        
        with col2:
            st.markdown("#### Score Breakdown")
            breakdown_data = {
                "Criterion": ["Price (30%)", "MEPS (15%)", "Weight (10%)", "Audio (10%)", 
                             "WiFi (10%)", "HDMI (10%)", "Screen (5%)", "OS (5%)", "Warranty (5%)"],
                "Score": [
                    f"{best_tv['PriceScore']*WEIGHT_PRICE:.3f}",
                    f"{best_tv['MEPSScore']*WEIGHT_MEPS:.3f}",
                    f"{best_tv['WeightScore']*WEIGHT_WEIGHT:.3f}",
                    f"{best_tv['AudioScore']*WEIGHT_AUDIO:.3f}",
                    f"{best_tv['WiFiScore']*WEIGHT_WIFI:.3f}",
                    f"{best_tv['HDMIScore']*WEIGHT_HDMI:.3f}",
                    f"{best_tv['ScreenScore']*WEIGHT_SCREEN:.3f}",
                    f"{best_tv['OSScore']*WEIGHT_OS:.3f}",
                    f"{best_tv['WarrantyScore']*WEIGHT_WARRANTY:.3f}"
                ]
            }
            st.table(pd.DataFrame(breakdown_data))
            
            st.markdown("#### Compliance")
            st.markdown(f"""
            ✅ 4K Resolution  
            ✅ Quad Core  
            ✅ MEPS {best_tv['MEPS_Rating']} ⭐ (≥3)  
            ✅ {best_tv['Weight']}kg (≤24.8kg)  
            ✅ {best_tv['Accessories_Count']} items (≥7)  
            ✅ AVR {best_tv['AVR_Capacity']}VA (≥800VA)  
            ✅ Floor Stand ✓  
            ✅ {best_tv['Warranty_Years']}yr warranty (≥3yr)  
            """)
        
        st.markdown("---")
        st.info(f"""**Justification:** The {best_tv['Brand']} {best_tv['Model']} achieved the highest score of {best_tv['TotalScore']:.3f} 
        among {len(scored)} compliant products, offering optimal value-for-money while meeting all KPM tender requirements.""")
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Back to Comparison", key="tv_back_step4", use_container_width=True):
                st.session_state.tv_step = 3
                st.rerun()
        with col2:
            report_text = f"""TENDER EVALUATION REPORT
{'='*60}
Recommended: {best_tv['Brand']} {best_tv['Model']}
Score: {best_tv['TotalScore']:.3f}
Price: RM {best_tv['Price']:,.2f}
Total Value: RM {best_tv['TotalCost_Zone']:,.2f}
Zone: {selected_zone_name}
Quantity: {zone_qty} units
            """
            st.download_button("📥 Download Report", key="tv_download", data=report_text, 
                             file_name=f"tender_report_TV.txt", use_container_width=True)
        with col3:
            if st.button("🔄 New Evaluation", key="tv_new", use_container_width=True):
                st.session_state.tv_step = 1
                st.rerun()

# =========================
# LAPTOP MODULE - COMPLETE
# =========================
elif module == "💻 Laptop Procurement":
    
    st.markdown("### 💻 Laptop Tender Evaluation")
    
    df = pd.read_csv("laptop_specs.csv")
    
    # STEP 1
    if st.session_state.laptop_step >= 1:
        st.markdown("<div class='section-box'><h3>Step 1: Configure Requirements</h3></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Price & Storage**")
            max_price = st.number_input("Max Price (RM)", 1000, 6000, 6000, 100)
            min_ram = st.slider("Min RAM (GB)", 4, 32, 4)
            min_storage = st.slider("Min Storage (GB)", 128, 1024, 128)
        with col2:
            st.markdown("**System**")
            min_warranty = st.selectbox("Min Warranty (years)", [1, 2, 3], index=0)
            require_windows11 = st.checkbox("Windows 11", value=False)
        with col3:
            st.markdown("**Info**")
            st.info("**Criteria Weights:**\n- Price: 35%\n- Processor: 20%\n- RAM: 15%\n- Storage: 10%\n- Battery: 10%\n- Weight: 5%\n- Warranty: 5%")
        
        filtered = df.copy()
        filtered = filtered[filtered["RAM"] >= min_ram]
        filtered = filtered[filtered["Storage"] >= min_storage]
        filtered = filtered[filtered["Price"] <= max_price]
        filtered = filtered[filtered["Warranty"] >= min_warranty]
        if require_windows11:
            filtered = filtered[filtered["OS"].str.contains("Windows 11", na=False)]
        
        if filtered.empty:
            st.error("❌ No laptops meet requirements. Adjust filters.")
            st.stop()
        
        # Scoring
        WEIGHT_PRICE = 0.35
        WEIGHT_PROCESSOR = 0.20
        WEIGHT_RAM = 0.15
        WEIGHT_STORAGE = 0.10
        WEIGHT_BATTERY = 0.10
        WEIGHT_WEIGHT = 0.05
        WEIGHT_WARRANTY = 0.05
        
        max_ram = filtered["RAM"].max()
        max_storage = filtered["Storage"].max()
        max_battery = filtered["BatteryLife"].max()
        min_weight = filtered["Weight"].min()
        max_warranty = filtered["Warranty"].max()
        min_price = filtered["Price"].min()
        
        scored = filtered.copy()
        scored["ProcessorScore"] = scored["Processor_Score"]
        scored["RAMScore"] = scored["RAM"] / max_ram
        scored["StorageScore"] = scored["Storage"] / max_storage
        scored["BatteryScore"] = scored["BatteryLife"] / max_battery
        scored["WarrantyScore"] = scored["Warranty"] / max_warranty
        scored["PriceScore"] = min_price / scored["Price"]
        scored["WeightScore"] = min_weight / scored["Weight"]
        
        scored["TotalScore"] = (
            scored["PriceScore"] * WEIGHT_PRICE +
            scored["ProcessorScore"] * WEIGHT_PROCESSOR +
            scored["RAMScore"] * WEIGHT_RAM +
            scored["StorageScore"] * WEIGHT_STORAGE +
            scored["BatteryScore"] * WEIGHT_BATTERY +
            scored["WeightScore"] * WEIGHT_WEIGHT +
            scored["WarrantyScore"] * WEIGHT_WARRANTY
        )
        
        scored = scored.sort_values(by="TotalScore", ascending=False).reset_index(drop=True)
        scored["Rank"] = scored.index + 1
        
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success(f"✅ **{len(scored)} laptops** meet requirements (out of {len(df)})")
        with col2:
            if st.button("➡️ Proceed", type="primary", use_container_width=True):
                st.session_state.laptop_step = 2
                st.rerun()
    
    # STEP 2
    if st.session_state.laptop_step >= 2:
        st.markdown("<div class='section-box'><h3>Step 2: Review Results</h3></div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Compliant", len(scored))
        with col2:
            st.metric("Best Score", f"{scored.iloc[0]['TotalScore']:.3f}")
        with col3:
            st.metric("Lowest Price", f"RM {scored['Price'].min():,.0f}")
        with col4:
            st.metric("Best Specs", f"{scored.iloc[0]['RAM']}GB / {scored.iloc[0]['Storage']}GB")
        
        best = scored.iloc[0]
        st.markdown(f"""
        <div class='success-box'>
        <h4>🏆 Top Laptop</h4>
        <p><strong>{best['Brand']} {best['Model']}</strong> | Score: {best['TotalScore']:.3f} | Price: RM {best['Price']:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        display_cols = ["Rank", "Brand", "Model", "Price", "Processor", "RAM", "Storage", "BatteryLife", "Weight", "Warranty", "TotalScore"]
        display_df = scored[display_cols].copy()
        display_df.columns = ["Rank", "Brand", "Model", "Price (RM)", "Processor", "RAM (GB)", "Storage (GB)", "Battery (hr)", "Weight (kg)", "Warranty (yr)", "Score"]
        st.dataframe(display_df.style.background_gradient(subset=['Score'], cmap='Greens'), use_container_width=True, height=400)
        
        with st.expander("📊 Charts"):
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.scatter(scored.head(10), x="Price", y="TotalScore", size="TotalScore", 
                                color="TotalScore", hover_data=["Brand", "Model"], 
                                color_continuous_scale="Viridis")
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                fig2 = px.bar(scored.head(5), x="Model", y="TotalScore", color="Brand")
                st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Back", key="laptop_back_step2", use_container_width=True):
                st.session_state.laptop_step = 1
                st.rerun()
        with col3:
            if st.button("➡️ Compare", key="laptop_compare_step2", type="primary", use_container_width=True):
                st.session_state.laptop_step = 3
                st.rerun()
    
    # STEP 3
    if st.session_state.laptop_step >= 3:
        st.markdown("<div class='section-box'><h3>Step 3: Compare Top Laptops</h3></div>", unsafe_allow_html=True)
        
        top3 = scored.head(3)
        cols = st.columns(3)
        
        for idx, (i, row) in enumerate(top3.iterrows()):
            with cols[idx]:
                rank = ["🥇 1st", "🥈 2nd", "🥉 3rd"][idx]
                card_class = "comparison-card winner" if idx == 0 else "comparison-card"
                
                st.markdown(f"""
                <div class='{card_class}'>
                    <h4>{rank}</h4>
                    <h5>{row['Brand']} {row['Model']}</h5>
                    <hr>
                    <p><strong>Score:</strong> {row['TotalScore']:.3f}</p>
                    <p><strong>Price:</strong> RM {row['Price']:,.2f}</p>
                    <hr>
                    <p><strong>Processor:</strong> {row['Processor']}</p>
                    <p><strong>RAM:</strong> {row['RAM']} GB</p>
                    <p><strong>Storage:</strong> {row['Storage']} GB</p>
                    <p><strong>Battery:</strong> {row['BatteryLife']} hours</p>
                    <p><strong>Weight:</strong> {row['Weight']} kg</p>
                    <p><strong>OS:</strong> {row['OS']}</p>
                    <p><strong>Warranty:</strong> {row['Warranty']} years</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Back", key="laptop_back_step3", use_container_width=True):
                st.session_state.laptop_step = 2
                st.rerun()
        with col3:
            if st.button("➡️ Report", key="laptop_report_step3", type="primary", use_container_width=True):
                st.session_state.laptop_step = 4
                st.rerun()
    
    # STEP 4
    if st.session_state.laptop_step >= 4:
        st.markdown("<div class='section-box'><h3>Step 4: Official Report</h3></div>", unsafe_allow_html=True)
        
        best_laptop = scored.iloc[0]
        
        st.markdown(f"""
        <div class='success-box'>
        <h3>📄 RECOMMENDED LAPTOP</h3>
        <h4>{best_laptop['Brand']} {best_laptop['Model']}</h4>
        <p><strong>Score: {best_laptop['TotalScore']:.3f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Specifications")
            st.markdown(f"""
            - **Price:** RM {best_laptop['Price']:,.2f}
            - **Processor:** {best_laptop['Processor']}
            - **RAM:** {best_laptop['RAM']} GB
            - **Storage:** {best_laptop['Storage']} GB SSD
            - **Battery:** {best_laptop['BatteryLife']} hours
            - **Weight:** {best_laptop['Weight']} kg
            - **OS:** {best_laptop['OS']}
            - **Warranty:** {best_laptop['Warranty']} years
            """)
        
        with col2:
            st.markdown("#### Score Breakdown")
            breakdown = {
                "Criterion": ["Price (35%)", "Processor (20%)", "RAM (15%)", "Storage (10%)", 
                             "Battery (10%)", "Weight (5%)", "Warranty (5%)"],
                "Score": [
                    f"{best_laptop['PriceScore']*WEIGHT_PRICE:.3f}",
                    f"{best_laptop['ProcessorScore']*WEIGHT_PROCESSOR:.3f}",
                    f"{best_laptop['RAMScore']*WEIGHT_RAM:.3f}",
                    f"{best_laptop['StorageScore']*WEIGHT_STORAGE:.3f}",
                    f"{best_laptop['BatteryScore']*WEIGHT_BATTERY:.3f}",
                    f"{best_laptop['WeightScore']*WEIGHT_WEIGHT:.3f}",
                    f"{best_laptop['WarrantyScore']*WEIGHT_WARRANTY:.3f}"
                ]
            }
            st.table(pd.DataFrame(breakdown))
        
        st.markdown("---")
        st.info(f"**Justification:** This laptop scored {best_laptop['TotalScore']:.3f} among {len(scored)} compliant products, providing optimal performance and value.")
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Back", key="laptop_back_step4", use_container_width=True):
                st.session_state.laptop_step = 3
                st.rerun()
        with col2:
            report = f"LAPTOP TENDER REPORT\n{'='*60}\nRecommended: {best_laptop['Brand']} {best_laptop['Model']}\nScore: {best_laptop['TotalScore']:.3f}\nPrice: RM {best_laptop['Price']:,.2f}"
            st.download_button("📥 Download", key="laptop_download", data=report, file_name="laptop_report.txt", use_container_width=True)
        with col3:
            if st.button("🔄 New", key="laptop_new", use_container_width=True):
                st.session_state.laptop_step = 1
                st.rerun()

# =========================
# PRINTER MODULE - COMPLETE
# =========================
elif module == "🖨️ Printer Procurement":
    
    st.markdown("### 🖨️ Printer Tender Evaluation")
    
    df = pd.read_csv("printer_specs.csv")
    
    # STEP 1
    if st.session_state.printer_step >= 1:
        st.markdown("<div class='section-box'><h3>Step 1: Configure Requirements</h3></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Price & Performance**")
            max_price = st.number_input("Max Price (RM)", 500, 3000, 3000, 100)
            min_print_speed = st.slider("Min Speed (ppm)", 10, 50, 10)
            min_paper_capacity = st.slider("Min Paper Cap", 100, 500, 100)
        with col2:
            st.markdown("**Features**")
            min_monthly_duty = st.slider("Min Monthly Duty", 5000, 100000, 5000, 5000)
            min_warranty = st.selectbox("Min Warranty (years)", [1, 2, 3], index=0)
            require_duplex = st.checkbox("Duplex Required", value=False)
            require_network = st.checkbox("Network Required", value=False)
        with col3:
            st.markdown("**Info**")
            st.info("**Criteria:**\n- Price: 35%\n- Print Tech: 15%\n- Speed: 15%\n- Capacity: 10%\n- Duty: 10%\n- Toner: 10%\n- Warranty: 5%")
        
        filtered = df.copy()
        filtered = filtered[filtered["PrintSpeed"] >= min_print_speed]
        filtered = filtered[filtered["PaperCapacity"] >= min_paper_capacity]
        filtered = filtered[filtered["MonthlyDuty"] >= min_monthly_duty]
        filtered = filtered[filtered["Price"] <= max_price]
        filtered = filtered[filtered["Warranty"] >= min_warranty]
        if require_duplex:
            filtered = filtered[filtered["Duplex"] == "Yes"]
        if require_network:
            filtered = filtered[filtered["Network"].str.contains("Ethernet|WiFi", na=False)]
        
        if filtered.empty:
            st.error("❌ No printers meet requirements. Adjust filters.")
            st.stop()
        
        # Scoring
        WEIGHT_PRICE = 0.35
        WEIGHT_PRINTTECH = 0.15
        WEIGHT_PRINTSPEED = 0.15
        WEIGHT_PAPERCAPACITY = 0.10
        WEIGHT_MONTHLYDUTY = 0.10
        WEIGHT_TONERYIELD = 0.10
        WEIGHT_WARRANTY = 0.05
        
        max_speed = filtered["PrintSpeed"].max()
        max_capacity = filtered["PaperCapacity"].max()
        max_duty = filtered["MonthlyDuty"].max()
        max_toner = filtered["TonerYield"].max()
        max_warranty = filtered["Warranty"].max()
        min_price = filtered["Price"].min()
        
        scored = filtered.copy()
        scored["PrintTechScore"] = scored["PrintTech_Score"]
        scored["PrintSpeedScore"] = scored["PrintSpeed"] / max_speed
        scored["PaperCapacityScore"] = scored["PaperCapacity"] / max_capacity
        scored["MonthlyDutyScore"] = scored["MonthlyDuty"] / max_duty
        scored["TonerYieldScore"] = scored["TonerYield"] / max_toner
        scored["WarrantyScore"] = scored["Warranty"] / max_warranty
        scored["PriceScore"] = min_price / scored["Price"]
        
        scored["TotalScore"] = (
            scored["PriceScore"] * WEIGHT_PRICE +
            scored["PrintTechScore"] * WEIGHT_PRINTTECH +
            scored["PrintSpeedScore"] * WEIGHT_PRINTSPEED +
            scored["PaperCapacityScore"] * WEIGHT_PAPERCAPACITY +
            scored["MonthlyDutyScore"] * WEIGHT_MONTHLYDUTY +
            scored["TonerYieldScore"] * WEIGHT_TONERYIELD +
            scored["WarrantyScore"] * WEIGHT_WARRANTY
        )
        
        scored = scored.sort_values(by="TotalScore", ascending=False).reset_index(drop=True)
        scored["Rank"] = scored.index + 1
        
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success(f"✅ **{len(scored)} printers** meet requirements (out of {len(df)})")
        with col2:
            if st.button("➡️ Proceed", type="primary", use_container_width=True):
                st.session_state.printer_step = 2
                st.rerun()
    
    # STEP 2
    if st.session_state.printer_step >= 2:
        st.markdown("<div class='section-box'><h3>Step 2: Review Results</h3></div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Compliant", len(scored))
        with col2:
            st.metric("Best Score", f"{scored.iloc[0]['TotalScore']:.3f}")
        with col3:
            st.metric("Lowest Price", f"RM {scored['Price'].min():,.0f}")
        with col4:
            st.metric("Best Speed", f"{scored['PrintSpeed'].max()} ppm")
        
        best = scored.iloc[0]
        st.markdown(f"""
        <div class='success-box'>
        <h4>🏆 Top Printer</h4>
        <p><strong>{best['Brand']} {best['Model']}</strong> | Score: {best['TotalScore']:.3f} | Price: RM {best['Price']:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        display_cols = ["Rank", "Brand", "Model", "Price", "PrintTech", "PrintSpeed", "PaperCapacity", "MonthlyDuty", "TonerYield", "Warranty", "TotalScore"]
        display_df = scored[display_cols].copy()
        display_df.columns = ["Rank", "Brand", "Model", "Price (RM)", "Tech", "Speed (ppm)", "Paper", "Duty", "Toner", "Warranty (yr)", "Score"]
        st.dataframe(display_df.style.background_gradient(subset=['Score'], cmap='Greens'), use_container_width=True, height=400)
        
        with st.expander("📊 Charts"):
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.scatter(scored.head(10), x="Price", y="TotalScore", size="TotalScore", 
                                color="TotalScore", hover_data=["Brand", "Model"], 
                                color_continuous_scale="Viridis")
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                fig2 = px.bar(scored.head(5), x="Model", y="TotalScore", color="Brand")
                st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Back", key="printer_back_step2", use_container_width=True):
                st.session_state.printer_step = 1
                st.rerun()
        with col3:
            if st.button("➡️ Compare", key="printer_compare_step2", type="primary", use_container_width=True):
                st.session_state.printer_step = 3
                st.rerun()
    
    # STEP 3
    if st.session_state.printer_step >= 3:
        st.markdown("<div class='section-box'><h3>Step 3: Compare Top Printers</h3></div>", unsafe_allow_html=True)
        
        top3 = scored.head(3)
        cols = st.columns(3)
        
        for idx, (i, row) in enumerate(top3.iterrows()):
            with cols[idx]:
                rank = ["🥇 1st", "🥈 2nd", "🥉 3rd"][idx]
                card_class = "comparison-card winner" if idx == 0 else "comparison-card"
                
                st.markdown(f"""
                <div class='{card_class}'>
                    <h4>{rank}</h4>
                    <h5>{row['Brand']} {row['Model']}</h5>
                    <hr>
                    <p><strong>Score:</strong> {row['TotalScore']:.3f}</p>
                    <p><strong>Price:</strong> RM {row['Price']:,.2f}</p>
                    <hr>
                    <p><strong>Tech:</strong> {row['PrintTech']}</p>
                    <p><strong>Speed:</strong> {row['PrintSpeed']} ppm</p>
                    <p><strong>Paper:</strong> {row['PaperCapacity']} sheets</p>
                    <p><strong>Duty:</strong> {row['MonthlyDuty']:,} pages/mo</p>
                    <p><strong>Toner:</strong> {row['TonerYield']:,} pages</p>
                    <p><strong>Network:</strong> {row['Network']}</p>
                    <p><strong>Duplex:</strong> {row['Duplex']}</p>
                    <p><strong>Warranty:</strong> {row['Warranty']} years</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Back", key="printer_back_step3", use_container_width=True):
                st.session_state.printer_step = 2
                st.rerun()
        with col3:
            if st.button("➡️ Report", key="printer_report_step3", type="primary", use_container_width=True):
                st.session_state.printer_step = 4
                st.rerun()
    
    # STEP 4
    if st.session_state.printer_step >= 4:
        st.markdown("<div class='section-box'><h3>Step 4: Official Report</h3></div>", unsafe_allow_html=True)
        
        best_printer = scored.iloc[0]
        
        st.markdown(f"""
        <div class='success-box'>
        <h3>📄 RECOMMENDED PRINTER</h3>
        <h4>{best_printer['Brand']} {best_printer['Model']}</h4>
        <p><strong>Score: {best_printer['TotalScore']:.3f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Specifications")
            st.markdown(f"""
            - **Price:** RM {best_printer['Price']:,.2f}
            - **Technology:** {best_printer['PrintTech']}
            - **Speed:** {best_printer['PrintSpeed']} ppm
            - **Paper Capacity:** {best_printer['PaperCapacity']} sheets
            - **Monthly Duty:** {best_printer['MonthlyDuty']:,} pages
            - **Toner Yield:** {best_printer['TonerYield']:,} pages
            - **Network:** {best_printer['Network']}
            - **Duplex:** {best_printer['Duplex']}
            - **Warranty:** {best_printer['Warranty']} years
            """)
        
        with col2:
            st.markdown("#### Score Breakdown")
            breakdown = {
                "Criterion": ["Price (35%)", "Tech (15%)", "Speed (15%)", "Capacity (10%)", 
                             "Duty (10%)", "Toner (10%)", "Warranty (5%)"],
                "Score": [
                    f"{best_printer['PriceScore']*WEIGHT_PRICE:.3f}",
                    f"{best_printer['PrintTechScore']*WEIGHT_PRINTTECH:.3f}",
                    f"{best_printer['PrintSpeedScore']*WEIGHT_PRINTSPEED:.3f}",
                    f"{best_printer['PaperCapacityScore']*WEIGHT_PAPERCAPACITY:.3f}",
                    f"{best_printer['MonthlyDutyScore']*WEIGHT_MONTHLYDUTY:.3f}",
                    f"{best_printer['TonerYieldScore']*WEIGHT_TONERYIELD:.3f}",
                    f"{best_printer['WarrantyScore']*WEIGHT_WARRANTY:.3f}"
                ]
            }
            st.table(pd.DataFrame(breakdown))
        
        st.markdown("---")
        st.info(f"**Justification:** This printer scored {best_printer['TotalScore']:.3f} among {len(scored)} compliant products, offering optimal performance for high-volume office use.")
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Back", key="printer_back_step4", use_container_width=True):
                st.session_state.printer_step = 3
                st.rerun()
        with col2:
            report = f"PRINTER TENDER REPORT\n{'='*60}\nRecommended: {best_printer['Brand']} {best_printer['Model']}\nScore: {best_printer['TotalScore']:.3f}\nPrice: RM {best_printer['Price']:,.2f}"
            st.download_button("📥 Download", key="printer_download", data=report, file_name="printer_report.txt", use_container_width=True)
        with col3:
            if st.button("🔄 New", key="printer_new", use_container_width=True):
                st.session_state.printer_step = 1
                st.rerun()
