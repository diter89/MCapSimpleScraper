import requests
from bs4 import BeautifulSoup
from rich.console import Console
import re
import sys

console = Console()

def fetch_filtered(coin_id):
    url = f"https://coinmarketcap.com/id/currencies/{coin_id}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Diter89/2.0)"
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        console.print(f"[red]Gagal ambil data untuk:[/] {coin_id} (Status {r.status_code})")
        return

    soup = BeautifulSoup(r.text, "html.parser")
    lines = soup.get_text(separator="\n").splitlines()

    def find_first_rp():
        for line in lines:
            if "Rp" in line:
                match = re.search(r"Rp[\s ]?([\d.,]+)", line)
                if match:
                    return "Rp " + match.group(1)
        return "[gray]❌ Not Found[/gray]"

    def grab_rp_after(label, max_steps=6):
        for i, line in enumerate(lines):
            if label.lower() in line.lower():
                for j in range(1, max_steps):
                    if i + j < len(lines):
                        lookahead = lines[i + j].strip()
                        match = re.search(r"Rp[\s ]?([\d.,]+)", lookahead)
                        if match:
                            return "Rp " + match.group(1)
        return find_first_rp()

    def grab_exact(label, baris_ke=5):
        for i, line in enumerate(lines):
            if label.lower() in line.lower():
                idx = i + baris_ke
                if idx < len(lines):
                    match = re.search(r"Rp[\s ]?([\d.,]+)", lines[idx])
                    if match:
                        return "Rp " + match.group(1)
        return "[gray]❌ Not Found[/gray]"

    def grab_unit_after(label, max_steps=5):
        for i, line in enumerate(lines):
            if label.lower() in line.lower():
                for j in range(1, max_steps):
                    if i + j < len(lines):
                        val = lines[i + j].strip()
                        match = re.search(r"([\d.,]+\s?[MK]?)", val)
                        if match:
                            return match.group(1)
        return "[gray]❌ Not Found[/gray]"

    console.print(f"[bold cyan]🧠 Elux Scraper Result for [yellow]{coin_id.upper()}[/yellow][/bold cyan]")
    console.print(f"[green]Harga:[/] {grab_rp_after(f'{coin_id} price')}")
    console.print(f"[green]Market Cap:[/] {grab_rp_after('Kapitalisasi pasar')}")
    console.print(f"[green]Volume 24h:[/] {grab_rp_after('Volume (24j)')}")
    console.print(f"[green]FDV:[/] {grab_rp_after('FDV')}")
    console.print(f"[green]Supply Beredar:[/] {grab_unit_after('Suplai beredar')}")
    console.print(f"[green]ATH:[/] {grab_exact('Tertinggi sepanjang masa', 5)}")
    console.print(f"[green]ATL:[/] {grab_exact('Terendah sepanjang masa', 5)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[red]Contoh pakai:[/] python elux_scraper_v2.py [green]kinto[/green]")
    else:
        fetch_filtered(sys.argv[1])
