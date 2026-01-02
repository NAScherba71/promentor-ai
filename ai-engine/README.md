# CodeMentor AI - Intelligent Programming Learning Platform

## Python AI Engine for Personalized Learning

This microservice powers the intelligent features of CodeMentor AI, including:
- Adaptive challenge generation
- Personalized learning path recommendations
- Code analysis and feedback
- AI-powered tutoring system

### Features

- **Adaptive Challenge Generation**: Creates personalized coding challenges based on user skill level
- **Code Analysis**: Analyzes student code for patterns, errors, and improvements
- **Learning Path Optimization**: Recommends optimal learning sequences
- **Natural Language Processing**: Powers conversational AI tutors
- **Multi-Provider LLM Support**: Choose between Local models, Google Vertex AI, or OpenRouter

### LLM Provider Architecture

**Strategy Pattern Implementation** - The engine now supports multiple LLM providers through a unified interface:

- **Local Models** (Default): TinyLlama-1.1B-Chat + CodeT5-Small - Free, runs locally
- **Google Vertex AI**: Gemini 1.5 Pro - High quality, production-grade
- **OpenRouter**: Access to multiple external LLMs via single API

### Requirements

- Python 3.9+
- PyTorch 2.x
- Transformers (Hugging Face)
- Redis (for caching)
- Google Cloud SDK (for Vertex AI provider)
- ~4GB disk space for local model cache

### Installation

```bash
cd ai-engine
pip install -r requirements.txt
```

### Model Setup (Local Provider Only)

Download and cache the required models (first time only):

```bash
python init_models.py
```

This will download:
- TinyLlama-1.1B-Chat model (~2.2GB)
- CodeT5-Small model (~500MB)

Models are cached locally and only need to be downloaded once.

### Configuration

Create a `.env` file:

#### Option 1: Local Models (Default)
```bash
LLM_PROVIDER=local
REDIS_URL=redis://localhost:6379
MODEL_CACHE_DIR=/path/to/model/cache  # Optional
```

#### Option 2: Google Vertex AI (Gemini)
```bash
LLM_PROVIDER=vertex
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
VERTEX_MODEL_NAME=gemini-1.5-pro  # Optional, this is default
REDIS_URL=redis://localhost:6379
```

**Authentication**: Vertex AI uses Application Default Credentials (ADC). Set up with:
```bash
gcloud auth application-default login
```

#### Option 3: OpenRouter
```bash
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxx
OPENROUTER_MODEL_NAME=google/gemini-pro-1.5  # Optional
REDIS_URL=redis://localhost:6379
```

### Running the Service

```bash
python main.py
```

The AI engine will start on port 5000 and expose REST API endpoints for the main application.

### API Endpoints

All endpoints work identically regardless of the selected provider:

- `POST /ai-tutor/chat` - AI tutor conversational interface
- `POST /code/analyze` - Code analysis with AI insights
- `POST /challenges/generate` - Adaptive challenge generation
- `POST /learning-path/recommend` - Personalized learning paths
- `GET /health` - Health check

### Provider Selection

Set the `LLM_PROVIDER` environment variable to choose:

| Provider | Value | Use Case | Cost | Quality |
|----------|-------|----------|------|---------|
| Local Models | `local` | Development, offline | Free | Good |
| Vertex AI | `vertex` | Production | Pay-per-use | Excellent |
| OpenRouter | `openrouter` | Multi-model access | Pay-per-use | Variable |

### Performance

**Local Models**:
- Latency: ~1-3 seconds per request (CPU), <1 second (GPU)
- Memory: ~2-4GB RAM for model loading
- Cost: $0 per request

**Vertex AI**:
- Latency: ~500ms-2 seconds per request
- Memory: Minimal (~100MB)
- Cost: Variable per Google Cloud pricing

**OpenRouter**:
- Latency: ~1-3 seconds per request
- Memory: Minimal (~100MB)
- Cost: Variable per model selection

### GPU Support (Local Provider)

For faster local inference, use a GPU:

```bash
# Install CUDA-enabled PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

The engine automatically detects and uses GPU if available.

### Testing

Run integration tests to verify the installation:

```bash
python test_integration.py
```

All tests should pass before deploying to production.

### Architecture

See [MIGRATION.md](./MIGRATION.md) for detailed architecture documentation and migration guide.

### Provider Implementation

Each provider implements the `AIProvider` interface:

```python
class AIProvider(ABC):
    @abstractmethod
    def generate_chat_response(self, user_message: str, context: Dict, personality: str) -> Dict:
        pass

    @abstractmethod
    def analyze_code(self, code: str, language: str) -> Dict:
        pass
```

This ensures consistent behavior across all providers.