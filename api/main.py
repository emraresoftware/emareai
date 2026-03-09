"""
Emare AI - FastAPI Server
OpenAI-compatible API for local LLM inference
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
import uuid
from typing import List, Dict, Any, Optional

from api.config import settings
from api.models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChoice,
    ChatMessage,
    Usage,
    EmbeddingRequest,
    EmbeddingResponse,
    EmbeddingData,
    ModelListResponse,
    ModelInfo,
    EmareAnalyzeRequest,
    EmareAnalyzeResponse,
    Role
)
from api.prompts import get_prompt
from inference.ollama_wrapper import OllamaWrapper

# Logging setup
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(

# === Emare Feedback ===
from feedback_router import router as feedback_router
app.include_router(feedback_router, prefix="/api/feedback", tags=["feedback"])
# ======================

    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Emare AI - Özel yapay zeka motoru. OpenAI-compatible API.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Ollama client
ollama = OllamaWrapper(
    base_url=settings.OLLAMA_BASE_URL,
    timeout=settings.OLLAMA_TIMEOUT
)


@app.on_event("startup")
async def startup_event():
    """Run on startup"""
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    logger.info(f"📡 Ollama URL: {settings.OLLAMA_BASE_URL}")
    
    # Health check Ollama
    health = await ollama.health_check()
    if health:
        logger.info("✅ Ollama connection successful")
        models = await ollama.list_models()
        logger.info(f"📦 Available models: {len(models)}")
        for model in models:
            logger.info(f"   - {model.get('name', 'unknown')}")
    else:
        logger.warning("⚠️  Ollama not reachable. Make sure Ollama is running!")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on shutdown"""
    logger.info("🛑 Shutting down Emare AI...")
    await ollama.close()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "chat": "/v1/chat/completions",
            "embeddings": "/v1/embeddings",
            "models": "/v1/models",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    ollama_healthy = await ollama.health_check()
    
    return {
        "status": "healthy" if ollama_healthy else "degraded",
        "ollama": "connected" if ollama_healthy else "disconnected",
        "timestamp": int(time.time())
    }


@app.get("/v1/models", response_model=ModelListResponse)
async def list_models():
    """
    List available models (OpenAI-compatible)
    """
    try:
        ollama_models = await ollama.list_models()
        
        models_data = []
        for idx, model in enumerate(ollama_models):
            model_info = ModelInfo(
                id=model.get("name", f"model-{idx}"),
                created=int(time.time()),
                owned_by="emare"
            )
            models_data.append(model_info)
        
        return ModelListResponse(
            object="list",
            data=models_data
        )
        
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list models: {str(e)}"
        )


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completion(request: ChatCompletionRequest):
    """
    Chat completion endpoint (OpenAI-compatible)
    
    Example:
    ```
    {
        "model": "llama3.1:8b",
        "messages": [
            {"role": "system", "content": "Sen yardımcı bir asistansın."},
            {"role": "user", "content": "Merhaba!"}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    ```
    """
    try:
        logger.info(f"Chat request: model={request.model}, messages={len(request.messages)}")
        
        # Convert messages to Ollama format
        ollama_messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in request.messages
        ]
        
        # Call Ollama
        start_time = time.time()
        response = await ollama.chat(
            model=request.model,
            messages=ollama_messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=request.stream
        )
        elapsed = time.time() - start_time
        
        # Parse Ollama response
        assistant_message = response.get("message", {})
        content = assistant_message.get("content", "")
        
        # Estimate tokens (rough approximation)
        prompt_tokens = sum(len(msg.content.split()) for msg in request.messages)
        completion_tokens = len(content.split())
        total_tokens = prompt_tokens + completion_tokens
        
        logger.info(f"✅ Response generated in {elapsed:.2f}s, {completion_tokens} tokens")
        
        # Build OpenAI-compatible response
        return ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4().hex[:8]}",
            created=int(time.time()),
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=ChatMessage(
                        role=Role.assistant,
                        content=content
                    ),
                    finish_reason="stop"
                )
            ],
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens
            )
        )
        
    except Exception as e:
        logger.error(f"Chat completion error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat completion failed: {str(e)}"
        )


