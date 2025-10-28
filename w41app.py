# app.py
# 🎨 Week 4 - Interactive Generative Poster (Streamlit version)
# Concepts: sliders, interactivity, parameter control
# Deployment-ready for Streamlit Cloud

import random, math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import streamlit as st

# --- Blob shape ---
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    """Generate a wobbly closed shape."""
    angles = np.linspace(0, 2 * math.pi, points, endpoint=False)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# --- Simple palette generator (HSV pastel/vivid/mono/dark/random) ---
def make_palette(k=6, mode="pastel", base_h=0.60):
    """Generate a list of RGB colors based on HSV palettes."""
    cols = []
    for _ in range(k):
        if mode == "pastel":
            h = random.random(); s = random.uniform(0.15, 0.35); v = random.uniform(0.9, 1.0)
        elif mode == "vivid":
            h = random.random(); s = random.uniform(0.8, 1.0); v = random.uniform(0.8, 1.0)
        elif mode == "mono":
            h = base_h; s = random.uniform(0.2, 0.6); v = random.uniform(0.5, 1.0)
        elif mode == "dark":
            h = random.random(); s = random.uniform(0.8, 1.0); v = random.uniform(0.2, 0.5)
        else:  # random
            h = random.random(); s = random.uniform(0.3, 1.0); v = random.uniform(0.5, 1.0)
        cols.append(tuple(hsv_to_rgb([h, s, v])))
    return cols

# --- Main drawing function ---
def draw_poster(n_layers=8, wobble=0.15, palette_mode="pastel", seed=0, bg_color="yellow"):
    """Draw a generative poster figure."""
    random.seed(seed)
    np.random.seed(seed)
    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")
    ax.set_facecolor(bg_color)

    palette = make_palette(6, mode=palette_mode)
    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x, y = blob((cx, cy), r=rr, wobble=wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.09, 0.3)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=None)

    ax.text(
        0.05, 0.95, f"Interactive Poster • {palette_mode}",
        transform=ax.transAxes, fontsize=12, weight="bold"
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig

# --- Streamlit UI ---
st.set_page_config(page_title="Interactive Generative Poster", layout="centered")

st.title("🎨 Week 4 - Interactive Generative Poster")
st.write("Explore parameter controls to create generative abstract art!")

# Sidebar controls
st.sidebar.header("🧩 Controls")
n_layers = st.sidebar.slider("Layers", min_value=3, max_value=20, value=8, step=1)
wobble = st.sidebar.slider("Wobble", min_value=0.01, max_value=0.3, value=0.15, step=0.01)
palette_mode = st.sidebar.selectbox("Palette Mode", ["pastel", "vivid", "mono", "random", "dark"])
seed = st.sidebar.number_input("Seed", min_value=0, max_value=9999, value=0, step=1)
bg_color = st.sidebar.color_picker("Background Color", "#FFFF00")  # default yellow

# Generate button
if st.button("Generate Poster"):
    fig = draw_poster(n_layers, wobble, palette_mode, seed, bg_color)
    st.pyplot(fig)

    # Download option
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0.1)
    st.download_button(
        "💾 Download Poster as PNG",
        data=buf.getvalue(),
        file_name=f"poster_{palette_mode}_seed{seed}.png",
        mime="image/png"
    )
else:
    st.info("👈 Adjust parameters in the sidebar and click **Generate Poster**.")
