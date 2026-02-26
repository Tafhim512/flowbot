# FlowBot - Universal AI Business Automation Platform

FlowBot is a **config-driven, multi-tenant AI automation backend** that serves any business by swapping configuration files and knowledge bases. No code changes required to add new businesses.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

### 3. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. Test the API

Visit the interactive API docs at `http://localhost:8000/docs`

---

## 📋 Onboarding a New Business

### Step 1: Create Business Configuration

Create a YAML file in `business_configs/`:

```yaml
# business_configs/my_business.yaml
business:
  name: "My Business"
  slug: "my_business"
  industry: "retail"

role: "receptionist"

personality:
  tone: "friendly"
  language: "English"
  greeting: "Hello! Welcome to My Business!"

rules:
  - "Be helpful and courteous"
  - "Always confirm details before proceeding"

services:
  - "Product Sales"
  - "Customer Support"

faqs:
  - question: "What are your hours?"
    answer: "We're open 9 AM to 5 PM, Monday to Friday."
```

### Step 2: Create Knowledge Base Files

Create a directory `knowledge_base/my_business/` with JSON files:

- `faqs.json` - Frequently asked questions
- `services.json` - List of services offered
- `pricing.json` - Pricing information

### Step 3: Register Business in Database

Make a POST request to create the business:

```bash
curl -X POST "http://localhost:8000/api/v1/businesses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Business",
    "slug": "my_business",
    "config_path": "business_configs/my_business.yaml"
  }'
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/messages` | POST | Send a message to the AI |
| `/api/v1/businesses` | GET | List all businesses |
| `/api/v1/businesses` | POST | Create a new business |
| `/api/v1/businesses/{id}` | GET | Get business details |
| `/api/v1/businesses/{id}` | DELETE | Delete a business |
| `/api/v1/leads` | GET | List all captured leads |
| `/api/v1/leads/{id}` | GET | Get lead details |
| `/docs` | GET | Interactive API documentation |

---

## 💬 Sending Messages

### Example: User Message

```bash
curl -X POST "http://localhost:8000/api/v1/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": "<business_id>",
    "session_id": "session-123",
    "text": "Hello, I have a question about your services"
  }'
```

### Response

```json
{
  "reply": "Hello! Welcome to City Health Clinic. I'd be happy to tell you about our services...",
  "intent": "question",
  "actions_taken": ["send_reply"],
  "session_id": "session-123"
}
```

---

## 🏢 Demo Businesses

The platform includes two pre-configured demo businesses:

1. **demo_clinic** - City Health Clinic (healthcare/receptionist)
2. **demo_restaurant** - The Gourmet Kitchen (restaurant/host)

To use a demo business, register it:

```bash
curl -X POST "http://localhost:8000/api/v1/businesses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "City Health Clinic",
    "slug": "demo_clinic",
    "config_path": "business_configs/demo_clinic.yaml"
  }'
```

---

## 🧠 How It Works

```
User Message → Message Intake API
                    ↓
            Load Business Config
                    ↓
            Knowledge Retrieval (FAQs, Services, Pricing)
                    ↓
            Intent Classification (question, lead, booking, support)
                    ↓
            Build Dynamic System Prompt
                    ↓
            Call LLM (OpenAI GPT)
                    ↓
            Execute Actions (reply, create lead, etc.)
                    ↓
            Save Conversation to Database
                    ↓
            Return Response
```

### Core Modules

| Module | Purpose |
|--------|---------|
| `app/core/brain.py` | AI Brain - LLM integration + memory |
| `app/core/decision.py` | Intent classification engine |
| `app/core/knowledge.py` | Knowledge base retrieval |
| `app/core/actions.py` | Action execution (leads, emails, bookings) |
| `app/services/llm_client.py` | OpenAI API wrapper |
| `app/utils/prompt_builder.py` | Dynamic prompt construction |

---

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black app/ tests/
isort app/ tests/
```

### Type Checking

```bash
mypy app/
```

---

## 📁 Project Structure

```
flowBot/
├── app/
│   ├── api/              # REST endpoints
│   ├── core/             # Business logic
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── services/        # External integrations
│   ├── utils/           # Helpers
│   ├── db/              # Database utilities
│   ├── main.py          # FastAPI app
│   └── config.py        # Configuration
├── business_configs/    # Business YAML configs
├── knowledge_base/      # Business knowledge files
├── tests/               # Test suite
├── requirements.txt     # Dependencies
├── pyproject.toml      # Project config
└── README.md           # This file
```

---

## 🔧 Configuration Options

### Business Config YAML

| Field | Type | Description |
|-------|------|-------------|
| `business.name` | string | Business name |
| `business.slug` | string | Unique identifier |
| `role` | string | AI role (receptionist, sales, etc.) |
| `personality.tone` | string | Tone (professional, friendly, casual) |
| `personality.greeting` | string | Initial greeting message |
| `rules` | list | Business-specific rules |
| `services` | list | List of offered services |
| `faqs` | list | Frequently asked questions |
| `automation` | object | Automation settings |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | sqlite:///./flowbot.db | Database connection |
| `OPENAI_API_KEY` | - | OpenAI API key (required) |
| `OPENAI_MODEL` | gpt-3.5-turbo | LLM model to use |
| `LOG_LEVEL` | INFO | Logging level |
| `APP_ENV` | development | Environment mode |

---

## 📝 License

MIT License - See LICENSE file for details.

---

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.
