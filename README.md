# Link shortener

(Test task from company) (No mobile support so far)
<br>
<br>

<b>Requirements:</b>
<ul>Docker-compose installed</ul>

<b>Usage:</b>
<ul>1. git clone repository</ul>
<ul>2. cd link_shortener</ul>
<ul>3. docker-compose --env-file ./.env.dev up -d --build nginx</ul>
<ul>4. open SITE_URL as in .env.dev</ul>

<b>Run tests:</b>
<ul>1. cd shortener_project</ul>
<ul>2. source your/venv</ul>
<ul>3. pip install -r requirements.txt</ul>
<ul>4. (run makemigrations and migrate)</ul>
<ul>5. pytest -s --showlocals</ul>
