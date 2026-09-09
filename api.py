from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from extractor import KeywordExtractor
from pydantic import BaseModel

app = FastAPI(
    title="API Content Analyzer API",
    description="Metin analizi, SEO kelimelerini ve Hastag üretimi için servis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

try:
    extractor_service = KeywordExtractor()
    print("AI Servisi başarıyla yüklendi")
except Exception as ex:
    print(f"Hata: {ex}")

class AnalyzerRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "API çalışıyor. Dökümantasyon için /docs adresine gidin."}

@app.post("/api/hashtags")
def get_hashtags(request: AnalyzerRequest):
    cleaned_text = validate_input(request.text)
    
    return {"hashtags": extractor_service.extract_hashtags(cleaned_text)}

@app.post("/api/keywords")
def get_keywords(request: AnalyzerRequest):
    cleaned_text = validate_input(request.text)
    return {"keywords": extractor_service.extract_keywords(cleaned_text)}

def validate_input(text: str):
    cleaned_text = text.strip()

    if not cleaned_text:
        raise HTTPException(status_code=400, detail="Metin alanı boş olamaz.")
    
    if len(cleaned_text) < 10:
        raise HTTPException(status_code=400, detail="Metin analizi için içerik çok kısa.")
    
    return cleaned_text