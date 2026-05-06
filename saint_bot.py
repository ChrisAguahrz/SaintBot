#!/usr/bin/python
# -*- coding: utf-8 -*-
import pywikibot
import re
import sys
import time

def main():
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

    # Replacement links stored clean (no brackets)
    replacement_links_clean = [
        "Watakatifu wa Agano la Kale",
        "Orodha ya Watakatifu Wakristo",
        "Orodha ya Watakatifu wa Afrika",
        "Orodha ya Watakatifu Mabradha wa Shule za Kikristo",
        "Orodha ya Watakatifu Waaugustino",
        "Orodha ya Watakatifu Wabazili",
        "Orodha ya Watakatifu Wabenedikto",
        "Orodha ya Watakatifu Wadominiko",
        "Orodha ya Watakatifu Wafransisko",
        "Orodha ya Watakatifu Wajesuiti",
        "Orodha ya Watakatifu Wakarmeli",
        "Orodha ya Watakatifu Wakolumbani",
        "Orodha ya Watakatifu Wamersedari",
        "Orodha ya Watakatifu Waoratori",
        "Orodha ya Watakatifu Wapasionisti",
        "Orodha ya Watakatifu Wapremontree",
        "Orodha ya Watakatifu Waredentori",
        "Orodha ya Watakatifu Wasalesiani",
        "Orodha ya Watakatifu Waskolopi",
        "Orodha ya Watakatifu Wateatini",
        "Orodha ya Watakatifu Watrinitari",
        "Orodha ya Watakatifu Watumishi wa Maria",
        "Orodha ya Watakatifu Wavinsenti"
    ]

    # Build full replacement block
    replacement_block = '\n'.join(f"* [[{link}]]" for link in replacement_links_clean)

    site = pywikibot.Site('sw', 'wikipedia')
    
    updated = 0
    skipped = 0
    
    start_time = time.time()
    
    for cat_name in categories:
        sys.stdout.write(f"\n[{cat_name}]\n")
        sys.stdout.flush()
        
        category = pywikibot.Category(site, cat_name)
        if not category.exists():
            continue
        
        pages = list(category.articles(namespaces=0))
        
        for page in pages:
            text = page.text
            
            # Must have target
            if "[[Orodha ya Watakatifu Wafransisko]]" not in text:
                skipped += 1
                continue
            
            # Find Tazama pia section
            section_match = re.search(r'(==\s*[Tt]azama\s*[Pp]ia\s*==\s*\n)(.*?)(?=\n==|\Z)', text, re.DOTALL)
            if not section_match:
                skipped += 1
                continue
            
            section_header = section_match.group(1)
            section_content = section_match.group(2)
            section_start = section_match.start()
            section_end = section_match.end()
            
            # Target must be IN this section
            if "[[Orodha ya Watakatifu Wafransisko]]" not in section_content:
                skipped += 1
                continue
            
            # === BUILD NEW SECTION ===
            lines = section_content.split('\n')
            new_lines = []
            seen_links = set()  # track links we've already added
            
            for line in lines:
                # Is this the target line? Replace with full block
                if '[[Orodha ya Watakatifu Wafransisko]]' in line:
                    for link in replacement_links_clean:
                        link_formatted = f"* [[{link}]]"
                        if link not in seen_links:
                            new_lines.append(link_formatted)
                            seen_links.add(link)
                    continue
                
                # Is this a Watakatifu list item?
                link_match = re.match(r'(\s*[\*\#]\s*)\[\[([^\]]+)\]\]', line)
                if link_match and 'Watakatifu' in link_match.group(2):
                    link_text = link_match.group(2)
                    prefix = link_match.group(1)
                    
                    # If this link is in our replacement list, it's a duplicate - skip it
                    if link_text in replacement_links_clean:
                        continue
                    
                    # If we've seen this link before, skip it (duplicate)
                    if link_text in seen_links:
                        continue
                    
                    seen_links.add(link_text)
                    new_lines.append(line)
                else:
                    new_lines.append(line)
            
            new_section = '\n'.join(new_lines)
            new_text = text[:section_start] + section_header + new_section + text[section_end:]
            
            if new_text == text:
                skipped += 1
                continue
            
            page.text = new_text
            try:
                page.save(summary="Imesasishwa: [[Orodha ya Watakatifu Wafransisko]] -> Orodha za watakatifu kwa shirika")
                updated += 1
                sys.stdout.write(f"  OK: {page.title()}\n")
            except Exception as e:
                sys.stdout.write(f"  FAIL: {page.title()} - {e}\n")
            
            sys.stdout.flush()
    
    elapsed = time.time() - start_time
    sys.stdout.write(f"\nDONE in {elapsed:.0f}s | Updated: {updated} | Skipped: {skipped}\n")
    sys.stdout.flush()


if __name__ == '__main__':
    main()
