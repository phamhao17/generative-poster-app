# app.py
# 🎨 Generative Poster Streamlit App

import random, math
import numpy as np
from matplotlib.colors import hsv_to_rgb
import matplotlib.pyplot as plt
import streamlit as st

# --- Functions ---

def blob(center=(0.03, 0.5), r=0.9, points=900, wobble=0.009):
    """Generate a wobbly closed shape around a center with base radius r."""
    angles = np.linspace(0, 2 * math.pi, points, endpoint=False)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.05))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def make_palette(k=3, mode="random", base_h=0.60):
    """Return k colors (RGB) by sampling HSV depending on mode."""
    cols = []
    for _ in range(k):
        if mode == "pastel":
            h = random.random(); s = random.uniform(0.15, 0.35); v = random.uniform(0.90, 1.00)
        elif mode == "vivid":
            h = random.random(); s = random.uniform(0.80, 1.00); v = random.uniform(0.80, 1.00)
        elif mode == "mono":
            h = base_h; s = random.uniform(0.20, 0.60); v = random.uniform(0.50, 1.00)
        else:
            h = random.random(); s = random.uniform(0.30, 1.00); v = random.uniform(0.50, 1.00)
        cols.append(tuple(hsv_to_rgb([h, s, v])))
    return cols

STYLE_PRESETS = {
    "Minimal": dict(n_layers=5, wobble_range=(0.02, 0.08), alpha_range=(0.30, 0.50), palette_mode="pastel"),
    "Vivid": dict(n_layers=12, wobble_range=(0.05, 0.20), alpha_range=(0.35, 0.70), palette_mode="vivid"),
    "NoiseTouch": dict(n_layers=14, wobble_range=(0.12, 0.30), alpha_range=(0.25, 0.55), palette_mode="mono"),
}

def generate_poster(style=None, seed=None, background=(0.4, 0.4, 0.4)):
    """Create a generative poster with optional style and seed."""
    # Apply style preset
    if style in STYLE_PRESETS:
        preset = STYLE_PRESETS[style]
        n_layers = preset["n_layers"]
        wobble_range = preset["wobble_range"]
        alpha_range = preset["alpha_range"]
        palette_mode = preset["palette_mode"]
    else:
        n_layers = 10
        wobble_range = (0.2, 0.7)
        alpha_range = (0.38, 0.3)
        palette_mode = "pastel"

    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(7, 10))
    ax.axis("off")
    ax.set_facecolor(background)
    palette = make_palette(30, mode=palette_mode)

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.05, 0.3)
        wob = random.uniform(*wobble_range)
        x, y = blob(center=(cx, cy), r=rr, wobble=wob)
        color = random.choice(palette)
        alpha = random.uniform(*alpha_range)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor="none")

    ax.text(0.05, 0.95, f"Generative Poster • {style or 'Custom'}",
            fontsize=14, weight="bold", transform=ax.transAxes, color="white")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    return fig

# --- Streamlit UI ---

st.set_page_config(page_title="Generative Poster", layout="centered")

st.title("🌀 Generative Poster")
st.write("Create your own abstract generative art poster using random shapes and color palettes!")

# Sidebar Controls
style = st.sidebar.selectbox("🎨 Choose a Style Preset", ["Minimal", "Vivid", "NoiseTouch", "Custom"])
seed = st.sidebar.number_input("🔢 Random Seed (for reproducibility)", min_value=0, value=42, step=1)
bg_color = st.sidebar.color_picker("Background Color", "#666666")

generate = st.button("Generate Poster")

if generate:
    bg_rgb = tuple(int(bg_color.lstrip("#")[i:i+2], 16)/255 for i in (0, 2, 4))
    fig = generate_poster(style=style, seed=seed, background=bg_rgb)
    st.pyplot(fig)

    # Add download button
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0.1)
    st.download_button("💾 Download Poster as PNG", data=buf.getvalue(), file_name=f"poster_{style.lower()}.png", mime="image/png")
else:
    st.info("👈 Choose a style and click 'Generate Poster' to begin.")
