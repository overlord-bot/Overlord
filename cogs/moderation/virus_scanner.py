import os

from dotenv import load_dotenv
import vt


# Checks the safety of a link by running it through VirusTotal's api. Returns True if safe and False if unsafe.
async def scan_link(link):
    print(f"---------------- Virus Scan for: {link} --------------")

    load_dotenv()
    vt_token = os.getenv("VT_TOKEN")

    if not vt_token:
        print(f"ERROR no Virus Total API Key, cannot process the safety of link: {link}")
        return False  # no API key, so link is unchecked, therefore not safe by default

    print("Opening Virus Total Client")
    vt_client = vt.Client(vt_token)

    url_id = vt.url_id(link)
    url = vt_client.get_object(f"/urls/{url_id}")
    # if url.times_submitted < 100:
    #     client.scan_url(link, wait_for_completion=True)
    #     url = client.get_object(f"/urls/{url_id}")

    print(f"Times link has been submitted for scan: {url.times_submitted}")
    print(f"Result of last scan: {url.last_analysis_stats}")  # format {'harmless': 61, 'malicious': 0, 'suspicious': 1, 'timeout': 0, 'undetected': 8}

    vt_client.close()
    print("Closed Virus Total Client")

    if url.last_analysis_stats["malicious"] > 0:
        print(f"-------------------- Link is malicious, ending scan. ------------------------")
        return False
    else:
        print(f"----------------------- Link is safe, ending scan. --------------------------")
        return True


# scan_link("https://myanimelist.net/anime/29803/Overlord")