<div align="center">

<!-- Animated Header Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D2017,50:1C5D42,100:31A572&height=200&section=header&text=EcoNews&fontSize=80&fontColor=ffffff&fontAlignY=38&desc=AI-Curated%20Daily%20News%20Digest&descAlignY=60&descSize=22&animation=fadeIn" width="100%"/>

<!-- Animated Typing -->
<a href="https://github.com/mayank-goyal09/news-curator">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=31A572&center=true&vCenter=true&multiline=true&width=700&height=80&lines=☕+Grab+your+coffee...;📰+Your+AI+news+curator+is+ready.;🎧+Sit+back+%26+listen+to+today's+digest." alt="Typing SVG" />
</a>

<br/>


<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-llama3.2-black?style=for-the-badge&logo=ollama&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Audio%20CDN-181717?style=for-the-badge&logo=github&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<br/>

> **EcoNews** fetches news from 10+ RSS feeds every day, curates the best 15 stories across 5 categories using a local AI (Ollama), converts them to audio, and emails the digest to subscribers — all automatically.

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 AI Curation
- Powered by **Ollama (llama3.2)** running 100% locally
- Picks the **top 3 stories per category** from 10+ RSS feeds
- Writes a `why_pick` explanation for each article
- Auto-generates tags and an overall daily summary

</td>
<td width="50%">

### 📰 5 News Categories
- 🎭 **Satire** — The Onion, The Babylon Bee
- 🤖 **AI & Technology** — TechCrunch, Ars Technica
- 🌍 **Worldwide News** — BBC, Reuters
- 💚 **Warming & Emotions** — Positive News, Upworthy
- 📈 **Market News** — MarketWatch, CNBC

</td>
</tr>
<tr>
<td width="50%">

### 🎧 Voice Digest
- Text-to-Speech via `pyttsx3` (offline)
- Reads all 15 curated articles by category
- MP3 uploaded to **GitHub** as CDN
- One-click **Voice Assistant** button on dashboard

</td>
<td width="50%">

### 📧 Email Newsletter
- Beautiful **HTML emails** with category sections
- Users subscribe via the dashboard popup
- Daily digest sent to **all subscribers** automatically
- Powered by Gmail App Passwords (SMTP)

</td>
</tr>
</table>

---
