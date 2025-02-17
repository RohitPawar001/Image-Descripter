from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "you are an helpfull assistance give the description about the user query"),
        ("user", "Tell me something about {topic}")
    ]
)
output_parser = StrOutputParser()
chain = prompt_template | llm |output_parser

result = chain.invoke({"topic": "tiger cat"})
print(result)
