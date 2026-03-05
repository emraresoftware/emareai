# 🤖 Emare AI v1.1.0

**Emare ekosistemi için özel yapay zeka motoru**

OpenAI-compatible API ile kendi sunucunuzda LLM inference.

---

## 🎯 Özellikler

- ✅ **OpenAI-compatible API** - Drop-in replacement
- 🔐 **Privacy-first** - Tüm data kendi sunucunuzda
- ⚡ **Fast** - Ollama ile optimize edilmiş inference
- 🌐 **Multi-language** - Türkçe ve İngilizce desteği
- 🔌 **Easy integration** - RESTful API
- 📊 **Custom endpoints** - Emare-specific analysis
- 🎨 **21 Proje Desteği** - Her proje için özelleştirilmiş endpoint'ler
- 💡 **Smart Prompts** - Proje bazlı optimize edilmiş promptlar

## 📋 Gereksinimler

- Python 3.11+
- [Ollama](https://ollama.ai/) (LLM inference engine)
- 8GB+ RAM (model boyutuna göre)

## 🚀 Hızlı Başlangıç

### 1. Ollama Kurulumu

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Ollama'yı başlat
ollama serve
```

### 2. Model İndirme

```bash
# LLaMA 3.1 8B (önerilen)
ollama pull llama3.1:8b

# Veya diğer modeller
ollama pull mistral:7b
ollama pull qwen2.5:7b
ollama pull gemma2:9b
```

### 3. Emare AI Kurulumu

```bash
# Repoyu klonla (zaten klonlandı)
cd /Users/emre/Desktop/Emare/emareai

# Virtual environment oluştur
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyasını oluştur
cp .env.example .env
```

### 4. Başlat

```bash
# Kolayca başlat
chmod +x start.sh
./start.sh

# Veya manuel
uvicorn api.main:app --host 0.0.0.0 --port 8888 --reload
```

## 📡 API Kullanımı

### Chat Completion (OpenAI-compatible)

```bash
curl -X POST http://localhost:8888/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "messages": [
      {"role": "system", "content": "Sen yardımcı bir asistansın."},
      {"role": "user", "content": "Merhaba! Kendini tanıt."}
    ],
    "temperature": 0.7,
    "max_tokens": 1024
  }'
```

### Python İstemcisi

```python
import httpx

API_URL = "http://localhost:8888/v1/chat/completions"

response = httpx.post(API_URL, json={
    "model": "llama3.1:8b",
    "messages": [
        {"role": "user", "content": "Python nedir?"}
    ]
})

result = response.json()
print(result["choices"][0]["message"]["content"])
```

### OpenAI Kütüphanesi İle

```python
from openai import OpenAI

# Emare AI'yi OpenAI client ile kullan
client = OpenAI(
    base_url="http://localhost:8888/v1",
    api_key="not-needed"  # API key zorunlu değil
)

response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

## 🎨 Endpoints

### OpenAI-Compatible

- `GET /v1/models` - Mevcut modelleri listele
- `POST /v1/chat/completions` - Chat completion
- `POST /v1/embeddings` - Text embeddings

### 🆕 Project-Specific Endpoints (v1.1.0)

**21 Emare projesi için özelleştirilmiş endpoint'ler!**

#### Emare Asistan 🤖
- `POST /v1/emare/asistan/whatsapp-reply` - WhatsApp cevap üretimi
- `POST /v1/emare/asistan/sentiment` - Müşteri duygu analizi

#### Emare Finance 💰
- `POST /v1/emare/finance/invoice-summary` - Fatura özeti
- `POST /v1/emare/finance/advice` - Finansal tavsiye

#### Emare Makale 📝
- `POST /v1/emare/makale/blog-post` - Blog yazısı üretimi
- `POST /v1/emare/makale/improve` - İçerik iyileştirme

#### SiberEmare 🛡️
- `POST /v1/emare/siber/vulnerability-explain` - Güvenlik açığı açıklama
- `POST /v1/emare/siber/pentest-report` - Pentest raporu

#### Emare Log 📡
- `POST /v1/emare/log/analyze` - Log anomali tespiti
- `POST /v1/emare/log/summary` - Log özeti

#### Code Generation 💻
- `POST /v1/emare/code/generate` - Kod üretimi
- `POST /v1/emare/code/review` - Kod inceleme
- `POST /v1/emare/code/explain` - Kod açıklama

#### Emare POS 🍽️
- `POST /v1/emare/pos/menu-suggestion` - Menü önerileri
- `POST /v1/emare/pos/order-prediction` - Sipariş tahmini

