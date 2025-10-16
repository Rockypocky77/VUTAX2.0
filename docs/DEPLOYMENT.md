# VUTAX 2.0 Deployment Guide

This guide covers deployment options for the VUTAX 2.0 fintech platform.

## 🚀 Quick Start (Development)

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+ and pip
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose (recommended)

### Option 1: Docker Compose (Recommended)

1. **Clone and setup environment**:
```bash
git clone <repository-url>
cd VUTAX-2.0
cp .env.example .env
# Edit .env with your API keys and configuration
```

2. **Start all services**:
```bash
docker-compose up -d
```

3. **Access the application**:
- Frontend: http://localhost:3000
- API Gateway: http://localhost:3001
- ML Service: http://localhost:8001
- Database: localhost:5432
- Redis: localhost:6379

### Option 2: Manual Setup

1. **Database Setup**:
```bash
# Install PostgreSQL and Redis
# Create database
createdb vutax
```

2. **Backend Setup**:
```bash
# API Gateway
cd backend/api-gateway
npm install
npm run build
npm start

# ML Service (in another terminal)
cd backend/ml-service
pip install -r requirements.txt
python main.py
```

3. **Frontend Setup**:
```bash
cd frontend
npm install
npm run build
npm start
```

## 🌐 Production Deployment

### Environment Variables

Create production `.env` files with these key variables:

```bash
# Production API URLs
NEXT_PUBLIC_API_URL=https://api.vutax.com
NEXT_PUBLIC_ML_API_URL=https://ml.vutax.com

# Database (use managed services)
DATABASE_URL=postgresql://user:pass@prod-db:5432/vutax
REDIS_HOST=prod-redis.cache.amazonaws.com

# API Keys (required)
ALPHA_VANTAGE_API_KEY=your_production_key
RESEND_API_KEY=your_resend_key

# Security
JWT_SECRET=your_secure_jwt_secret
NODE_ENV=production
```

### Deployment Options

#### Option 1: Cloud Platform (Vercel + Railway)

**Frontend (Vercel)**:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
cd frontend
vercel --prod
```

**Backend (Railway)**:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy API Gateway
cd backend/api-gateway
railway login
railway init
railway up

# Deploy ML Service
cd ../ml-service
railway init
railway up
```

#### Option 2: AWS/GCP/Azure

**Using Docker containers**:
```bash
# Build production images
docker build -t vutax-frontend ./frontend
docker build -t vutax-api ./backend/api-gateway
docker build -t vutax-ml ./backend/ml-service

# Push to container registry
docker tag vutax-frontend your-registry/vutax-frontend:latest
docker push your-registry/vutax-frontend:latest
```

#### Option 3: VPS/Dedicated Server

```bash
# Use production docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Or with nginx proxy
docker-compose --profile production up -d
```

### Database Migration

```bash
# Run database migrations
cd backend/api-gateway
npm run migrate

# Seed initial data
npm run seed
```

### SSL/HTTPS Setup

**Using Let's Encrypt with Nginx**:
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Monitoring & Maintenance

### Health Checks

The platform includes health check endpoints:
- Frontend: `GET /api/health`
- API Gateway: `GET /health`
- ML Service: `GET /health`

### Monitoring Stack

Enable monitoring with:
```bash
docker-compose --profile monitoring up -d
```

Access:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)

### Log Management

Logs are available via:
```bash
# View all logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f api-gateway
docker-compose logs -f ml-service
```

### Backup Strategy

**Database Backup**:
```bash
# Create backup
pg_dump -h localhost -U vutax_user vutax > backup_$(date +%Y%m%d).sql

# Restore backup
psql -h localhost -U vutax_user vutax < backup_20231201.sql
```

**Redis Backup**:
```bash
# Redis automatically creates dump.rdb
# Copy /data/dump.rdb for backup
```

## 🔧 Configuration

### API Rate Limits

Configure in `.env`:
```bash
RATE_LIMIT_WINDOW_MS=900000  # 15 minutes
RATE_LIMIT_MAX_REQUESTS=100  # 100 requests per window
```

### ML Model Configuration

```bash
MODEL_UPDATE_INTERVAL=1800000    # 30 minutes
MODEL_ACCURACY_THRESHOLD=0.75    # Minimum accuracy
PREDICTION_CONFIDENCE_MIN=0.6    # Minimum confidence
```

### Cache Configuration

```bash
CACHE_TTL_REALTIME=60      # 1 minute
CACHE_TTL_DAILY=3600       # 1 hour
CACHE_TTL_HISTORICAL=86400 # 24 hours
```

## 🚨 Troubleshooting

### Common Issues

1. **ML Service won't start**:
   - Check Python dependencies: `pip install -r requirements.txt`
   - Verify GPU/CPU compatibility
   - Check model file permissions

2. **Database connection errors**:
   - Verify DATABASE_URL format
   - Check network connectivity
   - Ensure database exists

3. **API rate limiting**:
   - Check API key quotas
   - Implement exponential backoff
   - Use caching effectively

4. **WebSocket connection issues**:
   - Verify WS_URL configuration
   - Check firewall settings
   - Enable WebSocket support in proxy

### Performance Optimization

1. **Frontend**:
   - Enable Next.js static optimization
   - Use CDN for assets
   - Implement proper caching headers

2. **Backend**:
   - Use Redis for session storage
   - Implement database connection pooling
   - Enable gzip compression

3. **ML Service**:
   - Use model quantization
   - Implement batch processing
   - Cache frequent predictions

### Security Checklist

- [ ] HTTPS enabled with valid certificates
- [ ] Environment variables secured
- [ ] Database credentials rotated
- [ ] API rate limiting configured
- [ ] CORS properly configured
- [ ] Input validation implemented
- [ ] SQL injection prevention
- [ ] XSS protection enabled

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale API Gateway
docker-compose up --scale api-gateway=3

# Load balancer configuration needed
```

### Database Scaling

- Use read replicas for analytics
- Implement connection pooling
- Consider database sharding for large datasets

### ML Service Scaling

- Use GPU instances for training
- Implement model serving with TensorFlow Serving
- Use message queues for batch processing

## 🔄 CI/CD Pipeline

Example GitHub Actions workflow:

```yaml
name: Deploy VUTAX
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          # Build and deploy steps
          docker build -t vutax .
          docker push registry/vutax:latest
```

## 📞 Support

For deployment issues:
1. Check logs first: `docker-compose logs`
2. Verify environment variables
3. Test health endpoints
4. Check resource usage: `docker stats`

---

**Note**: This platform handles financial data. Ensure compliance with relevant regulations (SEC, FINRA, etc.) in your jurisdiction before deploying to production.
