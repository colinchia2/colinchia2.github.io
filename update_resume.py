"""Put a résumé PDF on colinchia2.github.io and record today's date in resume.json.

    python update_resume.py "C:\\Users\\colin\\OneDrive\\Documents\\[01] Resume\\Oct 2026\\Colin Chiapello_Resume_Oct26.pdf"

Takes exactly the file you name (never guesses: the Résumé folder also holds tailored versions that must not go public),
copies it over the site's copy, sets "uploaded" to today, then commits and pushes (live a minute or two later).
"""
import datetime
import json
import pathlib
import shutil
import subprocess
import sys

SITE = pathlib.Path(__file__).resolve().parent
TARGET = 'Colin-Chiapello-Resume.pdf'

if len(sys.argv) != 2 or not sys.argv[1].lower().endswith('.pdf'):
    sys.exit('Name the résumé PDF to publish, e.g. python update_resume.py "...\\Colin Chiapello_Resume_Nov26.pdf"')
source = pathlib.Path(sys.argv[1]).resolve()
if not source.is_file():
    sys.exit(f'Not found: {source}')

shutil.copyfile(source, SITE / TARGET)
today = datetime.date.today().isoformat()
record = {'file': TARGET, 'source': source.name, 'uploaded': today}
(SITE / 'resume.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')

subprocess.run(['git', 'add', TARGET, 'resume.json'], cwd=SITE, check=True)
if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=SITE).returncode == 0:
    print(f'No change: {source.name} is already on the site.')
else:
    subprocess.run(['git', 'commit', '-q', '-m', f'Résumé updated {today} ({source.name})'], cwd=SITE, check=True)
    subprocess.run(['git', 'push', '-q'], cwd=SITE, check=True)
    print(f'Published {source.name} as of {today}. Live in a minute or two.')