#### EmareCloud ☁️
- `POST /v1/emare/cloud/server-health` - Sunucu sağlık analizi

#### Emare Ads 📢
- `POST /v1/emare/ads/page-analysis` - Sayfa içeriği analizi

#### Generic 🌐
- `POST /v1/emare/translate` - Çeviri (TR↔EN)
- `POST /v1/emare/project/task` - Generic proje görevi

**📖 Detaylı Dokümantasyon:** [`PROJECT_ENDPOINTS.md`](PROJECT_ENDPOINTS.md)

### Emare-Specific (Legacy)

- `POST /v1/emare/analyze` - Text analizi
  - `sentiment` - Duygu analizi
  - `entity` - Varlık tanıma
  - `summary` - Özet çıkarma
  - `general` - Genel analiz

### Monitoring

- `GET /` - API bilgisi
- `GET /health` - Health check
- `GET /docs` - Swagger UI (tüm endpoint'leri göster)
- `GET /redoc` - ReDoc UI

## 🔧 Konfigürasyon

`.env` dosyasını düzenleyin:

```bash
# API ayarları
API_PORT=8888
DEBUG=False

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama3.1:8b

# Performans
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=300
```

## 📦 Proje Yapısı

```
emareai/
├── api/
│   ├── __init__.py
│   ├── main.py           # FastAPI server
│   ├── models.py         # Pydantic models
│   └── config.py         # Configuration
├── inference/
│   ├── __init__.py
│   └── ollama_wrapper.py # Ollama integration
├── logs/                 # Log files
├── requirements.txt
├── .env.example
├── .gitignore
├── start.sh             # Start script
└── README.md

# Planlanan (v2+)
├── models/              # Custom model weights
├── training/            # Training scripts
└── evaluation/          # Benchmarks
```

## 🧪 Test

```bash
# Health check
curl http://localhost:8888/health

# List models
curl http://localhost:8888/v1/models

# Chat test
curl -X POST http://localhost:8888/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "messages": [{"role": "user", "content": "Merhaba"}]
  }'

# 🆕 Project-specific tests

# WhatsApp reply (Emare Asistan)
curl -X POST http://localhost:8888/v1/emare/asistan/whatsapp-reply \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Siparişim nerede?",
    "company_context": "E-ticaret, 2-3 gün teslimat"
  }'

# Code generation (EmareSetup/EmareHup/Emare Code)
curl -X POST http://localhost:8888/v1/emare/code/generate \
  -H "Content-Type: application/json" \
  -d '{
    "request": "FastAPI ile user endpoint yaz",
    "language": "python",
    "tech_stack": ["FastAPI", "SQLAlchemy"]
  }'

# Blog post (Emare Makale)
curl -X POST http://localhost:8888/v1/emare/makale/blog-post \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Python ile AI",
    "keywords": ["python", "AI", "machine learning"],
    "word_count": 500
  }'

# Translation
curl -X POST http://localhost:8888/v1/emare/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "source_lang": "en",
    "target_lang": "tr"
  }'
```

**📝 Daha fazla örnek:** [`examples/test_api.py`](examples/test_api.py) veya [`PROJECT_ENDPOINTS.md`](PROJECT_ENDPOINTS.md)
  }'
```

## 🚀 Production Deploy

### Docker (Yakında)

```bash
docker build -t emareai:v1 .
docker run -p 8888:8888 emareai:v1
```

### Systemd Service

```bash
# /etc/systemd/system/emareai.service
[Unit]
Description=Emare AI Service
After=network.target

[Service]
Type=simple
User=emre
WorkingDirectory=/Users/emre/Desktop/Emare/emareai
ExecStart=/Users/emre/Desktop/Emare/emareai/venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8888
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🔗 Emare Ekosistem Entegrasyonu

### Emare Asistan (WhatsApp AI Platform)

```python
# WhatsApp otomatik cevap
import httpx

async def reply_whatsapp(question: str, company: str):
    response = await httpx.post(
        "http://localhost:8888/v1/emare/asistan/whatsapp-reply",
        json={
            "question": question,
            "company_context": company
        }
    )
    return response.json()["reply"]

# Müşteri duygu analizi
async def analyze_customer(message: str):
    response = await httpx.post(
        f"http://localhost:8888/v1/emare/asistan/sentiment?text={message}"
    )
    return response.json()
```

### Emare Finance (POS + İşletme Yönetimi)

