from langchain_core.documents import Document
import json


def teaching_to_documents(teaching_json: str):
    """
    Convert structured teaching JSON into LangChain documents
    """

    data = json.loads(teaching_json)
    docs = []

    for key, items in data.items():

        if isinstance(items, list):
            for item in items:
                docs.append(
                    Document(
                        page_content=str(item),
                        metadata={"type": key}
                    )
                )
        else:
            docs.append(
                Document(
                    page_content=str(items),
                    metadata={"type": key}
                )
            )

    return docs