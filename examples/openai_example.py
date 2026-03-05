"""
OpenAI Python SDK ile Emare AI kullanımı
"""
from openai import OpenAI

# Emare AI'yi OpenAI client olarak kullan
client = OpenAI(
    base_url="http://localhost:8888/v1",
    api_key="not-needed"  # Emare AI API key gerektirmiyor (şimdilik)
)


def chat_example():
    """Basit chat örneği"""
    print("💬 Chat Example\n")
    
    response = client.chat.completions.create(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": "Sen Türkçe konuşan yardımcı bir asistansın."},
            {"role": "user", "content": "Python'da liste comprehension nedir? Kısa açıkla."}
        ],
        temperature=0.7,
        max_tokens=200
    )
    
    print(response.choices[0].message.content)
    print(f"\nTokens used: {response.usage.total_tokens}")


def multi_turn_conversation():
    """Çoklu mesajlaşma"""
    print("\n🔄 Multi-turn Conversation\n")
    
    messages = [
        {"role": "system", "content": "Sen bir Python programlama uzmanısın."},
        {"role": "user", "content": "Merhaba! Python'da decorator nedir?"},
    ]
    
    # İlk yanıt
    response = client.chat.completions.create(
        model="llama3.1:8b",
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )
    
    assistant_msg = response.choices[0].message.content
    print(f"🤖 Assistant: {assistant_msg}\n")
    
    # Konuşmaya devam et
    messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({"role": "user", "content": "Bir örnek verebilir misin?"})
    
    response = client.chat.completions.create(
        model="llama3.1:8b",
        messages=messages,
        temperature=0.7,
        max_tokens=200
    )
    
    print(f"🤖 Assistant: {response.choices[0].message.content}")


def code_generation():
    """Kod üretimi örneği"""
    print("\n💻 Code Generation\n")
    
    response = client.chat.completions.create(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": "Sen bir Python kod asistanısın. Sadece kod yaz, açıklama yapma."},
            {"role": "user", "content": "Python'da bir dosyadaki satırları ters çeviren fonksiyon yaz"}
        ],
        temperature=0.3,
        max_tokens=300
    )
    
    print(response.choices[0].message.content)


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Emare AI with OpenAI SDK")
    print("=" * 60)
    
    try:
        chat_example()
        multi_turn_conversation()
        code_generation()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Emare AI is running:")
        print("  ./start.sh")
