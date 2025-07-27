import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os
from pathlib import Path

#make dashboard
os.makedirs("generated_certificates", exist_ok=True)

# Load logos
white_logo = Image.open("jspmlogo.png").convert("RGBA").resize((80, 80))
yellow_logo = Image.open("hadapsarjspmlogo.jpeg").convert("RGBA").resize((80, 80))

# Fonts
FONT_DIR = Path("fonts")
TITLE_FONT = str(FONT_DIR / "arialbd.ttf")
BODY_FONT = str(FONT_DIR / "arial.ttf")

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
        header_font = ImageFont.truetype(TITLE_FONT, 60)
        title_font = ImageFont.truetype(TITLE_FONT, 80)
        sub_font = ImageFont.truetype(BODY_FONT, 50)
        name_font = ImageFont.truetype(TITLE_FONT, 40)
        footer_font = ImageFont.truetype(BODY_FONT, 30)
    except:
        header_font = title_font = sub_font = name_font = footer_font = ImageFont.load_default()

    draw.rectangle([(0, 0), (999, 699)], outline=config["border"], width=15)
    cert.paste(white_logo, (80, 30), white_logo)
    cert.paste(yellow_logo, (840, 30), yellow_logo)

    draw.text((500, 50), "JSPM GROUP OF INSTITUTES", fill=config["font"], anchor="mm", font=header_font)
    draw.text((500, 120), "Certificate of Completion", fill=config["font"], anchor="mm", font=title_font)
    draw.text((500, 200), "This certificate is proudly presented to", fill=config["font"], anchor="mm", font=sub_font)

    full_name = f"{prefix} {name}"
    draw.text((500, 260), full_name, fill=config["font"], anchor="mm", font=name_font)

    draw.text((500, 330), f"For being a {role}", fill=config["font"], anchor="mm", font=sub_font)
    draw.text((500, 370), f"in the event: '{event}'", fill=config["font"], anchor="mm", font=sub_font)
    draw.text((500, 410), f"Level: {level}", fill=config["font"], anchor="mm", font=sub_font)

    today = datetime.today().strftime("%d %B %Y")
    draw.text((100, 650), f"Date: {today}", fill=config["font"], font=footer_font)
    draw.text((850, 650), f"Signature", fill=config["font"], anchor="mm", font=footer_font)

    return cert

def send_email_with_attachment(receiver_email, subject, body, attachment_bytes, filename):
    sender_email = "timepass614315@gmail.com"         # ✅ Replace
    sender_password = "dwev roqc bvpn nsls"                # ✅ Replace

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
    
#dashboard

st.set_page_config("Certificate Generator", layout="wide")
st.sidebar.title("📁 Navigation")
page = st.sidebar.radio("Go to", ["🏆 Certificate Generator", "📊 Dashboard"])

# ───── Streamlit UI ─────
st.set_page_config("JSPM Certificate Generator", layout="wide")
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

# When the form is submitted
if submitted:
    st.session_state["submitted"] = True
    st.session_state["selected_style"] = None  # Reset selected style on new submit

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