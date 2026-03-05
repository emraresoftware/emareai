# 🎯 Emare AI - Proje Bazlı Endpoint Dokümantasyonu

> **Oluşturulma:** 4 Mart 2026  
> **Versiyon:** v1.1.0  
> **Amaç:** Her Emare projesi için özelleştirilmiş AI endpoint'leri

---

## 📋 İçindekiler

- [Emare Asistan Endpoints](#emare-asistan)
- [Emare Finance Endpoints](#emare-finance)
- [Emare Makale Endpoints](#emare-makale)
- [SiberEmare Endpoints](#siberemare)
- [Emare Log Endpoints](#emare-log)
- [Code Generation Endpoints](#code-generation)
- [Emare POS Endpoints](#emare-pos)
- [EmareCloud Endpoints](#emarecloud)
- [Emare Ads Endpoints](#emare-ads)
- [Generic Endpoints](#generic-endpoints)

---

## 🤖 Emare Asistan

### WhatsApp Reply Generation
```bash
POST /v1/emare/asistan/whatsapp-reply
```

**Request:**
```json
{
  "question": "Ürünüm ne zaman gelir?",
  "company_context": "E-ticaret şirketi, 2-3 iş günü teslimat",
  "customer_name": "Ahmet"
}
```

**Response:**
```json
{
  "reply": "Merhaba Ahmet! 😊 Siparişiniz 2-3 iş günü içinde kargoya verilecek. Takip numaranızı SMS ile göndereceğiz. ✅",
  "customer_name": "Ahmet"
}
```

### Customer Sentiment Analysis
```bash
POST /v1/emare/asistan/sentiment?text=Çok kızgınım, ürün gelmedi!
```

**Response:**
```json
{
  "sentiment": "negatif",
  "score": 2.5,
  "explanation": "Müşteri hayal kırıklığı yaşıyor ve acil müdahale gerekiyor"
}
```

---

## 💰 Emare Finance

### Invoice Summary
```bash
POST /v1/emare/finance/invoice-summary
```

**Request:**
```json
{
  "invoice_data": {
    "invoice_no": "2024-001",
    "customer": "ABC Ltd",
    "total": 15000,
    "items": [
      {"name": "Consulting", "qty": 10, "price": 1500}
    ]
  }
}
```

**Response:**
```json
{
  "summary": "Fatura No: 2024-001\nMüşteri: ABC Ltd\nToplam: 15.000 TL\nHizmet: Danışmanlık (10 saat)\nDurum: Ödendi"
}
```

### Financial Advice
```bash
POST /v1/emare/finance/advice
```

**Request:**
```json
{
  "financial_data": {
    "revenue": 100000,
    "expenses": 75000,
    "profit_margin": 25
  },
  "period": "monthly"
}
```

**Response:**
```json
{
  "advice": "1. Ciro trendi olumlu\n2. Kar marjı iyi seviyede (%25)\n3. Öneri: Maliyetleri %10 optimize edin..."
}
```

---

## 📝 Emare Makale

### Blog Post Generation
```bash
POST /v1/emare/makale/blog-post
```

**Request:**
```json
{
  "topic": "Python ile Web Scraping",
  "keywords": ["python", "beautifulsoup", "scraping"],
  "word_count": 500,
  "tone": "professional"
}
```

**Response:**
```json
{
  "title": "Python ile Web Scraping",
  "content": "# Python ile Web Scraping Rehberi\n\nWeb scraping...",
  "word_count": 487
}
```

### Content Improvement
```bash
POST /v1/emare/makale/improve
```

**Request:**
```json
{
  "original_text": "Bu yazı Python hakkında. Python iyidir.",
  "focus": "all"
}
```

**Response:**
```json
{
  "original": "Bu yazı Python hakkında. Python iyidir.",
  "improved": "Bu kapsamlı rehberde Python programlama dilinin avantajlarını keşfedeceksiniz..."
}
```

---

## 🛡️ SiberEmare

### Vulnerability Explanation
```bash
POST /v1/emare/siber/vulnerability-explain
```

**Request:**
```json
{
  "vulnerability": "SQL Injection",
  "technical_info": "User input not sanitized in login form"
}
```

**Response:**
```json
{
  "explanation": "SQL Injection nedir?\n\nBir saldırgan, giriş formuna özel kodlar yazarak veritabanınıza erişebilir..."
}
```

### Pentest Report Generation
```bash
POST /v1/emare/siber/pentest-report
```

**Request:**
```json
{
  "findings": [
    {
      "type": "SQL Injection",
      "severity": "critical",
      "affected": "Login form"
    }
  ],
  "target": "example.com"
}
```

**Response:**
```json
{
  "report": "## Penetrasyon Test Raporu\n\nHedef: example.com...",
  "target": "example.com",
  "findings_count": 1
}
```

---

## 📡 Emare Log

### Log Anomaly Detection
```bash
POST /v1/emare/log/analyze
```

**Request:**
```json
{
  "logs": [
    "2024-03-04 10:00:00 - User login: admin",
    "2024-03-04 10:01:00 - Failed login: admin (10 attempts)",
    "2024-03-04 10:02:00 - Database connection error"
  ],
  "normal_pattern": "Normal user activity",
  "time_range": "last_hour"
}
```

**Response:**
```json
{
  "analysis": "Anomaliler tespit edildi:\n1. Brute force saldırısı (10 başarısız giriş)\n2. Veritabanı bağlantı hatası\n\nRisk: Yüksek\nÖneri: IP'yi blokla",
  "logs_analyzed": 3
}
```

### Log Summary
```bash
POST /v1/emare/log/summary
```

**Request:**
```json
{
  "logs": ["...100 log lines..."],
  "time_range": "24h"
}
```

**Response:**
```json
{
  "summary": "24 saat özeti:\n- Toplam 1250 olay\n- 3 kritik hata\n- Normal trafik: %95",
  "time_range": "24h"
}
```

---

## 💻 Code Generation (EmareSetup, EmareHup, Emare Code)

### Generate Code
```bash
POST /v1/emare/code/generate
```

**Request:**
```json
{
  "request": "FastAPI ile user authentication endpoint'i yaz",
  "language": "python",
  "tech_stack": ["FastAPI", "JWT", "bcrypt"]
}
```

**Response:**
```json
{
  "code": "from fastapi import FastAPI, HTTPException\nfrom passlib.hash import bcrypt\n...",
  "language": "python"
}
```

### Code Review
```bash
POST /v1/emare/code/review
```

**Request:**
```json
{
  "code": "def login(user, pwd):\n    if user == 'admin' and pwd == '123':\n        return True",
  "language": "python"
}
```

**Response:**
```json
{
  "review": "Kod kalitesi: 3/10\n\nProblems:\n1. Hardcoded credentials (kritik güvenlik açığı)\n2. Plain text password\n3. Type hints yok\n\nÖneriler:\n- Database'den kullanıcı çek\n- Password hash kullan (bcrypt)\n- Type hints ekle",
  "language": "python"
}
```

### Explain Code
```bash
POST /v1/emare/code/explain?code=def fib(n): return n if n <= 1 else fib(n-1) + fib(n-2)&language=python
```

**Response:**
```json
{
  "explanation": "Bu fonksiyon Fibonacci sayılarını hesaplıyor.\n\nNasıl çalışır:\n- Eğer sayı 0 veya 1 ise, direkt döner\n- Değilse kendini 2 kez çağırır (recursive)\n\nÖrnek: fib(5) = 5 (0,1,1,2,3,5)"
}
```

---

## 🍽️ Emare POS

### Menu Suggestions
```bash
POST /v1/emare/pos/menu-suggestion
```

**Request:**
```json
{
  "order_history": {
    "most_ordered": ["burger", "pizza", "salad"],
    "trending": "vegan"
  },
  "season": "summer",
  "budget": "medium"
}
```

**Response:**
```json
{
  "suggestions": "Yeni menü önerileri:\n1. Vegan Burger - 85 TL\n2. Yaz Salatası - 65 TL\n3. Smoothie Bowl - 75 TL"
}
```

### Order Prediction
```bash
POST /v1/emare/pos/order-prediction
```

**Request:**
```json
{
  "historical_data": {
    "avg_daily_orders": 50,
    "peak_hours": [12, 19]
  },
  "special_days": ["cuma", "cumartesi"]
}
```

**Response:**
```json
{
  "prediction": "Gelecek hafta tahmini:\n- Ortalama 55 sipariş/gün\n- Cuma-Cumartesi: 70 sipariş\n- Stok önerisi: 2x burger, 1.5x pizza"
}
```

---

## ☁️ EmareCloud

### Server Health Analysis
```bash
POST /v1/emare/cloud/server-health
```

**Request:**
```json
{
  "metrics": {
    "cpu": 85,
    "memory": 70,
    "disk": 90,
    "uptime": "15 days"
  },
  "server_name": "prod-web-01"
}
```

**Response:**
```json
{
  "health_report": "Sunucu Durumu: ⚠️ Dikkat\n\nSağlık skoru: 6/10\n\nSorunlar:\n- CPU kullanımı yüksek (%85)\n- Disk dolmak üzere (%90)\n\nÖneriler:\n1. Disk temizliği yap\n2. CPU yoğunluğunu incele\n3. Auto-scaling aktif et",
  "server": "prod-web-01"
}
```

---

## 📢 Emare Ads

### Page Content Analysis
```bash
POST /v1/emare/ads/page-analysis
```

**Request:**
```json
{
  "page_content": "<html><head><title>Python Tutorial</title>...</html>",
  "url": "https://example.com/python-tutorial"
}
```

**Response:**
```json
{
  "analysis": "Sayfa Analizi:\n\nAna konu: Python programlama eğitimi\nAnahtar kelimeler: python, tutorial, programming\nSEO skoru: 7/10\n\nÖneriler:\n- Meta description ekle\n- H1 eksik\n- İç link sayısı az",
  "url": "https://example.com/python-tutorial"
}
```

---

## 🌐 Generic Endpoints (Tüm Projeler)

### Translation
```bash
POST /v1/emare/translate
```

**Request:**
```json
{
  "text": "Hello, how are you?",
  "source_lang": "en",
  "target_lang": "tr"
}
```

**Response:**
```json
{
  "original": "Hello, how are you?",
  "translated": "Merhaba, nasılsın?",
  "source_lang": "en",
  "target_lang": "tr"
}
```

### Generic Project Task
```bash
POST /v1/emare/project/task
```

**Request:**
```json
{
  "project": "asistan",
  "task": "whatsapp_reply",
  "data": {
    "question": "Siparişim nerede?",
    "company_context": "E-ticaret"
  },
  "model": "llama3.1:8b",
  "temperature": 0.7,
  "max_tokens": 200
}
```

**Response:**
```json
{
  "project": "asistan",
  "task": "whatsapp_reply",
  "result": "Merhaba! 😊 Siparişiniz kargoda...",
  "metadata": {...},
  "model_used": "llama3.1:8b",
  "tokens_used": 45
}
```

---

## 📊 Endpoint Özeti

| Proje | Endpoint Sayısı | Use Case |
|-------|----------------|----------|
| **Emare Asistan** | 2 | WhatsApp replies, sentiment |
| **Emare Finance** | 2 | Invoice summary, advice |
| **Emare Makale** | 2 | Blog generation, improvement |
| **SiberEmare** | 2 | Vuln explain, pentest report |
| **Emare Log** | 2 | Anomaly detection, summary |
| **Code** | 3 | Generate, review, explain |
| **Emare POS** | 2 | Menu suggestions, predictions |
| **EmareCloud** | 1 | Server health analysis |
| **Emare Ads** | 1 | Page analysis |
| **Generic** | 2 | Translation, generic task |

**Toplam:** 19 özel endpoint + OpenAI-compatible endpoints

---

## 🚀 Kullanım Örnekleri

### Python İstemcisi
```python
import httpx

API_URL = "http://localhost:8888"

# Emare Asistan - WhatsApp reply
response = httpx.post(f"{API_URL}/v1/emare/asistan/whatsapp-reply", json={
    "question": "Ürün ne zaman gelir?",
    "company_context": "2-3 gün teslimat"
})
print(response.json()["reply"])

# Emare Finance - Invoice summary
response = httpx.post(f"{API_URL}/v1/emare/finance/invoice-summary", json={
    "invoice_data": {"invoice_no": "2024-001", "total": 15000}
})
print(response.json()["summary"])

# Code generation
response = httpx.post(f"{API_URL}/v1/emare/code/generate", json={
    "request": "FastAPI CRUD endpoint yaz",
    "language": "python",
    "tech_stack": ["FastAPI", "SQLAlchemy"]
})
print(response.json()["code"])
```

### cURL Örnekleri
```bash
# WhatsApp reply
curl -X POST http://localhost:8888/v1/emare/asistan/whatsapp-reply \
  -H "Content-Type: application/json" \
  -d '{"question": "Siparişim nerede?", "company_context": "E-ticaret"}'

# Blog post generation
curl -X POST http://localhost:8888/v1/emare/makale/blog-post \
  -H "Content-Type: application/json" \
  -d '{"topic": "Python", "keywords": ["python", "tutorial"], "word_count": 500}'

# Log analysis
curl -X POST http://localhost:8888/v1/emare/log/analyze \
  -H "Content-Type: application/json" \
  -d '{"logs": ["error 1", "error 2"], "time_range": "1h"}'
```

---

## 🔧 Configuration

Tüm endpoint'ler `.env` dosyasındaki ayarları kullanır:

```bash
# Default model for all endpoints
DEFAULT_MODEL=llama3.1:8b

# Temperature settings (override per request)
DEFAULT_TEMPERATURE=0.7

# Max tokens (override per request)  
DEFAULT_MAX_TOKENS=1024
```

---

## 📈 Performance

| Endpoint Type | Avg Response Time | Model |
|--------------|-------------------|-------|
| WhatsApp reply | ~2-3s | llama3.1:8b |
| Code generation | ~5-8s | llama3.1:8b |
| Blog post | ~10-15s | llama3.1:8b |
| Simple analysis | ~1-2s | llama3.1:8b |

**Not:** Response time, modele ve prompt uzunluğuna göre değişir.

---

## 🎯 Best Practices

1. **Model Seçimi:** Basit görevler için 8B model, karmaşık için 70B kullan
2. **Temperature:** Code için 0.3, creative için 0.8
3. **Max Tokens:** Response uzunluğunu kontrol etmek için ayarla
4. **Error Handling:** Her zaman try-catch kullan
5. **Rate Limiting:** Production'da rate limit koy (settings.MAX_CONCURRENT_REQUESTS)

---

## 📞 Support

**API Documentation:** http://localhost:8888/docs  
**Emare Hub:** http://127.0.0.1:5555  
**GitHub:** `/Users/emre/Desktop/Emare/emareai`

---

**🌟 Emare AI v1.1.0 - 21 proje için özelleştirilmiş AI servisleri!**
