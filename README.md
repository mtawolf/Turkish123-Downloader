# Turkish123 Series Downloader 🇹🇷

A powerful, multi-language Python automation tool to download Turkish series with English subtitles directly from Turkish123. Optimized for media servers like **CasaOS**, **Plex**, and **Jellyfin**.

**Made by: [MTAwolf](https://github.com/mtawolf)**

---

## 🚀 Features
- **Multi-language support:** Interface available in English, Dutch, German, and French.
- **Auto-naming:** Files are automatically saved in `Series_Name_S01E01.mp4` format.
- **Stealth Browsing:** Uses Playwright to bypass basic bot detection.
- **Bulk Download:** Download an entire series or choose specific episodes.

---

## 📦 Installation
1. **Clone the repository:**
```bash
git clone https://github.com/mtawolf/turkish123-downloader.git
cd turkish123-downloader
```
2. **Go to the project folder:**
```bash
cd turkish123-downloader
```
3. **Install dependencies:**
```bash
pip install playwright yt-dlp
playwright install chromium
```
4.**Install browser engine:**
```bash
playwright install chromium
```
5.**Run the script:**
```bash
python turkish123downloader.py
```
🐳Docker (CasaOS)
To run this on your server (like CasaOS), use the official Playwright Python image.
```bash
[mcr.microsoft.com/playwright/python:v1.40.0-jammy](https://mcr.microsoft.com/playwright/python:v1.40.0-jammy)
```
Volume Mapping:
Map your server's download folder to:
```bash
/app/downloads
```
🤝 Contributing
Feel free to fork this project and submit pull requests. For major changes, please open an issue first.
Disclaimer: This tool is for educational purposes only. Please respect the copyright of the content owners. The developer is not responsible for any misuse.
