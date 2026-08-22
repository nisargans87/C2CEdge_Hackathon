# 🛡️ TrustChecker

## AI-Powered Fake News, Claim and Image Verification Telegram Bot

> ### **Think Before You Trust. Verify Before You Share.**

TrustChecker is an AI-assisted, evidence-based verification system designed to help users analyze suspicious news, claims, images, and online information.

The project primarily works as a **Telegram chatbot**, making verification simple and accessible. Instead of manually searching through multiple websites and sources, users can send suspicious information directly to the TrustChecker bot and receive an AI-generated analysis.

TrustChecker analyzes the submitted content, identifies the main claim, evaluates the available information, and provides a structured verification result with reasoning, confidence, and relevant supporting sources when available.

---

# 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Key Features](#-key-features)
- [How TrustChecker Works](#-how-trustchecker-works)
- [System Workflow](#-system-workflow)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation Guide](#-installation-guide)
- [API Configuration](#-api-configuration)
- [Running the Telegram Bot](#-running-the-telegram-bot)
- [Verification Process](#-verification-process)
- [Possible Verification Results](#-possible-verification-results)
- [Target Users](#-target-users)
- [Project Architecture](#-project-architecture)
- [Future Enhancements](#-future-enhancements)
- [Disclaimer](#-disclaimer)
- [Conclusion](#-conclusion)

---

# 🚨 Problem Statement

In today's digital world, information spreads faster than ever.

Social media platforms, messaging applications, online news portals, and digital communities allow people to share information instantly. However, this also creates a major problem: **misinformation can spread quickly before people have an opportunity to verify it**.

Users frequently receive:

- 📰 Suspicious news articles
- 📱 Viral social media posts
- 🖼️ Images with misleading captions
- ❗ Unverified claims
- 🚨 Breaking news messages
- 🌐 Information shared without reliable sources

Many people do not know how to verify whether this information is accurate.

Traditional fact-checking usually requires users to:

1. Identify the original claim.
2. Search multiple websites.
3. Compare different sources.
4. Check publication dates.
5. Identify reliable sources.
6. Understand whether the information is missing important context.

This process can be time-consuming and difficult.

As a result, people may unknowingly share false or misleading information.

### The core question is:

> **How can we make information verification faster, simpler, and accessible to ordinary users?**

TrustChecker is designed as a solution to this problem.

---

# 💡 Our Solution

TrustChecker is an AI-powered Telegram chatbot that allows users to submit suspicious information directly through Telegram.

The user can send:

- 📝 Text-based claims
- 📰 News information
- 🖼️ Images containing claims or news
- 📢 Viral messages
- ❓ Suspicious information found online

The system then processes the information and provides an AI-assisted verification result.

Instead of asking users to understand complicated fact-checking procedures, TrustChecker provides a simple workflow:

```text
Receive Information
        ↓
Send It to TrustChecker
        ↓
AI Understands the Claim
        ↓
Analyze Available Evidence
        ↓
Generate Verification Result
        ↓
Provide Reasoning and Sources
✨ Key Features
🤖 Telegram-Based Chatbot

TrustChecker works through Telegram, allowing users to verify information directly from a messaging platform.

Users do not need to install a separate application or learn a complicated system.

📝 Text and Claim Analysis

Users can send a suspicious claim or news text to the bot.

For example:

"NASA has announced that the Earth will experience
six days of darkness next month."

TrustChecker analyzes the claim and generates a verification response.

🖼️ Image-Based Information Analysis

Users can submit an image containing:

News headlines
Social media posts
Viral claims
Informational posters
Screenshots

The system attempts to understand the information contained in the image and analyze the main claim.

🧠 AI-Powered Reasoning

TrustChecker uses an AI model to understand the submitted information.

The AI can help:

Identify the main claim
Detect suspicious wording
Analyze context
Identify missing information
Compare available evidence
Generate understandable reasoning
📊 Confidence Score

The system can provide a confidence estimate based on the analysis.

Example:

Confidence: 82%

This score represents the confidence of the generated analysis and should not be interpreted as absolute proof.

⚠️ Clear Verification Categories

TrustChecker can classify information into understandable categories such as:

✅ Likely True
❌ Likely False
⚠️ Possibly Misleading
❓ Insufficient Evidence
🔍 Evidence-Based Analysis

The system attempts to support the verification process using available information and relevant sources.

The response can include:

Reasoning
Important context
Evidence summary
Relevant news information
Supporting links
🔄 How TrustChecker Works

The verification process is divided into several stages.

Step 1: User Sends Information

The user sends a message or image to the Telegram bot.

User
  │
  ▼
Telegram
  │
  ▼
TrustChecker Bot
Step 2: Content Processing

The chatbot determines the type of submitted content.

Possible inputs include:

Text
Image
News Claim
Online Information

The system prepares the content for further analysis.

Step 3: Claim Understanding

The AI identifies the central statement or claim that needs to be verified.

For example:

Input:
"A new law has banned all smartphones in India."

Extracted Claim:
"India has introduced a nationwide ban on all smartphones."

This helps the system focus on the actual information that needs verification.

Step 4: AI Analysis

The submitted claim is analyzed for:

Logical consistency
Context
Suspicious wording
Missing information
Possible exaggeration
Unverified statements
Misinformation patterns
Step 5: Evidence and Information Search

Relevant information can be searched and compared against the claim.

The system attempts to identify whether available evidence:

Supports the claim
Contradicts the claim
Provides additional context
Is insufficient for a reliable conclusion
Step 6: Generate Verification Result

Finally, TrustChecker generates a structured response.

Example:

🛡️ TRUSTCHECKER VERIFICATION RESULT

Status: ⚠️ POSSIBLY MISLEADING

Confidence: 78%

Claim:
The submitted information claims that a major event
has occurred.

Analysis:
The claim contains information that could not be fully
confirmed using the available evidence. Some elements
appear to lack important context.

Recommendation:
Do not share this information until it has been verified
through reliable and authoritative sources.

Supporting Information:
Relevant sources and information are provided when available.
🔁 System Workflow
┌──────────────────────┐
│        USER          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      TELEGRAM        │
│        BOT           │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   INPUT PROCESSING   │
│                      │
│  • Text              │
│  • News              │
│  • Image             │
│  • Claim             │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   CLAIM EXTRACTION   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     AI ANALYSIS      │
│                      │
│  • Understand claim  │
│  • Analyze context   │
│  • Detect issues     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   EVIDENCE SEARCH    │
│                      │
│  • Related news      │
│  • Available sources │
│  • Supporting facts  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ VERIFICATION ENGINE  │
│                      │
│ TRUE / FALSE /       │
│ MISLEADING /         │
│ UNCERTAIN            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  REASONING + RESULT  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│        USER          │
└──────────────────────┘
🛠️ Technology Stack
Programming Language
Python

Python is used as the primary programming language for the chatbot logic, verification system, API integration, and AI processing.

🤖 Telegram Bot API

Telegram provides the communication interface between the user and TrustChecker.

Users interact with the project directly through Telegram messages and images.

🧠 Groq AI API

Groq is used to access an AI model for:

Understanding user input
Analyzing claims
Generating structured reasoning
Producing verification responses
📰 News and Information API

A news API can be used to retrieve relevant information related to the submitted claim.

This helps provide additional context and supporting information.

🌐 Flask

Flask is included for optional web functionality and API handling.

However, the primary demonstration and user interaction for this project is through the Telegram chatbot.

🐙 GitHub

GitHub is used for:

Source code management
Version control
Project documentation
Sharing the project with judges and recruiters
📁 Project Structure
TrustChecker/
│
├── app.py
│
├── telegram_bot.py
│   └── Handles communication between Telegram and TrustChecker
│
├── verifier.py
│   └── Contains verification logic
│
├── realitychecker.py
│   └── Handles AI-assisted claim analysis
│
├── web_verifier.py
│   └── Supports web verification functionality
│
├── requirements.txt
│   └── Contains required Python packages
│
├── .gitignore
│   └── Prevents sensitive and unnecessary files from GitHub
│
├── README.md
│   └── Complete project documentation
│
└── templates/
    │
    └── index.html
        └── Optional web interface
⚙️ Installation Guide
1️⃣ Clone the Repository

Open a terminal and run:

git clone https://github.com/nisargans87/TrustChecker.git

Move into the project directory:

cd TrustChecker
2️⃣ Create a Virtual Environment
python -m venv venv
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
3️⃣ Install Dependencies

Run:

pip install -r requirements.txt

This installs the Python libraries required for the project.

🔐 API Configuration

TrustChecker requires API keys for external services.

Create a file named:

.env

Add your API credentials:

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
NEWS_API_KEY=your_news_api_key

Replace the placeholder values with your actual API keys.

🔒 Security

Never upload API keys to GitHub.

The .gitignore file should contain:

venv/
.env
__pycache__/
*.pyc

This prevents:

Virtual environment files
API keys
Python cache files
Unnecessary system files

from being uploaded to the repository.

🚀 Running the Telegram Bot

After configuring the required API keys, activate your virtual environment and run:

python telegram_bot.py

If your project uses a different main bot file, run that file instead.

Once the bot starts successfully, open Telegram and interact with your TrustChecker bot.

You can use commands such as:

/start

Then send:

A suspicious news message
A claim
A viral message
An image containing information
💬 Example User Interaction
User sends:
Breaking News:
A new government rule says all internet access
will be blocked after 10 PM.
TrustChecker analyzes the claim:
🔍 Analyzing the information...

Step 1: Understanding the claim
Step 2: Checking available information
Step 3: Generating verification result
Example response:
🛡️ TRUSTCHECKER RESULT

Verdict: ⚠️ POSSIBLY MISLEADING

Confidence: 81%

Reasoning:
The submitted claim could not be confirmed through
the available information. The statement may be missing
important context or may originate from an unreliable source.

Recommendation:
Do not share this information until it is confirmed
through official or trusted sources.
📊 Possible Verification Results
Result	Meaning
✅ LIKELY TRUE	Available evidence generally supports the claim
❌ LIKELY FALSE	Available evidence significantly contradicts the claim
⚠️ POSSIBLY MISLEADING	The claim may contain incomplete, exaggerated, or out-of-context information
❓ INSUFFICIENT EVIDENCE	Not enough reliable information is available to make a strong conclusion
🎯 Target Users

TrustChecker is designed for anyone who regularly consumes or shares online information.

👨‍🎓 Students

Students can use TrustChecker to verify information before using it in assignments, presentations, and research.

👩‍🏫 Teachers and Educators

Educators can use the system to demonstrate:

Digital literacy
Critical thinking
Responsible information sharing
📱 Social Media Users

People who receive viral messages and suspicious posts can quickly submit them to TrustChecker.

📰 Journalists and Content Creators

The system can act as an initial verification assistant before publishing or sharing information.

👨‍👩‍👧 General Public

Anyone who wants to check suspicious information can interact with the bot.

🏛️ Project Architecture
                 ┌──────────────┐
                 │     USER     │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   TELEGRAM   │
                 │     BOT      │
                 └──────┬───────┘
                        │
                        ▼
              ┌─────────────────────┐
              │   PYTHON BACKEND    │
              └──────────┬──────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     ┌─────────┐    ┌─────────┐   ┌──────────┐
     │   AI    │    │  NEWS   │   │  IMAGE   │
     │ ANALYSIS│    │ SEARCH  │   │ ANALYSIS │
     └────┬────┘    └────┬────┘   └────┬─────┘
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ VERIFICATION    │
                │ ENGINE          │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ RESULT +        │
                │ REASONING       │
                └────────┬────────┘
                         │
                         ▼
                       USER
🌟 Advantages of TrustChecker

TrustChecker provides several benefits:

⚡ Fast

Users can submit information directly through Telegram.

📱 Accessible

No complicated application interface is required.

🧠 AI-Assisted

AI helps analyze the meaning and context of claims.

🔍 Evidence-Oriented

The system aims to use available information and sources instead of generating only a simple answer.

🗣️ Easy to Understand

The final response is designed to provide clear reasoning instead of only saying "Real" or "Fake."

🚧 Current Limitations

TrustChecker is an AI-assisted system and has limitations.

AI analysis may occasionally be incorrect.
Available online information may be incomplete.
Breaking news may not yet have sufficient reliable coverage.
Images can be difficult to interpret accurately.
A confidence score is not absolute proof.
The system should not replace professional journalism or expert fact-checking.

Therefore, users should always verify important information using reliable and authoritative sources.

🔮 Future Enhancements

TrustChecker can be expanded with the following features.

🔍 Reverse Image Search

Check whether an image was previously published in a different context.

🎥 Video Verification

Analyze suspicious videos and identify potential misinformation.

🤖 Deepfake Detection

Detect possible AI-generated or manipulated media.

🌍 Multilingual Support

Allow users to submit information in multiple languages.

Possible future languages include:

English
Kannada
Hindi
Other regional languages
🎙️ Voice-Based Verification

Allow users to speak a claim instead of typing it.

📱 WhatsApp Integration

Expand TrustChecker to additional messaging platforms.

🗂️ Verification History

Store previous verification results so users can review them later.

📧 Automated Newsletter

Generate a newsletter containing:

Recently verified claims
Trending misinformation
Important fact-checking updates
Reliable information sources
🌐 Browser Extension

Allow users to verify suspicious information while browsing websites and social media platforms.

📊 Misinformation Analytics

Analyze trends such as:

Frequently submitted claims
Common misinformation topics
Viral false information
Categories of misleading content
⚠️ Disclaimer

TrustChecker is an AI-assisted verification tool.

The results generated by the system should not be considered absolute proof that a claim is true or false.

The verification result depends on:

Available information
Source quality
AI interpretation
Context
Timing
API availability

For important decisions, users should always verify information using official and authoritative sources.

TrustChecker is intended to assist users in developing better digital literacy and critical thinking habits.

🏆 Hackathon Vision

TrustChecker was developed as a project focused on addressing the growing problem of misinformation.

The project's central idea is simple:

People should not need advanced technical skills or spend hours searching the internet just to verify a suspicious message.

By integrating AI with a familiar messaging platform, TrustChecker aims to make information verification easier and more accessible.

🎤 Project Pitch

Every day, millions of people receive news, images, and messages that they cannot immediately verify. TrustChecker brings AI-powered verification directly into Telegram. A user simply sends suspicious information to the bot, and the system analyzes the claim, evaluates available evidence, and returns a clear verdict with reasoning and supporting information. Our goal is simple: make people think before they trust and verify before they share.

📈 Future Vision
Today
  │
  ▼
Telegram-Based Verification
  │
  ▼
Text + Image Analysis
  │
  ▼
AI Reasoning
  │
  ▼
Evidence-Based Results
  │
  ▼
────────────────────────────
Future
────────────────────────────
  │
  ├── WhatsApp Integration
  ├── Deepfake Detection
  ├── Video Verification
  ├── Reverse Image Search
  ├── Multilingual Support
  ├── Voice Verification
  ├── Browser Extension
  ├── Verification Database
  └── Misinformation Analytics
👨‍💻 Project Repository

Repository: TrustChecker

This repository contains the source code, configuration files, verification logic, and documentation for the TrustChecker project.

🤝 Contributing

Contributions, improvements, and suggestions are welcome.

Possible areas for contribution include:

Improving verification accuracy
Adding new data sources
Improving image analysis
Adding multilingual support
Improving response formatting
Adding database support
Creating advanced misinformation detection models
📄 License

This project is developed for:

Educational purposes
Research purposes
Learning
Demonstration
Hackathon participation

Please ensure that any external APIs and services used with this project comply with their respective terms of service.

❤️ Final Message
The internet gives everyone the power to share information.
TrustChecker helps give everyone the power to question it.
           🛡️ TRUSTCHECKER

        VERIFY THE INFORMATION
                ↓
        UNDERSTAND THE CLAIM
                ↓
        CHECK THE CONTEXT
                ↓
        ANALYZE THE EVIDENCE
                ↓
        THINK BEFORE YOU TRUST
                ↓
        VERIFY BEFORE YOU SHARE
⭐ If you find this project interesting, consider giving the repository a star!
🛡️ TrustChecker