
import streamlit as st
from PIL import Image
from io import BytesIO
import html

from src.web_backend import (
    restore_with_opencv,
    restore_with_realesrgan
)


# -------------------- PAGE CONFIGURATION --------------------

st.set_page_config(
    page_title="SiteRestore AI",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------- NEON THEME --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080d1a;
    --panel: #101a2e;
    --cyan: #00e5ff;
    --purple: #9d4edd;
    --text: #e8f1ff;
    --muted: #8b9bb4;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 10%, rgba(0,229,255,.10), transparent 35%),
        radial-gradient(ellipse at 85% 20%, rgba(157,78,221,.12), transparent 35%),
        var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1729, #090f1d);
    border-right: 1px solid rgba(0,229,255,.16);
}

section[data-testid="stSidebar"] * {
    color: var(--text);
}

.hero {
    padding: 28px 32px;
    border: 1px solid rgba(0,229,255,.3);
    border-radius: 18px;
    background: linear-gradient(120deg,
        rgba(0,229,255,.09),
        rgba(157,78,221,.10));
    box-shadow: 0 0 30px rgba(0,229,255,.07);
    margin-bottom: 28px;
    animation: fadeIn .7s ease;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1.5px;
    background: linear-gradient(90deg, #00e5ff, #9d4edd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #a8bad2;
    font-size: 14px;
    margin-top: 8px;
}

.section-heading {
    font-size: 20px;
    font-weight: 700;
    margin: 22px 0 14px;
    color: #e8f1ff;
}

.neon-card {
    background: rgba(16,26,46,.85);
    border: 1px solid rgba(0,229,255,.16);
    border-radius: 15px;
    padding: 21px;
    transition: all .3s ease;
    min-height: 125px;
}

.neon-card:hover {
    transform: translateY(-5px);
    border-color: rgba(0,229,255,.65);
    box-shadow: 0 0 22px rgba(0,229,255,.12);
}

.metric-value {
    font-size: 27px;
    font-weight: 800;
    color: #00e5ff;
    margin-top: 8px;
}

.metric-label {
    font-size: 13px;
    color: #91a4bf;
}

.status {
    display: inline-block;
    color: #00f5a0;
    background: rgba(0,245,160,.09);
    border: 1px solid rgba(0,245,160,.25);
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 11px;
    font-weight: 700;
}

div.stButton > button {
    background: linear-gradient(100deg, #00bcd4, #7650d8);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 10px 22px;
    transition: all .25s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 20px rgba(0,229,255,.35);
    border: none;
    color: white;
}

div[data-testid="stFileUploader"] {
    background: rgba(16,26,46,.65);
    border: 1px dashed rgba(0,229,255,.45);
    border-radius: 14px;
    padding: 14px;
}

div[data-testid="stImage"] img {
    border-radius: 12px;
    border: 1px solid rgba(0,229,255,.2);
}

hr {
    border-color: rgba(0,229,255,.13);
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(12px);}
    to {opacity: 1; transform: translateY(0);}
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown("## 📡 SiteRestore AI")
    st.caption("NETWORK DOCUMENTATION RESTORATION")
    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Image Restoration", "About Project"]
    )

    st.markdown("---")
    st.markdown(
        '<span class="status">● SYSTEM ONLINE</span>',
        unsafe_allow_html=True
    )
    st.caption("AI Restoration Platform")
    st.caption("Version 1.0")


# -------------------- HEADER --------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">SiteRestore AI</div>
    <div class="hero-subtitle">
        AI-powered restoration of degraded telecom infrastructure documentation.
    </div>
</div>
""", unsafe_allow_html=True)


# -------------------- DASHBOARD --------------------

if page == "Dashboard":

    st.markdown(
        '<div class="section-heading">System Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("AI MODEL", "Real-ESRGAN", "Integration available"),
        ("METHODS", "02", "OpenCV + AI"),
        ("DEGRADATIONS", "04", "Supported categories"),
        ("PLATFORM", "ACTIVE", "Local processing")
    ]

    for col, (label, value, description) in zip(
        [c1, c2, c3, c4], metrics
    ):
        with col:
            st.markdown(f"""
            <div class="neon-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{description}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">Restoration Capabilities</div>',
        unsafe_allow_html=True
    )

    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="neon-card">
            <h3>◈ OpenCV Enhancement</h3>
            <p style="color:#91a4bf">
                Traditional image processing for blur, noise,
                contrast and image enhancement.
            </p>
            <span class="status">AVAILABLE</span>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="neon-card">
            <h3>✦ Real-ESRGAN</h3>
            <p style="color:#91a4bf">
                Deep-learning-based image super-resolution.
            </p>
            <span class="status">CONNECTED</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">Supported Degradation Types</div>',
        unsafe_allow_html=True
    )

    degradation_info = [
        ("01", "Blur", "Reduced image sharpness"),
        ("02", "Noise", "Unwanted visual interference"),
        ("03", "Low Resolution", "Insufficient image detail"),
        ("04", "Low Contrast", "Poor visibility of structures")
    ]

    cols = st.columns(4)

    for col, (number, title, description) in zip(
        cols, degradation_info
    ):
        with col:
            st.markdown(f"""
            <div class="neon-card">
                <div class="metric-label">{number}</div>
                <h4>{title}</h4>
                <div class="metric-label">{description}</div>
            </div>
            """, unsafe_allow_html=True)


