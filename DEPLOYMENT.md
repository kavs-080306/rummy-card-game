# 🚀 Deployment Guide - Rummy Card Game

## Option 1: **Streamlit Cloud** (Easiest & Free)

### Step 1: Push to GitHub
```bash
cd rummy-card-game
git add .
git commit -m "Convert to Streamlit version"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub account
3. Click "New app"
4. Select your repo: `kavs-080306/rummy-card-game`
5. Main file: `app.py`
6. Click "Deploy"

### Step 3: Add Secrets (Firebase Credentials)
1. In Streamlit Cloud, go to "Advanced settings" → "Secrets"
2. Add your `.env` variables:
```toml
FIREBASE_API_KEY = "your-api-key"
FIREBASE_AUTH_DOMAIN = "your-auth-domain"
FIREBASE_PROJECT_ID = "your-project-id"
FIREBASE_STORAGE_BUCKET = "your-storage-bucket"
FIREBASE_MESSAGING_SENDER_ID = "your-sender-id"
FIREBASE_APP_ID = "your-app-id"
```

### Step 4: Share!
Your app is live at: `https://share.streamlit.io/kavs-080306/rummy-card-game`

---

## Option 2: **Heroku** (Alternative)

### Step 1: Create `Procfile`
```
web: streamlit run app.py --logger.level=error
```

### Step 2: Create `setup.sh`
```bash
mkdir -p ~/.streamlit/
echo "[theme]
primaryColor = '#6366f1'
backgroundColor = '#0f172a'
secondaryBackgroundColor = '#1e293b'
textColor = '#ffffff'
font = 'sans serif'

[client]
showErrorDetails = true" > ~/.streamlit/config.toml
```

### Step 3: Deploy
```bash
heroku create your-app-name
heroku config:set FIREBASE_API_KEY="your-api-key"
heroku config:set FIREBASE_AUTH_DOMAIN="your-auth-domain"
# ... set all env vars

git push heroku main
```

---

## Option 3: **AWS/GCP** (Advanced)

Use containerization:
```bash
# Create Dockerfile
docker build -t rummy-game .
docker run -p 8501:8501 rummy-game
```

Deploy to:
- AWS ECS/Fargate
- Google Cloud Run
- DigitalOcean App Platform

---

## Option 4: **Railway.app** (Recommended)

### Step 1: Connect GitHub
1. Go to https://railway.app
2. Click "Create New"
3. Select GitHub repository
4. Choose `rummy-card-game` repo

### Step 2: Configure Environment
- Add environment variables from `.env`
- Set `PORT=8501` (if needed)

### Step 3: Add Procfile
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Step 4: Deploy
Click "Deploy" - Railway handles everything!

---

## Post-Deployment Checklist

- [ ] Test login flow
- [ ] Create test game
- [ ] Join game with 2+ players
- [ ] Test card drawing
- [ ] Verify coin deduction
- [ ] Test game completion
- [ ] Check Firebase rules

---

## Environment Variables Reference

```env
# Firebase Credentials
FIREBASE_API_KEY=YOUR_API_KEY
FIREBASE_AUTH_DOMAIN=YOUR_AUTH_DOMAIN
FIREBASE_PROJECT_ID=YOUR_PROJECT_ID
FIREBASE_STORAGE_BUCKET=YOUR_STORAGE_BUCKET
FIREBASE_MESSAGING_SENDER_ID=YOUR_MESSAGING_SENDER_ID
FIREBASE_APP_ID=YOUR_APP_ID

# Optional: For production
DEBUG=False
ENVIRONMENT=production
```

---

## Troubleshooting

### App won't start
```bash
streamlit run app.py --logger.level=error
```

### Firebase connection issues
- Check `.env` variables
- Verify Firebase project is active
- Check CORS settings

### Port already in use
```bash
streamlit run app.py --server.port=8502
```

---

## Cost Estimate

| Platform | Cost |
|----------|------|
| Streamlit Cloud | **FREE** (up to 3 apps) |
| Railway | ~$5/month |
| Heroku | ~$6.50/month |
| Firebase | FREE tier + pay-as-you-go |

---

## Next Steps

After deployment:
1. Share link with friends
2. Invite them to play
3. Gather feedback
4. Iterate and improve

**Your Rummy game is live!** 🎉
