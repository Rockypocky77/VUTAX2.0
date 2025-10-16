# 🚀 VUTAX 2.0 Easy Training Launcher

## Quick Start - Just Run One File!

### Windows Users (Easiest)
```bash
# Double-click this file or run in terminal:
start_training.bat
```

### All Platforms (Python)
```bash
# Run this command:
python start_training.py
```

## What It Does

The training launcher automatically:

1. **🐳 Starts Services**: Launches ML service and training tracker
2. **🤖 Begins Training**: Starts training both AI models automatically
3. **🌐 Opens Dashboard**: Opens progress tracker at http://localhost:5000
4. **📊 Shows Progress**: Real-time updates on training progress
5. **⏱️ Estimates Time**: Shows how much time is left

## What You'll See

### 1. Startup Screen
```
================================================================
                VUTAX 2.0 - AI TRAINING LAUNCHER
================================================================

🤖 This script will:
   1. Start the ML service for training
   2. Launch the training progress tracker
   3. Begin training all AI models
   4. Open the progress dashboard in your browser

⏱️  Expected training time: 15-30 minutes
📊 Progress tracking: http://localhost:5000
```

### 2. Training Progress
```
🤖 Training in progress: feature_engineering (45.2%)
⏱️  Estimated time remaining: 12 minutes
   Last updated: 14:23:45

🤖 Training in progress: training (78.9%)
⏱️  Estimated time remaining: 5 minutes
   Last updated: 14:31:22
```

### 3. Dashboard Opens Automatically
- **Real-time progress bars**
- **Live training logs**
- **ETA countdown**
- **Model performance metrics**

## Training Stages You'll See

1. **📊 Collecting Data** (0-30%): Fetching market data for 45+ stocks
2. **🔧 Feature Engineering** (30-50%): Calculating 70+ technical indicators
3. **🤖 Model Training** (50-80%): Training gradient boosting algorithms
4. **✅ Validation** (80-90%): Testing model accuracy on real data
5. **🚀 Deployment** (90-100%): Deploying updated models

## Access Points

- **Training Dashboard**: http://localhost:5000 (progress tracking)
- **ML Service API**: http://localhost:8001 (model endpoints)
- **Main Platform**: http://localhost:3000 (trading platform)

## Requirements

- **Docker Desktop** (must be running)
- **Internet Connection** (for market data)
- **10GB Free Space** (for model files and data)

## Troubleshooting

### "Docker not found"
```bash
# Install Docker Desktop from:
https://www.docker.com/products/docker-desktop/

# Make sure Docker Desktop is running
```

### "Services won't start"
```bash
# Check if ports are free:
netstat -an | findstr ":5000"
netstat -an | findstr ":8001"

# Stop any conflicting services
```

### "Training won't start"
```bash
# Check ML service health:
curl http://localhost:8001/health

# Or visit in browser:
http://localhost:8001/health
```

### "Dashboard won't load"
```bash
# Check training tracker:
curl http://localhost:5000/api/status

# Or restart services:
docker-compose restart training-tracker
```

## Manual Control

If you want to control training manually:

### Start Training
```bash
# Analytical model
curl -X POST http://localhost:8001/training/start \
  -H "Content-Type: application/json" \
  -d '{"model_type":"analytical"}'

# Chatbot model  
curl -X POST http://localhost:8001/training/start \
  -H "Content-Type: application/json" \
  -d '{"model_type":"chatbot"}'
```

### Check Status
```bash
# Training status
curl http://localhost:8001/training/status

# Model status
curl http://localhost:8001/models/status
```

## Expected Timeline

| Stage | Duration | What's Happening |
|-------|----------|------------------|
| **Data Collection** | 2-5 min | Fetching stock data from APIs |
| **Feature Engineering** | 3-8 min | Calculating technical indicators |
| **Model Training** | 8-15 min | Training ML algorithms |
| **Validation** | 2-5 min | Testing model accuracy |
| **Deployment** | 1-2 min | Saving and deploying models |

**Total: 15-30 minutes** (depending on your computer speed)

## What Happens After Training

1. **✅ Models are automatically deployed**
2. **📊 Accuracy metrics are saved**
3. **🔄 Automatic retraining every 6 hours**
4. **📈 Better predictions in the main platform**
5. **🤖 Improved chatbot responses**

## Tips for Best Results

- **Leave computer on** for automatic retraining
- **Stable internet** for data fetching
- **Don't close Docker** during training
- **Monitor dashboard** for progress updates
- **Check logs** if anything goes wrong

## Files Created

After training, you'll find:
- `backend/ml-service/models/saved/` - Trained model files
- `logs/` - Training logs and metrics
- `data/` - Cached market data

## Next Steps

After training completes:
1. **Visit main platform**: http://localhost:3000
2. **Test AI recommendations** in the discover page
3. **Try the chatbot** for stock analysis
4. **Add stocks to watchlist** to see predictions
5. **Let models retrain automatically** every 6 hours

---

**That's it! Just run the launcher and watch your AI models train themselves!** 🎉🤖📈
