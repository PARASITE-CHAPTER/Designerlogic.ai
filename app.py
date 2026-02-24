import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
import io

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

# ---------------- PDF FUNCTION ----------------
def create_pdf(data):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="CenterTitle",
        parent=styles["Title"],
        alignment=TA_CENTER
    )

    body_style = styles["Normal"]

    story = []

    # Title
    story.append(Paragraph("Designerlogic.ai", title_style))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph(
        "Building Compliance & Estimation Report",
        styles["Heading2"]
    ))

    story.append(Spacer(1, 0.3 * inch))

    # Project Details
    for key, value in data.items():
        story.append(Paragraph(f"<b>{key}:</b> {value}", body_style))
        story.append(Spacer(1, 0.15 * inch))

    doc.build(story)

    buffer.seek(0)
    return buffer


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

# Fire classification hidden for residential
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

    summary_data = {
        "Project Name": project_name,
        "Building Type": building_type,
        "Plot Area": f"{plot_area} sq.m",
        "Built-up Area": f"{builtup_area} sq.m",
        "Floors": floors,
    }

    if building_type != "Residential":
        summary_data["Fire Classification"] = fire_classification
    else:
        summary_data["Fire Classification"] = "Not Required (Residential Project)"

    st.subheader("Project Summary")

    for k, v in summary_data.items():
        st.write(f"**{k}:** {v}")

    # -------- CREATE PDF --------
    pdf_file = create_pdf(summary_data)

    # -------- DOWNLOAD BUTTON --------
    st.download_button(
        label="⬇ Download PDF Report",
        data=pdf_file,
        file_name=f"{project_name}_Compliance_Report.pdf",
        mime="application/pdf"
    )
