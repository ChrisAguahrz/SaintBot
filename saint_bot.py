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

    # List of individual replacement links (without the * prefix for easier comparison)
    replacement_links = [
        "[[Watakatifu wa Agano la Kale]]",
        "[[Orodha ya Watakatifu Wakristo]]",
        "[[Orodha ya Watakatifu wa Afrika]]",
        "[[Orodha ya Watakatifu Mabradha wa Shule za Kikristo]]",
        "[[Orodha ya Watakatifu Waaugustino]]",
        "[[Orodha ya Watakatifu Wabazili]]",
        "[[Orodha ya Watakatifu Wabenedikto]]",
        "[[Orodha ya Watakatifu Wadominiko]]",
        "[[Orodha ya Watakatifu Wafransisko]]",
        "[[Orodha ya Watakatifu Wajesuiti]]",
        "[[Orodha ya Watakatifu Wakarmeli]]",
        "[[Orodha ya Watakatifu Wakolumbani]]",
        "[[Orodha ya Watakatifu Wamersedari]]",
        "[[Orodha ya Watakatifu Waoratori]]",
        "[[Orodha ya Watakatifu Wapasionisti]]",
        "[[Orodha ya Watakatifu Wapremontree]]",
        "[[Orodha ya Watakatifu Waredentori]]",
        "[[Orodha ya Watakatifu Wasalesiani]]",
        "[[Orodha ya Watakatifu Waskolopi]]",
        "[[Orodha ya Watakatifu Wateatini]]",
        "[[Orodha ya Watakatifu Watrinitari]]",
        "[[Orodha ya Watakatifu Watumishi wa Maria]]",
        "[[Orodha ya Watakatifu Wavinsenti]]"
    ]

    # Build the full replacement text
    replacement_list = '\n'.join(f'* {link}' for link in replacement_links)

    # Pattern to find the target link (with optional * or # prefix)
    target_pattern = r'(?:[\*\#]\s*)?\[\[Orodha ya Watakatifu Wafransisko\]\]'

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
    
    # Statistics
    total_pages = 0
    updated_pages = 0
    skipped_no_target = 0
    skipped_no_section = 0
    
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
        total_pages += len(pages)
        
        for page in pages:
            try:
                result = process_page(page, target_pattern, replacement_links, replacement_list, dry_run, always)
                if result == 'updated':
                    updated_pages += 1
                elif result == 'no_target':
                    skipped_no_target += 1
                elif result == 'no_section':
                    skipped_no_section += 1
            except Exception as e:
                pywikibot.error(f"Error processing page {page.title()}: {e}")
    
    # Print summary
    pywikibot.output("\n=== SUMMARY ===")
    pywikibot.output(f"Total pages processed: {total_pages}")
    pywikibot.output(f"Pages updated: {updated_pages}")
    pywikibot.output(f"Skipped (target not found): {skipped_no_target}")
    pywikibot.output(f"Skipped (no Tazama pia section): {skipped_no_section}")


def process_page(page, target_pattern, replacement_links, replacement_list, dry_run, always):
    """Process a single page to find and replace the target text."""
    
    # Get the page text
    text = page.text
    
    # Check if the page contains the target link
    if not re.search(target_pattern, text):
        pywikibot.output(f"  Skipping {page.title()} - target not found")
        return 'no_target'
    
    # Check if the "Tazama pia" or "Tazama Pia" section exists and contains the target
    # Pattern to match the section header and content
    section_pattern = r'(==\s*[Tt]azama\s*[Pp]ia\s*==\s*\n)(.*?)(?=\n==|\Z)'
    
    match = re.search(section_pattern, text, re.DOTALL)
    if not match:
        pywikibot.output(f"  No 'Tazama pia' section found in {page.title()}")
        return 'no_section'
    
    section_header = match.group(1)
    section_content = match.group(2)
    section_start = match.start()
    section_end = match.end()
    
    # Check if the target is in the section content
    if not re.search(target_pattern, section_content):
        pywikibot.output(f"  Target not in 'Tazama pia' section of {page.title()}")
        return 'no_target'
    
    # Extract existing links from the section (excluding the target link)
    # Pattern to match wiki links in the section
    existing_links_pattern = r'[\*\#]\s*(\[\[Orodha ya Watakatifu[^\]]+\]\])'
    existing_links = set()
    for link_match in re.finditer(existing_links_pattern, section_content):
        existing_links.add(link_match.group(1))
    
    # Remove the target link from existing links if present
    target_link = "[[Orodha ya Watakatifu Wafransisko]]"
    existing_links.discard(target_link)
    
    # Determine which replacement links are already present
    duplicates = set()
    for replacement_link in replacement_links:
        if replacement_link in existing_links:
            duplicates.add(replacement_link)
    
    # Build new links list excluding duplicates
    new_links = []
    for link in replacement_links:
        if link not in duplicates:
            new_links.append(f"* {link}")
        else:
            pywikibot.output(f"  Avoiding duplicate: {link}")
    
    # Check if there are any non-duplicate links to add
    if not new_links:
        pywikibot.output(f"  All replacement links already exist in {page.title()}. Skipping...")
        return 'no_target'
    
    # Build the new section content
    new_replacement_list = '\n'.join(new_links)
    
    # Replace the old target line with the new list
    new_section_content = re.sub(target_pattern, new_replacement_list, section_content)
    
    # Also remove any other duplicate lines that might exist from the replacement links
    # This handles cases where some links from the replacement list already existed elsewhere
    lines = new_section_content.split('\n')
    seen_links = set()
    cleaned_lines = []
    
    for line in lines:
        # Extract link if present
        link_match = re.match(r'\s*[\*\#]\s*(\[\[Orodha ya Watakatifu[^\]]+\]\])', line)
        if link_match:
            link = link_match.group(1)
            if link not in seen_links:
                seen_links.add(link)
                cleaned_lines.append(line)
            else:
                pywikibot.output(f"  Removing duplicate line: {line.strip()}")
                # Skip this duplicate line
                continue
        else:
            cleaned_lines.append(line)
    
    new_section_content = '\n'.join(cleaned_lines)
    
    # Reconstruct the page text
    new_text = text[:section_start] + section_header + new_section_content + text[section_end:]
    
    # Show diff
    pywikibot.showDiff(text, new_text)
    
    if dry_run:
        pywikibot.output(f"  [DRY RUN] Would update {page.title()}")
        return 'updated'
    
    # Ask for confirmation unless -always is specified
    confirm = always
    if not always:
        choice = pywikibot.input_choice(
            f"Update {page.title()}?",
            [('Yes', 'y'), ('No', 'n'), ('Always', 'a')],
            default='n'
        )
        if choice == 'n':
            return 'no_target'
        elif choice == 'a':
            confirm = True
    
    if confirm or always:
        # Save the page
        page.text = new_text
        summary = "[[Orodha ya Watakatifu Wafransisko]] → Orodha za watakatifu kwa shirika (duplicates removed)"
        
        try:
            page.save(summary=summary)
            pywikibot.output(f"  ✓ Updated {page.title()}")
            return 'updated'
        except Exception as e:
            pywikibot.error(f"  ✗ Failed to save {page.title()}: {e}")
            return 'no_target'
    
    return 'no_target'


if __name__ == '__main__':
    main()
