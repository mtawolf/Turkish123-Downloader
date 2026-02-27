import time
import subprocess
import re
from playwright.sync_api import sync_playwright

# ============================================================
#   Turkish123 Downloader Master Edition
#   Made by Mustafa Acikbas
#   GitHub: https://github.com/mtawolf
# ============================================================

LANGS = {
    "NL": {
        "made_by": "Gemaakt door: Mustafa Acikbas",
        "welcome": "--- BESCHIKBARE SERIES ---",
        "fetch_list": "[*] Bezig met ophalen van de volledige lijst...",
        "search_prompt": "Kies een nummer (1 t/m {max}): ",
        "fetching_eps": "[*] Afleveringen zoeken voor {name}...",
        "available_eps": "\nBeschikbare afleveringen voor {name}:",
        "download_all": "0. ALLES DOWNLOADEN",
        "which_ep": "\nWelke wil je downloaden? (0 voor alles): ",
        "done": "\n[V] Klaar! Je bestanden zijn gedownload."
    },
    "EN": {
        "made_by": "Made by: Mustafa Acikbas",
        "welcome": "--- AVAILABLE SERIES ---",
        "fetch_list": "[*] Fetching the complete series list...",
        "search_prompt": "Choose a number (1 to {max}): ",
        "fetching_eps": "[*] Searching episodes for {name}...",
        "available_eps": "\nAvailable episodes for {name}:",
        "download_all": "0. DOWNLOAD ALL",
        "which_ep": "\nWhich one do you want to download? (0 for all): ",
        "done": "\n[V] Done! Your files have been downloaded."
    },
    "DE": {
        "made_by": "Erstellt von: Mustafa Acikbas",
        "welcome": "--- VERFÜGBARE SERIEN ---",
        "fetch_list": "[*] Abrufen der vollständigen Serienliste...",
        "search_prompt": "Wähle eine Nummer (1 bis {max}): ",
        "fetching_eps": "[*] Suche Episoden für {name}...",
        "available_eps": "\nVerfügbare Episoden für {name}:",
        "download_all": "0. ALLES HERUNTERLADEN",
        "which_ep": "\nWelche möchtest du herunterladen? (0 für alle): ",
        "done": "\n[V] Fertig! Deine Dateien wurden heruntergeladen."
    },
    "FR": {
        "made_by": "Créé par : Mustafa Acikbas",
        "welcome": "--- SÉRIES DISPONIBLES ---",
        "fetch_list": "[*] Récupération de la liste complète des séries...",
        "search_prompt": "Choisissez un numéro (1 à {max}) : ",
        "fetching_eps": "[*] Recherche d'épisodes pour {name}...",
        "available_eps": "\nÉpisodes disponibles pour {name} :",
        "download_all": "0. TOUT TÉLÉCHARGER",
        "which_ep": "\nLequel voulez-vous télécharger ? (0 pour tous) : ",
        "done": "\n[V] Terminé ! Vos fichiers ont été téléchargés."
    }
}

def download_with_ytdlp(m3u8_url, serie_name, ep_num):
    clean_name = re.sub(r'[^\w\s-]', '', serie_name).strip().replace(' ', '_')
    filename = f"{clean_name}_S01E{ep_num}.mp4"
    print(f"\n[*] Start download: {filename}")
    subprocess.run(["python", "-m", "yt_dlp", "-o", filename, m3u8_url])

def run():
    print("============================================================")
    print("   Turkish123 Downloader Master Edition")
    print("   Made by Mustafa Acikbas | https://github.com/mtawolf")
    print("============================================================\n")

    print("Select Language / Kies Taal / Sprache Wählen / Choisir la Langue:")
    print("1. Nederlands (NL)\n2. English (EN)\n3. Deutsch (DE)\n4. Français (FR)")
    
    try:
        lang_choice = input("Choice (1-4): ")
        lang_key = ["NL", "EN", "DE", "FR"][int(lang_choice)-1]
    except:
        lang_key = "EN"
    
    t = LANGS[lang_key]
    print(f"\n>>> {t['made_by']} <<<") # Naam herhalen in gekozen taal

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Headless=True voor CasaOS/Docker
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0")
        page = context.new_page()

        print(f"{t['fetch_list']}")
        page.goto("https://ahs.turkish123.com/series-list/", wait_until="networkidle")
        
        series_data = page.evaluate("""
            () => {
                const results = [];
                document.querySelectorAll('.ml-item a').forEach(a => {
                    const href = a.getAttribute('href');
                    const name = a.getAttribute('oldtitle');
                    if (href && name) results.push({name: name, url: href});
                });
                return results;
            }
        """)

        all_series = {s['name']: s['url'] for s in series_data}
        sorted_names = sorted(all_series.keys())

        print(f"\n{t['welcome']}")
        for i, name in enumerate(sorted_names, 1):
            print(f"{i:3}. {name}")

        keuze_nr = int(input(f"\n{t['search_prompt'].format(max=len(sorted_names))}"))
        selected_name = sorted_names[keuze_nr - 1]
        selected_url = all_series[selected_name]

        # ... (Rest van de download logica zoals voorheen)
        browser.close()

if __name__ == "__main__":
    run()