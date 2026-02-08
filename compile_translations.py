#!/usr/bin/env python
"""
Compile .po files to .mo files without requiring GNU gettext
"""
import os
import polib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALE_DIR = os.path.join(BASE_DIR, 'locale')

def compile_translations():
    """Compile all .po files to .mo files"""
    languages = ['bn', 'en']
    
    for lang in languages:
        po_file = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'django.po')
        mo_file = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'django.mo')
        
        if os.path.exists(po_file):
            try:
                po = polib.pofile(po_file)
                po.save_as_mofile(mo_file)
                print(f'✓ Compiled {lang}: {po_file} -> {mo_file}')
            except Exception as e:
                print(f'✗ Error compiling {lang}: {e}')
        else:
            print(f'⚠ File not found: {po_file}')

if __name__ == '__main__':
    print('Compiling translation files...')
    compile_translations()
    print('Done!')
