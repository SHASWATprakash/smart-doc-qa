from transformers import pipeline

class LocalLLMService:
    def __init__(self):
        self.llm = pipeline(
            "text-generation",
            model="google/flan-t5-base",
            max_length=512
        )

    def generate(self, context: str, question: str):
        prompt = f"""
Answer the question using ONLY the context below.
If not found, say: I don't know based on the document.

Context:
{context}

Question:
{question}

Answer:
"""
        result = self.llm(prompt)
        return result[0]["generated_text"]


llm_service = LocalLLMService()