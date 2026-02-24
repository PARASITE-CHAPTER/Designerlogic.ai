# =====================================================
# DESIGNERLOGIC.AI — FEASIBILITY WEB APP
# =====================================================

import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Designerlogic.ai", layout="wide")

# =====================================================
# LOAD DATABASE
# =====================================================

FILE_NAME = "CMDA_RULE_ENGINE_TEMPLATE_V3.xlsx"

@st.cache_data
def load_data():
    xls = pd.ExcelFile(FILE_NAME)

    fsi_rules = pd.read_excel(xls, "1_FSI_RULES")
    setback_rules = pd.read_excel(xls, "2_SETBACK_RULES")
    parking_rules = pd.read_excel(xls, "3_PARKING_RULES")
    height_rules = pd.read_excel(xls, "4_HEIGHT_RULES")

    return fsi_rules, setback_rules, parking_rules, height_rules


fsi_rules, setback_rules, parking_rules, height_rules = load_data()

# =====================================================
# RULE ENGINE FUNCTIONS
# =====================================================

def get_fsi(building_type, road_width):

    rule = fsi_rules[
        (fsi_rules["category"].str.upper().str.startswith(building_type[0])) &
        (fsi_rules["min_road"] <= road_width) &
        (fsi_rules["max_road"] > road_width)
    ]

    return float(rule.iloc[0]["max_fsi"])


def get_height_limit(road_width):

    rule = height_rules[
        height_rules["road_width"] <= road_width
    ]

    return float(rule.iloc[-1]["max_height"])


def get_setback(building_type, height):

    rule = setback_rules[
        (setback_rules["category"].str.upper().str.startswith(building_type[0])) &
        (setback_rules["height_min"] <= height) &
        (setback_rules["height_max"] > height)
    ]

    row = rule.iloc[0]

    return {
        "front": float(row["front"]),
        "side": float(row["side"]),
        "rear": float(row["rear"])
    }


def calculate_parking(building_type, builtup):

    rule = parking_rules[
        parking_rules["category"].str.upper().str.startswith(building_type[0])
    ]

    unit_text = str(rule.iloc[0]["unit"])
    unit_area = float(unit_text.split("_")[0]) * 10.764  # sqm → sqft

    requirement = float(rule.iloc[0]["requirement"])

    return math.ceil((builtup / unit_area) * requirement)


# =====================================================
# AREA CALCULATION (NON-RESIDENTIAL ONLY)
# =====================================================

def calculate_area_breakdown(building_type, total_builtup, floors):

    floor_plate = total_builtup / floors

    core_ratio = 0.14   # professional feasibility assumption
    total_core_area = total_builtup * core_ratio

    result = {
        "floor_plate": floor_plate,
        "core_area": total_core_area,
        "sellable_area": total_builtup - total_core_area
    }

    return result


# =====================================================
# FIRE CLASSIFICATION
# =====================================================

def fire_safety_analysis(building_type, height):

    if building_type.startswith("R"):
        return None

    if height <= 15:
        category = "Low Rise Building"
        noc = "Standard Fire Compliance"
    elif height <= 24:
        category = "Mid Rise Building"
        noc = "Fire NOC Required"
    else:
        category = "High Rise Building"
        noc = "High-Rise Fire NOC Required"

    return {
        "building_class": category,
        "fire_noc": noc
    }


# =====================================================
# STREAMLIT UI
# =====================================================

st.subheader("Project Inputs")

building_type = st.selectbox(
    "Building Type",
    ["Residential", "Commercial", "Mixed"]
)

plot_area = st.number_input(
    "Plot Area (sq.ft)",
    min_value=1.0,
    step=100.0
)

road_width = st.number_input(
    "Road Width (m)",
    min_value=1.0,
    step=1.0
)

# =====================================================
# RUN ENGINE
# =====================================================

if st.button("Generate Feasibility Report"):

    fsi = get_fsi(building_type.upper(), road_width)
    height_limit = get_height_limit(road_width)

    total_builtup = plot_area * fsi
    floors = max(1, math.floor(height_limit / 3.3))

    setbacks = get_setback(building_type.upper(), height_limit)
    parking_required = calculate_parking(building_type.upper(), total_builtup)

    fire_data = fire_safety_analysis(building_type.upper(), height_limit)

    if not building_type.startswith("R"):
        area_data = calculate_area_breakdown(
            building_type.upper(),
            total_builtup,
            floors
        )

    # =====================================================
    # OUTPUT REPORT
    # =====================================================

    st.header("Feasibility Report")

    # BASIC CONTROLS
    st.subheader("Basic Controls")
    st.write("Permissible FSI:", fsi)
    st.write("Height Limit:", height_limit, "m")
    st.write("Estimated Floors (Zone-based):", floors)

    # AREA
    st.subheader("Area Statement")
    st.write("Total Built-up Area:", round(total_builtup,2), "sq.ft")

    if building_type.startswith("R"):
        st.write("Built-up Area (Residential):",
                 round(total_builtup,2), "sq.ft")
    else:
        st.write("Typical Floor Plate:",
                 round(area_data["floor_plate"],2), "sq.ft")

        st.write("Sellable Area:",
                 round(area_data["sellable_area"],2), "sq.ft")

    # SETBACKS
    st.subheader("Setbacks (m)")
    st.write("Front:", setbacks["front"])
    st.write("Side:", setbacks["side"])
    st.write("Rear:", setbacks["rear"])

    # PARKING
    st.subheader("Parking")
    st.write("Parking Required:", parking_required, "Cars")

    # FIRE CLASSIFICATION
    if fire_data is not None:
        st.subheader("Fire Classification")
        st.write("Building Category:", fire_data["building_class"])
        st.write("Compliance:", fire_data["fire_noc"])

    # NOTE
    st.info(
        "Note: Floor estimation is Zone-based approximation. "
        "Final approval subject to statutory authority verification."
    )
