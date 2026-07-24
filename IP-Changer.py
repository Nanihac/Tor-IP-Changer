import os
import sys
import time
import subprocess
import requests

# ANSI Color Codes
DEFAULT = "\033[0m"
GREEN = "\033[1;92m"
RED = "\033[1;91m"
YELLOW = "\033[1;93m"
YELLOW2 = "\033[1;33m"
ITALIC = "\033[3m"


def display_banner():
    banner = """
{4} █████ ███████████        █████████  █████   █████   █████████   ██████   █████   █████████  ██████████ ███████████{0}
{4}░░███ ░░███░░░░░███     ███░░░░░███░░███   ░░███   ███░░░░░███ ░░██████ ░░███   ███░░░░░███░░███░░░░░█░░███░░░░░███{0}
{4} ░███  ░███     ░███    ███     ░░░  ░███    ░███  ░███     ░███  ░███░███ ░███  ███     ░░░  ░███  █ ░  ░███     ░███{0}
{4} ░███  ░██████████    ░███          ░███████████  ░███████████  ░███░░███░███ ░███          ░██████    ░██████████{0}
{4} ░███  ░███░░░░░░     ░███          ░███░░░░░███  ░███░░░░░███  ░███ ░░██████ ░███    █████ ░███░░█    ░███░░░░░███{0}
{4} ░███  ░███           ░░███     ███ ░███    ░███  ░███     ░███  ░███  ░░█████ ░░███  ░░███  ░███ ░   █ ░███     ░███{0}
{4} █████ █████           ░░█████████  █████   █████ █████   █████ █████  ░░█████ ░░█████████  ██████████ █████   █████{0}
{4}░░░░░ ░░░░░              ░░░░░░░░░  ░░░░░   ░░░░░ ░░░░░   ░░░░░ ░░░░░    ░░░░░   ░░░░░░░░░  ░░░░░░░░░░ ░░░░░   ░░░░░{0}

                  {1}{5}================                                    {1}{5}======================
                    {3}{5}Version: {2}2.0{2}                                      {3}{5}Code Author: GUNJA RAHUL
                  {1}{5}================                                    {1}{5}======================
    """.format(
        DEFAULT, GREEN, RED, YELLOW, YELLOW2, ITALIC
    )
    print(banner)


