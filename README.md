# A.X.O.N.

**Advanced eXecutive Optimization Nexus**  
*A Local-First AI Operating Assistant.*

---

## 🚀 Overview

**A.X.O.N.** is a modular, extensible, and privacy-focused AI operating assistant.

Designed to be your personal digital operating companion, A.X.O.N. understands natural language, automates workflows, controls your computer, remembers important information, and interacts with your local environment.

Unlike cloud-dependent assistants, **A.X.O.N. follows a Local-First philosophy**. Core functionality—including conversations, voice interaction, memory, and system control—works entirely on your computer whenever possible.

Internet connectivity is optional and only used when required for services such as web search, weather, online APIs, or cloud AI models.

---

# ✨ Features

## 🧠 Local AI

- Offline conversational AI
- Local LLM support (Ollama / llama.cpp)
- Optional cloud AI fallback
- Context-aware conversations

## 🎙️ Voice Assistant

- Wake-word detection ("Hey Axon")
- Offline speech recognition
- Natural text-to-speech
- Continuous listening mode

## 💾 Memory

- Long-term memory
- User preferences
- Conversation history
- Context awareness
- Local database

## ⚙️ System Control

- Launch applications
- Manage files and folders
- Execute terminal commands
- Windows automation
- Workflow execution

## 🧩 Skills

Every feature is implemented as an independent module.

Examples:

- 📁 File Manager
- 🌐 Browser
- 🎵 Music
- 📝 Notes
- 📅 Calendar
- 🧮 Calculator
- 📧 Email
- 🌦 Weather
- 🏠 Smart Home

## 👁️ Vision *(Planned)*

- Screen understanding
- Camera support
- OCR
- Object detection

## 🌍 Online Services *(Optional)*

- Web Search
- News
- Weather
- Cloud AI
- External APIs

---

# 🏗️ Architecture

```
A.X.O.N.
│
├── Core
├── Brain
├── Memory
├── Voice
├── Vision
├── Skills
├── System
├── Interface
├── Network
└── Config
```

Each module is independent, making the project easy to maintain and extend.

---

# 🛠️ Tech Stack

### Language

- Python 3.12+

### AI

- Ollama
- llama.cpp
- Transformers
- OpenAI API *(optional)*

### Speech

- Vosk
- whisper.cpp
- Piper TTS

### Memory

- SQLite
- ChromaDB *(optional)*

### Vision

- OpenCV
- Pillow

### Automation

- PyAutoGUI
- psutil
- keyboard
- pywin32

### Development

- VS Code
- Git

---

# 🗺️ Roadmap

## Phase 1 — Core

- [x] Project architecture
- [ ] Configuration system
- [ ] Logging
- [ ] Plugin framework

## Phase 2 — Voice

- [ ] Wake-word detection
- [ ] Offline speech recognition
- [ ] Offline TTS

## Phase 3 — Intelligence

- [ ] Local LLM
- [ ] Context manager
- [ ] Long-term memory

## Phase 4 — System

- [ ] App launcher
- [ ] File manager
- [ ] Windows automation
- [ ] Terminal control

## Phase 5 — Skills

- [ ] Browser
- [ ] Music
- [ ] Calendar
- [ ] Notes
- [ ] Email
- [ ] Calculator

## Phase 6 — Vision

- [ ] Screen analysis
- [ ] OCR
- [ ] Camera support

## Phase 7 — Interfaces

- [ ] Desktop application
- [ ] Web dashboard
- [ ] Mobile companion

---

# 📄 License

Distributed under the MIT License.

See **LICENSE** for more information.

---

## ⭐ Vision

> **"A.X.O.N. is more than a chatbot. It is designed to become your personal AI operating companion—private, modular, intelligent, and always under your control."**
