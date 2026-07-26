import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image, UnidentifiedImageError

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
MODEL_PATH = "models/apple_formalin_classifier.keras"
IMAGE_HEIGHT = 128
IMAGE_WIDTH = 128
CLASSES = ["Formalin-mixed", "Fresh"]
LOW_CONFIDENCE_THRESHOLD = 65.0  # below this, don't let the UI sound certain

st.set_page_config(
    page_title="Apple Quality Scanner",
    page_icon="🍎",
    layout="centered",
)

# ------------------------------------------------------------------
# Styling — orchard palette: deep leaf green, crimson accent, warm cream
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --leaf: #2E4B2F;
        --leaf-light: #4C7A4F;
        --crimson: #B23A3A;
        --cream: #FBF6EE;
        --charcoal: #2B2620;
    }

    .stApp {
        background: var(--cream);
    }

    .block-container {
        padding-top: 2rem;
        max-width: 780px;
    }

    .scanner-header {
        text-align: center;
        padding: 1.2rem 0 0.4rem 0;
    }
    .scanner-header h1 {
        font-family: 'Georgia', serif;
        color: var(--leaf);
        font-size: 2.4rem;
        margin-bottom: 0.1rem;
        letter-spacing: -0.5px;
    }
    .scanner-header p {
        color: var(--charcoal);
        opacity: 0.7;
        font-size: 0.95rem;
        margin-top: 0;
    }

    div[data-testid="stFileUploader"] {
        border: 2px dashed var(--leaf-light);
        border-radius: 14px;
        padding: 1rem;
        background: #ffffffaa;
    }

    .result-card {
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-top: 1rem;
        color: white;
    }
    .result-fresh { background: linear-gradient(135deg, var(--leaf), var(--leaf-light)); }
    .result-formalin { background: linear-gradient(135deg, #7A2222, var(--crimson)); }
    .result-uncertain { background: linear-gradient(135deg, #6b5b1f, #a08a2e); }

    .result-card h2 {
        margin: 0 0 0.2rem 0;
        font-size: 1.6rem;
    }
    .result-card p {
        margin: 0;
        opacity: 0.9;
        font-size: 0.9rem;
    }

    .prob-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: var(--charcoal);
        margin-top: 1.2rem;
        margin-bottom: 0.2rem;
    }

    .disclaimer {
        background: #fff3e0;
        border-left: 4px solid #d99a2b;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        font-size: 0.82rem;
        color: #5c4a1f;
        margin-top: 1.5rem;
    }

    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="scanner-header">
        <h1>🍎 Apple Quality Scanner</h1>
        <p>Upload a photo to screen for signs of surface adulteration</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# Model loading — cached so it doesn't reload on every interaction
# ------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_model(path: str):
    return tf.keras.models.load_model(path)


try:
    with st.spinner("Loading model..."):
        model = load_model(MODEL_PATH)
except Exception as e:
    st.error(
        f"Couldn't load the model from `{MODEL_PATH}`. "
        f"Check that the file exists and is a valid Keras model.\n\nDetails: {e}"
    )
    st.stop()

# ------------------------------------------------------------------
# Upload + inference
# ------------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Drop an apple image here, or click to browse",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file:
    try:
        image = Image.open(uploaded_file).convert("RGB")
    except UnidentifiedImageError:
        st.error("That file doesn't look like a valid image. Try a different one.")
        st.stop()

    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(image, caption="Uploaded image", use_container_width=True)

    try:
        img = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        with st.spinner("Analyzing..."):
            prediction = model.predict(img_array, verbose=0)[0]

        predicted_index = int(np.argmax(prediction))
        predicted_class = CLASSES[predicted_index]
        confidence = float(prediction[predicted_index] * 100)

    except Exception as e:
        st.error(f"Something went wrong while running the prediction: {e}")
        st.stop()

    with col2:
        if confidence < LOW_CONFIDENCE_THRESHOLD:
            st.markdown(
                f"""
                <div class="result-card result-uncertain">
                    <h2>⚠️ Uncertain</h2>
                    <p>Best guess: {predicted_class} at only {confidence:.1f}% confidence.
                    Consider a clearer photo or a physical check.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif predicted_class == "Fresh":
            st.markdown(
                f"""
                <div class="result-card result-fresh">
                    <h2>✅ Fresh</h2>
                    <p>{confidence:.1f}% confidence</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="result-card result-formalin">
                    <h2>🚫 Formalin-mixed</h2>
                    <p>{confidence:.1f}% confidence</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div class='prob-row'><span>Breakdown</span></div>", unsafe_allow_html=True)
    for cls, prob in zip(CLASSES, prediction):
        st.markdown(
            f"<div class='prob-row'><span>{cls}</span><span>{prob*100:.1f}%</span></div>",
            unsafe_allow_html=True,
        )
        st.progress(float(prob))

    st.markdown(
        """
        <div class="GROUP 16">
        <strong>Note:</strong> this is a visual classifier of FRESH AND FORMALIN-MIXED APPLES done by GROUP 16 OF COMPUTER ENGINEERING STUDENT, UNIVERSITY OF UYO.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<p style='text-align:center; opacity:0.6; margin-top:2rem;'>"
        "No image yet — upload one to get started.</p>",
        unsafe_allow_html=True,
    )