def main():
    os.system("cls" if os.name == "nt" else "clear")

    if os.name == "posix" and os.geteuid() != 0:
        print(
            "\033[1;91m[!]\033[1;93m This script must be run with root privileges.\033[0m"
        )
        return

    tor_process = None
    tor_url = "https://archive.torproject.org/tor-package-archive/torbrowser/14.0.7/tor-expert-bundle-windows-x86_64-14.0.7.tar.gz"
    filename = "tor.tar.gz"
    default_extract_path = "tor_path.txt"
    extract_path = "."
    tor_path = ""

    url = "https://httpbin.org/ip"
    proxy = {
        "http": "socks5://127.0.0.1:9050",
        "https": "socks5://127.0.0.1:9050",
    }

    try:
        print("\033[1;34m[*] Checking if Tor is installed...\033[0m")
        time.sleep(1)

        if os.name == "posix":
            if (
                subprocess.run(
                    ["which", "tor"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                ).returncode
                != 0
            ):
                print(
                    "\033[1;91m[!]\033[1;93m Tor is not installed. Installing it...\033[0m"
                )
                if (
                    os.system(
                        "sudo apt update && sudo apt install tor -y > /dev/null 2>&1"
                    )
                    != 0
                ):
                    print(
                        "\033[1;91m[!]\033[1;93m Failed to install Tor!\n[!]\033[1;93m Please check your network connection.\033[0m"
                    )
                    return
                else:
                    print(
                        "\033[1;92m[+] Tor has been successfully installed.\033[0m"
                    )
                    time.sleep(1)
            else:
                print("\033[1;92m[+] Tor is already installed.\033[0m")
                time.sleep(1)

        elif os.name == "nt":
            if os.path.exists(default_extract_path):
                with open(default_extract_path, "r") as f:
                    extract_path = f.read().strip()

            tor_path = os.path.join(
                extract_path, "Tor Expert Bundle", "tor", "tor.exe"
            )

            if not os.path.exists(tor_path):
                print("\033[1;91m[!]\033[1;93m Tor is not installed.\033[0m")
                import tarfile
                import urllib.request

                try:
                    print(
                        f"\033[1;34m[*] Downloading Tor bundle from '{tor_url}'...\033[0m"
                    )
                    urllib.request.urlretrieve(tor_url, filename)
                    print("\033[1;92m[+] Download complete.\033[0m")
                except Exception as err:
                    sys.exit(f"\033[1;91m[-] Download Error: {err}\033[0m")

                user_choice = (
                    input(
                        f"\033[1;92m[>] Extract Tor to '{extract_path}' by default? (y/N) \xBB\033[0m\033[1;77m "
                    )
                    .strip()
                    .lower()
                )
                if user_choice in ["y", "yes"]:
                    extract_path = input(
                        "\033[1;92m[>] Enter extraction directory:\033[0m\033[1;77m "
                    ).strip()
                    if not os.path.exists(extract_path):
                        sys.exit(
                            f"\033[1;93m[!] Path '{extract_path}' does not exist.\033[0m"
                        )
                    elif not os.access(extract_path, os.W_OK):
                        sys.exit(
                            f"\033[1;91m[-] Path '{extract_path}' is not writable.\033[0m"
                        )

                try:
                    target_dir = os.path.join(
                        extract_path, "Tor Expert Bundle"
                    )
                    with tarfile.open(filename, "r:gz") as tar:
                        tar.extractall(target_dir)

                    if os.path.exists(filename):
                        os.remove(filename)

                    print(
                        f"\033[1;92m[+] Tor extracted to '{target_dir}'.\033[0m"
                    )
                    with open(default_extract_path, "w") as f:
                        f.write(extract_path)
                    time.sleep(2)
                except tarfile.ReadError:
                    sys.exit(
                        "\033[1;91m[-] Corrupted archive file.\033[0m"
                    )
            else:
                print("\033[1;92m[+] Tor is already installed.\033[0m")
                time.sleep(1)

        display_banner()

        # Check Tor Version
        try:
            if os.name == "posix":
                version = (
                    os.popen("tor --version")
                    .read()
                    .strip()
                    .split("\n")[0]
                    .split(" ")[2]
                )
                print(f"\033[1;34m[*] Tor version: {version}\033[0m")
            elif os.name == "nt":
                version = (
                    subprocess.run(
                        [tor_path, "--version"],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    .stdout.splitlines()[0]
                    .split(" ")[2]
                )
                print(f"\033[1;34m[*] Tor version: {version}\033[0m")
        except Exception:
            pass

        # Fetch initial direct IP
        try:
            response = requests.get(url, timeout=10)
            current_ip = response.json().get("origin")
            print(
                f"\033[1;34m[*] Original IP address: {current_ip}\033[0m"
            )
        except Exception:
            pass

        # Interval setup
        try:
            time_interval = int(
                input(
                    "\033[1;92m[>] Enter rotation interval (in seconds) \xBB\033[0m\033[1;77m "
                )
            )
            if time_interval <= 0:
                raise ValueError
        except ValueError:
            print(
                "\033[1;91m[!]\033[1;93m Interval must be a positive integer.\033[0m"
            )
            return

        print(
            f"\033[1;91m[!]\033[1;93m IP will change every {time_interval} seconds. Press Ctrl + C to stop.\033[0m"
        )
        time.sleep(1)

        # Service Startup
        print("\033[1;34m[*] Checking Tor connection...\033[0m")
        if os.name == "posix":
            status_check = subprocess.run(
                ["sudo", "service", "tor", "status"],
                capture_output=True,
                text=True,
            )
            if "Active: active" in status_check.stdout:
                print("\033[1;92m[+] Tor service is running.\033[0m")
            else:
                print(
                    "\033[1;93m[-] Starting Tor service...\033[0m"
                )
                subprocess.run(
                    ["sudo", "service", "tor", "start"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                time.sleep(3)
        elif os.name == "nt":
            tasklist = subprocess.run(
                ["tasklist"], capture_output=True, text=True
            ).stdout
            if "tor.exe" in tasklist:
                print("\033[1;92m[+] Tor process is running.\033[0m")
            else:
                print(
                    "\033[1;93m[-] Starting Tor process...\033[0m"
                )
                tor_process = subprocess.Popen(
                    [tor_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                time.sleep(3)

        # Main Loop
        while True:
            try:
                response = requests.get(url, proxies=proxy, timeout=15)
                changed_ip = response.json().get("origin")
                print(
                    f"\033[1;92m[+] New Tor IP address: {changed_ip}\033[0m"
                )
            except Exception:
                print(
                    "\033[1;91m[-] Error!\033[1;93m Failed to retrieve IP. Retrying...\033[0m"
                )

            time.sleep(time_interval)

            if os.name == "posix":
                subprocess.run(
                    "sudo service tor reload",
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            elif os.name == "nt":
                subprocess.run(
                    ["taskkill", "/F", "/IM", "tor.exe"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                tor_process = subprocess.Popen(
                    [tor_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )

    except KeyboardInterrupt:
        print("\n\033[1;91m[!]\033[1;93m Exiting...\033[0m")
        if os.name == "posix":
            print("\033[1;34m[*] Stopping Tor service...\033[0m")
            subprocess.run(
                ["sudo", "service", "tor", "stop"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif os.name == "nt" and tor_process:
            print("\033[1;34m[*] Stopping Tor process...\033[0m")
            tor_process.kill()


if __name__ == "__main__":
    main()
