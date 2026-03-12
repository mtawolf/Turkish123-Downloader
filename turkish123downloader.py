import time
import subprocess
import re
import sys
from playwright.sync_api import sync_playwright

# ============================================================
#    Turkish123 Downloader Master Edition (Final Expert Fix)
#    Made by Mustafa Acikbas | Version 2.1 (2026)
# ============================================================

LANGS = {
    "NL": {
        "made_by": "Gemaakt door: Mustafa Acikbas",
        "welcome": "--- BESCHIKBARE SERIES ---",
        "fetch_list": "[*] Bezig met ophalen van de lijst...",
        "search_prompt": "Kies een nummer (1 t/m {max}): ",
        "fetching_eps": "[*] Afleveringen zoeken voor {name}...",
        "available_eps": "\nBeschikbare afleveringen voor {name}:",
        "download_all": "0. ALLES DOWNLOADEN",
        "which_ep": "\nWelke wil je downloaden? (0 voor alles): ",
        "done": "\n[V] Klaar! Je bestanden zijn gedownload.",
        "searching_stream": "[*] Zoeken naar video-stream... Klik op 'Play' in de browser als de download niet start."
    },
    "EN": {
        "made_by": "Made by: Mustafa Acikbas",
        "welcome": "--- AVAILABLE SERIES ---",
        "fetch_list": "[*] Fetching the series list...",
        "search_prompt": "Choose a number (1 to {max}): ",
        "fetching_eps": "[*] Searching episodes for {name}...",
        "available_eps": "\nAvailable episodes for {name}:",
        "download_all": "0. DOWNLOAD ALL",
        "which_ep": "\nWhich one do you want to download? (0 for all): ",
        "done": "\n[V] Done! Your files have been downloaded.",
        "searching_stream": "[*] Extracting stream... Click 'Play' in the browser if it doesn't start."
    }
}

def download_with_ytdlp(m3u8_url, serie_name, ep_title):
    # EXTRA BEVEILIGING: Verwijder enters (\n, \r) en illegale Windows tekens uit namen
    def clean_string(text):
        text = text.replace('\n', ' ').replace('\r', '').strip()
        text = re.sub(r'[\\/*?:"<>|]', '', text) # Verwijder Windows verboden tekens
        text = re.sub(r'\s+', '_', text)         # Vervang spaties door underscores
        return text

    clean_serie = clean_string(serie_name)
    clean_ep = clean_string(ep_title)
    filename = f"{clean_serie}_{clean_ep}.mp4"
    
    # Voorkom extreem lange namen
    if len(filename) > 150:
        filename = filename[:140] + ".mp4"

    print(f"\n[*] Start download: {filename}")
    
    # Commando met de juiste headers om blokkades te voorkomen
    cmd = [
        "python", "-m", "yt_dlp", 
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "--referer", "https://ahs.turkish123.com/",
        "--no-check-certificate",
        "-o", filename, 
        m3u8_url
    ]
    subprocess.run(cmd)

def run():
    print("============================================================")
    print("    Turkish123 Downloader Master Edition")
    print("    Expert Verified & Clean Filename Version")
    print("============================================================\n")

    # Taalkeuze
    print("Select Language / Kies Taal: 1. NL | 2. EN")
    t = LANGS["EN"] 
    try:
        l_choice = input("Choice: ")
        t = LANGS["NL"] if l_choice == "1" else LANGS["EN"]
    except: pass

    print(f"\n>>> {t['made_by']} <<<")

    with sync_playwright() as p:
        # Browser openen (headless=False om Cloudflare vinkjes te kunnen zetten)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()

        # 1. Series Lijst ophalen
        print(f"\n{t['fetch_list']}")
        try:
            page.goto("https://ahs.turkish123.com/series-list/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector(".ml-item", timeout=10000)
        except:
            print("[!] Waarschuwing: Pagina laden duurt lang, we proberen de data te extraheren...")
        
        series_data = page.evaluate("""
            () => {
                const results = [];
                document.querySelectorAll('.ml-item a').forEach(a => {
                    const href = a.getAttribute('href');
                    const name = a.getAttribute('oldtitle') || a.innerText;
                    if (href && name) results.push({name: name.trim(), url: href});
                });
                return results;
            }
        """)

        all_series = {s['name']: s['url'] for s in series_data}
        sorted_names = sorted(all_series.keys())

        if not sorted_names:
            print("[X] Kon geen series vinden. Controleer je internetverbinding.")
            browser.close()
            return

        for i, name in enumerate(sorted_names, 1):
            # Verwijder enters uit de weergegeven naam voor een schone lijst
            display_name = name.replace('\n', ' ').strip()
            print(f"{i:3}. {display_name}")

        choice = int(input(f"\n{t['search_prompt'].format(max=len(sorted_names))}"))
        selected_name = sorted_names[choice - 1]
        selected_url = all_series[selected_name]

        # 2. Afleveringen zoeken
        print(f"\n{t['fetching_eps'].format(name=selected_name)}")
        try:
            page.goto(selected_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector(".les-title, .les-content, a[href*='episode']", timeout=15000)
        except: pass

        ep_data = page.evaluate("""
            () => {
                const links = Array.from(document.querySelectorAll('.les-title a, .les-content a, a[href*="episode"]'));
                return links.map(a => ({title: a.innerText.trim(), url: a.href}))
                            .filter((v,i,a) => v.title && a.findIndex(t => t.url === v.url) === i);
            }
        """)
        
        # Sorteer afleveringen (meestal staan ze omgekeerd op de site)
        ep_data.reverse()

        if not ep_data:
            print("[X] Geen afleveringen gevonden op deze pagina.")
            browser.close()
            return

        print(f"{t['available_eps'].format(name=selected_name)}")
        for i, ep in enumerate(ep_data, 1):
            # Ook hier enters verwijderen voor de weergave
            clean_title = ep['title'].replace('\n', ' ').strip()
            print(f"{i:2}. {clean_title}")

        ep_choice = int(input(f"{t['which_ep']}"))
        to_download = ep_data if ep_choice == 0 else [ep_data[ep_choice - 1]]

        # 3. Download Proces (Network Sniffing)
        for target in to_download:
            print(f"\n{t['searching_stream']}")
            m3u8_url = None

            def intercept(request):
                nonlocal m3u8_url
                if ".m3u8" in request.url and ("master" in request.url or "index" in request.url):
                    m3u8_url = request.url

            page.on("request", intercept)
            page.goto(target['url'], wait_until="domcontentloaded")

            # Wacht op m3u8 link (max 30s)
            end_time = time.time() + 30
            while not m3u8_url and time.time() < end_time:
                page.wait_for_timeout(1000)
                try: page.click(".play-button, #player, .video-content", timeout=500)
                except: pass

            if m3u8_url:
                print(f"[V] Stream link onderschept!")
                download_with_ytdlp(m3u8_url, selected_name, target['title'])
            else:
                print(f"[X] Kon de stream niet automatisch vinden voor {target['title']}.")

        browser.close()
        print(f"{t['done']}")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"\n[!] Er is een fout opgetreden: {e}")
    except KeyboardInterrupt:
        print("\n[!] Gestopt door gebruiker.")
