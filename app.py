# ==============================
# ===== FEASIBILITY REPORT UI ==
# ==============================

st.title("Feasibility Report")

# ---------- BASIC CONTROLS ----------
st.subheader("Basic Controls")

st.write("Permissible FSI:", fsi)
st.write("Height Limit:", height_limit, "m")
st.write("Estimated Floors (Zone-based):", floors)


# ---------- AREA STATEMENT ----------
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


# ---------- SETBACKS ----------
st.subheader("Setbacks (m)")

st.write("Front:", setbacks["front"])
st.write("Side:", setbacks["side"])
st.write("Rear:", setbacks["rear"])


# ---------- PARKING ----------
st.subheader("Parking")

st.write("Parking Required:", parking_required, "Cars")


# ---------- FIRE CLASSIFICATION ----------
if fire_data is not None:

    st.subheader("Fire Classification")

    st.write(
        "Building Category:",
        fire_data["building_class"]
    )

    st.write(
        "Compliance:",
        fire_data["fire_noc"]
    )


# ---------- NOTE ----------
st.info(
    "Note: Floor estimation is Zone-based approximation. "
    "Final approval subject to statutory authority verification."
)
