from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage ,SystemMessage,HumanMessage

model = ChatMistralAI(
    model="mistral-small-latest"
)
msg=[
SystemMessage(content="you are a sad AI agent ")
]
print("----------hellow press 0 for exist---------")
while True: 
    prompt=input("you :")
    msg.append(HumanMessage(content=prompt))
    if(prompt==0):
        break
    response = model.invoke(msg)
    msg.append(AIMessage(content=response.content))
    print("bot :" ,response.content)