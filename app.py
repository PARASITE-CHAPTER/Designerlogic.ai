import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Designerlogic.ai",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    max-width: 700px;
    margin: auto;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 40px;
}

.stButton>button {
    width: 100%;
    border-radius: 8px;
    height: 45px;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    "<div class='title'>Designerlogic.ai</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>AI-Powered Building Compliance & Cost Intelligence Platform</div>",
    unsafe_allow_html=True
)

# ---------------- FORM ----------------
st.header("Project Inputs")

project_name = st.text_input("Project Name")

building_type = st.selectbox(
    "Building Type",
    [
        "Residential",
        "Commercial",
        "Mixed Use",
        "Industrial",
        "Institutional"
    ]
)

plot_area = st.number_input("Plot Area (sq.m)", min_value=0.0)
builtup_area = st.number_input("Built-up Area (sq.m)", min_value=0.0)
floors = st.number_input("Number of Floors", min_value=1, step=1)

# -------- FIRE CLASSIFICATION LOGIC --------
fire_classification = None

if building_type != "Residential":
    fire_classification = st.selectbox(
        "Fire Classification",
        [
            "Low Hazard",
            "Moderate Hazard",
            "High Hazard"
        ]
    )

# ---------------- GENERATE REPORT ----------------
if st.button("Generate Compliance Report"):

    st.success("Report Generated Successfully ✅")

    st.subheader("Project Summary")

    st.write(f"**Project Name:** {project_name}")
    st.write(f"**Building Type:** {building_type}")
    st.write(f"**Plot Area:** {plot_area} sq.m")
    st.write(f"**Built-up Area:** {builtup_area} sq.m")
    st.write(f"**Floors:** {floors}")

    if building_type != "Residential":
        st.write(f"**Fire Classification:** {fire_classification}")
    else:
        st.write("**Fire Classification:** Not Required (Residential Project)")

    # Placeholder for next step
    st.info("PDF Download Button will be added next.")
