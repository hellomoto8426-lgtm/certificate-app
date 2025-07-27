import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os
from pathlib import Path

# Create directory for dashboard
os.makedirs("generated_certificates", exist_ok=True)

# Load logos
white_logo = Image.open("jspmlogo.png").convert("RGBA").resize((80, 80))
yellow_logo = Image.open("hadapsarjspmlogo.jpeg").convert("RGBA").resize((80, 80))

# Set absolute font paths
BASE_DIR = Path(__file__).resolve().parent
FONT_DIR = BASE_DIR / "fonts"
TITLE_FONT = str(FONT_DIR / "arialbd.ttf")
BODY_FONT = str(FONT_DIR / "arial.ttf")

# Font sizes (bigger for deployment)
if os.getenv("STREAMLIT_SERVER") or os.getenv("HOME") == "/home/appuser":
    HEADING_FONT_SIZE = 70
    NAME_FONT_SIZE = 65
    BODY_FONT_SIZE = 45
    FOOTER_FONT_SIZE = 30
else:
    HEADING_FONT_SIZE = 60
    NAME_FONT_SIZE = 55
    BODY_FONT_SIZE = 40
    FOOTER_FONT_SIZE = 24

# Styles
STYLES = [
    "Classic Gold", "Minimal Blue", "Dark Accent", "University Style",
    "Creative Event", "Royal Blue Formal", "Elegant Silver Grey",
    "Modern Geometric", "Retro Orange", "Green Nature",
    "Black-Gold Executive", "Purple Galaxy"
]

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

    try:
        header_font = ImageFont.truetype(TITLE_FONT, HEADING_FONT_SIZE - 20)
        title_font = ImageFont.truetype(TITLE_FONT, HEADING_FONT_SIZE)
        sub_font = ImageFont.truetype(BODY_FONT, BODY_FONT_SIZE)
        name_font = ImageFont.truetype(TITLE_FONT, NAME_FONT_SIZE)
        footer_font = ImageFont.truetype(BODY_FONT, FOOTER_FONT_SIZE)
    except:
        header_font = title_font = sub_font = name_font = footer_font = ImageFont.load_default()

    draw.rectangle([(0, 0), (999, 699)], outline=config["border"], width=15)
    cert.paste(white_logo, (80, 30), white_logo)
    cert.paste(yellow_logo, (840, 30), yellow_logo)

    draw.text((500, 50), "JSPM GROUP OF INSTITUTES", fill=config["font"], anchor="mm", font=header_font)
    draw.text((500, 130), "Certificate of Completion", fill=config["font"], anchor="mm", font=title_font)
    draw.text((500, 210), "This certificate is proudly presented to", fill=config["font"], anchor="mm", font=sub_font)

    full_name = f"{prefix} {name}"
    draw.text((500, 280), full_name, fill=config["font"], anchor="mm", font=name_font)

    draw.text((500, 350), f"For being a {role}", fill=config["font"], anchor="mm", font=sub_font)
    draw.text((500, 390), f"in the event: '{event}'", fill=config["font"], anchor="mm", font=sub_font)
    draw.text((500, 430), f"Level: {level}", fill=config["font"], anchor="mm", font=sub_font)

    today = datetime.today().strftime("%d %B %Y")
    draw.text((100, 650), f"Date: {today}", fill=config["font"], font=footer_font)
    draw.text((850, 650), "Signature", fill=config["font"], anchor="mm", font=footer_font)

    return cert

def send_email_with_attachment(receiver_email, subject, body, attachment_bytes, filename):
    sender_email = "timepass614315@gmail.com"
    sender_password = "dwev roqc bvpn nsls"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)
    msg.add_attachment(attachment_bytes.getvalue(), maintype='application', subtype='pdf', filename=filename)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Streamlit UI
st.set_page_config("Certificate Generator", layout="wide")
st.sidebar.title("📁 Navigation")
page = st.sidebar.radio("Go to", ["🏆 Certificate Generator", "📊 Dashboard"])

st.title("🎓 AI-Powered Certificate Generator - JSPM Group")

with st.form("input_form"):
    prefix = st.selectbox("Prefix", ["Mr.", "Mrs."])
    name = st.text_input("Recipient Name")
    event = st.text_input("Event Name")
    role = st.text_input("Role (e.g., Participant, Winner)")
    level = st.selectbox("Certificate Level", ["Participation", "First Place", "Second Place", "Merit", "Special Mention"])
    email = st.text_input("Recipient Email (for sending certificate)")
    submitted = st.form_submit_button("Generate Certificates")

if "submitted" not in st.session_state:
    st.session_state["submitted"] = False
if "selected_style" not in st.session_state:
    st.session_state["selected_style"] = None

if submitted:
    st.session_state["submitted"] = True
    st.session_state["selected_style"] = None

if st.session_state["submitted"]:
    st.subheader("🎨 Select from 12 AI-Designed Certificates")
    cert_images = {}
    cert_cols = st.columns(4)

    for i, style in enumerate(STYLES):
        cert_img = draw_certificate(style, prefix, name, event, role, level)
        cert_images[style] = cert_img

        with cert_cols[i % 4]:
            st.image(cert_img, caption=style)
            if st.button(f"✅ Select '{style}'", key=style):
                st.session_state["selected_style"] = style

    selected_style = st.session_state["selected_style"]

    if selected_style:
        st.success(f"✅ You selected: {selected_style}")
        img = cert_images[selected_style].convert("RGB")
        pdf_bytes = io.BytesIO()
        img.save(pdf_bytes, format="PDF")
        pdf_bytes.seek(0)

        st.download_button(
            label="⬇️ Download Certificate",
            data=pdf_bytes.getvalue(),
            file_name=f"{name}_{selected_style}_certificate.pdf",
            mime="application/pdf"
        )
    else:
        st.info("👆 Please select a certificate design to download.")

if st.button("📧 Send Certificate to Email"):
    if email:
        sent = send_email_with_attachment(
            receiver_email=email,
            subject="Your Certificate from JSPM Group",
            body=f"Dear {prefix} {name},\n\nPlease find your attached certificate for '{event}'.\n\nRegards,\nJSPM Team",
            attachment_bytes=pdf_bytes,
            filename=f"{name}_{selected_style}.pdf"
        )
        if sent:
            st.success("✅ Email sent successfully!")
    else:
        st.warning("⚠️ Please enter a valid email address.")

elif page == "📊 Dashboard":
    st.title("📊 Certificate Dashboard")
    cert_files = os.listdir("generated_certificates")

    if cert_files:
        for cert in cert_files:
            cert_path = os.path.join("generated_certificates", cert)
            st.write(f"📄 {cert}")
            with open(cert_path, "rb") as f:
                st.download_button("Download Again", f, file_name=cert, key=cert)
    else:
        st.info("No certificates generated yet.")
