import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Image Prompt Generator",
    page_icon="🎨",
    layout="wide",
)

MODEL = "llama-3.3-70b-versatile"

STYLES = [
    "Photorealistic",
    "Cinematic",
    "Anime",
    "3D Render",
    "Fantasy",
    "Cyberpunk",
    "Watercolor",
    "Oil Painting",
    "Minimalist",
    "Concept Art",
]

LIGHTING_OPTIONS = [
    "Soft lighting",
    "Golden hour",
    "Studio lighting",
    "Neon glow",
    "Moody shadows",
    "Natural daylight",
    "Dramatic lighting",
]

ASPECT_RATIOS = [
    "1:1",
    "16:9",
    "9:16",
    "4:5",
    "3:2",
]


# Get Groq client
def get_client():
    if "Image Translate" not in st.secrets:
        st.error("Missing secret: 'Image Translate'")
        st.stop()

    api_key = st.secrets["Image Translate"]

    if not api_key or not str(api_key).strip():
        st.error("API key is empty.")
        st.stop()

    return Groq(api_key=api_key)


# Generate image prompt
def generate_prompt(subject, style, lighting, aspect_ratio, details):
    client = get_client()

    prompt = f"""
Create a high-quality AI image generation prompt.

Subject: {subject}
Style: {style}
Lighting: {lighting}
Aspect Ratio: {aspect_ratio}
Details: {details}

Return format:

TITLE:
...

PROMPT:
...

NEGATIVE PROMPT:
...

Make it detailed and visually rich.
Only return this format.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


# UI
st.title("🎨 AI Image Prompt Generator")
st.caption("Powered by Groq")

with st.sidebar:
    st.header("Settings")
    style = st.selectbox("Style", STYLES)
    lighting = st.selectbox("Lighting", LIGHTING_OPTIONS)
    aspect_ratio = st.selectbox("Aspect Ratio", ASPECT_RATIOS)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input")
    subject = st.text_input("Enter your idea")
    details = st.text_area("Extra details", height=200)

    generate = st.button("Generate Prompt", type="primary", use_container_width=True)

with col2:
    st.subheader("Output")
    output = st.empty()


if generate:
    if not subject.strip():
        st.warning("Please enter an idea first.")
    else:
        try:
            with st.spinner("Generating..."):
                result = generate_prompt(subject, style, lighting, aspect_ratio, details)

            output.code(result, language="text")

        except Exception as e:
            st.error(f"Error: {e}")
