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


def get_client():
    if "Translation" not in st.secrets:
        st.error("Missing Streamlit secret: Translation")
        st.stop()

    api_key = st.secrets["Translation"]

    if not api_key or not str(api_key).strip():
        st.error("The secret 'Translation' is empty.")
        st.stop()

    return Groq(api_key=api_key)


def generate_image_prompt(subject, style, lighting, aspect_ratio, extra_details):
    client = get_client()

    system_prompt = (
        "You are an expert AI image prompt engineer. "
        "Create high-quality prompts for image generation models. "
        "Return concise, production-ready outputs."
    )

    user_prompt = f"""
Create an advanced AI image generation package for this concept.

Subject:
{subject}

Style:
{style}

Lighting:
{lighting}

Aspect ratio:
{aspect_ratio}

Extra details:
{extra_details}

Return the result in exactly this format:

TITLE:
<short creative title>

PROMPT:
<a single rich prompt optimized for image generation>

NEGATIVE PROMPT:
<a clean negative prompt>

SUGGESTED SETTINGS:
- Quality: <value>
- Camera/Composition: <value>
- Color Mood: <value>
- Detail Level: <value>

Make the prompt vivid, specific, and visually strong.
Do not add explanations outside the format.
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.7,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content.strip()


st.title("🎨 AI Image Prompt Generator")
st.caption("Built with Streamlit + Groq")

with st.sidebar:
    st.header("Prompt Settings")
    style = st.selectbox("Style", STYLES, index=0)
    lighting = st.selectbox("Lighting", LIGHTING_OPTIONS, index=0)
    aspect_ratio = st.selectbox("Aspect Ratio", ASPECT_RATIOS, index=0)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input")
    subject = st.text_input(
        "What image do you want to create?",
        placeholder="Example: A futuristic cat sitting on a neon-lit rooftop in Tokyo",
    )
    extra_details = st.text_area(
        "Extra details",
        height=220,
        placeholder="Example: rainy night, reflective streets, ultra detailed, cinematic composition, glowing signs",
    )

    generate_btn = st.button("Generate Prompt", type="primary", use_container_width=True)

with col2:
    st.subheader("Output")
    output_box = st.empty()

if generate_btn:
    if not subject.strip():
        st.warning("Please enter an image idea first.")
    else:
        try:
            with st.spinner("Generating image prompt..."):
                result = generate_image_prompt(
                    subject=subject,
                    style=style,
                    lighting=lighting,
                    aspect_ratio=aspect_ratio,
                    extra_details=extra_details,
                )

            output_box.code(result, language="text")
        except Exception as e:
            st.error(f"Request failed: {e}")

st.markdown("---")
st.info(
    "Note: This app uses Groq to generate image prompts, not to render actual images. "
    "Groq’s current official docs describe text output workflows, including text and image inputs, "
    "but not native text-to-image output."
)
