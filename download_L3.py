import datetime
from bs4 import BeautifulSoup
import requests
import re
import subprocess
from config import base_url_l3


def download_l3():
    """
    Function to download Level 3 soil moisture data from NASA LPRM AMSR2 DS for current month.
    Keeps track of files already downloaded in downloaded_l3.txt
    """

    # Generating links
    base_url = base_url_l3
    d = datetime.datetime.now()
    year = str(d.year)
    month = f"{d:%m}"
    date = f"{d:%d}"
    base_url = base_url + year + "/" + month + "/"
    page = requests.get(base_url).text
    soup = BeautifulSoup(page, "html.parser")
    links = soup.find_all("a")
    links = [i.get("href") for i in links]
    links = [i for i in links if re.search("[a-zA-Z0-9]+.nc4$", i)]
    links = list(set(links))
    links = [base_url + i for i in links]
    # LPRM data has 1 day lag, so if its first day of the month, we need to download from the previous month
    if date == "01":
        today = datetime.date.today()
        first = today.replace(day=1)
        last = first - datetime.timedelta(days=1)
        lmonth = f"{last:%m}"
        lday = f"{last:%d}"
        print(lmonth, lday)
        last_url = base_url + year + "/" + lmonth + "/"
        print(last_url)
        if month == "01":
            lyear = str(last.year)
            print(lyear)
            last_url = base_url + lyear + "/" + lmonth + "/"
        page = requests.get(last_url).text
        soup = BeautifulSoup(page, "html.parser")
        oldlinks = soup.find_all("a")
        oldlinks = [i.get("href") for i in oldlinks]
        oldlinks = [i for i in oldlinks if re.search("[a-zA-Z0-9]+.nc4$", i)]
        oldlinks = list(set(oldlinks))
        oldlinks = [last_url + i for i in oldlinks]
        oldlinks = sorted(oldlinks)
        lastday = oldlinks[-1]
        print(lastday)
        links.append(lastday)
    urls = []
    try:
        with open("downloaded_l3.txt", "r") as f:
            for url in f:
                url = url.strip()
                urls.append(url)
    except:
        with open("downloaded_l3.txt", "a") as f:
            to_write = "\n".join(links)
            f.write(to_write)
    links = [i for i in links if i not in urls]
    links = sorted(links)
    if len(links) != 0:
        with open("downloaded_l3.txt", "a") as f:
            urls = "\n".join(links)
            f.write(urls)
            f.write("\n")
    # downloading files
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
