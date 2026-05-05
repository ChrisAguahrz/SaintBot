#!/usr/bin/python
import os, pywikibot, time

DRY_RUN = False
SUMMARY = "Bot: Panua orodha ya watakatifu"
OLD_TEXT = "* [[Orodha ya Watakatifu Wafransisko]]"
NEW_TEXT = """* [[Orodha ya Watakatifu Mabradha wa Shule za Kikristo]]
* [[Orodha ya Watakatifu Waaugustino]]
* [[Orodha ya Watakatifu Wabazili]]
* [[Orodha ya Watakatifu Wabenedikto]]
* [[Orodha ya Watakatifu Wadominiko]]
* [[Orodha ya Watakatifu Wafransisko]]
* [[Orodha ya Watakatifu Wajesuiti]]
* [[Orodha ya Watakatifu Wakarmeli]]
* [[Orodha ya Watakatifu Wakolumbani]]
* [[Orodha ya Watakatifu Wamersedari]]
* [[Orodha ya Watakatifu Waoratori]]
* [[Orodha ya Watakatifu Wapasionisti]]
* [[Orodha ya Watakatifu Wapremontree]]
* [[Orodha ya Watakatifu Waredentori]]
* [[Orodha ya Watakatifu Wasalesiani]]
* [[Orodha ya Watakatifu Waskolopi]]
* [[Orodha ya Watakatifu Wateatini]]
* [[Orodha ya Watakatifu Watrinitari]]
* [[Orodha ya Watakatifu Watumishi wa Maria]]
* [[Orodha ya Watakatifu Wavinsenti]]"""

def main():
    username = os.getenv('WIKI_USERNAME', 'Gayle-Bot')
    password = os.getenv('WIKI_PASSWORD', 'CountryBot@it3ipj55bu65vg6vjq57i8dq4olhsrp2')
    site = pywikibot.Site("sw", "wikipedia")
    from pywikibot.login import ClientLoginManager
    lm = ClientLoginManager(site=site, user=username)
    lm.password = password
    lm.login()
    
    cat = pywikibot.Category(site, "Watakatifu Wakristo")
    pages = list(cat.articles(recurse=True))
    print(f"Found {len(pages)} pages")
    done = 0
    for page in pages:
        try:
            text = page.text
            if OLD_TEXT in text and text.count(OLD_TEXT) == 1:
                page.text = text.replace(OLD_TEXT, NEW_TEXT)
                page.save(summary=SUMMARY, minor=False)
                done += 1
                print(f"{page.title()}: done")
                time.sleep(5)
        except Exception as e:
            print(f"{page.title()}: error - {e}")
    print(f"Finished. Changed {done} pages.")

if __name__ == "__main__":
    main()
