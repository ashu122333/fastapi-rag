import requests
import os
from dotenv import load_dotenv
from pinecone import Pinecone
import time
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

index_name = "multi-pdf-collection"
pc=Pinecone("e6d17400-b5c0-4dca-8015-5f4c59ffaf80")
index = pc.Index(index_name)

API_URL = "https://api-inference.huggingface.co/models/ggrn/e5-small-v2"
headers = {"Authorization": f"Bearer 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"}

llm=ChatGroq(
    # model="llama-3.2-90b-text-preview",
    model="llama-3.1-70b-versatile",
    api_key="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",
    temperature=0)

def get_context(payload):  # Add 2-second delay in the request
    response = requests.post(API_URL, headers=headers, json={"inputs": payload})
    
    if response.status_code != 200:
        time.sleep(2)
        response = requests.post(API_URL, headers=headers, json={"inputs": payload})
        if response.status_code !=200:
            print(f"Error with embedding API: {response.status_code} {response.text}")
            return None
        else:
            pass
    
    embeddings = response.json()  # Ensure this is the correct format
    if not isinstance(embeddings, list):  # Check if the API returns a valid list
        print("Error: Embeddings returned are not a list.")
        return None
    
    try:
        res = index.query(  # Use the embedding to query Pinecone
            namespace="ns1",
            vector=embeddings,  # Assuming payload is for one item; adapt if multiple
            top_k=3,
            include_metadata=True
        )
        contents=[]
        matches=res["matches"]
        for element in matches:
            content=element["metadata"]["content"]
            contents.append(content)
        return contents  # Return the query results
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return None



prompt_ans = PromptTemplate.from_template(
    """
    ### PROVIDED CONTENT:
    {content_section}

    ### INSTRUCTIONS:
    You are an intelligent assistant, and your task is to provide an accurate response to the query below **using only the content provided**.
    Do not add any information not explicitly mentioned in the provided content. If the answer cannot be found in the content, respond with "The answer is not available in the provided content."

    ### QUERY:
    {query}

    ### RESPONSE:
    """
)


def gen_ans(contents,query):
    ans_chain=prompt_ans | llm
    ans=ans_chain.invoke(input={"content_section":contents,"query":query})
    # print(ans.content)
    return ans.content

# input="what is DBMS?"


def query(input):
    query_content=get_context(input)
    # print(query_content)
    answer=gen_ans(query_content,input)
    # print(answer)
    return answer


# print(query("what does CREATE do ?"))
