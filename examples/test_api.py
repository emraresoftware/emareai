"""
Emare AI - Örnek Kullanım Script'i
FastAPI'ye istek gönderen örnek client
"""
import httpx
import asyncio
import json


async def test_health():
    """Health check testi"""
    print("\n🔍 Health Check...")
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8888/health")
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))


async def test_list_models():
    """Modelleri listele"""
    print("\n📦 Listing Models...")
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8888/v1/models")
        data = response.json()
        print(f"Found {len(data['data'])} models:")
        for model in data['data']:
            print(f"  - {model['id']}")


async def test_chat():
    """Chat completion testi"""
    print("\n💬 Chat Completion Test...")
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "http://localhost:8888/v1/chat/completions",
            json={
                "model": "llama3.1:8b",
                "messages": [
                    {"role": "system", "content": "Sen yardımcı bir yapay zeka asistanısın."},
                    {"role": "user", "content": "Merhaba! Kendini kısaca tanıt."}
                ],
                "temperature": 0.7,
                "max_tokens": 200
            }
        )
        
        data = response.json()
        print(f"Model: {data['model']}")
        print(f"Response: {data['choices'][0]['message']['content']}")
        print(f"Tokens: {data['usage']['total_tokens']}")


async def test_emare_analyze():
    """Emare custom analysis testi"""
    print("\n🔬 Emare Analysis Test...")
    async with httpx.AsyncClient(timeout=60.0) as client:
        text = "Bugün hava çok güzel! Ancak biraz üzgünüm çünkü projem bitmedi. Ama çok mutluyum ki yeni bir şeyler öğreniyorum."
        
        response = await client.post(
            "http://localhost:8888/v1/emare/analyze",
            json={
                "text": text,
                "analysis_type": "sentiment",
                "language": "tr"
            }
        )
        
        data = response.json()
        print(f"Analysis Type: {data['analysis_type']}")
        print(f"Result: {data['result']['text']}")


async def test_turkish_conversation():
    """Türkçe konuşma testi"""
    print("\n🇹🇷 Turkish Conversation Test...")
    
    messages = [
        {"role": "system", "content": "Sen Türkçe konuşan bir yapay zeka asistanısın. Emare AI adlı yerel bir AI motorusun."},
        {"role": "user", "content": "Emare AI nedir? Neler yapabilirsin?"}
    ]
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "http://localhost:8888/v1/chat/completions",
            json={
                "model": "llama3.1:8b",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 300
            }
        )
        
        data = response.json()
        assistant_message = data['choices'][0]['message']['content']
        print(f"🤖 Emare AI: {assistant_message}")


async def main():
    """Tüm testleri çalıştır"""
    print("=" * 60)
    print("🤖 Emare AI v1.0.0 - Test Suite")
    print("=" * 60)
    
    try:
        await test_health()
        await test_list_models()
        await test_chat()
        await test_turkish_conversation()
        await test_emare_analyze()
        
        print("\n" + "=" * 60)
        print("✅ Tüm testler başarılı!")
        print("=" * 60)
        
    except httpx.ConnectError:
        print("\n❌ Hata: Emare AI'ye bağlanılamadı!")
        print("Sunucunun çalıştığından emin olun:")
        print("  ./start.sh")
    except Exception as e:
        print(f"\n❌ Hata: {e}")


if __name__ == "__main__":
    asyncio.run(main())
