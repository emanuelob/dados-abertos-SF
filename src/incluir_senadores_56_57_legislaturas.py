import sqlite3
import pandas as pd

# Load senators data from the CSV file
senadores_df = pd.read_csv('data/senadores_legislaturas_56_57.csv')

# Connect to the SQLite3 database (or create it if it doesn't exist)
conn = sqlite3.connect('data/discursos.db')
cursor = conn.cursor()

# Insert data into the Senadores table
for _, row in senadores_df.iterrows():
    cursor.execute('''
    INSERT OR IGNORE INTO Senadores (
        codigo_parlamentar, nome_parlamentar, nome_completo, sexo, sigla_partido, uf, forma_tratamento, url_foto, url_pagina, email
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['codigo_parlamentar'], row['nome_parlamentar'], row['nome_completo'], row['sexo'], row['sigla_partido'],
        row['uf'], row['forma_tratamento'], row['url_foto'], row['url_pagina'], row['email']
    ))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Senadores table created and populated successfully.")