from app.services.gemini_chat import gemini_chat
import json
import traceback

print('GEMINI_API_KEY present:', bool(getattr(gemini_chat, 'api_key', None)))
print('IS_AVAILABLE:', gemini_chat.is_available())

try:
    res = gemini_chat.chat('Apa motivasimu mengikuti GDGOC?', user_profile={'name':'John Doe','role':'student'}, system_prompt='Jawab singkat dalam Bahasa Indonesia')
    print('CHAT_RESULT:', json.dumps(res, default=str, ensure_ascii=False))
except Exception:
    traceback.print_exc()
