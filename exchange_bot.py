import requests, bs4, time
from fake_useragent import UserAgent

TICKET_TYPES = [
    # "day1/a", # vrijdag chill
    # "day1/b", # vrijdag relax
    # "day1/n", # vrijdag no camping
    # "day2/a", # zaterdag chill
    # "day2/b", # zaterdag relax
    # "day2/n", # zaterdag no camping
    # "day3/a", # zondag chill
    # "day3/b", # zondag relax
    # "day3/n", # zondag no camping
    "combi/a", # Combi chill
    "combi/b", # Combi relax
    "combi/n", # Combi no camping
]
CONTACT_DETAILS = [
    {
        "firstname": "Firstname",
        "lastname": "Lastname",
        "email": "email-adress@hotmail.com",
        "confirm": 1,
    }
]
REFRESH_TIMEOUT = 2
FORM_SUBMIT_TIMEOUT = 0.5
# gets the form data before submitting it, makes requests look more legit, probably not needed
GET_BEFORE_POST = True 
FORM_GET_TIMEOUT = 0.2


chrome = UserAgent().chrome
session = requests.Session()
headers = {
    "User-Agent": chrome,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Host": "tickets.pukkelpop.be",
    "Referer": "https://tickets.pukkelpop.be/nl/meetup/demand/",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
}


links_used = []
while True:
    time.sleep(REFRESH_TIMEOUT)
    for ticket_type in TICKET_TYPES:
        try:
            resp = session.get(f"https://tickets.pukkelpop.be/nl/meetup/demand/{ticket_type}/", headers=headers)
            resp.raise_for_status()
            main_soup = bs4.BeautifulSoup(resp.text, "html.parser")
            links = main_soup.findAll("a", {"class": "button -full -arrow -sp"})
            for link in main_soup.findAll("a", {"class": "button -full -arrow -sp"}):
                if not link.get("href") in links_used:
                    # add time to print
                    print("Found new link: " + link.get("href"))
                    form_url = link.get("href")
                    post_headers = {
                        "Referer": form_url,
                        "Content-Type": "application/x-www-form-urlencoded",
                        **headers,
                    }
                    for contact_detail in CONTACT_DETAILS:
                        if GET_BEFORE_POST:
                            time.sleep(FORM_GET_TIMEOUT)
                            print("Trying to get form for ticket")
                            session.get(form_url, headers=headers)
                        time.sleep(FORM_SUBMIT_TIMEOUT)
                        print("Trying to send form for " + contact_detail["email"])
                        resp = session.post(form_url, headers=post_headers, data=contact_detail)
                        print(resp.status_code)
                    links_used.append(link.get("href"))
        except Exception as ex:
            print(ex)
