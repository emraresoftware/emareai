"""
Pydantic models for API requests and responses
OpenAI-compatible schemas
"""
from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class Role(str, Enum):
    """Message role"""
    system = "system"
    user = "user"
    assistant = "assistant"


class ChatMessage(BaseModel):
    """Chat message"""
    role: Role
    content: str


class ChatCompletionRequest(BaseModel):
    """OpenAI-compatible chat completion request"""
    model: str = Field(default="llama3.1:8b", description="Model to use")
    messages: List[ChatMessage]
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=1024, ge=1, le=32000)
    top_p: Optional[float] = Field(default=1.0, ge=0, le=1)
    stream: Optional[bool] = Field(default=False)
    stop: Optional[Union[str, List[str]]] = None


class ChatCompletionChoice(BaseModel):
    """A single completion choice"""
    index: int
    message: ChatMessage
    finish_reason: str


class Usage(BaseModel):
    """Token usage statistics"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    """OpenAI-compatible chat completion response"""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Usage


class EmbeddingRequest(BaseModel):
    """Embedding request"""
    model: str = Field(default="all-minilm", description="Embedding model")
    input: Union[str, List[str]]


class EmbeddingData(BaseModel):
    """Single embedding"""
    object: str = "embedding"
    embedding: List[float]
    index: int


class EmbeddingResponse(BaseModel):
    """Embedding response"""
    object: str = "list"
    data: List[EmbeddingData]
    model: str
    usage: Usage


class ModelInfo(BaseModel):
    """Model information"""
    id: str
    object: str = "model"
    created: int
    owned_by: str = "emare"


class ModelListResponse(BaseModel):
    """List of available models"""
    object: str = "list"
    data: List[ModelInfo]


class EmareAnalyzeRequest(BaseModel):
    """Emare-specific analysis request"""
    text: str
    analysis_type: str = Field(
        default="general",
        description="Type: general, sentiment, entity, summary"
    )
    language: str = Field(default="tr", description="Language: tr or en")


class EmareAnalyzeResponse(BaseModel):
    """Emare analysis response"""
    analysis_type: str
    result: Dict[str, Any]
    language: str
    model_used: str


# Project-specific models

class ProjectTaskRequest(BaseModel):
    """Generic project task request"""
    project: str = Field(description="Project name (asistan, finance, makale, etc.)")
    task: str = Field(description="Task type specific to project")
    data: Dict[str, Any] = Field(description="Task-specific data")
    model: str = Field(default="llama3.1:8b", description="Model to use")
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=1024, ge=1, le=8000)


class ProjectTaskResponse(BaseModel):
    """Generic project task response"""
    project: str
    task: str
    result: str
    metadata: Dict[str, Any]
    model_used: str
    tokens_used: int


# Emare Asistan specific
class WhatsAppReplyRequest(BaseModel):
    """WhatsApp customer reply request"""
    question: str
    company_context: Optional[str] = ""
    customer_name: Optional[str] = None


class SentimentAnalysisResponse(BaseModel):
    """Sentiment analysis response"""
    sentiment: str
    score: float
    explanation: str


# Emare Finance specific  
class InvoiceSummaryRequest(BaseModel):
    """Invoice summary request"""
    invoice_data: Dict[str, Any]


class FinancialAdviceRequest(BaseModel):
    """Financial advice request"""
    financial_data: Dict[str, Any]
    period: str = "monthly"


# Emare Makale specific
class BlogPostRequest(BaseModel):
    """Blog post generation request"""
    topic: str
    keywords: List[str] = []
    word_count: int = 500
    tone: str = "professional"


class ContentImproveRequest(BaseModel):
    """Content improvement request"""
    original_text: str
    focus: str = "all"  # seo, readability, grammar


# SiberEmare specific
class VulnerabilityExplainRequest(BaseModel):
    """Vulnerability explanation request"""
    vulnerability: str
    technical_info: str


class PentestReportRequest(BaseModel):
    """Pentest report generation request"""
    findings: List[Dict[str, Any]]
    target: str


# Emare Log specific
class LogAnalysisRequest(BaseModel):
    """Log analysis request"""
    logs: List[str]
    normal_pattern: Optional[str] = None
    time_range: str


# Code generation specific
class CodeGenerationRequest(BaseModel):
    """Code generation request"""
    request: str
    language: str = "python"
    tech_stack: List[str] = []


class CodeReviewRequest(BaseModel):
    """Code review request"""
    code: str
    language: str = "python"


# Translation
class TranslationRequest(BaseModel):
    """Translation request"""
    text: str
    source_lang: str = "tr"
    target_lang: str = "en"
