# app.py
# 🎨 Week 4 - 3D-like Generative Poster (Streamlit version)
# Concepts: shadow, transparency, layering, depth cues
# Deployment-ready for Streamlit Cloud

import random, math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb, LinearSegmentedColormap
import streamlit as st

# --- Functions ---

def blob(center=(0.5,0.5), r=0.3, points=500, wobble=0.39):
    """Generate a wobbly closed shape."""
    angles = np.linspace(0, 2*math.pi, points, endpoint=False)
    radii  = r * (1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def make_palette(k=6, mode="pastel", base_h=0.60):
    """Generate color palette in different styles."""
    cols = []
    for _ in range(k):
        if mode == "pastel":
            h = random.random(); s = random.uniform(0.15,0.35); v = random.uniform(0.9,1.0)
        elif mode == "vivid":
            h = random.random(); s = random.uniform(0.8,1.0);  v = random.uniform(0.8,1.0)
        elif mode == "mono":
            h = base_h; s = random.uniform(0.2,0.6); v = random.uniform(0.5,1.0)
        elif mode == "dark":
            h = random.random(); s = random.uniform(0.8,1.0); v = random.uniform(0.2,0.5)
        elif mode == "grey":
            h = 0; s = 0; v = random.uniform(0.1,0.6)
        else:  # random
            h = random.random(); s = random.uniform(0.3,1.0); v = random.uniform(0.5,1.0)
        cols.append(tuple(hsv_to_rgb([h,s,v])))
    return cols

def make_rainbow_palette(k):
    """Generate rainbow-like color gradients."""
    colors = [(1, 0, 0), (1, 0.5, 0), (1, 1, 0), (0, 1, 0),
              (0, 0, 1), (0.29, 0, 0.51), (0.58, 0, 0.83)]
    cmap = LinearSegmentedColormap.from_list("rainbow_cmap", colors, N=256)
    return [cmap(i/k) for i in range(k)]

def generate_3d_poster(n_layers=10, seed=0, num_shadows=10):
    """Generate a 3D-like generative poster figure."""
    random.seed(seed); np.random.seed(seed)
    fig, ax = plt.subplots(figsize=(6,7))
    ax.axis('off')
    ax.set_facecolor((0.95,0.95,0.95))

    grey_palette = make_palette(n_layers, mode="grey")
    rainbow_palette = make_rainbow_palette(num_shadows)

    large_shape_index = random.randint(0, n_layers - 1)

    for i in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.3) if i == large_shape_index else random.uniform(0.02, 0.08)
        x, y = blob((cx,cy), r=rr, wobble=0.12)

        # Rainbow shadows
        for j in range(num_shadows):
            shadow_color = rainbow_palette[j % len(rainbow_palette)]
            offset_x = 0.02 * (j + 1) / num_shadows
            offset_y = -0.02 * (j + 1) / num_shadows
            ax.fill(x + offset_x, y + offset_y, color=shadow_color, alpha=0.1)

        color = grey_palette[i]
        alpha = 0.4 + i * 0.08
        ax.fill(x, y, color=color, alpha=min(alpha, 1.0))

    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.set_title("3D-like Generative Poster", fontsize=14, weight="bold")

    return fig

# --- Streamlit UI ---

st.set_page_config(page_title="3D-like Generative Poster", layout="centered")
st.title("🌀 Week 4 - 3D-like Generative Poster")
st.write("Experiment with depth, shadow, and layering using generative art!")

# Sidebar
st.sidebar.header("Controls 🎨")
n_layers = st.sidebar.slider("Number of Layers", 5, 100, 50)
num_shadows = st.sidebar.slider("Number of Rainbow Shadows", 3, 20, 10)
seed = st.sidebar.number_input("Random Seed", min_value=0, value=250, step=1)

generate = st.button("Generate Poster")

if generate:
    with st.spinner("Generating your poster..."):
        fig = generate_3d_poster(n_layers=n_layers, seed=seed, num_shadows=num_shadows)
        st.pyplot(fig)

        # Download option
        import io
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0.1)
        st.download_button("💾 Download Poster as PNG", data=buf.getvalue(),
                           file_name=f"3d_poster_seed{seed}.png", mime="image/png")
else:
    st.info("👈 Use the sidebar to set parameters and click 'Generate Poster'.")
