from langchain_classic.chains import (
    create_retrieval_chain,
    create_history_aware_retriever
)

from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

from langchain_core.prompts import (
    MessagesPlaceholder,
    ChatPromptTemplate
)

from langchain_groq import ChatGroq

from langchain_community.chat_message_histories import (
    ChatMessageHistory
)

from langchain_core.chat_history import (
    BaseChatMessageHistory
)

from langchain_core.runnables.history import (
    RunnableWithMessageHistory
)

from playbook_product_review.data_ingestion import data_ingestion

from dotenv import load_dotenv

import os


# =========================================================
# Load Environment Variables
# =========================================================

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


# =========================================================
# Load LLM
# =========================================================

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5
)


# =========================================================
# Chat History Store
# =========================================================

store = {}


def get_session_history(
    session_id: str
) -> BaseChatMessageHistory:

    if session_id not in store:

        store[session_id] = ChatMessageHistory()

    return store[session_id]


# =========================================================
# Main Generation Function
# =========================================================

def generation(vstore):

    # =====================================================
    # Retriever
    # =====================================================

    retriever = vstore.as_retriever(
        search_kwargs={"k": 3}
    )

    # =====================================================
    # Contextualize Question Prompt
    # =====================================================

    retriever_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. "
        "Do NOT answer the question. "
        "Only reformulate it if needed."
    )

    contextualize_q_prompt = (
        ChatPromptTemplate.from_messages(
            [
                ("system", retriever_prompt),

                MessagesPlaceholder(
                    variable_name="chat_history"
                ),

                ("human", "{input}"),
            ]
        )
    )

    # =====================================================
    # History Aware Retriever
    # =====================================================

    history_aware_retriever = (
        create_history_aware_retriever(
            model,
            retriever,
            contextualize_q_prompt
        )
    )

    # =====================================================
    # Product Bot Prompt
    # =====================================================

    PRODUCT_BOT_TEMPLATE = """
You are an ecommerce product recommendation assistant.

Your job is to:
- Recommend products
- Answer customer product queries
- Analyze product titles and reviews
- Provide concise and accurate answers

Use ONLY the provided context.

If the answer is not available in the context,
say:
'I could not find relevant product information.'

CONTEXT:
{context}

QUESTION:
{input}

ANSWER:
"""

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", PRODUCT_BOT_TEMPLATE),

            MessagesPlaceholder(
                variable_name="chat_history"
            ),

            ("human", "{input}")
        ]
    )

    # =====================================================
    # Question Answer Chain
    # =====================================================

    question_answer_chain = (
        create_stuff_documents_chain(
            model,
            qa_prompt
        )
    )

    # =====================================================
    # Retrieval Chain
    # =====================================================

    rag_chain = create_retrieval_chain(
        history_aware_retriever,
        question_answer_chain
    )

    # =====================================================
    # Conversational RAG Chain
    # =====================================================

    conversational_rag_chain = (
        RunnableWithMessageHistory(

            rag_chain,

            get_session_history,

            input_messages_key="input",

            history_messages_key="chat_history",

            output_messages_key="answer",
        )
    )

    return conversational_rag_chain


# =========================================================
# Main Execution
# =========================================================

if __name__ == "__main__":

    # Load Vector Store
    vstore = data_ingestion("done")

    # Create Conversational RAG Chain
    conversational_rag_chain = generation(vstore)

    # =====================================================
    # First Query
    # =====================================================

    answer = conversational_rag_chain.invoke(

        {
            "input": (
                "Can you tell me the best bluetooth buds?"
            )
        },

        config={
            "configurable": {
                "session_id": "justinfi.info"
            }
        }

    )["answer"]

    print("\nFirst Answer:\n")

    print(answer)

    # =====================================================
    # Follow-Up Query
    # =====================================================

    answer1 = conversational_rag_chain.invoke(

        {
            "input": "What was my previous question?"
        },

        config={
            "configurable": {
                "session_id": "justinfi.info"
            }
        }

    )["answer"]

    print("\nSecond Answer:\n")

    print(answer1)