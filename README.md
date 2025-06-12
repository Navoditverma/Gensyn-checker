# Gensyn Peer ID Checker

A simple web-based tool to check Gensyn peer ID status, rewards, scores, and availability (online/offline). Built using Python, Flask, and HTML/CSS.

## 🚀 Features

- Submit multiple Gensyn Peer IDs (separated by new lines)
- Fetches peer details including:
  - Peer Name
  - Reward
  - Score
  - Online/Offline status
- Clean, responsive UI
- Fast results using multithreading (asynchronous fetch)

## 🔧 Technologies Used

- Python 3
- Flask
- Requests (for API calls)
- HTML/CSS (no JS framework)

## 📷 Preview

![Screenshot](screenshot.png) <!-- Replace with actual screenshot path -->

## 📦 Setup

```bash
git clone https://github.com/navoditverma/gensyn-peer-checker.git
cd gensyn-peer-checker
pip install -r requirements.txt
python app.py
