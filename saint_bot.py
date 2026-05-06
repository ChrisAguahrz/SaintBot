#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Script to replace [[Orodha ya Watakatifu Wafransisko]] with a full list
of Orodha ya Watakatifu links in the "Tazama pia" or "Tazama Pia" section
of pages in specified categories.

Parameters:
    -dry:       Dry run - don't save changes
    -always:    Don't prompt for confirmation
"""

import pywikibot
from pywikibot import pagegenerators
import re


def main():
    # List of categories to process
    categories = [
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

    # The replacement text
    replacement_list = """\
* [[Orodha ya Watakatifu Mabradha wa Shule za Kikristo]]
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

    # Pattern to find the target link
    target_pattern = r'[\*\#]\s*\[\[Orodha ya Watakatifu Wafransisko\]\]'

    # Get command line arguments
    dry_run = False
    always = False
    local_args = pywikibot.handle_args()

    for arg in local_args:
        if arg == '-dry':
            dry_run = True
        elif arg == '-always':
            always = True

    # Variable for the site (default Swahili Wikipedia)
    site = pywikibot.Site('sw', 'wikipedia')
    
    # Process each category
    for cat_name in categories:
        pywikibot.output(f"\n=== Processing category: {cat_name} ===")
        
        category = pywikibot.Category(site, cat_name)
        
        if not category.exists():
            pywikibot.warning(f"Category '{cat_name}' does not exist. Skipping...")
            continue
        
        # Get all pages in the category
        pages = list(category.articles(namespaces=0))
        pywikibot.output(f"Found {len(pages)} pages in category '{cat_name}'")
        
        for page in pages:
            try:
                process_page(page, target_pattern, replacement_list, dry_run, always)
            except Exception as e:
                pywikibot.error(f"Error processing page {page.title()}: {e}")


def process_page(page, target_pattern, replacement_list, dry_run, always):
    """Process a single page to find and replace the target text."""
    
    # Get the page text
    text = page.text
    
    # Check if the page contains the target link
    if not re.search(target_pattern, text):
        pywikibot.output(f"  Skipping {page.title()} - target not found")
        return
    
    # Check if the "Tazama pia" or "Tazama Pia" section exists and contains the target
    # Pattern to match the section header and content
    section_pattern = r'(==\s*[Tt]azama\s*[Pp]ia\s*==\s*\n)(.*?)(?=\n==|\Z)'
    
    match = re.search(section_pattern, text, re.DOTALL)
    if not match:
        pywikibot.output(f"  No 'Tazama pia' section found in {page.title()}")
        return
    
    section_header = match.group(1)
    section_content = match.group(2)
    section_start = match.start()
    section_end = match.end()
    
    # Check if the target is in the section content
    if not re.search(target_pattern, section_content):
        pywikibot.output(f"  Target not in 'Tazama pia' section of {page.title()}")
        return
    
    # Replace the old target line with the new list
    new_section_content = re.sub(target_pattern, replacement_list, section_content)
    
    # Reconstruct the page text
    new_text = text[:section_start] + section_header + new_section_content + text[section_end:]
    
    # Show diff
    pywikibot.showDiff(text, new_text)
    
    if dry_run:
        pywikibot.output(f"  [DRY RUN] Would update {page.title()}")
        return
    
    # Ask for confirmation unless -always is specified
    if not always:
        choice = pywikibot.input_choice(
            f"Update {page.title()}?",
            [('Yes', 'y'), ('No', 'n'), ('Always', 'a')],
            default='n'
        )
        if choice == 'n':
            return
        elif choice == 'a':
            always = True
    
    # Save the page
    page.text = new_text
    summary = "[[Orodha ya Watakatifu Wafransisko]] → Orodha za watakatifu kwa shirika"
    
    try:
        page.save(summary=summary)
        pywikibot.output(f"  ✓ Updated {page.title()}")
    except Exception as e:
        pywikibot.error(f"  ✗ Failed to save {page.title()}: {e}")


if __name__ == '__main__':
    main()    else:
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
