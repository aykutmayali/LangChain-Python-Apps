from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()

class KeywordExtractor:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("API Key bulunamadı.")
        
        self.client = OpenAI(api_key=api_key)

        self.model_id = "gpt-4o-mini"

    def extract_hashtags(self, text):
        system_prompt = """
            Sen yaratıcı bir sosyal medya yöneticisisin.
            Görevin verilen metinden paylaşılabilir, popüler 5 adet hastag üret.
            Her kelimenin başında '#' işareti olsun.
            Cevabı SADECE şu JSON formatında ver:
            {"hashtags": ["#tag1", "#tag2"...]}
        """

        raw_tags = self._call_openai(system_prompt, text, "hashtags")

        formatted_tags = [self._format_tag(tag) for tag in raw_tags]

        return formatted_tags

    def extract_keywords(self, text):
        system_prompt = """
            Sen deneyimli bir SEO uzmanısın.
            Görevin verilen metinden en önemli 5 anahtar kelimeyi bulmaktır.
            Cevabı SADECE şu JSON formatında ver:
            {"keywords": ["kelime1", "kelime2"...]}
        """

        return self._call_openai(system_prompt, text, "keywords")

    
    def _call_openai(self, system_prompt, text, json_key):
        print(f"AI çalışıyor ({json_key})")
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Metin: {text}"}
                ],
                response_format={"type":"json_object"},
                temperature=0.3
            )

            raw_content = response.choices[0].message.content

            parsed_content = json.loads(raw_content)

            return parsed_content.get(json_key, [])
        
        except Exception as e:
            print(f"Hata: {e}")
            return []
        
    def _format_tag(self, tag):
        clean_tag = tag.replace(" ", "").lower()

        if not clean_tag.startswith("#"):
            clean_tag = f"#{clean_tag}"

        return clean_tag
        
def main():
    print("Test uygulaması başlatılıyor...")

    try:
        extractor = KeywordExtractor()
    except ValueError as e:
        print(f"hata: {e}")
        return
    
    test_metni = """
    Python, günümüzün en popüler programlama dillerinden biridir. 
    Özellikle Yapay Zeka, Veri Bilimi ve Web Geliştirme alanlarında sıkça kullanılır.
    Django ve FastAPI gibi kütüphaneler sayesinde hızlıca API geliştirebilirsiniz.
    """

    print(f"Analiz edilen metin:\n{test_metni}")

    keywords = extractor.extract_keywords(test_metni)

    print("Çıkarılan kelimeler:")

    for i, kelime in enumerate(keywords, 1):
        print(f"{i}. {kelime}")

    hashtags = extractor.extract_hashtags(test_metni)

    print("Çıkarılan Hashtags:")

    for i, kelime in enumerate(hashtags, 1):
        print(f"{i}. {kelime}")
        
if __name__ == "__main__":
    main()