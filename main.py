from flask import Flask, request, jsonify
import pyttsx3
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from context import MyModule

app = Flask(__name__)

myContext = MyModule.contextSample()

template = """
Answer the question below.

Here is the conversation History:{context}

Question: {question}

Answer:

"""

model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('question')
    context = data.get('context', myContext)
    
    result = chain.invoke({"context": context, "question": user_input})
    
    engine = pyttsx3.init()
    engine.say(result)
    engine.runAndWait()
    
    return jsonify({"response": result, "context": context + f"\nUser:{user_input}\nAI:{result}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)