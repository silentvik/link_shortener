# Link shortener
<b> Custom link shortener only functional so far, no frills.</b><br>

Task details: ЗАДАНИЕ.md
<br>
<br>

<b>Requirements:</b>
<ul>Docker-compose installed</ul>

<b>Usage:</b>
<ul>1. git clone repository</ul>
<ul>2. cd link_shortener</ul>
<ul>3. docker-compose --env-file ./.env.dev up -d --build nginx</ul>

<b>Run tests:</b>
<ul>1. cd shortener_project</ul>
<ul>2. pip install -r requirements.txt</ul>
<ul>3. pytest -s --showlocals</ul>