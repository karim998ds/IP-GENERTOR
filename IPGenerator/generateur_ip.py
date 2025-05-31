import random
import time
import os
import requests
from colorama import init, Fore, Style

init(autoreset=True)

WEBHOOK_URL = "https://discord.com/api/webhooks/1234567890"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def loading_bar(duration=2, text="Chargement"):
    print(Fore.CYAN + Style.BRIGHT + f"\n[{text}]".center(60))
    for i in range(31):
        time.sleep(duration / 30)
        bar = ("█" * i).ljust(30)
        percent = int(i * 100 / 30)
        print(Fore.GREEN + f"\r[{bar}] {percent}%", end="")
    print("\n")

def print_banner():
    clear()
    print(Fore.MAGENTA + Style.BRIGHT)
    print("╔" + "═" * 60 + "╗")
    print("║" + " " * 60 + "║")
    print("║" + " 🛰️  Générateur & Info IP  🛰️ ".center(60) + "║")
    print("║" + " " * 60 + "║")
    print("╚" + "═" * 60 + "╝\n" + Style.RESET_ALL)

def print_menu():
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT)
    print("╔══════════════════════════════════════╗")
    print("║              MENU PRINCIPAL          ║")
    print("╠══════════════════════════════════════╣")
    print("║ 1. Générer des IP publiques          ║")
    print("║ 2. Quitter                          ║")
    print("╚══════════════════════════════════════╝")
    print(Style.RESET_ALL)

def is_public_ip(ip):
    parts = list(map(int, ip.split('.')))
    if parts[0] == 10:
        return False
    if parts[0] == 172 and 16 <= parts[1] <= 31:
        return False
    if parts[0] == 192 and parts[1] == 168:
        return False
    if parts[0] == 127:
        return False
    if parts[0] == 0:
        return False
    if parts[0] >= 224:
        return False
    return True

def generate_public_ip():
    while True:
        ip = ".".join(str(random.randint(1, 223)) for _ in range(4))
        if is_public_ip(ip):
            return ip

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,query,lat,lon,timezone,mobile,proxy,hosting", timeout=5)
        data = response.json()
        if data.get("status") == "success":
            return data
    except:
        pass
    return None

def send_ip_to_webhook(ip_info):
    if ip_info is None:
        return
    embed = {
        "title": f"📡 Infos IP: {ip_info['query']}",
        "color": 0x00ffdd,
        "fields": [
            {"name": "Pays", "value": ip_info.get("country", "N/A"), "inline": True},
            {"name": "Région", "value": ip_info.get("regionName", "N/A"), "inline": True},
            {"name": "Ville", "value": ip_info.get("city", "N/A"), "inline": True},
            {"name": "Fournisseur (ISP)", "value": ip_info.get("isp", "N/A"), "inline": False},
            {"name": "Fuseau horaire", "value": ip_info.get("timezone", "N/A"), "inline": True},
            {"name": "Mobile ?", "value": str(ip_info.get("mobile", "N/A")), "inline": True},
            {"name": "Proxy ?", "value": str(ip_info.get("proxy", "N/A")), "inline": True},
            {"name": "Hosting ?", "value": str(ip_info.get("hosting", "N/A")), "inline": True},
            {"name": "Latitude", "value": str(ip_info.get("lat", "N/A")), "inline": True},
            {"name": "Longitude", "value": str(ip_info.get("lon", "N/A")), "inline": True},
        ],
        "footer": {"text": "🛰️ Généré par Script IP Info • by ChatGPT"}
    }
    payload = {"embeds": [embed]}
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code not in (200, 204):
            print(Fore.RED + f"❌ Erreur webhook: code {response.status_code}")
        else:
            print(Fore.GREEN + f"✅ Envoyé: {ip_info['query']}")
    except Exception as e:
        print(Fore.RED + f"❌ Exception webhook: {e}")

def generate_ips_flow():
    print(Fore.YELLOW + Style.BRIGHT + "🟡 Saisissez le nombre d'IP à générer (1 à 10) : ")
    count = input(Fore.CYAN + ">> ").strip()
    while not count.isdigit() or int(count) < 1 or int(count) > 10:
        print(Fore.RED + "❌ Entrée invalide. Veuillez entrer un nombre entre 1 et 10.")
        count = input(Fore.CYAN + ">> ").strip()
    count = int(count)

    print("\n" + Fore.MAGENTA + Style.BRIGHT + f"Lancement de la génération pour {count} IP(s)...\n")

    for i in range(1, count + 1):
        print(Fore.LIGHTBLUE_EX + f"[{i}/{count}] Génération d'une IP publique...")
        ip = generate_public_ip()
        print(Fore.LIGHTGREEN_EX + f"   ➜ IP générée: {ip}")
        print(Fore.LIGHTBLUE_EX + "   Récupération des informations...")
        info = get_ip_info(ip)
        if info:
            send_ip_to_webhook(info)
        else:
            print(Fore.RED + "   ⚠️ Échec récupération info IP.")
        time.sleep(1)
        print()

def main():
    while True:
        print_banner()
        print_menu()
        choice = input(Fore.CYAN + "Votre choix > ").strip()
        if choice == "1":
            clear()
            loading_bar(1.5, "Préparation")
            generate_ips_flow()
            input(Fore.LIGHTBLACK_EX + "\nAppuyez sur Entrée pour revenir au menu...")
            clear()
        elif choice == "2":
            print(Fore.LIGHTMAGENTA_EX + "👋 Merci et à bientôt !")
            break
        else:
            print(Fore.RED + "❌ Choix invalide. Réessayez.")
            time.sleep(1)
            clear()

if __name__ == "__main__":
    main()