# -------------------- IMAGE RESTORATION --------------------

elif page == "Image Restoration":

    st.markdown(
        '<div class="section-heading">Image Restoration Workspace</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1, 1.2], gap="large")

    with left:

        st.markdown("### Upload Documentation")

        uploaded_file = st.file_uploader(
            "Choose a telecom image",
            type=["png", "jpg", "jpeg", "bmp"],
            key="restoration_upload"
        )

        degradation_options = {
            "Blur": "blur",
            "Noise": "noise",
            "Low Resolution": "low_resolution",
            "Low Contrast": "contrast"
        }

        degradation = st.selectbox(
            "Degradation Type",
            list(degradation_options.keys())
        )

        method = st.selectbox(
            "Restoration Method",
            ["OpenCV", "Real-ESRGAN"]
        )

        run_button = st.button(
            "✦ Run Restoration",
            use_container_width=True
        )

    if uploaded_file:

        original_bytes = uploaded_file.getvalue()

        if run_button:

            try:

                if method == "OpenCV":

                    with st.spinner("Restoring image using OpenCV..."):

                        restored_bytes, processing_time = (
                            restore_with_opencv(
                                original_bytes,
                                degradation_options[degradation]
                            )
                        )

                else:

                    with st.spinner(
                        "Restoring image using Real-ESRGAN... "
                        "This may take several minutes on CPU."
                    ):

                        restored_bytes, processing_time = (
                            restore_with_realesrgan(
                                original_bytes
                            )
                        )

                st.session_state["restored_image"] = restored_bytes
                st.session_state["processing_time"] = processing_time
                st.session_state["restoration_method"] = method
                st.session_state["restored_filename"] = uploaded_file.name
                st.session_state["restored_degradation"] = degradation

                st.success("Image restoration completed!")

            except Exception as error:

                st.error(f"Restoration failed: {error}")

        with right:
            st.markdown("### Uploaded Image")

            image = Image.open(BytesIO(original_bytes)).convert("RGB")

            st.image(
                image,
                caption="Original Documentation",
                width="stretch"
            )

            st.caption(
                f"Resolution: {image.width} × {image.height} pixels"
            )

        # Display results only when they belong to the current upload/configuration

        result_matches = (
            st.session_state.get("restored_filename") == uploaded_file.name
            and st.session_state.get("restoration_method") == method
            and st.session_state.get("restored_degradation") == degradation
        )

        if result_matches:

            st.markdown("---")
            st.markdown("### Restoration Results")

            original_col, restored_col = st.columns(2, gap="large")

            with original_col:
                st.markdown("**Original Image**")
                st.image(
                    original_bytes,
                    width="stretch"
                )

            with restored_col:
                st.markdown("**Restored Image**")
                st.image(
                    st.session_state["restored_image"],
                    width="stretch"
                )

            st.markdown("---")

            metric1, metric2, metric3 = st.columns(3)

            with metric1:
                st.metric(
                    "Processing Time",
                    f"{st.session_state['processing_time']:.3f} sec"
                )

            with metric2:
                st.metric(
                    "Method",
                    st.session_state["restoration_method"]
                )

            with metric3:
                st.metric(
                    "Degradation",
                    st.session_state["restored_degradation"]
                )

            st.download_button(
                label="⬇ Download Restored Image",
                data=st.session_state["restored_image"],
                file_name=(
                    "restored_"
                    + uploaded_file.name.rsplit(".", 1)[0]
                    + ".png"
                ),
                mime="image/png",
                use_container_width=True
            )

    else:

        with right:
            st.markdown("""
            <div class="neon-card" style="text-align:center;padding:65px 20px;">
                <div style="font-size:42px;color:#00e5ff;">＋</div>
                <h4>Waiting for Image</h4>
                <p style="color:#91a4bf">
                    Upload telecom documentation to begin restoration.
                </p>
            </div>
            """, unsafe_allow_html=True)


# -------------------- ABOUT PROJECT --------------------

elif page == "About Project":

    st.markdown(
        '<div class="section-heading">About SiteRestore AI</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="neon-card">
        <h3>Project Objective</h3>
        <p style="color:#a8bad2">
        SiteRestore AI aims to improve the visual quality of degraded
        telecom infrastructure documentation using image processing
        and deep-learning-based restoration.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">Technology Stack</div>',
        unsafe_allow_html=True
    )

    st.write("""
    - **Python** — Core programming language
    - **Streamlit** — Interactive web interface
    - **OpenCV** — Image preprocessing and enhancement
    - **PyTorch** — Deep learning framework
    - **Real-ESRGAN** — AI image restoration
    - **PSNR and SSIM** — Image quality evaluation
    """)

    st.markdown(
        '<div class="section-heading">Project Workflow</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="neon-card">
        **01 — Input** → Upload degraded telecom documentation

        **02 — Preprocessing** → Analyze and prepare the image

        **03 — Restoration** → Apply OpenCV or Real-ESRGAN

        **04 — Evaluation** → Measure image quality and processing time

        **05 — Output** → Compare and download restored results
    </div>
    """, unsafe_allow_html=True)


# -------------------- FOOTER --------------------

st.markdown("---")
st.caption(
    "SiteRestore AI | AI-Powered Telecom Documentation Restoration"
)
