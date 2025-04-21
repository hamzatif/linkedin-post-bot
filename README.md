# 🤖 LinkedIn Post Bot

This GitHub Actions-powered bot automatically generates and emails a daily LinkedIn post using OpenAI’s GPT models. It’s designed for professionals who want to consistently share fresh, insightful content about AI, data science, machine learning, and more — without lifting a finger.

---

## ✨ What It Does

- 🎯 Selects a topic from a rotating pool (AI, ML, Data Science, etc.)
- 🧠 Generates a high-quality post using OpenAI’s GPT model (GPT-3.5 or GPT-4)
- 📧 Emails the post to you daily
- ☁️ Runs fully in the cloud via GitHub Actions — no setup required after install

---

## 🛠️ How It Works

### 1. GitHub Actions Workflow
A scheduled workflow runs `daily_post.py` every morning at 7:30 AM EST.

### 2. Environment Variables (Secrets)
All credentials are securely injected via GitHub Actions secrets:

| Name              | Description                               |
|-------------------|-------------------------------------------|
| `OPENAI_API_KEY`  | Your OpenAI API key from platform.openai.com |
| `EMAIL_ADDRESS`   | Gmail address used to send the email      |
| `EMAIL_PASSWORD`  | Gmail app password (requires 2FA)         |
| `RECIPIENT_EMAIL` | The inbox where the daily post is sent    |

### 3. Prompt Tracking
A `used_prompts.json` file ensures each topic is only used once before repeating.

---

## 🚀 Getting Started

### Step 1: Clone or Fork This Repo

```bash
git clone https://github.com/yourusername/linkedin-post-bot.git
cd linkedin-post-bot

## 🚀 Getting Started

### Step 2: Add Secrets in GitHub
Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**  
Add each of the following:

| Name              | Value                          |
|-------------------|--------------------------------|
| `OPENAI_API_KEY`  | Your OpenAI key (starts with `sk-...`) |
| `EMAIL_ADDRESS`   | Your Gmail address             |
| `EMAIL_PASSWORD`  | Your Gmail App Password        |
| `RECIPIENT_EMAIL` | The email that receives the post |

---

### Step 3: Run the Workflow
Once the files are pushed, GitHub Actions will automatically run the job daily based on the schedule.

To **test it manually**:
- Go to the **Actions** tab in your repo
- Select **“Daily LinkedIn Post”**
- Click **“Run workflow”**

---

## ⏰ Change the Schedule

This is set to run **every day at 7:30 AM EST** (12:30 PM UTC).  
To change it, update the `cron:` line in `.github/workflows/daily.yml`:

```yaml
cron: '30 12 * * *'  # Change 12 to your desired UTC hour
