# Fiscalmate-AI
# 💰 Fiscalmate AI

**Fiscalmate AI** is an autonomous, context-aware financial intelligence agent designed to bridge the financial literacy gap. It automates personal wealth management by using **Natural Language Processing (NLP)** for voice-based and text logging, **OCR** for instant receipt scanning, and **Predictive Analytics** to safeguard users from debt traps in volatile economies.

---

### 🚀 Key Features
* **AI-Powered Expense Logging:** Simply describe your spending in natural language, and the AI categorizes it automatically.
* **Context-Aware Insights:** Provides smart feedback based on your spending habits.
* **Fast & Lightweight:** Built with a high-performance backend for real-time processing.

---

### 🛠 Tech Stack
* **Backend:** FastAPI (Python 3.10+)
* **AI Engine:** Groq API (Running Llama 3 for high-speed inference)
* **Database:** Supabase (PostgreSQL with Real-time capabilities)
* **Frontend:** HTML5, Modern CSS (Tailwind CSS)
* **Deployment:** Render / Vercel

---

### ⚙️ How It Works (System Architecture)
1.  **User Input:** User enters a transaction (e.g., "Spent 5000 for dinner") through the web interface.
2.  **Processing:** The FastAPI backend receives the request and sends the text to the **Groq AI engine**.
3.  **Intelligence:** Llama 3 extracts the `Amount`, `Category`, and `Note` from the unstructured text.
4.  **Storage:** The structured data is securely saved in the **Supabase** database.
5.  **Response:** The AI provides a confirmation or a financial tip back to the user.

---

### 🔮 Future Improvements
* 📊 **Visual Analytics:** Adding interactive charts and graphs for monthly expense tracking.
* 🌍 **Multi-Currency Support:** Implementing real-time exchange rates to support users in volatile economies.
* 🔐 **User Authentication:** Secure login systems (OAuth/Supabase Auth) to provide personalized and private data storage.
* 📸 **Advanced OCR:** Full receipt scanning to extract line items automatically using computer vision.

---
### 🌐 Live Demo
You can access the application here: [https://fiscalmate-ai--CKBuilds.replit.app]
