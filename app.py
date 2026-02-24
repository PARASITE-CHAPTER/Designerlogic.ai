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
# CUSTOM CSS
# (CENTER HEADER + LEFT REPORT)
# ---------------------------------------------------
st.markdown("""
<style>

.block-container{
    max-width: 850px;
    margin: auto;
}

/* Center only titles */
h1, h2 {
    text-align:center;
}

/* LEFT align report content */
.report-left {
    text-align:left;
}

div.stButton > button {
    display:block;
    margin:auto;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("DesignerLogic.ai")

st.markdown(
    "<p style='font-size:18px;text-align:center;'>AI-Driven Building Feasibility, Compliance & Estimation</p>",
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

    st.markdown("---")
    st.header("Feasibility Report")

    st.markdown('<div class="report-left">', unsafe_allow_html=True)

    report_text.append("DESIGNERLOGIC.AI FEASIBILITY REPORT")
    report_text.append(f"Building Type: {building_type}")

    # BASIC CONTROLS
    st.subheader("Basic Controls")

    st.markdown(f"**Permissible FSI:** {fsi}")
    st.markdown(f"**Height Limit:** {height_limit} m")
    st.markdown(f"**Estimated Floors (Zone-based):** {floors}")

    report_text += [
        f"Permissible FSI: {fsi}",
        f"Height Limit: {height_limit} m",
        f"Estimated Floors (Zone-based): {floors}"
    ]

    # AREA STATEMENT
    st.subheader("Area Statement")

    st.markdown(f"**Total Built-up Area:** {total_builtup:,.2f} sq.ft")
    st.markdown(f"**Typical Floor Plate:** {typical_floor:,.2f} sq.ft")
    st.markdown(f"**Sellable Area:** {sellable_area:,.2f} sq.ft")

    report_text += [
        f"Total Built-up Area: {total_builtup:,.2f} sq.ft",
        f"Typical Floor Plate: {typical_floor:,.2f} sq.ft",
        f"Sellable Area: {sellable_area:,.2f} sq.ft"
    ]

    # SETBACKS
    st.subheader("Setbacks (m)")

    st.markdown(f"Front: {setback_front}")
    st.markdown(f"Side: {setback_side}")

    report_text += [
        f"Front Setback: {setback_front} m",
        f"Side Setback: {setback_side} m"
    ]

    # FIRE CLASSIFICATION (NOT FOR RESIDENTIAL)
    if building_type in ["Commercial", "Mixed Use"]:

        st.subheader("Fire Classification")

        if height_limit <= 15:
            fire_class = "Low Rise"
        elif height_limit <= 24:
            fire_class = "Mid Rise"
        else:
            fire_class = "High Rise"

        st.markdown(f"Building Category: {fire_class}")
        report_text.append(f"Fire Classification: {fire_class}")

    # ---------------------------------------------------
    # NOTE SECTION
    # ---------------------------------------------------
    st.markdown("---")
    st.subheader("Notes")

    note_text = """
• Estimated floors are zone-based approximations and subject to authority approval.<br>
• FSI, setbacks and height limits are indicative planning values.<br>
• Detailed architectural and statutory verification required before approvals.<br>
• Fire compliance applicable only for Commercial and Mixed Use developments.
"""

    st.markdown(note_text, unsafe_allow_html=True)

    report_text.append("NOTES:")
    report_text.append("Estimated floors are zone-based approximations.")
    report_text.append("Values subject to authority approval.")
    report_text.append("Fire compliance applies only to Commercial and Mixed Use.")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------
    # DOWNLOAD PDF
    # ---------------------------------------------------
    st.markdown("---")

    pdf_file = generate_pdf(report_text)

    st.download_button(
        label="Download Feasibility Report (PDF)",
        data=pdf_file,
        file_name="DesignerLogic_Feasibility_Report.pdf",
        mime="application/pdf"
    )
