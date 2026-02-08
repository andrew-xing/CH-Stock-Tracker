import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# --- 1. SETTINGS & CUSTOM THEME ---
st.set_page_config(page_title="CH Stock Tracker", page_icon="🛡️", layout="centered")

# Custom CSS for the "Dark Luxe" aesthetic
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stApp { background-color: #000000; color: #E0E0E0; }
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { 
        background-color: #1A1A1A; color: white; border: 1px solid #333; 
        border-radius: 0px; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { border: 1px solid #FFFFFF; background-color: #333; }
    div[data-baseweb="select"] > div { background-color: #1A1A1A; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE CONNECTION ---
SUPABASE_URL = "https://jganzsgsvuzmmxklmgwq.supabase.co"
SUPABASE_KEY = "process.env.SUPABASE_KEY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 3. STORE DATA ---
STORES = {
    "Americas": ["Aspen", "Honolulu", "LV - Caesars", "LV - Fontainebleau", "LV - Wynn", "LA - Robertson Blvd",
                 "Malibu", "Miami", "NY - Madison Ave", "NY - Washington St", "St. Barth"],
    "Asia": ["Beijing - Yintai", "Chengdu - SKP", "Guangzhou", "Hangzhou", "HK - Peninsula", "HK - Prince's Bldg",
             "Nagoya", "Osaka", "Seoul - Cheongdam", "Seoul - Shinsegae", "Shanghai - Reel", "Singapore", "Taipei",
             "Tokyo - Aoyama", "Tokyo - Ginza", "Tokyo - Shinjuku", "Tokyo - Roppongi"],
    "Europe": ["London - Mount St", "London - Selfridges", "Manchester", "Paris"]
}

# --- 4. APP UI ---
st.title("🛡️ CH STOCK TRACKER")
st.caption("GLOBAL REAL-TIME INVENTORY | CROWDSOURCED")

tab_report, tab_live = st.tabs(["🚀 SUBMIT INTEL", "📡 LIVE FEED"])

with tab_report:
    # Location Picker
    col_reg, col_sto = st.columns(2)
    with col_reg:
        reg = st.selectbox("Region", list(STORES.keys()))
    with col_sto:
        sto = st.selectbox("Store", STORES[reg])

    st.markdown("---")

    # Jewelry Levels
    st.subheader("Jewelry Availability")
    c1, c2, c3 = st.columns(3)
    with c1:
        s_lvl = st.select_slider("Silver 925", ["OOS", "LOW", "GOOD"], value="LOW")
    with c2:
        g_lvl = st.select_slider("22k Gold", ["OOS", "LOW", "GOOD"], value="OOS")
    with c3:
        w_lvl = st.select_slider("18k WG", ["OOS", "LOW", "GOOD"], value="OOS")

    st.markdown("---")

    # Non-Jewelry Toggles
    st.subheader("Apparel & Accessories")
    ca, cb, cc, cd = st.columns(4)
    with ca:
        apparel = st.checkbox("👕 Tops")
    with cb:
        pants = st.checkbox("👖 Pants")
    with cc:
        leather = st.checkbox("👜 Bags")
    with cd:
        glasses = st.checkbox("👓 Eyewear")

    # Comments
    note = st.text_input("Specific Finds", placeholder="e.g., Black Levi's 32, Dagger Pendant in 22k")

    if st.button("SEND ANONYMOUS REPORT"):
        timestamp = datetime.now().strftime("%H:%M Local")
        report_data = {
            "store_name": sto,
            "silver_lvl": s_lvl,
            "gold_22k_lvl": g_lvl,
            "gold_18k_lvl": w_lvl,
            "has_apparel": apparel,
            "has_pants": pants,
            "has_leather": leather,
            "has_eyewear": glasses,
            "comment": note,
            "report_local_time": timestamp
        }

        try:
            supabase.table("ch_stock_tracker").insert(report_data).execute()
            st.success(f"Intel shared for {sto} at {timestamp}")
            st.balloons()
        except Exception as e:
            st.error(f"Upload failed: {e}")

with tab_live:
    st.subheader("Recent Global Reports")
    try:
        response = supabase.table("ch_stock_tracker").select("*").order("created_at", desc=True).limit(15).execute()
        for r in response.data:
            with st.container():
                st.markdown(f"**📍 {r['store_name']}** (`{r['report_local_time']}`)")

                # Visual badges for stock
                stock_line = f"Silver: `{r['silver_lvl']}`"
                if r['gold_22k_lvl'] != "OOS": stock_line += f" | 22k: `{r['gold_22k_lvl']}`"
                st.markdown(stock_line)

                # Category Icons
                icons = []
                if r['has_apparel']: icons.append("👕")
                if r['has_pants']: icons.append("👖")
                if r['has_leather']: icons.append("👜")
                if r['has_eyewear']: icons.append("👓")
                if icons: st.markdown(f"Available: {' '.join(icons)}")

                if r['comment']:
                    st.info(f"Note: {r['comment']}")
                st.divider()
    except:
        st.write("Refreshing feed...")