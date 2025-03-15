from transformers import pipeline

# Load a question-answering model
qa_model = pipeline("question-answering")

def answer_customer_query(query, context):
    try:
        result = qa_model(question=query, context=context)
        return result['answer']
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    context = input("Enter context: ")  # Dynamic context input
    query = input("Enter your question: ")
    answer = answer_customer_query(query, context)
    print(f"Answer: {answer}")