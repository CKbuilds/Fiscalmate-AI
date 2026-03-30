import os
import re
import traceback
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# Groq පමණක් භාවිතා කරයි
from groq import Groq

# 1. Groq Configuration - ඔයාගේ API Key එක මෙතනට දාන්න
# (Get it from: https://console.groq.com/keys)
groq_client = Groq(api_key="Groq api key")

app = FastAPI()

# 2. CORS (කිසිදු වෙනසක් නැත)
allowed_origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    text: str
    user_id: str

SINHALA_RE = re.compile(r"[\u0D80-\u0DFF]")
NUMBER_RE = re.compile(r"\b\d[\d,]*(?:\.\d+)?\b")
MONEY_PREFIX_HINTS = ("lkr", "rs", "රුපියල්")

def normalize_currency_text(advice: str, user_text: str) -> str:
    text = advice or ""
    use_sinhala = bool(SINHALA_RE.search(user_text or ""))
    currency_word = "රුපියල්" if use_sinhala else "Rs"
    
    text = text.replace("$", f"{currency_word} ")
    text = re.sub(r"\bLKR\b\.?\s*", f"{currency_word} ", text, flags=re.IGNORECASE)
    if use_sinhala:
        text = re.sub(r"\bRs\.?\b\s*", f"{currency_word} ", text, flags=re.IGNORECASE)
    else:
        text = re.sub(r"රුපියල්\s*", f"{currency_word} ", text)

    def prefix_if_money_context(match: re.Match) -> str:
        num = match.group(1)
        start = match.start(1)
        left = text[max(0, start - 16):start].lower()
        right = text[match.end(1):match.end(1) + 6].lower()
        if any(hint in left for hint in MONEY_PREFIX_HINTS):
            return f"{num} "
        if right.startswith("%"):
            return f"{num} "
        return f"{currency_word} {num} "

    text = re.sub(
        r"(Logged\s*:?\s*)(\d[\d,]*(?:\.\d+)?)\s*(?=for\b)",
        lambda m: f"{m.group(1)}{currency_word} {m.group(2)} ",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"(\d[\d,]*(?:\.\d+)?)\s*(?=for\b)",
        lambda m: prefix_if_money_context(m),
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(r"(?i)\b(spent|spend|expense|paid|cost|bill)\s+(\d[\d,]*(?:\.\d+)?)\b",
                  lambda m: f"{m.group(1)} {currency_word} {m.group(2)}", text)

    return text

@app.post("/api/ai")
async def process_ai_input(data: UserMessage):
    try:
        user_is_sinhala = bool(SINHALA_RE.search(data.text or ""))
        currency_pref = "රුපියල්" if user_is_sinhala else "Rs"
        
        # Groq Request
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are FiscalMate AI for a Sri Lankan user. Always treat money as Sri Lankan Rupees. Include currency as '{currency_pref}'. Keep advice short and friendly."
                },
                {
                    "role": "user",
                    "content": data.text,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        
        advice_text = chat_completion.choices[0].message.content or ""
        
        # Supabase Save එක මෙතනින් අයින් කළා (Testing සඳහා)
        
        advice_text = normalize_currency_text(advice_text, data.text)
        return {"advice": advice_text, "success": True}
        
    except Exception as e:
        traceback.print_exc()
        return {"advice": f"Backend Error! {str(e)}", "success": False}

if __name__ == "__main__":
    import uvicorn
    # 127.0.0.1:8080 හි රන් වේ
    uvicorn.run(app, host="127.0.0.1", port=8080)