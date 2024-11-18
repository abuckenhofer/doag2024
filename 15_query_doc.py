import torch
from transformers import BertTokenizer, BertModel
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Generierung von Embeddings mit BERT
def generate_embedding(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Verwenden des Durchschnitts der letzten versteckten Zustände als Embedding
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding.tolist()

# Verbindung zur PostgreSQL-Datenbank
conn = psycopg2.connect(
    dbname=os.environ["PG_DBNAME"], 
    user=os.environ["PG_USER"], 
    password=os.environ["PG_PASSWORD"], 
    host=os.environ["PG_HOST"], 
    port=os.environ["PG_PORT"]
)
cursor = conn.cursor()

# Testdaten
doc_list = ["I like apples"]

# Generieren von Embeddings 
doc_embeddings = [generate_embedding(text) for text in doc_list]

# Query for similarity search
doc_query = """
SELECT doc_text, doc_vector <=> %s::vector AS similarity
FROM doc
ORDER BY similarity
LIMIT 5
"""

# Execute the query for each generated embedding
# Execute the query for each generated embedding
for embedding in doc_embeddings:
    cursor.execute(doc_query, (embedding,))
    results = cursor.fetchall()
    
    print("Similarity Results:")
    for doc_text, similarity in results:
        print(f"{doc_text}, Similarity: {similarity}")


# Commit und Aufräumen
conn.commit()
cursor.close()
conn.close()
