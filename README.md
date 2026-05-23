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
