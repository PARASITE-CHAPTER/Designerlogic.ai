import streamlit as st
import math

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Designerlogic.ai",
    layout="centered"
)

st.title("Designerlogic.ai")
st.subheader("Feasibility Engine — CMDA Based")

# ---------------- USER INPUT ----------------
building_type = st.selectbox(
    "Building Type",
    ["Residential", "Commercial", "Mixed"]
)

plot_area = st.number_input(
    "Plot Area (sq.ft)",
    min_value=100.0,
    value=3000.0
)

road_width = st.number_input(
    "Road Width (m)",
    min_value=3.0,
    value=12.0
)

# ---------------- MOCK RULE ENGINE ----------------
# (Your real functions will replace this later)

def get_fsi(bt, road):
    if bt == "Commercial":
        return 3.5
    elif bt == "Mixed":
        return 2.5
    return 2.0

def get_height_limit(road):
    if road >= 30:
        return 30
    elif road >= 18:
        return 24
    return 15

def fire_category(height):
    if height <= 15:
        return "Low Rise Building"
    elif height <= 24:
        return "Mid Rise Building"
    return "High Rise Building"


# ---------------- CALCULATION ----------------
if st.button("Generate Feasibility Report"):

    fsi = get_fsi(building_type, road_width)
    height_limit = get_height_limit(road_width)

    total_builtup = plot_area * fsi
    floors = max(1, math.floor(height_limit / 3.3))
    floor_plate = total_builtup / floors

    st.divider()

    st.header("Feasibility Report")

    st.subheader("Basic Controls")
    st.write("Permissible FSI:", fsi)
    st.write("Height Limit:", height_limit, "m")
    st.write("Estimated Floors (Zone based):", floors)

    st.subheader("Area Statement")
    st.write("Total Built-up Area:", round(total_builtup, 2), "sq.ft")
    st.write("Typical Floor Plate:", round(floor_plate, 2), "sq.ft")

    if building_type == "Commercial":
        sellable = total_builtup * 0.85
        st.write("Sellable Area:", round(sellable, 2), "sq.ft")
    else:
        carpet = total_builtup * 0.75
        st.write("Carpet Area:", round(carpet, 2), "sq.ft")

    st.subheader("Fire Classification")
    st.write("Building Category:", fire_category(height_limit))

    st.info(
        "Note: Floor estimation is Zone-based approximation. "
        "Final approval subject to statutory authority verification."
    )
