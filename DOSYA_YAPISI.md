# 📁 Emare AI — Dosya Yapısı

> **Oluşturulma:** Otomatik  
> **Amaç:** Yapay zekalar kod yazmadan önce mevcut dosya yapısını incelemeli

---

## Proje Dosya Ağacı

```
/Users/emre/Desktop/Emare/emareai
├── .env
├── .env.example
├── .gitignore
├── .vscode
│   └── settings.json
├── DOSYA_YAPISI.md
├── Dockerfile
├── EMARE_ORTAK_CALISMA -> /Users/emre/Desktop/Emare/EMARE_ORTAK_CALISMA
├── README.md
├── __init__.py
├── api
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   └── models.py
├── docker-compose.yml
├── emareai_hafiza.md
├── examples
│   ├── openai_example.py
│   └── test_api.py
├── inference
│   ├── __init__.py
│   └── ollama_wrapper.py
├── logs
│   └── .gitkeep
├── pyrightconfig.json
├── requirements.txt
├── setup_ollama.sh
├── start.sh
└── test.sh

7 directories, 24 files

```

---

## 📌 Kullanım Talimatları (AI İçin)

Bu dosya, kod üretmeden önce projenin mevcut yapısını kontrol etmek içindir:

1. **Yeni dosya oluşturmadan önce:** Bu ağaçta benzer bir dosya var mı kontrol et
2. **Yeni klasör oluşturmadan önce:** Mevcut klasör yapısına uygun mu kontrol et
3. **Import/require yapmadan önce:** Dosya yolu doğru mu kontrol et
4. **Kod kopyalamadan önce:** Aynı fonksiyon başka dosyada var mı kontrol et

**Örnek:**
- ❌ "Yeni bir auth.py oluşturalım" → ✅ Kontrol et, zaten `app/auth.py` var mı?
- ❌ "config/ klasörü oluşturalım" → ✅ Kontrol et, zaten `config/` var mı?
- ❌ `from utils import helper` → ✅ Kontrol et, `utils/helper.py` gerçekten var mı?

---

**Not:** Bu dosya otomatik oluşturulmuştur. Proje yapısı değiştikçe güncellenmelidir.

```bash
# Güncelleme komutu
python3 /Users/emre/Desktop/Emare/create_dosya_yapisi.py
```
