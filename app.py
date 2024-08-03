import os
from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent, tool
from langchain_core.prompts import PromptTemplate
from langchain_experimental.utilities import PythonREPL
from langchain_openai import ChatOpenAI
import requests
import json
import numpy as np
from PIL import Image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["OPENAI_API_BASE"] = "http://localhost:8080/v1"
os.environ["OPENAI_API_KEY"] = "NONE"

message_history = SQLChatMessageHistory(
    session_id="test_session_id", connection_string="sqlite:///sqlite.db"
)

memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=message_history
)

chat_llm = ChatOpenAI(model="mixtral", temperature=0)

wrapper = DuckDuckGoSearchAPIWrapper(max_results=2)
search = DuckDuckGoSearchResults(api_wrapper=wrapper)

python_repl = PythonREPL()

@tool
def get_image_from_text(text: str):
    """Generates an image from a a text-only prompt. Useful when a text is given and asked to generate an image."""
    response = requests.get("http://<model_server_ip>:8001/predictions/sdxl", data=text)
    # Contruct image from response
    image = Image.fromarray(np.array(json.loads(response.text), dtype="uint8"))
    img_url = "sdxl_output" + "_".join(text.split) + ".jpg"
    image.save(img_url)
    return img_url

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="""Use this tool in the following circumstances:
            - User is asking about current events or something that requires real-time information
            - User is asking about some term you are totally unfamiliar with (it might be new)
            - User explicitly asks you to browse or provide links to references
        """
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math, but not date calculations, only math",
    ),
    Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl.run
    ),
    get_image_from_text
    """
    Create an image from a text-only prompt
    """
]

template = '''

'''

prompt = PromptTemplate.from_template(template)

agent = create_react_agent(chat_llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

@app.get("/infer")
async def infer(text: str):
    output = await agent_executor.ainvoke({"input": text})
    return output

@app.get("/health")
async def health():
    return {"Health": "Ok"}

