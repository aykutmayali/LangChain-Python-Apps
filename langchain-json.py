from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from pydantic import BaseModel, Field

load_dotenv()

class YemekTarifi(BaseModel):
    yemek_adi: str = Field(description="Yemek adı")
    hazirlama_suresi: int = Field(description="Dakika cinsinden hazırlama süresi")
    malzemeler: list[str] = Field(description="Kullanılan malzemeler")
    hazirlama: str =Field(description="İşlem sırası")
    kalori: int = Field(description="Kalori cinsinden değeri")
    
class TarifListesi(BaseModel):
    tarifler: list[YemekTarifi] = Field(description="yemek tarif listesi")

LLM = ChatOpenAI(model = "gpt-4o-mini", temperature=0.8)

parser = JsonOutputParser(pydantic_object=YemekTarifi)

format_instructions = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Sen bir beşyıldızlı Michelin restoranının baş aşçısısın. "
        "Yanıtını aşağıdaki JSON formatına uygun ver:\n{format_instructions}"
    ),
    MessagesPlaceholder(variable_name="gecmis"),
    ("human", "{soru}")
])
prompt = prompt.partial(format_instructions = format_instructions)

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain = prompt | LLM

chain_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="soru",
    history_messages_key="gecmis"
)

chain = chain_memory | parser

config = {"configurable": {"session_id": "sess_1"}}
sonuc = chain.invoke(
    {"soru": "Merhaba, ben yeni bir gastronomi öğrencisiyim, Hindi ile ne yemek yapabilirim ?"},
    config= config
)



import json
print(json.dumps(sonuc, indent=2, ensure_ascii=False))

sonuc_2 = chain_memory.invoke(
    {"soru": "Merhaba, ben az önce hangi Yemeği sordum ?"},
    config= config
)
print(f"sonuc_2: {sonuc_2.content}")