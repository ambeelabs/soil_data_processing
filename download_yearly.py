from bs4 import BeautifulSoup
import requests
import re
import subprocess
from pprint import pprint


def download_yearly(year):
    """
    Function to bulk download yearly soil data

    Args:
    year: year in string
    """
    base_url = (
        "https://hydro1.gesdisc.eosdis.nasa.gov/data/WAOB/LPRM_AMSR2_DS_A_SOILM3.001/"
    )
    months = [f"{i:02d}" for i in range(1, 13)]
    year = str(year)
    base_urls = []
    for month in months:
        final_url = base_url + year + "/" + month + "/"
        base_urls.append(final_url)
    for base_url in base_urls:
        page = requests.get(base_url).text
        soup = BeautifulSoup(page, "html.parser")
        links = soup.find_all("a")
        links = [i.get("href") for i in links]
        links = [i for i in links if re.search("[a-zA-Z0-9]+.nc4$", i)]
        links = list(set(links))
        links = [base_url + i for i in links]
        urls = []
        try:
            with open("downloaded_yearly.txt", "r") as f:
                for url in f:
                    url = url.strip()
                    urls.append(url)
        except:
            with open("downloaded_yearly.txt", "a") as f:
                to_write = "\n".join(links)
                f.write(to_write)
        links = [i for i in links if i not in urls]
        links = sorted(links)
        if len(links) != 0:
            with open("downloaded_yearly.txt", "a") as f:
                urls = "\n".join(links)
                f.write(urls)
                f.write("\n")
        pprint(links)
        try:
            for i in links:
                command = (
                    "wget --load-cookies .urs_cookies --save-cookies .urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition "
                    + i
                )
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
        except Exception as e:
            print(e)
        for i in links:
            print(i)
