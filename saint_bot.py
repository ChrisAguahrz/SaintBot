#!/usr/bin/python
import os, pywikibot, time

DRY_RUN = False
SUMMARY = "Bot: Panua orodha ya watakatifu katika sehemu ya 'Tazama pia'"

OLD_TEXT = "* [[Orodha ya Watakatifu Wafransisko]]"

SAINT_LINKS = [
    "Mabradha wa Shule za Kikristo",
    "Waaugustino",
    "Wabazili",
    "Wabenedikto",
    "Wadominiko",
    "Wafransisko",
    "Wajesuiti",
    "Wakarmeli",
    "Wakolumbani",
    "Wamersedari",
    "Waoratori",
    "Wapasionisti",
    "Wapremontree",
    "Waredentori",
    "Wasalesiani",
    "Waskolopi",
    "Wateatini",
    "Watrinitari",
    "Watumishi wa Maria",
    "Wavinsenti"
]

def get_page_title_category(page):
    """Extract the saint group from the page title if it matches a known pattern."""
    title = page.title().lower()
    for saint in SAINT_LINKS:
        if saint.lower() in title:
            return saint
    return None

def build_new_links(exclude_saint=None):
    """Build the new links list, excluding the one matching the page's own category."""
    links = []
    for saint in SAINT_LINKS:
        if exclude_saint and saint.lower() == exclude_saint.lower():
            continue
        links.append(f"* [[Orodha ya Watakatifu {saint}]]")
    return "\n".join(links)

def process_page(page):
    text = page.text
    
    # Check if the old text exists
    if OLD_TEXT not in text:
        return False
    
    # Find what saint group this page belongs to (from title)
    page_saint = get_page_title_category(page)
    
    # Build new links excluding the page's own category
    new_links = build_new_links(page_saint)
    
    # Remove the old single link
    new_text = text.replace(OLD_TEXT, "")
    
    # Remove any duplicate saint links that might already exist
    for saint in SAINT_LINKS:
        link = f"* [[Orodha ya Watakatifu {saint}]]"
        new_text = new_text.replace(link, "")
    
    # Clean up extra blank lines (more than 2 consecutive)
    import re
    new_text = re.sub(r'\n{3,}', '\n\n', new_text)
    
    # Find the "Tazama pia" section and add the new links
    if "== Tazama pia ==" in new_text:
        new_text = new_text.replace("== Tazama pia ==", "== Tazama pia ==\n" + new_links)
    elif "==Tazama pia==" in new_text:
        new_text = new_text.replace("==Tazama pia==", "==Tazama pia==\n" + new_links)
    else:
        # Add Tazama pia section at the end
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
    
    # Phase 1: Watakatifu Wakristo category
    print("Phase 1: Watakatifu Wakristo")
    cat = pywikibot.Category(site, "Watakatifu Wakristo")
    for page in cat.articles(recurse=True):
        if page.title() not in seen_pages:
            seen_pages.add(page.title())
            try:
                if process_page(page):
                    done += 1
                    print(f"{page.title()}: done")
                    time.sleep(5)
            except Exception as e:
                print(f"{page.title()}: error - {e}")
    
    # Phase 2: All pages A-Z
    print("Phase 2: All pages A-Z")
    for page in site.allpages(namespace=0):
        if page.title() not in seen_pages:
            seen_pages.add(page.title())
            try:
                if process_page(page):
                    done += 1
                    print(f"{page.title()}: done")
                    time.sleep(5)
            except Exception as e:
                print(f"{page.title()}: error - {e}")
    
    print(f"Finished. Checked {len(seen_pages)} pages, changed {done} pages.")

if __name__ == "__main__":
    main()
