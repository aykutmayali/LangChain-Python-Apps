from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

load_dotenv()

class TatliTarifi(BaseModel):
    tatli_adi: str = Field(description="Tatli adı")
    hazirlama_suresi: int = Field(description="Dakika cinsinden hazırlama süresi")
    malzemeler: list[str] = Field(description="Kullanılan malzemeler")
    kalori: int = Field(description="Kalori cinsinden değeri")
    
class TarifListesi(BaseModel):
    tarifler: list[TatliTarifi] = Field(description="Tatlı tarif listesi")

LLM = ChatOpenAI(model = "gpt-4o-mini", temperature=0.8)

parser = JsonOutputParser(pydantic_object=TatliTarifi)

format_instructions = parser.get_format_instructions()
prompt = ChatPromptTemplate.from_template("Bana {meyve} ile yapılan 3 tatlı tarifi ver. \n {format_instructions}")

prompt = prompt.partial(format_instructions = format_instructions)

chain = prompt | LLM | parser

sonuc = chain.invoke({"meyve":"Muz"})

import json
print(json.dumps(sonuc, indent=2, ensure_ascii=False))