# Architecture Diagram Generator

An AI-powered tool that automatically converts plain-English architecture descriptions into beautiful, production-ready Mermaid.js diagrams. Designed for developers, architects, and technical writers who want to quickly visualize systems without manually writing complex diagram syntax.

## ✨ Features

- **Natural Language to Diagrams:** Describe your architecture in plain English and let the AI do the heavy lifting.
- **Powered by Groq:** Uses the blazing-fast `llama-3.3-70b-versatile` model via the Groq API for near-instant diagram generation.
- **Premium UI/UX:** A sleek, modern SaaS interface built with Tailwind CSS, featuring smooth animations and a clean dark mode.
- **Interactive Preview & Code Editing:** Toggle instantly between the visual diagram and the raw Mermaid.js code.
- **One-Click Export:** Export your generated architecture diagrams directly to SVG for use in documentation, presentations, or code repositories.
- **Zero Config Local Dev:** Easy to spin up locally with a FastAPI backend and a vanilla HTML/JS frontend.

## 🛠️ Technology Stack

- **Backend:** Python, FastAPI, Uvicorn, Groq API
- **Frontend:** HTML5, Tailwind CSS, Mermaid.js, Phosphor Icons
- **AI Model:** `llama-3.3-70b-versatile`

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing.

### Prerequisites

- Python 3.8+
- A [Groq API Key](https://console.groq.com/keys)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ayush20-lex/architecture-diagram-generator.git
   cd architecture-diagram-generator
   ```

2. **Configure Environment Variables:**
   Navigate to the `backend` directory and create a `.env` file:
   ```bash
   cd backend
   ```
   Add your Groq API key to the `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Install Backend Dependencies:**
   It is highly recommended to use a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
   Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Backend Server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   The backend will start running at `http://localhost:8000`.

5. **Open the Frontend:**
   You don't need a build step for the frontend! Simply open `frontend/index.html` in your favorite web browser to start using the application. 

## 💡 Usage

1. Open the UI and type a description into the input box on the left.
   *Example: "A React frontend communicates with an API Gateway. The API Gateway routes requests to three separate microservices: User Service, Product Service, and Order Service. Each microservice has its own dedicated database."*
2. Click **Generate Diagram**.
3. View the rendered architecture schematic. You can toggle to the **Code** view if you wish to manually tweak the Mermaid syntax.
4. Click **Export SVG** to download the final diagram!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
