import click
import requests
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()

def fetch_and_debug(url, labels):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Diter89/1.5)"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    lines = soup.get_text(separator="\n").splitlines()

    def debug_label(label):
        for i, line in enumerate(lines):
            if label.lower() in line.lower():
                console.rule(f"🔍 {label}")
                for j in range(1, 10):  # ambil 10 baris ke bawahnya
                    if i + j < len(lines):
                        baris = lines[i + j].strip()
                        if "Rp" in baris or "US$" in baris:
                            console.print(f"[green]{j:02d}: {baris}[/green]")
                        else:
                            console.print(f"[dim]{j:02d}: {baris}[/dim]")
                console.rule()

    for label in labels:
        debug_label(label)

@click.command()
@click.option('-u', '--url', help='URL dari halaman yang akan dianalisis', required=True)
@click.option('-db', '--debug_labels', help='Label yang ingin dicari, pisahkan dengan //', required=True)
def cli(url, debug_labels):
    label_list = [lbl.strip() for lbl in debug_labels.split("//") if lbl.strip()]
    fetch_and_debug(url, label_list)

if __name__ == '__main__':
    cli()
