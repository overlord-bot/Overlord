import os

from dotenv import load_dotenv
import vt


# Checks the safety of a link by running it through VirusTotal's api. Returns True if safe and False if unsafe.
def test_function(link):
    print(f"---------------- Scanning {link} --------------")

    load_dotenv()
    vt_token = os.getenv("VT_TOKEN")

    if not vt_token:
        print(f"ERROR no Virus Total API Key, cannot process the safety of link: {link}")
        return False  # no API key, so link is unchecked, therefore not safe by default

    print("Opening Virus Total Client")
    client = vt.Client(vt_token)

    url_id = vt.url_id(link)
    url = client.get_object(f"/urls/{url_id}")
    recent_stats = url.last_analysis_stats

    print(f"Times link has been submitted for scan: {url.times_submitted}")
    print(f"Result of last scan: {recent_stats}")  # format {'harmless': 61, 'malicious': 0, 'suspicious': 1, 'timeout': 0, 'undetected': 8}

    client.close()
    print("Closed Virus Total Client")

    if recent_stats["malicious"] > 0:
        print(f"-------------------- Link is malicious. Ending scan. ------------------------")
        return False
    else:
        print(f"----------------------- Link is safe. Ending scan. --------------------------")
        return True


test_function("https://myanimelist.net/anime/29803/Overlord")
