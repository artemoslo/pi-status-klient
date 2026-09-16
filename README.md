# Pi-monitor – elev

Denne Pi-en viser sin egen status på en nettside, og sender den også infoen til en server på lærerens PI.

## 1. Skriv inn navn og lærerens IP

Åpne `elev_klient/app.py` og endre de to øverste linjene:

```python
TEACHER_URL = "http://192.168.1.1:5000/data"   # ← IP-adressen du får av læreren
NAME = "Ola Nordmann"                           # ← ditt eget navn
```


## 2. Installer og start
Åpne mappen med filene og kjør disse linjene en etter en:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

La vinduet stå åpent – programmet må kjøre hele tiden.


## 3. Se din egen side

Åpne i nettleseren på Pi-en: `http://localhost:8080`

Statusen din dukker også opp i lærerens oversikt i løpet av et halvt minutt.


## Neste gang du vil kjøre programmet

Du trenger bare lage `venv` første gang du kjører programmet. Så neste gang skriver du bare:

```bash
cd elev_klient # åpne mappen elev_klient i terminalen
source venv/bin/activate
python app.py
```


## Feilsøking

| Problem | Sjekk |
|-|-|
| Kommer ikke opp i lærerens oversikt | Er `TEACHER_URL` riktig? Kjører programmet fortsatt? |
| Får ikke åpnet `localhost:8080` | Kjører `python app.py`? Står det (venv) i terminalen? |
| `externally-managed-environment` ved `pip install` | Du glemte `source venv/bin/activate` |
| Andre får ikke sett nettsiden min. | Port 8080 er blokkert i brannmuren. Prøv `sudo ufw allow 8080` |

## Prosjektstyring
* [Trello Board](https://trello.com/b/aF8KIKGW)
