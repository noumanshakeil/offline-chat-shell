# Dev server for offline-chat-shell
$env:LLM_MODE = "mock"
uvicorn backend.main:app --reload --port 8000
