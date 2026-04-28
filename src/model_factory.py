import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

class ModelFactory:
    @staticmethod
    def get_vision_chain():
        # Google Gemini 2.0 Flash
        google_llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            max_retries=0 
        )

        # GitHub Models gpt-4o
        github_4o = ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("GITHUB_TOKEN"),
            base_url="https://models.inference.ai.azure.com",
            max_retries=0
        )

        # GitHub Models gpt-4o-mini 
        github_4o_mini = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("GITHUB_TOKEN"),
            base_url="https://models.inference.ai.azure.com",
            max_retries=0
        )

        # Model fallback sequence
        fallback_chain = google_llm.with_fallbacks([github_4o, github_4o_mini])

        return fallback_chain

    @staticmethod
    def analyze_image(chain, base64_image, prompt_text):
        # Construct multimodal message and invoke AI model
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt_text},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        )

        response = chain.invoke([message])
        return response.content