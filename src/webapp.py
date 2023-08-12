import streamlit as st
import os, glob
from PIL import Image
from pathlib import Path
from app import filenames, neighbors


# Set Basic Page Configuration
st.set_page_config(
    page_title="WallFindr",
    page_icon="https://cdn-icons-png.flaticon.com/512/5182/5182930.png"
)


# Entry section
logo = Path.cwd()/"images/logo.png"
wallfindr = Image.open(logo)
st.image(wallfindr)
st.title("Ultimate WallPaper Recommender")


# Save User's WallPaper in Uploaded Backgrounds Directory
def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join(Path.cwd()/'uploaded_backgrounds', uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.read())
        return 1
    except:
        return 0

# Make a function to keep only last 100 files
def keep_last_100(directory: str) -> None:
    files = glob.glob(os.path.join(directory, "*"))
    max_files = 100

    # Sort the file by modification time
    files.sort(key=lambda x: os.path.getatime(x))

    # Calculate no of files to delete
    iterate = len(files) - max_files
    for i in range(iterate):
        os.remove(files[i])

# main function
def main() -> None:
    # File Uploader
    uploaded_file = st.file_uploader("Upload Your WallPaper")
    if uploaded_file is not None:
        if save_uploaded_file(uploaded_file):
            distancs, indices = neighbors(os.path.join(Path.cwd()/"uploaded_backgrounds", uploaded_file.name))
            
            original_backgrounds = set()
            for index in indices[0]:
                original_backgrounds.add(filenames[index])

            # Set some style before displaying image
            card_style = (
                f"border-radius: 15px; box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.2); padding: 20px;"
                f"background-color: white; display: inline-block;"
            )

            # Display each wallpaper based on similarity 
            for background in original_backgrounds:
                st.markdown(
                    f'<a href="{background}" target="_blank">'
                    f'<div style="{card_style}">'
                    f'<img src="{background}" width="100%" alt="Clickable Image">'
                    f'</div></a>',
                    unsafe_allow_html=True,
                )

        else:
            st.error("Encountered some Error!")


if __name__ == "__main__":
    main() # call main function
    keep_last_100(Path.cwd()/"uploaded_backgrounds") # delete all files excluding last 100