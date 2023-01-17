import datetime
from bs4 import BeautifulSoup
import requests
import re
import subprocess
from config import base_url_l2


def download_l2():
    """
    Function to download Level 2 soil moisture data from NASA LPRM AMSR2 DS for current day.
    Keeps track of files already downloaded in downloaded_l2.txt
    Keeps track of days already processsed in {year}_doys.txt
    """

    # Generating links to be downloaded
    base_url = base_url_l2
    d = datetime.datetime.now()
    year = str(d.year)
    base_url = base_url + year + "/"
    page = requests.get(base_url).text
    soup = BeautifulSoup(page, "html.parser")
    links_doy = soup.find_all("a")
    links_doy = [i.get("href") for i in links_doy]
    links_doy = [i for i in links_doy if re.search("^[0-9]+", i)]
    links_doy = sorted(list(set(links_doy)))
    print(links_doy)
    doys = []
    filename = year + "_doys.txt"
    try:
        with open(filename, "r") as f:
            for url in f:
                url = url.strip()
                doys.append(url)
    except:
        with open(filename, "a") as f:
            to_write = "\n".join(links_doy)
            f.write(to_write)
    links_doy = [i for i in links_doy if i not in doys[:-7]]
    links_doy = [base_url + i for i in links_doy]
    for i in links_doy:
        print(i)
    links = []
    for i in links_doy:
        page = requests.get(i).text
        soup = BeautifulSoup(page, "html.parser")
        temp = soup.find_all("a")
        temp = [i.get("href") for i in temp]
        temp = [i for i in temp if re.search("^LPRM-AMSR2_L2_DS_A_SOILM2_.+.nc4$", i)]
        temp = sorted(list(set(temp)))
        links.extend([i + j for j in temp])
    urls = []
    try:
        with open("downloaded_l2.txt", "r") as f:
            for url in f:
                url = url.strip()
                urls.append(url)
    except:
        with open("downloaded_l2.txt", "a") as f:
            to_write = "\n".join(links)
            f.write(to_write)
    links = [i for i in links if i not in urls]
    if len(links) != 0:
        with open("downloaded_l2.txt", "a") as f:
            urls = "\n".join(links)
            f.write(urls)
            f.write("\n")
    # Downloading the files
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
