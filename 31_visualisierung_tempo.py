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

tempo = vectors[:, 3] # Dritte Stelle im Vektor

# Anwenden von t-SNE auf die Vektordaten
tsne = TSNE(n_components=2, perplexity=4, n_iter=1000, random_state=42)
tsne_results = tsne.fit_transform(vectors)

#Farbcodierung nach Tempo
plt.figure(figsize=(8, 6))
scatter = plt.scatter(tsne_results[:, 0], tsne_results[:, 1], c=tempo, cmap='coolwarm', alpha=0.7)
plt.colorbar(scatter, label="Tempo")
plt.title("t-SNE Visualisierung: Tempo")
plt.xlabel("t-SNE Component 1")
plt.ylabel("t-SNE Component 2")
plt.show()

plt.savefig("tsne_visualization_tempo.png")
print("Abbildung gespeichert als tsne_visualization_tempo.png")

