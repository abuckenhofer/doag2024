import torch
from transformers import BertTokenizer, BertModel
import psycopg2
from psycopg2.extras import execute_batch
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

# Truncate table to delete existing data
truncate_query = "TRUNCATE TABLE doc"
cursor.execute(truncate_query)

# Testdaten
doc_list = ["I eat apples", 
            "I eat pears", 
            "I drink red wine",
            "I drive a Mercedes-Benz",
            "I live in a flat"
            ]

# Generieren von Embeddings 
doc_embeddings = [generate_embedding(text) for text in doc_list]

# Einfügen von Embeddings in die Datenbank
doc_insert_query = "INSERT INTO doc (doc_text, doc_vector) VALUES (%s, %s)"
data_to_insert = [(doc_list[i], doc_embeddings[i]) for i in range(len(doc_list))]

execute_batch(cursor, doc_insert_query, data_to_insert)

# Commit und Aufräumen
conn.commit()
cursor.close()
conn.close()

print("Embeddings erfolgreich eingefügt.")
