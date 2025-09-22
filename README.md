# 🏗️ Agile Task Manager

**Agile Task Manager** è una web-app interattiva sviluppata in **Python con Streamlit** per la gestione dei task in modalità Agile. Permette di monitorare lo stato dei task, generare grafici di andamento, utilizzare un Kanban board interattivo, analizzare la velocità del team e inviare notifiche automatiche sui task in ritardo.

---

## 🌟 Funzionalità principali

1. **Upload dati**

   * Supporta Excel (`.xlsx`, `.xls`) e integrazione con Google Sheets.
   * Filtra automaticamente i task assegnati all’utente loggato.

2. **Login utenti**

   * Sistema di autenticazione con username e password.
   * Ogni utente visualizza solo i propri task.

3. **Dashboard e grafici**

   * Task completati per settimana.
   * Velocità del team (Story Points completati per sprint).
   * **Burn-down chart**: story points rimanenti fino a fine sprint.
   * Distribuzione dei task per persona o categoria.

4. **Kanban interattivo**

   * Colonne rappresentano gli stati dei task (Da fare, In corso, Completato).
   * Drag & drop per aggiornare lo stato dei task direttamente nella web-app.

5. **Esportazione report**

   * PDF con riepilogo task e grafici.
   * Excel con tutti i dati filtrati o completi.

6. **Notifiche automatiche**

   * Avvisa tramite email se un task è in ritardo.

---

## 🗂️ Struttura del progetto

```
agile-task-manager/
│
├─ app.py                   # Entry point principale Streamlit
├─ requirements.txt         # Librerie Python necessarie
├─ utils/
│   ├─ data_loader.py       # Gestione dati (Excel / Google Sheets)
│   ├─ kanban.py            # Kanban board interattiva
│   ├─ charts.py            # Grafici (Burn-down, velocità, task/settimana)
│   ├─ reports.py           # Esportazione PDF / Excel
│   └─ notifications.py     # Invio email notifiche
└─ config/
    └─ auth_config.py       # Utenti/password hashed
```

---

## ⚙️ Installazione

1. Clona il repository:

```bash
git clone https://github.com/tuo-username/agile-task-manager.git
cd agile-task-manager
```

2. Crea e attiva un ambiente virtuale (opzionale ma consigliato):

```bash
python -m venv venv
source venv/bin/activate    # Linux / macOS
venv\Scripts\activate       # Windows
```

3. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

---

## 🚀 Esecuzione

Avvia l’applicazione Streamlit:

```bash
streamlit run app.py
```

Apri il browser e visita l’URL fornito da Streamlit (`http://localhost:8501` di default).

---

## 📊 Configurazione Google Sheets (opzionale)

1. Crea un progetto su Google Cloud Platform.
2. Abilita le **Google Sheets API** e crea un **Service Account**.
3. Scarica il file JSON delle credenziali e salvalo in `config/credentials.json`.
4. Passa il percorso del file e il nome del foglio a `data_loader.load_google_sheet()`.

---

## ✉️ Configurazione Notifiche Email

1. Modifica `utils/notifications.py` con i dati del tuo account email (Gmail consigliato).
2. Attiva l’**accesso alle app meno sicure** o utilizza un **App Password**.
3. I task in ritardo saranno segnalati e potenzialmente inviati via email.

---

## 📌 Esempio Excel di input

| Task               | Assegnato a | Stato      | Data inizio | Data fine  | Story Points | Categoria |
| ------------------ | ----------- | ---------- | ----------- | ---------- | ------------ | --------- |
| Implementare login | Mario       | In corso   | 2025-09-01  | 2025-09-10 | 5            | Backend   |
| Dashboard grafici  | Anna        | Completato | 2025-09-02  | 2025-09-08 | 8            | Frontend  |

---

## 📈 Tecnologie e librerie utilizzate

* Python 3.10+
* [Streamlit](https://streamlit.io/)
* pandas, matplotlib, openpyxl
* streamlit-authenticator
* streamlit-sortable (Kanban drag\&drop)
* gspread, oauth2client (Google Sheets)
* reportlab (PDF)
* smtplib (invio email)

---

## 🔮 Evoluzioni possibili

* Kanban con aggiornamento in tempo reale su Google Sheets.
* Integrazione notifiche push o Slack.
* Analisi avanzata: velocity chart, burn-up chart.
* Login con OAuth2 / SSO aziendale.

---

## ⚖️ Licenza

MIT License – libero utilizzo e modifica.

Vuoi che lo faccia?
