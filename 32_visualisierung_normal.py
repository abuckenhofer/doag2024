import psycopg2
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

# Verbindung zur Datenbank
connection = psycopg2.connect(
    host=os.environ["PG_HOST"], 
    dbname=os.environ["PG_DBNAME"], 
    user=os.environ["PG_USER"], 
    password=os.environ["PG_PASSWORD"], 
)

cursor = connection.cursor()
cursor.execute("SELECT songvector as vector FROM music")
vectors = cursor.fetchall()
cursor.close()
connection.close()

# Konvertieren in numpy-Array
vectors = np.array([np.fromstring(vector[0][1:-1], sep=',') for vector in vectors])

# Anwenden von t-SNE
tsne = TSNE(n_components=2, perplexity=4, n_iter=1000, random_state=42)
tsne_results = tsne.fit_transform(vectors)

# Visualisierung aller Datenpunkte
plt.figure(figsize=(8, 6))
plt.scatter(tsne_results[:, 0], tsne_results[:, 1], alpha=0.8)
plt.title("t-SNE Visualisierung aller Musikdaten")
plt.xlabel("t-SNE Component 1")
plt.ylabel("t-SNE Component 2")
plt.show()

plt.savefig("tsne_visualization_normal.png")
print("Abbildung gespeichert als tsne_visualization_normal.png")