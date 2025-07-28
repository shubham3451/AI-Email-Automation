from langchain.llms import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from config import settings

PROMPT_TEMPLATE = """
You are a helpful assistant. Use the conversation thread, attachment contents, and relevant documents (if any) to craft a polite and accurate reply.

Thread history:
{thread}

Attachment contents:
{attachments}

Document context:
{docs}

Latest customer message:
{latest}

Reply:
"""

def get_llm():
     return HuggingFaceHub(
            repo_id=settings.HUGGINGFACE_MODEL,
            huggingfacehub_api_token=settings.HUGGINGFACETOKEN,
            model_kwargs={
                "temperature": 0.7,
                "max_new_tokens": 512
            }
        )

def generate_reply(thread: str, attachments: str, docs: str, latest: str) -> str:
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["thread", "attachments", "docs", "latest"],
        template=PROMPT_TEMPLATE
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(thread=thread, attachments=attachments, docs=docs, latest=latest)
