import os
import streamlit as st
import google.generativeai as genai
from sqlalchemy import create_engine, text

import config
import sqlite3
import tempfile

google_api_key = config.GOOGLE_API_KEY
chat_model = config.CHAT_MODEL

genai.configure(api_key=google_api_key)
# schema_sql = SELECT sql FROM sqlite_master WHERE type='table';

model = genai.GenerativeModel(model_name=chat_model)


def create_database_from_sql(sql_content):
    temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.db', delete=False)
    try:
        with sqlite3.connect(temp_file.name) as conn:
            conn.executescript(sql_content)
            print("Connected to SQLite database")
        st.write("Connected to SQLite database")
    except Exception as e:
        print("Error creating SQLite database:", e)
        st.write("Error creating SQLite database:", e)
    finally:
        conn.close()
    return temp_file.name

def get_schema(db_file):
    try:
        engine = create_engine(f"sqlite://{db_file}", echo=True)
        conn = engine.connect()
        result = conn.execute(text("SELECT sql FROM sqlite_master WHERE type='table';"))
        schema = result.fetchall()
        return schema
    except Exception as e:
        print("Error getting schema:", e)
        st.write("Error getting schema:", e)


def get_model_response(question,schema):
    prompt = f"""
You are an expert SQL devloper. Given and input question {question} and the schema {schema} , you are able to think through and create a correct SQL query to run which will fetch the exact result as desired by the question. 
important : You should only give output a SQL query only and nothing else. The query should be directly executable on the db so respond in the same manner. Do not apply any quote or extra. Do not apply ``` at the beginning or end. 
"""
    response = model.generate_content([prompt])
    return response.text.strip()

def query_database(db_file,sql_query):
    try:
        engine = create_engine(f"sqlite://{db_file}",echo=True)
        conn = engine.connect()
        result = conn.execute(text(sql_query))
        return result.fetchall()
    except Exception as e:
        print("Error querying database:", e)
        st.write("Error querying database:", e)


def run():
    st.header("Query Database")
    uploaded_file = st.file_uploader("Upload a .sql file", type="sql")
    # st.button("Submit", type="primary")
    input = st.text_input("Enter your question about the database",key="input")
    st.text("Here are some sample question:")
    st.text("What are the name of the tables in the database?")
    st.text("What are the name of the artists?")
    if st.button("Submit", type="primary"):
        if uploaded_file:
            if input:
                sql_content = uploaded_file.getvalue().decode("utf-8")
                db_file = create_database_from_sql(sql_content)
                schema = get_schema(db_file)
                sql_query = get_model_response(input, schema)
                st.text_area("Generated SQL Query", sql_query, height=200)
                results = query_database(db_file, sql_query)
                st.write("Query Results:")
                for row in results:
                    st.write(row)

if __name__ == "__main__":
    run()
    







