# LangChain Python Apps

OpenAI ve LangChain kullanılarak geliştirilmiş Python uygulamaları. Projede metinlerden SEO anahtar kelimeleri ve sosyal medya hashtag'leri üreten bir FastAPI servisi ile yapılandırılmış JSON çıktısı üreten bir LangChain örneği bulunur.

## Özellikler

- OpenAI ile metin analizi
- Metinden SEO anahtar kelimeleri çıkarma
- Sosyal medya için hashtag üretme
- FastAPI tabanlı REST API
- Swagger/OpenAPI dokümantasyonu
- LangChain ve Pydantic ile yapılandırılmış JSON çıktısı

## Gereksinimler

- Python 3.10 veya üzeri
- OpenAI API anahtarı

## Kurulum

1. Projeyi klonlayın ve klasöre girin:

```bash
git clone https://github.com/aykutmayali/LangChain-Python-Apps.git
cd LangChain-Python-Apps
```

2. Sanal ortam oluşturun:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell için:

```powershell
.venv\Scripts\Activate.ps1
```

3. Bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

4. Kök dizinde `.env` dosyası oluşturun:

```env
OPENAI_API_KEY=your_openai_api_key
```

## FastAPI servisini çalıştırma

```bash
uvicorn api:app --reload
```

Servis çalıştıktan sonra:

- API: http://127.0.0.1:8000
- Swagger dokümantasyonu: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API kullanımı

### Sağlık kontrolü

```bash
curl http://127.0.0.1:8000/
```

### SEO anahtar kelimeleri çıkarma

```bash
curl -X POST http://127.0.0.1:8000/api/keywords \
  -H "Content-Type: application/json" \
  -d '{"text":"Python ve yapay zeka ile modern web uygulamaları geliştirme"}'
```

Örnek yanıt:

```json
{
  "keywords": [
    "Python",
    "yapay zeka",
    "web uygulamaları"
  ]
}
```

### Hashtag üretme

```bash
curl -X POST http://127.0.0.1:8000/api/hashtags \
  -H "Content-Type: application/json" \
  -d '{"text":"Python ve yapay zeka ile modern web uygulamaları geliştirme"}'
```

Örnek yanıt:

```json
{
  "hashtags": [
    "#python",
    "#yapayzeka",
    "#webgelistirme"
  ]
}
```

Metin boşsa veya 10 karakterden kısaysa API `400 Bad Request` döndürür.

## Komut satırı örneği

`extractor.py`, API dışında doğrudan test amacıyla da çalıştırılabilir:

```bash
python extractor.py
```

## LangChain JSON örneği

`langchain-json.py`, LangChain `ChatPromptTemplate`, `ChatOpenAI`, `JsonOutputParser` ve Pydantic kullanarak yapılandırılmış tatlı tarifi çıktısı üretir:

```bash
python langchain-json.py
```

Bu örnek için de `.env` dosyasında `OPENAI_API_KEY` tanımlı olmalıdır.

## Proje yapısı

```text
.
├── api.py              # FastAPI uygulaması ve endpoint'ler
├── extractor.py        # OpenAI tabanlı anahtar kelime ve hashtag servisi
├── langchain-json.py   # LangChain ile JSON çıktı örneği
├── requirements.txt    # Python bağımlılıkları
└── .env                # API anahtarı, Git'e eklenmez
```

## Güvenlik

- API anahtarınızı kaynak koduna yazmayın.
- `.env` dosyasını Git'e göndermeyin.
- Üretim ortamında `allow_origins=["*"]` ayarını yalnızca ihtiyaç duyulan domain'lerle sınırlandırın.

## Lisans

Bu proje eğitim ve deneme amaçlıdır.
