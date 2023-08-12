import pickle
import numpy as np
from tensorflow import keras
from sklearn.neighbors import NearestNeighbors
from pathlib import Path

# Create ResNet50 Model
model = keras.applications.resnet50.ResNet50(
    include_top=False,
    weights="imagenet",
    input_shape=(224, 224, 3)
)

model.trainable = False
model = keras.Sequential([
    model,
    keras.layers.GlobalMaxPool2D()
])

# Load Binary files
embeddings = pickle.load(open(Path.cwd()/'bin/embeddings.pkl', 'rb'))
filenames = pickle.load(open(Path.cwd()/'bin/url_container.pkl', 'rb'))

# Create Embeddings for new image
def generate_embeddings(img_path) -> np.ndarray:
    img = keras.preprocessing.image.load_img(img_path, target_size=(224, 224))
    img_array = keras.preprocessing.image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    output = model.predict(expanded_img_array)
    normalized_output = output / np.linalg.norm(output)

    return normalized_output.flatten()

# Closest Matching Embeddings
def neighbors(img_path):
    neighbors = NearestNeighbors(n_neighbors=50, algorithm="brute", metric="euclidean")
    neighbors.fit(embeddings)

    output = generate_embeddings(img_path=img_path)
    distances, indices = neighbors.kneighbors([output])

    return distances, indices

# End of the file
if __name__ == "__main__":
    distances, indices = neighbors(Path.cwd()/"uploaded_backgrounds/dracula-arch.png")
    print(distances, indices)