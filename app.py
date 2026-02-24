import streamlit as st

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="DesignerLogic.ai",
    layout="centered",
)

# ---------------------------------------------------
# CUSTOM CSS (CENTER ALIGN + CLEAN UI)
# ---------------------------------------------------
st.markdown("""
<style>

.block-container{
    max-width: 850px;
    margin: auto;
}

h1, h2, h3, p {
    text-align: center;
}

div.stButton > button {
    display: block;
    margin: auto;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("DesignerLogic.ai")

st.markdown(
    "<p style='font-size:18px;'>Plot Data to Project Feasibility</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------------------------------------------
# PROJECT INPUTS
# ---------------------------------------------------
st.header("Project Inputs")

building_type = st.selectbox(
    "Building Type",
    ["Residential", "Commercial"]
)

plot_area = st.number_input(
    "Plot Area (sq.ft)",
    min_value=1.0,
    value=1000.0,
    step=100.0
)

road_width = st.number_input(
    "Road Width (m)",
    min_value=1.0,
    value=9.0,
    step=1.0
)

generate = st.button("Generate Feasibility Report")

# ---------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------
if generate:

    # Basic zoning assumptions
    if road_width < 9:
        fsi = 1.5
        height_limit = 10
        floors = 3
        setback_front = 3
        setback_side = 1.5
    elif road_width < 18:
        fsi = 2.5
        height_limit = 20
        floors = 6
        setback_front = 5
        setback_side = 3
    else:
        fsi = 3.5
        height_limit = 30
        floors = 9
        setback_front = 7
        setback_side = 4

    total_builtup = plot_area * fsi
    typical_floor = total_builtup / floors
    sellable_area = total_builtup * 0.85

    st.markdown("---")
    st.header("Feasibility Report")

    # ---------------------------------------------------
    # BASIC CONTROLS
    # ---------------------------------------------------
    st.subheader("Basic Controls")

    st.markdown(f"**Permissible FSI:** `{fsi}`")
    st.markdown(f"**Height Limit:** `{height_limit} m`")
    st.markdown(f"**Estimated Floors (Zone-based):** `{floors}`")

    # ---------------------------------------------------
    # AREA STATEMENT
    # ---------------------------------------------------
    st.subheader("Area Statement")

    st.markdown(f"**Total Built-up Area:** `{total_builtup:,.2f} sq.ft`")
    st.markdown(f"**Typical Floor Plate:** `{typical_floor:,.2f} sq.ft`")
    st.markdown(f"**Sellable Area:** `{sellable_area:,.2f} sq.ft`")

    # ---------------------------------------------------
    # SETBACKS
    # ---------------------------------------------------
    st.subheader("Setbacks (m)")

    st.markdown(f"**Front:** `{setback_front}`")
    st.markdown(f"**Side:** `{setback_side}`")

    # ---------------------------------------------------
    # FIRE CLASSIFICATION (ONLY NON-RESIDENTIAL)
    # ---------------------------------------------------
    if building_type != "Residential":
        st.subheader("Fire Classification")

        if height_limit <= 15:
            fire_class = "Low Rise"
        elif height_limit <= 24:
            fire_class = "Mid Rise"
        else:
            fire_class = "High Rise"

        st.markdown(f"**Building Category:** `{fire_class}`")
