import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def check_https(url):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        response = requests.get(url, timeout=5)
        if response.url.startswith("https://"):
            console.print(f"[✓] [bold green]HTTPS is enabled for {url}[/bold green]")
        else:
            console.print(f"[!] [bold yellow]HTTPS not enforced[/bold yellow]")
    except Exception as e:
        console.print(f"[x] [bold red]Error checking HTTPS:[/bold red] {e}")

def check_privacy_policy(url):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        found = False
        for link in soup.find_all('a', href=True):
            link_text = link.text.strip().lower()
            if "privacy" in link_text or "data protection" in link_text:
                console.print(f"[✓] [bold green]Privacy policy link found:[/bold green] {link['href']}")
                found = True
                break
        if not found:
            console.print("[!] [bold yellow]No privacy policy link found[/bold yellow]")
    except Exception as e:
        console.print(f"[x] [bold red]Error checking privacy policy:[/bold red] {e}")

def check_cookie_banner(url):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        cookie_keywords = ["cookie", "accept", "consent", "gdpr"]
        found = False
        for div in soup.find_all(['div', 'section', 'footer']):
            text = div.get_text().lower()
            if any(keyword in text for keyword in cookie_keywords):
                console.print(f"[✓] [bold green]Possible cookie banner detected[/bold green]")
                found = True
                break
        if not found:
            console.print("[!] [bold yellow]No cookie banner detected[/bold yellow]")
    except Exception as e:
        console.print(f"[x] [bold red]Error checking cookie banner:[/bold red] {e}")

def check_security_headers(url):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        expected_headers = {
            "Content-Security-Policy": "Protects against XSS and data injection",
            "X-Frame-Options": "Prevents clickjacking",
            "Strict-Transport-Security": "Enforces HTTPS",
            "X-Content-Type-Options": "Prevents MIME-sniffing",
            "Referrer-Policy": "Controls what data is sent in Referer header"
        }

        console.print("\n[bold underline]Security Headers Check:[/bold underline]")

        for header, purpose in expected_headers.items():
            if header in headers:
                console.print(f"[✓] [bold green]{header}[/bold green] is set ✔ — {purpose}")
            else:
                console.print(f"[!] [bold yellow]{header}[/bold yellow] is missing ⚠ — {purpose}")

    except Exception as e:
        console.print(f"[x] [bold red]Error checking headers:[/bold red] {e}")

if __name__ == "__main__":
    console.print(Markdown("# 🛡️ UK GDPR Compliance Checker CLI Tool"))
    site = input("Enter website (without https): ")
    check_https(site)
    check_privacy_policy(site)
    check_cookie_banner(site)
    check_security_headers(site)
