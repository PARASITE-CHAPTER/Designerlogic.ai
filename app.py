import streamlit as st
import io

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="DesignerLogic.ai",
    layout="centered"
)

# ---------------------------------------------------
# CUSTOM CSS (CENTER ALIGN CONTENT)
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
    "<p style='font-size:18px;'>AI-Driven Building Feasibility, Compliance & Estimation</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------------------------------------------
# PDF GENERATOR
# ---------------------------------------------------
def generate_pdf(report_lines):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    story = []

    for line in report_lines:
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 12))

    doc.build(story)

    buffer.seek(0)
    return buffer


# ---------------------------------------------------
# PROJECT INPUTS
# ---------------------------------------------------
st.header("Project Inputs")

building_type = st.selectbox(
    "Building Type",
    ["Residential", "Commercial", "Mixed Use"]
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

    report_text = []

    # ---- Zoning Logic ----
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

    # ---- Area Calculations ----
    total_builtup = plot_area * fsi
    typical_floor = total_builtup / floors
    sellable_area = total_builtup * 0.85

    # ---------------------------------------------------
    # REPORT UI
    # ---------------------------------------------------
    st.markdown("---")
    st.header("Feasibility Report")

    report_text.append("DESIGNERLOGIC.AI FEASIBILITY REPORT")
    report_text.append(f"Building Type: {building_type}")

    # BASIC CONTROLS
    st.subheader("Basic Controls")

    st.markdown(f"**Permissible FSI:** `{fsi}`")
    st.markdown(f"**Height Limit:** `{height_limit} m`")
    st.markdown(f"**Estimated Floors (Zone-based):** `{floors}`")

    report_text.append(f"Permissible FSI: {fsi}")
    report_text.append(f"Height Limit: {height_limit} m")
    report_text.append(f"Estimated Floors (Zone-based): {floors}")

    # AREA STATEMENT
    st.subheader("Area Statement")

    st.markdown(f"**Total Built-up Area:** `{total_builtup:,.2f} sq.ft`")
    st.markdown(f"**Typical Floor Plate:** `{typical_floor:,.2f} sq.ft`")
    st.markdown(f"**Sellable Area:** `{sellable_area:,.2f} sq.ft`")

    report_text.append(f"Total Built-up Area: {total_builtup:,.2f} sq.ft")
    report_text.append(f"Typical Floor Plate: {typical_floor:,.2f} sq.ft")
    report_text.append(f"Sellable Area: {sellable_area:,.2f} sq.ft")

    # SETBACKS
    st.subheader("Setbacks (m)")

    st.markdown(f"**Front:** `{setback_front}`")
    st.markdown(f"**Side:** `{setback_side}`")

    report_text.append(f"Front Setback: {setback_front} m")
    report_text.append(f"Side Setback: {setback_side} m")

    # FIRE CLASSIFICATION
    # NOT REQUIRED FOR RESIDENTIAL
    if building_type in ["Commercial", "Mixed Use"]:

        st.subheader("Fire Classification")

        if height_limit <= 15:
            fire_class = "Low Rise"
        elif height_limit <= 24:
            fire_class = "Mid Rise"
        else:
            fire_class = "High Rise"

        st.markdown(f"**Building Category:** `{fire_class}`")

        report_text.append(f"Fire Classification: {fire_class}")

    # ---------------------------------------------------
    # DOWNLOAD PDF BUTTON
    # ---------------------------------------------------
    st.markdown("---")

    pdf_file = generate_pdf(report_text)

    st.download_button(
        label="Download Feasibility Report (PDF)",
        data=pdf_file,
        file_name="DesignerLogic_Feasibility_Report.pdf",
        mime="application/pdf"
    )
