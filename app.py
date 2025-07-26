import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
from datetime import datetime

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

# Load logos
white_logo = Image.open("jspmlogo.png").convert("RGBA").resize((80, 80))
yellow_logo = Image.open("hadapsarjspmlogo.jpeg").convert("RGBA").resize((80, 80))

# Fonts
TITLE_FONT = "arialbd.ttf"
BODY_FONT = "arial.ttf"

# Styles
STYLES = [
    "Classic Gold", "Minimal Blue", "Dark Accent", "University Style",
    "Creative Event", "Royal Blue Formal", "Elegant Silver Grey",
    "Modern Geometric", "Retro Orange", "Green Nature",
    "Black-Gold Executive", "Purple Galaxy"
]

# Design Configurations
STYLE_CONFIGS = {
    "Classic Gold": {"bg": "#fff8dc", "border": "#bfa12d", "font": "#000", "accent": "#d4af37"},
    "Minimal Blue": {"bg": "#ffffff", "border": "#0066cc", "font": "#000", "accent": "#cce6ff"},
    "Dark Accent": {"bg": "#1c1c1c", "border": "#555555", "font": "#ffffff", "accent": "#e0c97f"},
    "University Style": {"bg": "#fefcf3", "border": "#800000", "font": "#000", "accent": "#d4af37"},
    "Creative Event": {"bg": "#f7faff", "border": "#ff66b2", "font": "#222", "accent": "#ffe6f0"},
    "Royal Blue Formal": {"bg": "#e6f0ff", "border": "#002060", "font": "#000", "accent": "#3366cc"},
    "Elegant Silver Grey": {"bg": "#f2f2f2", "border": "#cccccc", "font": "#333", "accent": "#999999"},
    "Modern Geometric": {"bg": "#ffffff", "border": "#000000", "font": "#111", "accent": "#ffcc00"},
    "Retro Orange": {"bg": "#fff0e0", "border": "#ff6600", "font": "#000", "accent": "#ff9966"},
    "Green Nature": {"bg": "#f0fff0", "border": "#228B22", "font": "#000", "accent": "#90ee90"},
    "Black-Gold Executive": {"bg": "#000000", "border": "#FFD700", "font": "#ffffff", "accent": "#FFD700"},
    "Purple Galaxy": {"bg": "#f9f3ff", "border": "#800080", "font": "#222", "accent": "#e0b3ff"},
}

def draw_certificate(style, prefix, name, event, role, level):
    config = STYLE_CONFIGS[style]
    cert = Image.new("RGB", (1000, 700), config["bg"])
    draw = ImageDraw.Draw(cert)

    # Fonts
    try:
        header_font = ImageFont.truetype(TITLE_FONT, 38)
        title_font = ImageFont.truetype(TITLE_FONT, 58)
        sub_font = ImageFont.truetype(BODY_FONT, 30)
        name_font = ImageFont.truetype(TITLE_FONT, 55)
        footer_font = ImageFont.truetype(BODY_FONT, 24)
    except:
        header_font = title_font = sub_font = name_font = footer_font = ImageFont.load_default()

    # Border
    draw.rectangle([(0, 0), (999, 699)], outline=config["border"], width=15)

    # Logos
    cert.paste(white_logo, (80, 30), white_logo)
    cert.paste(yellow_logo, (840, 30), yellow_logo)

    # Institute Name
    draw.text((500, 50), "JSPM GROUP OF INSTITUTES", fill=config["font"], anchor="mm", font=header_font)

    # Certificate Title
    draw.text((500, 120), "Certificate of Completion", fill=config["font"], anchor="mm", font=title_font)

    # Subtitle
    draw.text((500, 200), "This certificate is proudly presented to", fill=config["font"], anchor="mm", font=sub_font)

    # Participant Name with prefix
    full_name = f"{prefix} {name}"
    draw.text((500, 260), full_name, fill=config["font"], anchor="mm", font=name_font)

    # Details
    draw.text((500, 330), f"For being a {role}", fill=config["font"], anchor="mm", font=sub_font)
    draw.text((500, 370), f"in the event: '{event}'", fill=config["font"], anchor="mm", font=sub_font)
    draw.text((500, 410), f"Level: {level}", fill=config["font"], anchor="mm", font=sub_font)

    # Footer
    today = datetime.today().strftime("%d %B %Y")
    draw.text((100, 650), f"Date: {today}", fill=config["font"], font=footer_font)
    draw.text((850, 650), f"Signature", fill=config["font"], anchor="mm", font=footer_font)

    return cert

# ───── Streamlit UI ─────
st.set_page_config("JSPM Certificate Generator", layout="wide")
st.title("🎓 AI-Powered Certificate Generator - JSPM Group")

with st.form("input_form"):
    prefix = st.selectbox("Prefix", ["Mr.", "Mrs."])
    name = st.text_input("Recipient Name")
    event = st.text_input("Event Name")
    role = st.text_input("Role (e.g., Participant, Winner)")
    level = st.selectbox("Certificate Level", ["Participation", "First Place", "Second Place", "Merit", "Special Mention"])
    submitted = st.form_submit_button("Generate Certificates")

if submitted:
    st.subheader("🎨 Select from 12 AI-Designed Certificates")
    cert_cols = st.columns(4)
    cert_images = {}

    for i, style in enumerate(STYLES):
        cert_img = draw_certificate(style, prefix, name, event, role, level)
        cert_images[style] = cert_img
        cert_cols[i % 4].image(cert_img, caption=style, use_column_width=True)

    selected = st.selectbox("📌 Choose a Design to Download", STYLES)
    if st.button("📥 Download Selected Certificate as PDF"):
        pdf_bytes = io.BytesIO()
        cert_images[selected].save(pdf_bytes, format="PDF")
        st.download_button("Download PDF", data=pdf_bytes.getvalue(), file_name=f"{name}_{selected}.pdf", mime="application/pdf")