@app.post("/v1/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(request: EmbeddingRequest):
    """
    Generate embeddings (OpenAI-compatible)
    """
    try:
        # Handle single string or list
        texts = [request.input] if isinstance(request.input, str) else request.input
        
        embeddings_data = []
        total_tokens = 0
        
        for idx, text in enumerate(texts):
            embedding = await ollama.embeddings(
                model=request.model,
                prompt=text
            )
            
            embeddings_data.append(
                EmbeddingData(
                    embedding=embedding,
                    index=idx
                )
            )
            total_tokens += len(text.split())
        
        return EmbeddingResponse(
            object="list",
            data=embeddings_data,
            model=request.model,
            usage=Usage(
                prompt_tokens=total_tokens,
                completion_tokens=0,
                total_tokens=total_tokens
            )
        )
        
    except Exception as e:
        logger.error(f"Embeddings error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Embeddings generation failed: {str(e)}"
        )


@app.post("/v1/emare/analyze", response_model=EmareAnalyzeResponse)
async def emare_analyze(request: EmareAnalyzeRequest):
    """
    Emare-specific text analysis
    
    Custom endpoint for domain-specific tasks:
    - general: Genel analiz
    - sentiment: Duygu analizi
    - entity: Varlık tanıma
    - summary: Özet çıkarma
    """
    try:
        # Build prompt based on analysis type
        prompts = {
            "sentiment": f"Bu metinde duygu analizi yap (pozitif/negatif/nötr): {request.text}",
            "entity": f"Bu metindeki önemli varlıkları (kişi, yer, kurum) tespit et: {request.text}",
            "summary": f"Bu metni özetle: {request.text}",
            "general": f"Bu metni analiz et: {request.text}"
        }
        
        prompt = prompts.get(request.analysis_type, prompts["general"])
        
        # Call model
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.3,
            max_tokens=512
        )
        
        result_text = response.get("response", "")
        
        return EmareAnalyzeResponse(
            analysis_type=request.analysis_type,
            result={
                "text": result_text,
                "original_length": len(request.text),
                "response_length": len(result_text)
            },
            language=request.language,
            model_used=settings.DEFAULT_MODEL
        )
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


# ============================================================================
# PROJECT-SPECIFIC ENDPOINTS
# ============================================================================

