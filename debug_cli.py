import click
import requests
from bs4 import BeautifulSoup

@click.command()
@click.option('-u', '--url', required=True, help='URL target halaman')
@click.option('-db', '--debug', default='', help='Mode debug untuk pencarian teks tertentu')
def debug_page(url, debug):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    print(f"🔍 Mengambil halaman: {url}")
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    all_text = [t.get_text(strip=True) for t in soup.find_all(['span', 'div']) if t.get_text(strip=True)]

    if debug:
        filtered = [t for t in all_text if debug.lower() in t.lower()]
        print(f"\n🎯 Hasil Debug untuk: '{debug}'\n{filtered}")
    else:
        print(f"\n📦 Total Elemen Terbaca: {len(all_text)}\n")
        for i, t in enumerate(all_text):
            print(f"[{i}] {t}")

if __name__ == '__main__':
    debug_page()
