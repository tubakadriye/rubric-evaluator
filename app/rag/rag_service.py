from app.rag.from_vision import teaching_to_documents
from app.rag.splitter import split_documents
from app.rag.embeddings import get_embeddings
from app.rag.vectorstore import build_vectorstore
from app.rag.retriever import get_retriever


class RAGService:

    def __init__(self, teaching_json: str):

        # 1. Convert vision → docs
        docs = teaching_to_documents(teaching_json)

        # 2. Split
        splits = split_documents(docs)

        # 3. Embeddings
        embeddings = get_embeddings()

        # 4. Vector store
        vectorstore = build_vectorstore(splits, embeddings)
        self.vectorstore = vectorstore

        # 5. Retriever
        self.retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 4}
        )

    def retrieve(self, query: str, k: int = 4):

        docs = self.vectorstore.similarity_search(query, k=k)
        return "\n\n".join([d.page_content for d in docs])
    

    
    def retrieve_per_criterion(self, rubric_structured):

        contexts = []

        criteria = rubric_structured.get("criteria", [])

        for rule in criteria:
            name = rule.get("name", "")
            description = rule.get("description", "")

            query = f"""
        Criterion: {name}
        Description: {description}
        Find relevant teaching material.
        """

            docs = self.vectorstore.similarity_search(query, k=3)

            context = "\n".join([d.page_content for d in docs])

            contexts.append({
                "criterion": name,
                "context": context
            })

        return contexts


    def retrieve_structured(self, query: str):

        docs = self.retriever.invoke(query)

        return [
            {
                "content": d.page_content,
                "type": d.metadata.get("type")
            }
            for d in docs
        ]
    
