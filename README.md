Install dependencies and init virtual environment

```bash
npm install

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the app in **dev** mode

```bash
npm run dev
```

The app should be available at http://localhost:3000

---

Process uploaded CVs

```bash
python scripts/extract_details.py
```
