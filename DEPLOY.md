# 🚀 Deploy to Render (Free)

This guide will help you deploy the Bedtime Story Generator to Render's free tier.

## Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com) (free)
3. **OpenAI API Key**: Get one from [OpenAI](https://platform.openai.com/api-keys)

## Step-by-Step Deployment

### 1. Fork or Clone the Repository

If you haven't already, make sure your code is in a GitHub repository.

### 2. Sign Up for Render

1. Go to [render.com](https://render.com)
2. Click "Get Started" 
3. Sign up with your GitHub account

### 3. Create a New Web Service

1. In your Render dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub account if prompted
4. Select your `story-time` repository
5. Click "Connect"

### 4. Configure the Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `bedtime-story-generator` (or any name you prefer)
- **Region**: Choose the closest to your users
- **Branch**: `main`
- **Root Directory**: (leave blank)
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

**Advanced Settings:**
- **Plan Type**: Free
- **Auto-Deploy**: Yes (recommended)

### 5. Set Environment Variables

In the "Environment" section, add these variables:

```
OPENAI_API_KEY=your_actual_openai_api_key_here
FLASK_SECRET_KEY=your_random_secret_key_here
FLASK_ENV=production
```

**To generate a secret key:**
```python
import secrets
print(secrets.token_hex(16))
```

### 6. Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your app
3. This process takes 2-5 minutes

### 7. Set Up Database (Optional)

For persistent data storage:

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Choose the free plan
3. Note the database URL provided
4. Add to your web service environment variables:
   ```
   DATABASE_URL=postgresql://username:password@hostname:port/database
   ```

### 8. Access Your App

Once deployed, you'll get a URL like:
`https://bedtime-story-generator.onrender.com`

## Important Notes

### Free Tier Limitations
- **Sleep Mode**: Apps sleep after 15 minutes of inactivity
- **Cold Starts**: First request after sleeping takes 30+ seconds
- **750 Hours/Month**: Usually sufficient for demos and light usage

### Cost Considerations
- **OpenAI API**: Each story costs ~$0.001-0.003
- **Render**: Free tier is truly free
- **Database**: Free PostgreSQL has 1GB limit

### Performance Tips
- Keep your app awake with services like [UptimeRobot](https://uptimerobot.com) (free)
- Optimize your OpenAI prompts to reduce token usage
- Consider upgrading to paid plan for production use

## Troubleshooting

### Common Issues

**Build Fails:**
- Check that `requirements.txt` is in the root directory
- Ensure all dependencies are properly listed

**App Won't Start:**
- Verify the start command: `gunicorn --bind 0.0.0.0:$PORT app:app`
- Check that your main file is named `app.py`

**OpenAI Errors:**
- Confirm your API key is valid and has credits
- Check that the environment variable name is exactly `OPENAI_API_KEY`

**Database Issues:**
- Verify the DATABASE_URL format
- Check PostgreSQL connection limits (free tier has 20 connections)

### Logs and Debugging

1. In Render dashboard, go to your service
2. Click "Logs" tab to see real-time logs
3. Look for error messages during startup

### Manual Deploy

If auto-deploy isn't working:
1. Go to your service dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

## Example Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-proj-abc123...
FLASK_SECRET_KEY=a1b2c3d4e5f6...

# Optional
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@hostname:5432/dbname
```

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] Story generation works
- [ ] Database connections work (if using PostgreSQL)
- [ ] PDF export functions properly
- [ ] Mobile responsiveness looks good

## Updating Your App

When you push changes to GitHub:
1. Render automatically detects changes
2. Rebuilds and redeploys your app
3. Usually takes 2-3 minutes

## Getting Help

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Community**: [community.render.com](https://community.render.com)
- **Support**: Available through Render dashboard

---

🎉 **Congratulations!** Your Bedtime Story Generator is now live and accessible to anyone on the internet!

**Share your deployed app:**
`https://your-app-name.onrender.com`
