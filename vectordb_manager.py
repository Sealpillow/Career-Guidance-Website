from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class VectorDBManager:
    def __init__(self, collection_name="job_collection", persist_directory="./chromadb"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self._setup_vectordb()

    def _setup_vectordb(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.vectordb = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
        )

    def _normalize_string(self, s):
        return s.lower().strip().replace(" and ", " & ")

    def populate_db(self, df):
        # Check if the collection already exists
        if self.vectordb._collection is None:
            # If it doesn't exist, create a new collection
            self.vectordb = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
            )
        else:
            # If it exists, just use the existing collection
            pass

        texts = []
        metadatas = []
        ids = []
        df_cleaned = df.dropna(subset=['job_id'])
        for index, row in df_cleaned.iterrows():
            skills = self._normalize_string(str(row['description']) + ' ' + str(row['skill_name']))
            texts.append(skills)
            metadatas.append({
                'job_id': str(int(row['job_id'])),
                'company_name': row['company_name'],
                'title': row['title'],
                'location': row['location'],
                'job_posting_url': row['job_posting_url']
            })
            ids.append(str(int(row['job_id'])))

        # Append new data to the existing collection
        self.vectordb.add_texts(texts=texts, metadatas=metadatas, ids=ids)

    def similarity_search(self, query, k=10, score_threshold=0.5):
        normalized_query = self._normalize_string(query)
        results = self.vectordb.similarity_search_with_score(normalized_query, k=k)
        # for doc,score in results:
        #     print(score)
        
        # Filter results based on the score threshold
        filtered_results = [
            (doc, score) for doc, score in results
            if score <= score_threshold + 0.5
        ]
        
        return filtered_results

    def get_collection_count(self):
        return self.vectordb._collection.count()
    
    def get_all_data(self):
        results = self.vectordb.get()
        print(results)
        return