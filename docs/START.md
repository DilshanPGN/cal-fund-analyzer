# 🚀 QUICK START - 30 SECONDS TO RUNNING APP

## Windows Users:

```bash
scripts\migrate.bat
scripts\start.bat
```

## Mac/Linux Users:

```bash
chmod +x scripts/*.sh
./scripts/migrate.sh
./scripts/start.sh
```

## Then open your browser to:

```
http://localhost:5000
```

## That's it! 🎉

---

## Troubleshooting

### If you get "pip not found":
```bash
# Install Python from python.org
# Then try again
```

### If you get "Permission denied" (Mac/Linux):
```bash
chmod +x scripts/start.sh
chmod +x scripts/migrate.sh
```

### If port 5000 is busy:
Edit `backend/config.py` and change PORT to 5001

---

## First Time Setup

1. Select a fund from dropdown
2. Click "Fetch New Data"
3. Wait 30-60 seconds for data to load
4. View your chart!
5. Try clicking "Analyze Current View"

---

**Need help?** Read `COMPLETE.md` for detailed guide
**Want to learn?** Read `README.md` for architecture details

