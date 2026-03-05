"""
Specialized prompts for different Emare projects
Each project has its own optimized prompts
"""

# Emare Asistan - WhatsApp Customer Service
PROMPTS_ASISTAN = {
    "whatsapp_reply": """Sen bir müşteri hizmetleri asistanısın. WhatsApp üzerinden gelen müşteri sorusuna profesyonel ve dostça cevap ver.

Müşteri sorusu: {question}
Şirket bilgisi: {company_context}

Kurallar:
- Kısa ve öz ol (maksimum 2-3 cümle)
- Emoji kullan (😊 👍 ✅ gibi)
- Türkçe karakterleri doğru kullan
- Profesyonel ama samimi ton

Cevap:""",
    
    "customer_sentiment": """Bu müşteri mesajının duygusunu analiz et ve kategorize et.

Mesaj: {message}

Kategoriler: pozitif, negatif, nötr, acil
Skala: 1-10
Açıklama: Kısa analiz

JSON formatında döndür:""",
}

# Emare Finance - Financial Analysis
PROMPTS_FINANCE = {
    "invoice_summary": """Bu faturayı özetle ve önemli noktaları çıkar.

Fatura detayları: {invoice_data}

Çıktı format:
- Toplam tutar
- Ürün/hizmet özeti
- Ödeme durumu
- Önemli notlar

Özet:""",
    
    "financial_advice": """Aşağıdaki finansal verilere göre işletmeye tavsiyelerde bulun.

Veriler: {financial_data}

Analiz et:
1. Ciro trendi
2. Kar marjı
3. Nakit akışı
4. 3 somut öneri

Analiz:""",
}

# Emare Makale - Content Generation
PROMPTS_MAKALE = {
    "blog_post": """Aşağıdaki konu hakkında SEO-friendly Türkçe blog yazısı yaz.

Konu: {topic}
Anahtar kelimeler: {keywords}
Uzunluk: {word_count} kelime

Yapı:
- Dikkat çekici başlık (H1)
- Giriş paragrafı
- 3-5 alt başlık (H2)
- Sonuç ve CTA

Yazı:""",
    
    "content_improve": """Bu metni daha iyi hale getir: SEO, okunabilirlik, akıcılık.

Orijinal metin: {original_text}

İyileştirilmiş versiyon:""",
}

# SiberEmare - Security Analysis
PROMPTS_SIBER = {
    "vulnerability_explain": """Bu güvenlik açığını teknik olmayan birine açıkla.

Açık: {vulnerability}
Teknik detay: {technical_info}

Açıklama (Türkçe, sade dil):
1. Ne?
2. Nasıl tehlikeli?
3. Nasıl korunulur?

Açıklama:""",
    
    "pentest_report": """Bu pentest bulgularından profesyonel rapor oluştur.

Bulgular: {findings}
Hedef sistem: {target}

Rapor içeriği:
- Executive Summary (yöneticiler için)
- Teknik detaylar
- Risk seviyeleri
- Öneriler

Rapor:""",
}

# Emare Log - Log Analysis
PROMPTS_LOG = {
    "log_anomaly": """Bu logları analiz et ve anormal aktivite tespit et.

Loglar: {logs}
Normal pattern: {normal_pattern}

Anomaliler:
- Neler bulundu
- Risk seviyesi
- Olası sebep
- Önerilen aksiyon

Analiz:""",
    
    "log_summary": """Bu log verilerini özetle ve önemli olayları çıkar.

Loglar: {logs}
Zaman aralığı: {time_range}

Özet:
- Toplam olay sayısı
- Kritik olaylar
- Trendler
- Dikkat gerektiren noktalar

Özet:""",
}

# EmareSetup / EmareHup / Emare Code - Code Generation
PROMPTS_CODE = {
    "generate_code": """Aşağıdaki açıklamaya göre {language} kodu yaz.

İstek: {request}
Teknoloji: {tech_stack}

Gereksinimler:
- Clean code
- Yorumlar
- Error handling
- Type hints (Python için)

Kod:""",
    
    "code_review": """Bu kodu gözden geçir ve iyileştirme önerileri sun.

Kod:
{code}

İnceleme:
1. Kod kalitesi (1-10)
2. Potansiyel buglar
3. Performance sorunları
4. Güvenlik açıkları
5. İyileştirme önerileri

Review:""",
    
    "code_explain": """Bu kodu Türkçe olarak açıkla (teknik olmayan birine).

Kod:
{code}

Açıklama:
- Ne yapıyor?
- Nasıl çalışıyor?
- Önemli noktalar

Açıklama:""",
}

# Emare POS - Restaurant Analytics
PROMPTS_POS = {
    "menu_suggestion": """Aşağıdaki sipariş geçmişine göre yeni menü önerileri sun.

Sipariş geçmişi: {order_history}
Sezon: {season}
Maliyet hedefi: {budget}

Öneriler:
- 3 yeni yemek
- Fiyat aralığı
- Benzer restoranlardan örnekler

Öneriler:""",
    
    "order_prediction": """Bu verilere göre gelecek hafta satış tahmini yap.

Geçmiş veriler: {historical_data}
Özel günler: {special_days}

Tahmin:
- Günlük ortalama sipariş
- Popüler ürünler
- Stok önerileri

Tahmin:""",
}

# EmareCloud - Infrastructure Analysis
PROMPTS_CLOUD = {
    "server_health": """Bu sunucu metriklerini analiz et ve durum raporu ver.

Metrikler: {metrics}
Sunucu: {server_name}

Durum raporu:
- Genel sağlık (1-10)
- Potansiyel sorunlar
- Kaynak kullanımı
- Önerilen aksiyonlar

Rapor:""",
}

# Emare Ads - Content Analysis
PROMPTS_ADS = {
    "page_analysis": """Bu web sayfasını analiz et ve öneriler sun.

Sayfa içeriği: {page_content}
URL: {url}

Analiz:
- Ana konu
- Anahtar kelimeler
- SEO skoru (tahmini)
- İyileştirme önerileri

Analiz:""",
}

# Generic prompts
PROMPTS_GENERIC = {
    "translate": """Aşağıdaki metni {source_lang} dilinden {target_lang} diline çevir.

Metin: {text}

Çeviri:""",
    
    "summarize": """Bu metni {length} kelimeyle özetle.

Metin: {text}

Özet:""",
    
    "sentiment": """Bu metnin duygusunu analiz et.

Metin: {text}

Duygu analizi (pozitif/negatif/nötr):""",
}


def get_prompt(project: str, task: str, **kwargs) -> str:
    """
    Get optimized prompt for specific project and task
    
    Args:
        project: Project name (asistan, finance, makale, etc.)
        task: Task type (whatsapp_reply, invoice_summary, etc.)
        **kwargs: Variables to inject into prompt
    
    Returns:
        Formatted prompt string
    """
    prompts_map = {
        "asistan": PROMPTS_ASISTAN,
        "finance": PROMPTS_FINANCE,
        "makale": PROMPTS_MAKALE,
        "siber": PROMPTS_SIBER,
        "log": PROMPTS_LOG,
        "code": PROMPTS_CODE,
        "pos": PROMPTS_POS,
        "cloud": PROMPTS_CLOUD,
        "ads": PROMPTS_ADS,
        "generic": PROMPTS_GENERIC,
    }
    
    project_prompts = prompts_map.get(project, PROMPTS_GENERIC)
    prompt_template = project_prompts.get(task)
    
    if not prompt_template:
        raise ValueError(f"Unknown task '{task}' for project '{project}'")
    
    return prompt_template.format(**kwargs)
