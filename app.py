import streamlit as st

st.set_page_config(page_title="DesignerLogic Feasibility Engine")

st.title("🏗️ DESIGNERLOGIC FEASIBILITY ENGINE")

# INPUTS
building_type = st.selectbox(
    "Building Type",
    ["Residential", "Commercial", "Mixed"]
)

plot_area = st.number_input("Plot Area (sq.ft)", min_value=0.0)
road_width = st.number_input("Road Width (m)", min_value=0.0)

# SIMPLE RULE ENGINE
def calculate_fsi(bt):
    if bt == "Residential":
        return 2.0
    elif bt == "Commercial":
        return 3.5
    else:
        return 2.5

def height_limit(road):
    if road >= 30:
        return 30.0
    return 15.0

# RUN BUTTON
if st.button("Generate Feasibility Report"):

    fsi = calculate_fsi(building_type)
    height = height_limit(road_width)

    total_builtup = plot_area * fsi
    floors = int(height // 3.3)

    st.header("FEASIBILITY REPORT")

    st.subheader("Basic Controls")
    st.write("Permissible FSI:", fsi)
    st.write("Height Limit:", height, "m")
    st.write("Estimated Floors:", floors)

    st.subheader("Area Statement")

    if building_type == "Commercial":
        sellable = total_builtup * 0.85
        st.write("Total Built-up Area:", round(total_builtup, 2), "sq.ft")
        st.write("Sellable Area:", round(sellable, 2), "sq.ft")
        st.write("Core includes: lifts, staircases, fire exits, services")
    else:
        carpet = total_builtup * 0.7
        st.write("Total Built-up Area:", round(total_builtup, 2), "sq.ft")
        st.write("Carpet Area:", round(carpet, 2), "sq.ft")

    st.subheader("Fire Safety")
    st.write("Fire Exit Staircases: Minimum 2")
    st.write("High-Rise Fire NOC Required")
