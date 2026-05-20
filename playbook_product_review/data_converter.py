import pandas as pd
from langchain_core.documents import Document


def dataconverter():

    # =====================================================
    # Load Dataset
    # =====================================================

    product_data = pd.read_csv("data/playbook_product_review.csv")

    # Select Required Columns
    data = product_data[["product_title", "review"]]

    # =====================================================
    # Convert Data into Dictionary Format
    # =====================================================

    product_list = []

    for index, row in data.iterrows():

        obj = {
            "product_name": row["product_title"],
            "review": row["review"]
        }

        product_list.append(obj)

    # =====================================================
    # Convert into LangChain Documents
    # =====================================================

    docs = []

    for obj in product_list:

        metadata = {
            "product_name": obj["product_name"]
        }

        doc = Document(
            page_content=obj["review"],
            metadata=metadata
        )

        docs.append(doc)

    # =====================================================
    # Return Documents
    # =====================================================

    return docs