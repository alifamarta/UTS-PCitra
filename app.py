import streamlit as st
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

st.title("Manipulasi Gambar")

# Memuat gambar yang diupload oleh pengguna
uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Konversi ke ruang warna HSV
    if st.button("Konversi ke HSV"):
        img_array = np.array(image)
        hsv_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        st.image(hsv_image, caption='HSV Image.', use_column_width=True)

    # Tampilkan histogram gambar
    if st.button("Tampilkan Histogram"):
        img_array = np.array(image)
        color = ('b', 'g', 'r')
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        for i, col in enumerate(color):
            hist = cv2.calcHist([img_array], [i], None, [256], [0, 256])
            axs[i].plot(hist, color=col)
            axs[i].set_xlim([0, 256])
        st.pyplot(fig)

    # Tampilkan kontur gambar
    if st.button("Tampilkan Contour"):
        img_array = np.array(image)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contour_img = img_array.copy()
        cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
        st.image(contour_img, caption='Contours Image.', use_column_width=True)

    # Penyesuaian kecerahan dan kontras
    st.write("Sesuaikan Kecerahan dan Kontras")
    brightness = st.slider("Brightness", -100, 100, 0)
    contrast = st.slider("Contrast", -100, 100, 0)
    if st.button("Terapkan"):
        img_array = np.array(image)
        adjusted = cv2.convertScaleAbs(img_array, alpha=1 + contrast / 100, beta=brightness)
        st.image(adjusted, caption='Adjusted Image.', use_column_width=True)
else:
    st.warning("Upload gambar terlebih dahulu.")
