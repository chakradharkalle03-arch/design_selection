# Render 24/7 Deployment & Uptime Keeping Guide

This guide details how to deploy your backend to **Render** and configure a free Uptime Monitor to keep it **live 24/7 with zero sleeping**.

---

## Step 1: Deploy your app to Render

1. Push your code to a **GitHub** or **GitLab** repository.
2. Go to [Render Dashboard](https://dashboard.render.com/) and log in.
3. Click **New +** -> **Web Service**.
4. Connect your GitHub repository.
5. Fill in the following details:
   - **Name**: `embroidery-ai-backend` (or your preferred name)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
6. Click **Create Web Service**.
7. Once deployed, Render will provide a URL like:
   `https://embroidery-ai-backend.onrender.com`

---

## Step 2: Test your live health check URL

Open your browser or run curl to test the health check endpoint:
```bash
curl https://embroidery-ai-backend.onrender.com/api/health
```
You should see:
```json
{
  "status": "healthy",
  "service": "Embroidery AI Backend"
}
```

---

## Step 3: Set up UptimeRobot to Keep it Alive 24/7

Since Render free services go to sleep after 15 minutes of inactivity, we ping it every 5 to 10 minutes so it stays awake permanently.

1. Go to **[UptimeRobot.com](https://uptimerobot.com)** and create a free account.
2. Click **+ Add New Monitor**.
3. Set the configuration as follows:
   - **Monitor Type**: `HTTP(s)`
   - **Friendly Name**: `Render Backend Keep-Alive`
   - **URL (or IP)**: `https://embroidery-ai-backend.onrender.com/api/health`
   - **Monitoring Interval**: `Every 5 minutes` or `Every 10 minutes`
4. Click **Create Monitor**.

---

## Alternative: Using cron-job.org

If you prefer `cron-job.org`:
1. Go to **[cron-job.org](https://cron-job.org)** and sign up.
2. Click **Cronjobs** -> **Create Cronjob**.
3. Title: `Keep Render Alive`
4. Address: `https://embroidery-ai-backend.onrender.com/api/health`
5. Schedule: Every 5 or 10 minutes.
6. Click **Save**.

---

## 🎉 Result

* UptimeRobot or cron-job.org will send an HTTP GET request to your Render app every 5-10 minutes.
* Render detects active incoming traffic and keeps your web service container **running 24/7 without ever spinning down or sleeping**.
