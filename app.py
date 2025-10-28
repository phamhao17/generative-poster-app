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

def random_palette(k=5):
    custom_palette = ["#ffb6c1", "#db7093", "#dda0dd"]  # Define custom palette
    return random.choices(custom_palette, k=k)

def blob(center=(0.8, 0.7), r=0.3, points=25, wobble=0.06):
    """Generate a wobbly closed shape"""
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# Sidebar for user control
st.sidebar.header("Customize your poster 🎨")
n_layers = st.sidebar.slider("Number of layers", 3, 15, 8)
random_seed = st.sidebar.number_input("Random seed", min_value=0, value=random.randint(0, 1000))
st.sidebar.write("Tip: Change the
