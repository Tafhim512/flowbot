# Testing Instructions for FlowBot

## Step 1: Add Your API Key

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## Step 2: Start the Server

```bash
cd c:/flowBot
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## Step 3: Test with cURL Commands

### 3.1 Create a Business (Demo Clinic)

```bash
curl -X POST "http://localhost:8000/api/v1/businesses" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"City Health Clinic\", \"slug\": \"demo_clinic\", \"config_path\": \"business_configs/demo_clinic.yaml\"}"
```

**Copy the `id` from the response!** You'll need it for the next step.

### 3.2 Send a Message (Test the AI)

Replace `YOUR_BUSINESS_ID` with the ID you got from step 3.1:

```bash
curl -X POST "http://localhost:8000/api/v1/messages" ^
  -H "Content-Type: application/json" ^
  -d "{\"business_id\": \"YOUR_BUSINESS_ID\", \"session_id\": \"test-001\", \"text\": \"Hello, what services do you offer?\"}"
```

### 3.3 Test Different Scenarios

**Test Question Intent:**
```bash
curl -X POST "http://localhost:8000/api/v1/messages" ^
  -H "Content-Type: application/json" ^
  -d "{\"business_id\": \"YOUR_BUSINESS_ID\", \"session_id\": \"test-002\", \"text\": \"What are your office hours?\"}"
```

**Test Lead Capture:**
```bash
curl -X POST "http://localhost:8000/api/v1/messages" ^
  -H "Content-Type: application/json" ^
  -d "{\"business_id\": \"YOUR_BUSINESS_ID\", \"session_id\": \"test-003\", \"text\": \"I'm interested! Please call me at 555-123-4567 or email me at john@example.com\"}"
```

**Test Booking Intent:**
```bash
curl -X POST "http://localhost:8000/api/v1/messages" ^
  -H "Content-Type: application/json" ^
  -d "{\"business_id\": \"YOUR_BUSINESS_ID\", \"session_id\": \"test-004\", \"text\": \"I'd like to book an appointment for tomorrow\"}"
```

**Test Support Intent:**
```bash
curl -X POST "http://localhost:8000/api/v1/messages" ^
  -H "Content-Type: application/json" ^
  -d "{\"business_id\": \"YOUR_BUSINESS_ID\", \"session_id\": \"test-005\", \"text\": \"I have a problem with my recent visit\"}"
```

### 3.4 View Captured Leads

```bash
curl -X GET "http://localhost:8000/api/v1/leads"
```

### 3.5 View All Businesses

```bash
curl -X GET "http://localhost:8000/api/v1/businesses"
```

## Step 4: Test via Web Interface

Open your browser and go to:
- **API Docs:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

You can test all endpoints interactively from there.

## Step 5: Register Your Real Business

### 5.1 Create Your Business Config

Create a new file `business_configs/your_business.yaml`:

```yaml
business:
  name: "Your Business Name"
  slug: "your_business"
  industry: "retail"

role: "receptionist"

personality:
  tone: "professional"
  language: "English"
  greeting: "Hello! Welcome to Your Business!"

rules:
  - "Be helpful and courteous"
  - "Confirm details before proceeding"

services:
  - "Product Sales"
  - "Customer Support"

faqs:
  - question: "What are your hours?"
    answer: "We're open Monday to Friday, 9 AM to 5 PM."
```

### 5.2 Create Knowledge Base

Create directory `knowledge_base/your_business/` with JSON files:
- `faqs.json`
- `services.json`
- `pricing.json`

### 5.3 Register in Database

```bash
curl -X POST "http://localhost:8000/api/v1/businesses" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Your Business Name\", \"slug\": \"your_business\", \"config_path\": \"business_configs/your_business.yaml\"}"
```

## Troubleshooting

### If you get "Business not found" error:
- Make sure you copied the correct `id` from the business creation response
- The id should be a UUID like `550e8400-e29b-41d4-a716-446655440000`

### If LLM calls fail:
- Verify your `OPENAI_API_KEY` is correct in `.env`
- Check the terminal for error messages

### If knowledge isn't being retrieved:
- Verify the `knowledge_dir` path in your YAML config exists
- Make sure JSON files are properly formatted
