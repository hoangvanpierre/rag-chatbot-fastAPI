from rag_chatbot import build_rag_prompt

prompt = build_rag_prompt(
    "Toán học đóng vai trò như thế nào đối với AI",
    document_name="The mathematics of AI Paper.pdf"
)
print(prompt)