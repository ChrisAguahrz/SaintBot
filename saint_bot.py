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

SUBCATEGORIES = [
    "Watakatifu wa Afrika Kusini", "Watakatifu wa Argentina", "Watakatifu wa Australia",
    "Watakatifu wa Afrika Kaskazini", "Watakatifu wa Albania", "Watakatifu wa Algeria",
    "Watakatifu wa Armenia", "Watakatifu wa Austria", "Watakatifu wa Bosnia na Herzegovina",
    "Watakatifu wa Belarus", "Watakatifu wa Brazil", "Watakatifu wa Bulgaria",
    "Watakatifu wa Chile", "Watakatifu wa China", "Watakatifu wa Cuba",
    "Watakatifu wa Denmark", "Watakatifu wa Ekwador", "Watakatifu wa El Salvador",
    "Watakatifu wa Eritrea", "Watakatifu wa Ethiopia", "Watakatifu wa Ghana",
    "Watakatifu wa Georgia", "Watakatifu wa Gwatemala", "Watakatifu wa Hispania",
    "Watakatifu wa Hungaria", "Watakatifu wa India", "Watakatifu wa Irak",
    "Watakatifu wa Ireland", "Watakatifu wa Israeli", "Watakatifu wa Italia",
    "Watakatifu wa Japani", "Watakatifu wa Kanada", "Watakatifu wa Katar",
    "Watakatifu wa Kolombia", "Watakatifu wa Korasya", "Watakatifu wa Korea",
    "Watakatifu wa Kupro", "Watakatifu wa Luxemburg", "Watakatifu wa Lebanoni",
    "Watakatifu wa Libya", "Watakatifu wa Lituania", "Watakatifu wa Madagaska",
    "Watakatifu wa Malta", "Watakatifu wa Mesopotamia", "Mabikira",
    "Watakatifu wa Marekani", "Watakatifu wa Masedonia Kaskazini",
    "Watakatifu wa Meksiko", "Watakatifu wa Misri", "Watakatifu wa Montenegro",
    "Watakatifu wa Moroko", "Watakatifu wa Norwei", "Watakatifu wa Oceania",
    "Watakatifu wa Papua Guinea Mpya", "Watakatifu wa Paraguay",
    "Watakatifu wa Palestina", "Watakatifu wa Peru", "Watakatifu wa Polandi",
    "Watakatifu wa Romania", "Watakatifu wa Saudia", "Watakatifu wa Slovenia",
    "Watakatifu wa Sri Lanka", "Watakatifu wa San Marino", "Watakatifu wa Serbia",
    "Watakatifu wa Siria", "Watakatifu wa Sudan", "Watakatifu wa Tanzania",
    "Watakatifu wa Tunisia", "Watakatifu wa Uajemi", "Watakatifu wa Ufini",
    "Watakatifu wa Uruguay", "Watakatifu wa Ubelgiji", "Watakatifu wa Ucheki",
    "Watakatifu wa Ufaransa", "Watakatifu wa Ufilipino", "Watakatifu wa Uganda",
    "Watakatifu wa Ugiriki", "Watakatifu wa Uholanzi", "Watakatifu wa Uingereza",
    "Watakatifu wa Ujerumani", "Watakatifu wa Ukraine", "Watakatifu wa Ureno",
    "Watakatifu wa Urusi", "Watakatifu wa Uskoti", "Watakatifu wa Uswidi",
    "Watakatifu wa Uswisi", "Watakatifu wa Uturuki", "Watakatifu wa Venezuela",
    "Watakatifu wa Vietnam", "Wafiadini Wakristo", "Watakatifu wa Latvia",
    "Watakatifu wa Slovakia", "Watakatifu wa Wales", "Watakatifu wa Yemen",
    "Watakatifu wa Yordani", "Yurodivy"
]

def build_new_links():
    return "\n".join([f"* [[Orodha ya Watakatifu {s}]]" for s in sorted(SAINT_LINKS)])

def process_page(page):
    text = page.text
    if OLD_TEXT not in text:
        return False
    new_text = text.replace(OLD_TEXT, "")
    for saint in SAINT_LINKS:
        new_text = new_text.replace(f"* [[Orodha ya Watakatifu {saint}]]", "")
    new_text = re.sub(r'\n{3,}', '\n\n', new_text)
    links = build_new_links()
    if "== Tazama pia ==" in new_text:
        new_text = new_text.replace("== Tazama pia ==", "== Tazama pia ==\n" + links)
    elif "==Tazama pia==" in new_text:
        new_text = new_text.replace("==Tazama pia==", "==Tazama pia==\n" + links)
    else:
        new_text = new_text.rstrip() + "\n\n== Tazama pia ==\n" + links + "\n"
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
    
    seen = set()
    done = 0
    
    for cat_name in SUBCATEGORIES:
        cat = pywikibot.Category(site, cat_name)
        print(f"Category: {cat_name}")
        try:
            pages = list(cat.articles())
            print(f"  {len(pages)} pages")
            for page in pages:
                if page.title() in seen:
                    continue
                seen.add(page.title())
                try:
                    if process_page(page):
                        done += 1
                        print(f"  {page.title()}: OK ({done})")
                        time.sleep(3)
                except Exception as e:
                    print(f"  {page.title()}: {e}")
        except Exception as e:
            print(f"  Error: {e}")
    
    print(f"Done. Edited {done} pages from {len(seen)} checked.")

if __name__ == "__main__":
    main()
