# Gemini-WhatsApp AI Assistant 🤖💬
---

## 💡 More Than a Feature: A Custom-Built Platform

While WhatsApp has a built-in "Meta AI", this project is fundamentally different. This is not a consumer feature; it is a complete, **custom-built backend platform** that I created and control.

Using the built-in AI is like driving a car. **This project is about building the entire engine and system that makes it run.**

Key differences that make this a unique backend achievement:

* **Total Control Over the "Brain":** The heart of this bot is Google's Gemini API, but the architecture is flexible. The AI model can be swapped out for any other, demonstrating true backend flexibility.
* **Unlimited Potential:** Unlike a closed feature, this bot is a platform. It can be extended to connect with other APIs to manage calendars, fetch real-time data, or even control smart home devices.
* **Developer, Not a User:** This project showcases the skills of a backend developer—integrating multiple professional APIs, managing cloud services, and handling real-time data—not just the skills of an app user.

---

A real-time, personal AI assistant on WhatsApp, powered by Google's Gemini API and deployed on a 24/7 cloud server. This project handles incoming WhatsApp messages via webhooks and generates intelligent, conversational responses in seconds.

---

## ✨ Demo

![WhatsApp Image 2025-07-19 at 23 58 40_ea49c8d1](https://github.com/user-attachments/assets/af36fbde-e345-4b3f-b14b-e57ba5de4c79)

---

## 🚀 Features

* **Real-time Conversation:** Responds to messages instantly.
* **Intelligent & Knowledgeable:** Powered by Google's `gemini-1.5-flash` model for high-quality, informative answers.
* **24/7 Availability:** Deployed on a cloud service (Render) that runs continuously.
* **Secure & Official:** Uses the official WhatsApp Business Platform API for stable and secure communication.

---

## 🛠️ Tech Stack & Architecture

This project integrates several powerful services to create a seamless conversational flow.

* **Backend:** Python, Flask
* **AI Model:** Google Gemini API
* **Platform:** WhatsApp Business Platform
* **Hosting:** Render (PaaS)
* **Version Control:** Git & GitHub

### Architecture Flow

The application is built on an event-driven architecture using webhooks:

`User on WhatsApp` → `Meta Servers` → `Render Webhook` → `Flask App` → `Google Gemini API` → `Flask App` → `Meta Servers` → `User on WhatsApp`

---

## ⚙️ Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a file named `.env` in the root directory and add the following keys. This file is included in `.gitignore` and should not be committed.
    ```
    WHATSAPP_TOKEN="your_permanent_whatsapp_token"
    VERIFY_TOKEN="your_custom_verify_token"
    WHATSAPP_PHONE_NUMBER_ID="your_whatsapp_phone_number_id"
    GEMINI_API_KEY="your_google_ai_api_key"
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```
    You will also need a tunneling service like `ngrok` or `pinggy` to expose your local server to the internet for WhatsApp's webhook during local testing.

---

## 🧠 Challenges & Learnings

This project was a deep dive into real-world backend development and involved solving numerous challenges:

* **Hardware Limitations:** The initial attempt to self-host an open-source model (`Gemma-2B`, `TinyLlama`) on free-tier hardware failed due to memory limitations and slow CPU performance, resulting in critical server timeouts.
* **API Integration:** Successfully integrated and authenticated with two separate, professional-grade APIs (Meta and Google).
* **Real-time Debugging:** Diagnosed and fixed a series of complex issues, including authentication failures (`401`), server errors (`404`, `422`), and timeouts (`500`), by analyzing live logs across multiple platforms.
* **The "Middle Ground":** The final architecture using the Gemini API's free tier represents the optimal solution, balancing performance, intelligence, and cost.
**microsoft/DialoGPT-small**
  **Faults Earlier**
  ![WhatsApp Image 2025-07-19 at 02 44 23_e213f537](https://github.com/user-attachments/assets/4006e6d3-2179-46d3-9a59-12c192dd7552)

---

## 📄 License

This project is licensed under the MIT License.