```php
// Laravel'den Emare AI kullan - Fatura özeti
$response = Http::post('http://localhost:8888/v1/emare/finance/invoice-summary', [
    'invoice_data' => [
        'invoice_no' => '2024-001',
        'customer' => 'ABC Ltd',
        'total' => 15000
    ]
]);

$summary = $response->json()['summary'];

// Finansal tavsiye al
$response = Http::post('http://localhost:8888/v1/emare/finance/advice', [
    'financial_data' => [
        'revenue' => 100000,
        'expenses' => 75000
    ],
    'period' => 'monthly'
]);
```

### Emare Makale (İçerik Üretimi)

```python
# Blog yazısı üret
import httpx

response = httpx.post(
    "http://localhost:8888/v1/emare/makale/blog-post",
    json={
        "topic": "Python ile Web Scraping",
        "keywords": ["python", "beautifulsoup", "scraping"],
        "word_count": 500
    }
)

blog_post = response.json()["content"]
```

### EmareSetup / EmareHup / Emare Code (Kod Üretimi)

```python
# Kod üret
response = httpx.post(
    "http://localhost:8888/v1/emare/code/generate",
    json={
        "request": "FastAPI ile CRUD endpoint yaz",
        "language": "python",
        "tech_stack": ["FastAPI", "SQLAlchemy"]
    }
)

generated_code = response.json()["code"]

# Kod incele
response = httpx.post(
    "http://localhost:8888/v1/emare/code/review",
    json={
        "code": my_code,
        "language": "python"
    }
)

review = response.json()["review"]
```

### SiberEmare (Pentest)

```python
# Güvenlik açığını açıkla
response = httpx.post(
    "http://localhost:8888/v1/emare/siber/vulnerability-explain",
    json={
        "vulnerability": "SQL Injection",
        "technical_info": "User input not sanitized"
    }
)

# Pentest raporu üret
response = httpx.post(
    "http://localhost:8888/v1/emare/siber/pentest-report",
    json={
        "findings": [{"type": "SQL Injection", "severity": "critical"}],
        "target": "example.com"
    }
)
```

### Emare Log (Log Yönetimi)

```python
# Log analizi - anomali tespiti
response = httpx.post(
    "http://localhost:8888/v1/emare/log/analyze",
    json={
        "logs": log_lines,
        "time_range": "24h"
    }
)

analysis = response.json()["analysis"]
```

## 📊 Model Karşılaştırması

| Model | Boyut | RAM | Hız | Türkçe | Use Case |
|-------|-------|-----|-----|--------|----------|
| llama3.1:8b | 4.7GB | 8GB | ⚡⚡⚡ | ⭐⭐⭐ | Genel (önerilen) |
| mistral:7b | 4.1GB | 8GB | ⚡⚡⚡ | ⭐⭐ | Kod, teknik |
| qwen2.5:7b | 4.7GB | 8GB | ⚡⚡ | ⭐⭐⭐⭐ | Türkçe ağırlıklı |
| gemma2:9b | 5.4GB | 16GB | ⚡⚡ | ⭐⭐⭐ | Balanced |

## 🗺️ Roadmap

### v1.0 ✅ (Tamamlandı)
- OpenAI-compatible API
- Ollama integration
- Basic endpoints
- Health monitoring

### v1.1 ✅ (Tamamlandı - Mevcut Versiyon)
- **21 Proje Özelleştirilmiş AI Endpoint'leri**
- Project-specific prompt templates
- Specialized models for each use case
- Comprehensive API documentation

### v1.2 (Planlanan)
- Streaming support
- Rate limiting
- API key authentication
- Request caching

### v2.0 (Gelecek)
- Fine-tuned models
- RAG (Retrieval-Augmented Generation)
- Vector database (ChromaDB)
- Custom training pipeline

### v3.0 (Vizyon)
- Custom LLM (from scratch)
- Distributed inference
- Model quantization
- Mobile deployment

## 📝 Lisans

**Proprietary** - Emare ekosistemi için geliştirilmiştir.

## 🤝 Katkı

Bu proje Emare ekosisteminin bir parçasıdır. 

**Geliştirici:** Emre  
**İletişim:** Emare Hub üzerinden

---

## 🔗 İlgili Projeler

- [Emare Asistan](../emareasistan) - Multi-tenant AI platform
- [EmareSetup](../emaresetup) - AI-powered project generator
- [EmareHup](../EmareHup) - AI developer team (DevM)

---

**🌟 Emare AI - Kendi yapay zekanız, sizin kontrolünüzde!**
