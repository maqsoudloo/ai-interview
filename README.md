# 🎧 AI Interview Copilot (`ai-interview`)

An advanced, real-time AI-powered interview assistant designed to process live audio streams, generate instant transcriptions, and deliver contextualized paragraph suggestions during high-stakes professional and academic interviews.

This repository is a customized and optimized fork of the open-source project **Ecoute**. It has been redesigned to integrate custom prompt engineering, eliminate text clutter, and provide optimized real-time response generation utilizing Large Language Models (LLMs).

---

## 🚀 Key Features & Enhancements (Customized Version)

- **Real-Time Live Transcription:** Dual-stream interception that captures and transcribes both your microphone input (You) and the speaker output (Interviewer) simultaneously.
- **Zero-Bullet Presentation Mode:** Deeply optimized prompt engineering that forces the AI engine to output responses in clean, short, scannable paragraphs instead of generic bullet lists—ideal for teleprompter-style natural reading.
- **Intelligent Silence Detection:** Dynamically monitors when the candidate is speaking fluidly to stay quiet, avoiding visual distractions and minimizing token consumption.
- **Generic Template Architecture:** Replaced all personal data with an abstract, universally applicable structure, allowing any professional to insert their own career or scholarship framework safely.

---

## 📋 Prerequisites

- Python >= 3.8.0
- An OpenAI API key (with access to Whisper and GPT models)
- Windows OS (Core audio routing is verified on Windows)
- FFmpeg 

### Installing FFmpeg on Windows
If FFmpeg is not installed on your system, you can install it using Chocolatey. Open PowerShell as **Administrator** and run:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('[https://community.chocolatey.org/install.ps1](https://community.chocolatey.org/install.ps1)'))

Once Chocolatey is installed, install FFmpeg:

PowerShell
choco install ffmpeg

🔧 Installation & Setup
Clone the repository:

Bash
   git clone [https://github.com/YOUR_USERNAME/ai-interview.git](https://github.com/YOUR_USERNAME/ai-interview.git)
   cd ai-interview
Install the required packages:

Bash
   pip install -r requirements.txt
Set Up Your OpenAI API Key:
Create a keys.py file manually in the root directory or use the following command prompt shortcut (replace API_KEY with your actual token):

Bash
   python -c "with open('keys.py', 'w', encoding='utf-8') as f: f.write('OPENAI_API_KEY=\"API_KEY\"')"
🎬 Running the Assistant
To run the main application with optimized live API support (highly recommended for multi-language accuracy and lightning-fast response times):

Bash
python main.py --api
Upon initiation, the system will begin capturing your microphone input and speaker output in real-time. The --api flag ensures that the advanced Whisper API and GPT engine process the transcriptions smoothly, tailoring the responses strictly to the custom paragraph constraints defined in the system prompts.

⚙️ Custom Prompt Engineering
The behavior of this assistant relies entirely on the abstract system_instruction prompt configured inside the source code. It has been stripped of personal data and ready for custom deployment:

Python
system_instruction = """You are a highly intelligent and expert AI Interview Assistant...
=== CRITICAL FORMATTING & STYLE RULES ===
1. NO BULLET POINTS: Output responses exclusively in short paragraphs.
2. CONVERSATIONAL TONE: Write exactly how a confident professional speaks.
..."""
⚠️ Known Limitations
Default Audio Routing: The tool is configured to listen strictly to the default microphone and speaker devices selected in your Windows system settings.

API Dependency: Running with the --api flag delivers the best speed and multi-language capability but requires active OpenAI API credits.

📖 License
This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Acknowledgements
This tool is a derived work based on the original architecture of Ecoute. Significant modifications were introduced to advance human-computer interaction (HCI) layouts, conversational flow alignment, and strict paragraph formatting constraints necessary for real-time interview simulations.
