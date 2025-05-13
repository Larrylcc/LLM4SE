import os
from dotenv import load_dotenv
import chromadb
import documents
from openai import OpenAI
from chromadb.utils import embedding_functions


load_dotenv()

openai_key = os.getenv("ALIYUN_API_KEY")

# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#     api_key=openai_key, model_name="text-embedding-3-small"
# )

chroma_client = chromadb.PersistentClient(path="chroma_persistent_storage")
collection_name = "document_qa_collection"
collection = chroma_client.get_or_create_collection(
    name=collection_name
    # embedding_function=openai_ef
)

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", api_key=openai_key
)

# completion = client.chat.completions.create(
#     # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
#     model="qwen-plus",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "How are you?",
#         },
#     ],
#     # Qwen3模型通过enable_thinking参数控制思考过程（开源版默认True，商业版默认False）
#     # 使用Qwen3开源版模型时，若未启用流式输出，请将下行取消注释，否则会报错
#     # extra_body={"enable_thinking": False},
# )
# # print(completion.model_dump_json())
# print(completion.choices[0].message.content)


def load_documents_from_directory(directory_path):
    print("==== Loading documents from directory ====")
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), encoding="utf-8") as file:
                documents.append({"id": filename, "text": file.read()})
    return documents


def split_text(text, chunk_size=1000, chunk_overlap=20):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks


def get_openai_embedding(text):
    response = client.embeddings.create(input=[text], model="text-embedding-v3")
    # print("==== Getting OpenAI embedding ====")
    return response.data[0].embedding


def get_aliyun_embedding(text):
    response = client.embeddings.create(input=[text], model="text-embedding-v3")
    return response.data[0].embedding


def query_documents(question, n_results=2):
    query_embedding = get_aliyun_embedding(question)
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)

    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]
    print("==== Returning relevant chunks ====")
    return relevant_chunks


def generate_response(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "你是一个问答任务的助手。使用以下检索到的上下文片段来回答这个问题。如果你不知道答案，就说不知道。最多使用三句话，保持答案简洁。"
        + context
        + "\n\nQuestion:\n"
        + question
    )

    completion = client.chat.completions.create(
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ],
    )
    answer = completion.choices[0].message.content
    return answer


def original_response(question):
    completion = client.chat.completions.create(
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[
            {"role": "system", "content": "你是软件工程课程助手。"},
            {"role": "user", "content": question},
        ],
    )
    return completion.choices[0].message.content


if "__main__" == "__main__":
    directory_path = "./TXT2025"
    documents = load_documents_from_directory(directory_path)
    print(f"Loaded {len(documents)} documents.")

    # Split documents into chunks
    print("==== Splitting documents ====")
    chunked_documents = []
    for doc in documents:
        chunks = split_text(doc["text"])
        # print("==== Splitting documents ====")
        for i, chunk in enumerate(chunks):
            chunked_documents.append({"id": f"{doc['id']}-{i}", "text": chunk})

    print(f"Split documents into {len(chunked_documents)} chunks.")

    print("==== Generating embeddings ====")
    for doc in chunked_documents:
        # print("==== Generating embeddings ====")
        doc["embedding"] = get_openai_embedding(doc["text"])
    # print(doc["embedding"])

    print("==== Inserting chunks into db; ====")
    for doc in chunked_documents:
        # print("==== Inserting chunks into db; ====")
        collection.upsert(
            ids=[doc["id"]],
            documents=[doc["text"]],
            embeddings=[doc["embedding"]],
        )

    print("====样例问题：面向对象设计分为哪些阶段？====")
    print(
        "====理论最佳参考文本为第十一讲第十一行开始的文本：◼面向对象设计分为 系统设计 和对象设计 阶段。"
    )
    question = "面向对象设计分为哪些阶段？"
    relevant_chunks = query_documents(question)
    answer = generate_response(question, relevant_chunks)
    print("==== 原始无RAG的大模型回答 ====")
    print(original_response(question))
    print("==== 样例回答 ====")
    print(answer)

    print("====数据库初始化完成，请输入您的问题（输入'exit'退出）====")
    while True:
        question = input("用户: ")
        if question.lower() == "exit()":
            print("==== 退出程序 ====")
            break
        if not question.strip():
            print("==== 请输入问题 ====")
            continue

        relevant_chunks = query_documents(question)
        if not relevant_chunks:
            print("AI: 抱歉，我没有找到相关信息。")
            continue
        answer = generate_response(question, relevant_chunks)
        print(f"AI: {answer}")
