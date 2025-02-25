from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


class DescriptionGenerator:
    
    def __init__(self):
        pass
        
    def generate_description(self,recognized_image):
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)

        """prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "you are an helpfull assistance give the description about the user query"),
                ("user", "Tell me something about {topic}")
            ]
        )"""
        
        prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are an expert image analysis assistant specialized in generating detailed, accurate, and well-structured descriptions of images.

        When describing images:
        1. Start with a concise overview of the Recognized Image
        2. For complex images, organize your description in a logical flow
        3. Mention any technical aspects if relevant (image quality, filters, etc.)

        Your descriptions should be comprehensive but concise, focusing on what's visually present without unnecessary speculation."""),
            
            ("human", """Here is an image to describe.

        Recognized Image: {image_context}

        Please provide a detailed description of this image.""")
        ])
        
        output_parser = StrOutputParser()
        chain = prompt_template | llm | output_parser

        return chain.invoke({"image_context": recognized_image})
        