@app.post("/v1/emare/project/task", response_model=ProjectTaskResponse)
async def project_task(request: ProjectTaskRequest):
    """
    Generic project task endpoint
    Route to project-specific prompts and processing
    """
    try:
        from api.models import ProjectTaskRequest, ProjectTaskResponse
        
        # Get optimized prompt for project
        prompt = get_prompt(
            project=request.project,
            task=request.task,
            **request.data
        )
        
        # Call model
        response = await ollama.generate(
            model=request.model,
            prompt=prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        result_text = response.get("response", "")
        tokens = len(result_text.split())
        
        return ProjectTaskResponse(
            project=request.project,
            task=request.task,
            result=result_text,
            metadata=request.data,
            model_used=request.model,
            tokens_used=tokens
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Project task error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Task failed: {str(e)}"
        )


# EMARE ASISTAN ENDPOINTS
@app.post("/v1/emare/asistan/whatsapp-reply")
async def whatsapp_reply(request: WhatsAppReplyRequest):
    """Generate WhatsApp customer reply"""
    from api.models import WhatsAppReplyRequest
    
    try:
        prompt = get_prompt(
            project="asistan",
            task="whatsapp_reply",
            question=request.question,
            company_context=request.company_context or "Genel müşteri hizmetleri"
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.7,
            max_tokens=200
        )
        
        return {
            "reply": response.get("response", ""),
            "customer_name": request.customer_name
        }
    except Exception as e:
        raise HTTPException(500, f"WhatsApp reply failed: {str(e)}")


@app.post("/v1/emare/asistan/sentiment")
async def customer_sentiment(text: str):
    """Analyze customer message sentiment"""
    from api.models import SentimentAnalysisResponse
    
    try:
        prompt = get_prompt(
            project="asistan",
            task="customer_sentiment",
            message=text
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.3,
            max_tokens=150
        )
        
        # Parse JSON response (basic, should be improved)
        import json
        try:
            result = json.loads(response.get("response", "{}"))
        except:
            result = {"sentiment": "nötr", "score": 5, "explanation": "Analiz yapılamadı"}
        
        return SentimentAnalysisResponse(
            sentiment=result.get("sentiment", "nötr"),
            score=result.get("score", 5.0),
            explanation=result.get("explanation", "")
        )
    except Exception as e:
        raise HTTPException(500, f"Sentiment analysis failed: {str(e)}")


# EMARE FINANCE ENDPOINTS
@app.post("/v1/emare/finance/invoice-summary")
async def invoice_summary(request: InvoiceSummaryRequest):
    """Summarize invoice"""
    from api.models import InvoiceSummaryRequest
    
    try:
        prompt = get_prompt(
            project="finance",
            task="invoice_summary",
            invoice_data=str(request.invoice_data)
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.3,
            max_tokens=300
        )
        
        return {"summary": response.get("response", "")}
    except Exception as e:
        raise HTTPException(500, f"Invoice summary failed: {str(e)}")


@app.post("/v1/emare/finance/advice")
async def financial_advice(request: FinancialAdviceRequest):
    """Get financial advice"""
    from api.models import FinancialAdviceRequest
    
    try:
        prompt = get_prompt(
            project="finance",
            task="financial_advice",
            financial_data=str(request.financial_data)
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.5,
            max_tokens=500
        )
        
        return {"advice": response.get("response", "")}
    except Exception as e:
        raise HTTPException(500, f"Financial advice failed: {str(e)}")


# EMARE MAKALE ENDPOINTS
@app.post("/v1/emare/makale/blog-post")
async def generate_blog_post(request: BlogPostRequest):
    """Generate blog post"""
    from api.models import BlogPostRequest
    
    try:
        prompt = get_prompt(
            project="makale",
            task="blog_post",
            topic=request.topic,
            keywords=", ".join(request.keywords),
            word_count=request.word_count
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.8,
            max_tokens=request.word_count * 2
        )
        
        return {
            "title": request.topic,
            "content": response.get("response", ""),
            "word_count": len(response.get("response", "").split())
        }
    except Exception as e:
        raise HTTPException(500, f"Blog post generation failed: {str(e)}")


@app.post("/v1/emare/makale/improve")
async def improve_content(request: ContentImproveRequest):
    """Improve existing content"""
    from api.models import ContentImproveRequest
    
    try:
        prompt = get_prompt(
            project="makale",
            task="content_improve",
            original_text=request.original_text
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.5,
            max_tokens=len(request.original_text.split()) * 2
        )
        
        return {
            "original": request.original_text,
            "improved": response.get("response", "")
        }
    except Exception as e:
        raise HTTPException(500, f"Content improvement failed: {str(e)}")


# SIBEREMARE ENDPOINTS
@app.post("/v1/emare/siber/vulnerability-explain")
async def explain_vulnerability(request: VulnerabilityExplainRequest):
    """Explain security vulnerability in simple terms"""
    from api.models import VulnerabilityExplainRequest
    
    try:
        prompt = get_prompt(
            project="siber",
            task="vulnerability_explain",
            vulnerability=request.vulnerability,
            technical_info=request.technical_info
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.3,
            max_tokens=400
        )
        
        return {"explanation": response.get("response", "")}
    except Exception as e:
        raise HTTPException(500, f"Vulnerability explanation failed: {str(e)}")


@app.post("/v1/emare/siber/pentest-report")
async def generate_pentest_report(request: PentestReportRequest):
    """Generate professional pentest report"""
    from api.models import PentestReportRequest
    
    try:
        prompt = get_prompt(
            project="siber",
            task="pentest_report",
            findings=str(request.findings),
            target=request.target
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.4,
            max_tokens=2000
        )
        
        return {
            "report": response.get("response", ""),
            "target": request.target,
            "findings_count": len(request.findings)
        }
    except Exception as e:
        raise HTTPException(500, f"Pentest report generation failed: {str(e)}")


# EMARE LOG ENDPOINTS
@app.post("/v1/emare/log/analyze")
async def analyze_logs(request: LogAnalysisRequest):
    """Analyze logs for anomalies"""
    from api.models import LogAnalysisRequest
    
    try:
        prompt = get_prompt(
            project="log",
            task="log_anomaly",
            logs="\n".join(request.logs[:100]),  # Limit to 100 lines
            normal_pattern=request.normal_pattern or "Normal sistem aktivitesi"
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.3,
            max_tokens=600
        )
        
        return {
            "analysis": response.get("response", ""),
            "logs_analyzed": len(request.logs)
        }
    except Exception as e:
        raise HTTPException(500, f"Log analysis failed: {str(e)}")


@app.post("/v1/emare/log/summary")
async def summarize_logs(request: LogAnalysisRequest):
    """Summarize log data"""
    from api.models import LogAnalysisRequest
    
    try:
        prompt = get_prompt(
            project="log",
            task="log_summary",
            logs="\n".join(request.logs[:100]),
            time_range=request.time_range
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.3,
            max_tokens=400
        )
        
        return {
            "summary": response.get("response", ""),
            "time_range": request.time_range
        }
    except Exception as e:
        raise HTTPException(500, f"Log summary failed: {str(e)}")


# CODE GENERATION ENDPOINTS (EmareSetup, EmareHup, Emare Code)
@app.post("/v1/emare/code/generate")
async def generate_code(request: CodeGenerationRequest):
    """Generate code from description"""
    from api.models import CodeGenerationRequest
    
    try:
        prompt = get_prompt(
            project="code",
            task="generate_code",
            request=request.request,
            language=request.language,
            tech_stack=", ".join(request.tech_stack)
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.4,
            max_tokens=1500
        )
        
        return {
            "code": response.get("response", ""),
            "language": request.language
        }
    except Exception as e:
        raise HTTPException(500, f"Code generation failed: {str(e)}")


@app.post("/v1/emare/code/review")
async def review_code(request: CodeReviewRequest):
    """Review code and provide feedback"""
    from api.models import CodeReviewRequest
    
    try:
        prompt = get_prompt(
            project="code",
            task="code_review",
            code=request.code
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.3,
            max_tokens=800
        )
        
        return {
            "review": response.get("response", ""),
            "language": request.language
        }
    except Exception as e:
        raise HTTPException(500, f"Code review failed: {str(e)}")


@app.post("/v1/emare/code/explain")
async def explain_code(code: str, language: str = "python"):
    """Explain code in simple terms"""
    try:
        prompt = get_prompt(
            project="code",
            task="code_explain",
            code=code
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.3,
            max_tokens=500
        )
        
        return {"explanation": response.get("response", "")}
    except Exception as e:
        raise HTTPException(500, f"Code explanation failed: {str(e)}")


# TRANSLATION ENDPOINT (All projects)
@app.post("/v1/emare/translate")
async def translate_text(request: TranslationRequest):
    """Translate text between languages"""
    from api.models import TranslationRequest
    
    try:
        prompt = get_prompt(
            project="generic",
            task="translate",
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.3,
            max_tokens=len(request.text.split()) * 2
        )
        
        return {
            "original": request.text,
            "translated": response.get("response", ""),
            "source_lang": request.source_lang,
            "target_lang": request.target_lang
        }
    except Exception as e:
        raise HTTPException(500, f"Translation failed: {str(e)}")


# POS ENDPOINTS (Emare POS)
@app.post("/v1/emare/pos/menu-suggestion")
async def suggest_menu_items(order_history: Dict[str, Any], season: str = "spring", budget: str = "medium"):
    """Suggest new menu items based on order history"""
    try:
        prompt = get_prompt(
            project="pos",
            task="menu_suggestion",
            order_history=str(order_history),
            season=season,
            budget=budget
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.7,
            max_tokens=600
        )
        
        return {"suggestions": response.get("response", "")}
    except Exception as e:
        raise HTTPException(500, f"Menu suggestion failed: {str(e)}")


@app.post("/v1/emare/pos/order-prediction")
async def predict_orders(historical_data: Dict[str, Any], special_days: List[str] = []):
    """Predict future orders"""
    try:
        prompt = get_prompt(
            project="pos",
            task="order_prediction",
            historical_data=str(historical_data),
            special_days=", ".join(special_days)
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.4,
            max_tokens=500
        )
        
        return {"prediction": response.get("response", "")}
    except Exception as e:
        raise HTTPException(500, f"Order prediction failed: {str(e)}")


# CLOUD ENDPOINTS (EmareCloud)
@app.post("/v1/emare/cloud/server-health")
async def analyze_server_health(metrics: Dict[str, Any], server_name: str):
    """Analyze server health metrics"""
    try:
        prompt = get_prompt(
            project="cloud",
            task="server_health",
            metrics=str(metrics),
            server_name=server_name
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.3,
            max_tokens=400
        )
        
        return {
            "health_report": response.get("response", ""),
            "server": server_name
        }
    except Exception as e:
        raise HTTPException(500, f"Server health analysis failed: {str(e)}")


# ADS ENDPOINTS (Emare Ads)
@app.post("/v1/emare/ads/page-analysis")
async def analyze_page(page_content: str, url: str):
    """Analyze web page content"""
    try:
        prompt = get_prompt(
            project="ads",
            task="page_analysis",
            page_content=page_content[:2000],  # Limit content
            url=url
        )
        
        response = await ollama.generate(
            model=settings.DEFAULT_MODEL,
            prompt=prompt,
            temperature=0.4,
            max_tokens=500
        )
        
        return {
            "analysis": response.get("response", ""),
            "url": url
        }
    except Exception as e:
        raise HTTPException(500, f"Page analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
