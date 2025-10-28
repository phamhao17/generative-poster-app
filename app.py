# app.py
# Generative Abstract Poster (Streamlit version)

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Generative Abstract Poster", layout="centered")

st.title("🎨 Generative Abstract Poster")
st.caption("Concepts: randomness, lists, loops, functions, matplotlib")

# Function to create a random color palette
def random_palette(k=5):
    custom_palette = ["#ffb6c1", "#db7093", "#dda0dd"]
    return random.choices(custom_palette, k=k)

# Function to create a blobby shape
def blob(center=(0.8, 0.7), r=0.3, points=25, wobble=0.06):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# Sidebar controls
st.sidebar.header("Customize Your Poster 🎨")
n_layers = st.sidebar.slider("Number of Layers", 3, 15, 8)
seed = st.sidebar.number_input("Random Seed", min_value=0, value=random.randint(0, 10000))
st.sidebar.write("Change the seed or number of layers to generate a new design!")

# Apply seed
random.seed(seed)

# Plot setup
fig, ax = plt.subplots(figsize=(7, 10))
ax.axis('off')
ax.set_facecolor((0.98, 0.98, 0.97))

# Generate shapes
palette = random_palette(6)
for i in range(n_layers):
    cx, cy = random.random(), random.random()
    rr = random.uniform(0.15, 0.45)
    x, y = blob(center=(cx, cy), r=rr, wobble=random.uniform(0.05, 0.25))
    color = random.choice(palette)
    alpha = random.uniform(0.25, 0.6)
    ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

# Add text
ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold', transform=ax.transAxes)
ax.text(0.05, 0.91, "Week 2 • Arts & Advanced Big Data", fontsize=11, transform=ax.transAxes)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Display
st.pyplot(fig)

# Optional: Add regenerate button
if st.button("🔄 Generate New Poster"):
    st.experimental_rerun()
