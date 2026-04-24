import openai

async def answer_question(req):
    context = "retrieved chunks here"

    prompt = f"""
    Answer based ONLY on context.
    If not found, say: I don't know.

    Context:
    {context}

    Question:
    {req.question}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"answer": response.choices[0].message.content}