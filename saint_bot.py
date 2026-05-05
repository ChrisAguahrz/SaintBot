#!/usr/bin/python
import os, pywikibot, time, re

DRY_RUN = False
SUMMARY = "Bot: Panua orodha ya watakatifu katika sehemu ya 'Tazama pia'"
OLD_TEXT = "* [[Orodha ya Watakatifu Wafransisko]]"
SAINT_LINKS = [
    "Mabradha wa Shule za Kikristo", "Waaugustino", "Wabazili", "Wabenedikto",
    "Wadominiko", "Wafransisko", "Wajesuiti", "Wakarmeli", "Wakolumbani",
    "Wamersedari", "Waoratori", "Wapasionisti", "Wapremontree", "Waredentori",
    "Wasalesiani", "Waskolopi", "Wateatini", "Watrinitari", "Watumishi wa Maria", "Wavinsenti"
]
READ_DELAY = 2
EDIT_DELAY = 5

def get_page_saint_category(page):
    title_lower = page.title().lower()
    for saint in SAINT_LINKS:
        if saint.lower() in title_lower:
            return saint
    return None

def build_new_links(exclude_saint=None):
    links = []
    for saint in SAINT_LINKS:
        if exclude_saint and saint.lower() == exclude_saint.lower():
            continue
        links.append(f"* [[Orodha ya Watakatifu {saint}]]")
    return "\n".join(links)

def process_page(page):
    text = page.text
    if OLD_TEXT not in text:
        return False
    page_saint = get_page_saint_category(page)
    new_links = build_new_links(page_saint)
    new_text = text.replace(OLD_TEXT, "")
    for saint in SAINT_LINKS:
        link = f"* [[Orodha ya Watakatifu {saint}]]"
        new_text = new_text.replace(link, "")
    new_text = re.sub(r'\n{3,}', '\n\n', new_text)
    if "== Tazama pia ==" in new_text:
        new_text = new_text.replace("== Tazama pia ==", "== Tazama pia ==\n" + new_links)
    elif "==Tazama pia==" in new_text:
        new_text = new_text.replace("==Tazama pia==", "==Tazama pia==\n" + new_links)
    else:
        new_text = new_text.rstrip() + "\n\n== Tazama pia ==\n" + new_links + "\n"
    if new_text == text:
        return False
    page.text = new_text
    page.save(summary=SUMMARY, minor=False)
    return True

def main():
    username = os.getenv('WIKI_USERNAME', 'Gayle-Bot')
    password = os.getenv('WIKI_PASSWORD', 'CountryBot@it3ipj55bu65vg6vjq57i8dq4olhsrp2')
    site = pywikibot.Site("sw", "wikipedia")
    from pywikibot.login import ClientLoginManager
    lm = ClientLoginManager(site=site, user=username)
    lm.password = password
    lm.login()
    seen_pages = set()
    done = 0
    
    print("=== PHASE 1 ===")
    main_cat = pywikibot.Category(site, "Watakatifu Wakristo")
    for subcat in main_cat.subcategories():
        print(f"  {subcat.title()}")
        time.sleep(READ_DELAY)
        for page in subcat.articles():
            if page.title() in seen_pages:
                continue
            seen_pages.add(page.title())
            try:
                if process_page(page):
                    done += 1
                    print(f"    {page.title()}: done")
                    time.sleep(EDIT_DELAY)
            except Exception as e:
                print(f"    {page.title()}: error - {e}")
    
    print("=== PHASE 2 ===")
    for cat_name in ["Wakristo", "Ukristo"]:
        cat = pywikibot.Category(site, cat_name)
        for page in cat.articles(recurse=True):
            if page.title() in seen_pages:
                continue
            seen_pages.add(page.title())
            try:
                if process_page(page):
                    done += 1
                    print(f"  {page.title()}: done")
                    time.sleep(EDIT_DELAY)
            except Exception as e:
                print(f"  {page.title()}: error - {e}")
    
    print("=== PHASE 3 ===")
    for cat_page in site.allcategories(prefix="Watakatifu"):
        cat = pywikibot.Category(site, cat_page.title())
        for page in cat.articles():
            if page.title() in seen_pages:
                continue
            seen_pages.add(page.title())
            try:
                if process_page(page):
                    done += 1
                    print(f"  {page.title()}: done")
                    time.sleep(EDIT_DELAY)
            except Exception as e:
                print(f"  {page.title()}: error - {e}")
    
    print("=== PHASE 4 ===")
    for page in site.allpages(namespace=0):
        if page.title() in seen_pages:
            continue
        seen_pages.add(page.title())
        try:
            if process_page(page):
                done += 1
                print(f"  {page.title()}: done")
                time.sleep(EDIT_DELAY)
        except Exception as e:
            print(f"  {page.title()}: error - {e}")
    
    print(f"Done. Edited {done} pages.")

if __name__ == "__main__":
    main()
