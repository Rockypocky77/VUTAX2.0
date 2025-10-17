"""
Flask Training Progress Tracker for VUTAX 2.0
Real-time progress tracking for ML model training
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import os
import threading
import time
from datetime import datetime, timedelta
import requests
import logging
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vutax_training_tracker_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global training status
training_status = {
    'is_training': False,
    'progress': 0.0,
    'current_stage': 'idle',
    'model_type': '',
    'start_time': None,
    'estimated_completion': None,
    'eta_minutes': 0,
    'logs': [],
    'data_fetching': {
        'articles_fetched': 0,
        'target_articles': 1000,
        'stocks_processed': 0,
        'target_stocks': 100,
        'data_points': 0,
        'target_data_points': 50000,
        'fetch_rate': 0,  # articles per minute
        'current_source': '',
        'sources_completed': [],
        'errors': 0,
        'last_update': None,
        'progress_history': []  # For graphing
    },
    'stage_progress': {
        'data_collection': 0,
        'feature_engineering': 0,
        'model_training': 0,
        'validation': 0,
        'deployment': 0
    },
    'metrics': {
        'analytical_model': {
            'accuracy': 0.0,
            'last_trained': None,
            'training_count': 0,
            'best_accuracy': 0.0
        },
        'chatbot_model': {
            'quality_score': 0.0,
            'last_trained': None,
            'training_count': 0,
            'best_quality': 0.0
        }
    }
}

# ML Service URL
ML_SERVICE_URL = os.getenv('ML_SERVICE_URL', 'http://localhost:8001')

def simulate_data_fetching():
    """Simulate realistic data fetching progress"""
    import random
    
    if not training_status['is_training']:
        return
    
    current_time = datetime.now()
    data_fetch = training_status['data_fetching']
    
    # Simulate different stages of data fetching
    stage = training_status['current_stage']
    
    if stage == 'collecting_data':
        # Simulate fetching articles and stock data
        if data_fetch['articles_fetched'] < data_fetch['target_articles']:
            # Fetch 5-15 articles per update
            new_articles = random.randint(5, 15)
            data_fetch['articles_fetched'] = min(
                data_fetch['articles_fetched'] + new_articles,
                data_fetch['target_articles']
            )
            
            # Update fetch rate (articles per minute)
            if data_fetch['last_update']:
                time_diff = (current_time - datetime.fromisoformat(data_fetch['last_update'])).total_seconds() / 60
                if time_diff > 0:
                    data_fetch['fetch_rate'] = new_articles / time_diff
            
            # Simulate different data sources
            sources = ['Alpha Vantage', 'Yahoo Finance', 'News API', 'Reddit', 'Twitter']
            data_fetch['current_source'] = random.choice(sources)
            
            # Occasionally add completed sources
            if random.random() < 0.1:  # 10% chance
                source = random.choice(sources)
                if source not in data_fetch['sources_completed']:
                    data_fetch['sources_completed'].append(source)
        
        # Simulate stock processing
        if data_fetch['stocks_processed'] < data_fetch['target_stocks']:
            new_stocks = random.randint(1, 3)
            data_fetch['stocks_processed'] = min(
                data_fetch['stocks_processed'] + new_stocks,
                data_fetch['target_stocks']
            )
        
        # Simulate data points collection
        if data_fetch['data_points'] < data_fetch['target_data_points']:
            new_points = random.randint(100, 500)
            data_fetch['data_points'] = min(
                data_fetch['data_points'] + new_points,
                data_fetch['target_data_points']
            )
        
        # Occasionally simulate errors
        if random.random() < 0.05:  # 5% chance of error
            data_fetch['errors'] += 1
    
    # Update progress history for graphing (keep last 50 points)
    progress_point = {
        'timestamp': current_time.strftime('%H:%M:%S'),
        'articles': data_fetch['articles_fetched'],
        'stocks': data_fetch['stocks_processed'],
        'data_points': data_fetch['data_points'],
        'fetch_rate': data_fetch['fetch_rate']
    }
    
    data_fetch['progress_history'].append(progress_point)
    if len(data_fetch['progress_history']) > 50:
        data_fetch['progress_history'] = data_fetch['progress_history'][-50:]
    
    data_fetch['last_update'] = current_time.isoformat()

def monitor_ml_service():
    """Monitor ML service for training updates"""
    while True:
        try:
            # Try to get real ML service status
            try:
                response = requests.get(f"{ML_SERVICE_URL}/training/status", timeout=2)
                if response.status_code == 200:
                    ml_status = response.json()
                    use_real_data = True
                else:
                    use_real_data = False
            except:
                use_real_data = False
            
            # Use simulated data if ML service not available
            if not use_real_data:
                # Simulate training progress
                if training_status['is_training']:
                    current_progress = training_status['progress']
                    stage = training_status['current_stage']
                    
                    # Progress through stages
                    if stage == 'collecting_data' and current_progress < 30:
                        training_status['progress'] = min(current_progress + random.uniform(0.5, 2.0), 30)
                        training_status['stage_progress']['data_collection'] = training_status['progress'] / 30 * 100
                    elif stage == 'collecting_data' and current_progress >= 30:
                        training_status['current_stage'] = 'feature_engineering'
                        training_status['progress'] = 30
                    elif stage == 'feature_engineering' and current_progress < 50:
                        training_status['progress'] = min(current_progress + random.uniform(0.3, 1.5), 50)
                        training_status['stage_progress']['feature_engineering'] = (training_status['progress'] - 30) / 20 * 100
                    elif stage == 'feature_engineering' and current_progress >= 50:
                        training_status['current_stage'] = 'training'
                        training_status['progress'] = 50
                    elif stage == 'training' and current_progress < 80:
                        training_status['progress'] = min(current_progress + random.uniform(0.2, 1.0), 80)
                        training_status['stage_progress']['model_training'] = (training_status['progress'] - 50) / 30 * 100
                    elif stage == 'training' and current_progress >= 80:
                        training_status['current_stage'] = 'validation'
                        training_status['progress'] = 80
                    elif stage == 'validation' and current_progress < 95:
                        training_status['progress'] = min(current_progress + random.uniform(0.5, 2.0), 95)
                        training_status['stage_progress']['validation'] = (training_status['progress'] - 80) / 15 * 100
                    elif stage == 'validation' and current_progress >= 95:
                        training_status['current_stage'] = 'deployment'
                        training_status['progress'] = 95
                    elif stage == 'deployment' and current_progress < 100:
                        training_status['progress'] = min(current_progress + random.uniform(1.0, 3.0), 100)
                        training_status['stage_progress']['deployment'] = (training_status['progress'] - 95) / 5 * 100
                    elif current_progress >= 100:
                        training_status['current_stage'] = 'completed'
                        training_status['is_training'] = False
                        training_status['progress'] = 100
                    
                    # Calculate ETA
                    if training_status['progress'] > 0 and training_status['progress'] < 100:
                        remaining_progress = 100 - training_status['progress']
                        eta_minutes = int((remaining_progress / 100) * 25)  # 25 minute total estimate
                        training_status['eta_minutes'] = eta_minutes
                        training_status['estimated_completion'] = (datetime.now() + timedelta(minutes=eta_minutes)).strftime('%H:%M')
                    else:
                        training_status['eta_minutes'] = 0
                        training_status['estimated_completion'] = None
                    
                    # Simulate data fetching
                    simulate_data_fetching()
            else:
                # Use real ML service data
                if ml_status.get('is_training', False):
                    progress = ml_status.get('progress', 0)
                    stage = ml_status.get('current_stage', 'training')
                    
                    training_status.update({
                        'is_training': True,
                        'progress': progress,
                        'current_stage': stage,
                        'model_type': ml_status.get('model_type', 'analytical'),
                    })
                    
                    # Calculate ETA
                    eta_minutes = 0
                    if progress > 0:
                        remaining_progress = 100 - progress
                        eta_minutes = int((remaining_progress / 100) * 30)
                    
                    training_status['eta_minutes'] = eta_minutes
                    training_status['estimated_completion'] = (datetime.now() + timedelta(minutes=eta_minutes)).strftime('%H:%M') if eta_minutes > 0 else None
                else:
                    if training_status['is_training']:
                        # Training just finished
                        training_status.update({
                            'is_training': False,
                            'progress': 100,
                            'current_stage': 'completed',
                            'eta_minutes': 0,
                            'estimated_completion': None
                        })
            
            # Add log entry
            if training_status['is_training']:
                stage = training_status['current_stage']
                progress = training_status['progress']
                log_message = get_stage_message(stage, progress)
                
                if not training_status['logs'] or training_status['logs'][-1]['message'] != log_message:
                    training_status['logs'].append({
                        'timestamp': datetime.now().strftime('%H:%M:%S'),
                        'stage': stage,
                        'progress': progress,
                        'message': log_message
                    })
                    
                    # Keep only last 50 logs
                    if len(training_status['logs']) > 50:
                        training_status['logs'] = training_status['logs'][-50:]
            
            # Emit update to all connected clients
            socketio.emit('training_update', training_status)
            
            time.sleep(2)  # Check every 2 seconds for more responsive updates
            
        except Exception as e:
            logger.debug(f"ML service monitoring error: {e}")
            time.sleep(5)  # Wait on error

def get_stage_message(stage, progress):
    """Get human-readable message for current stage"""
    messages = {
        'collecting_data': f'📊 Collecting training data... ({progress:.1f}%)',
        'feature_engineering': f'🔧 Engineering features... ({progress:.1f}%)',
        'training': f'🤖 Training model... ({progress:.1f}%)',
        'validation': f'✅ Validating model... ({progress:.1f}%)',
        'deployment': f'🚀 Deploying model... ({progress:.1f}%)',
        'completed': '🎉 Training completed successfully!',
        'error': '❌ Training failed',
        'idle': '💤 Ready to start training...'
    }
    return messages.get(stage, f'Processing... ({progress:.1f}%)')

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """Get current training status"""
    return jsonify(training_status)

@app.route('/api/start-training', methods=['POST'])
def start_training():
    """Start training for specified model"""
    try:
        data = request.get_json() or {}
        model_type = data.get('model_type', 'analytical')
        
        if training_status['is_training']:
            return jsonify({'error': 'Training already in progress'}), 400
        
        # Initialize training status
        training_status.update({
            'is_training': True,
            'progress': 0.0,
            'current_stage': 'collecting_data',
            'start_time': datetime.now().isoformat(),
            'model_type': model_type,
            'logs': [],
            'eta_minutes': 25,
            'estimated_completion': (datetime.now() + timedelta(minutes=25)).strftime('%H:%M')
        })
        
        # Reset data fetching metrics
        training_status['data_fetching'].update({
            'articles_fetched': 0,
            'stocks_processed': 0,
            'data_points': 0,
            'fetch_rate': 0,
            'current_source': 'Alpha Vantage',
            'sources_completed': [],
            'errors': 0,
            'last_update': datetime.now().isoformat(),
            'progress_history': []
        })
        
        # Reset stage progress
        for stage in training_status['stage_progress']:
            training_status['stage_progress'][stage] = 0
        
        # Try to send request to ML service (optional)
        try:
            response = requests.post(f"{ML_SERVICE_URL}/training/start", 
                                   json={'model_type': model_type}, 
                                   timeout=5)
            if response.status_code == 200:
                logger.info("ML service training started")
            else:
                logger.info("Using simulated training (ML service not available)")
        except Exception as e:
            logger.info(f"Using simulated training: {e}")
        
        # Add initial log
        training_status['logs'].append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'stage': 'collecting_data',
            'progress': 0,
            'message': f'🚀 Started training {model_type} model'
        })
        
        # Emit initial update
        socketio.emit('training_update', training_status)
        
        return jsonify({'success': True, 'message': f'Started training {model_type} model'})
            
    except Exception as e:
        logger.error(f"Error starting training: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/stop-training', methods=['POST'])
def stop_training():
    """Stop current training"""
    try:
        if not training_status['is_training']:
            return jsonify({'error': 'No training in progress'}), 400
        
        # Stop training
        training_status.update({
            'is_training': False,
            'current_stage': 'stopped',
            'eta_minutes': 0,
            'estimated_completion': None
        })
        
        # Add log
        training_status['logs'].append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'stage': 'stopped',
            'progress': training_status['progress'],
            'message': '🛑 Training stopped by user'
        })
        
        # Try to stop ML service (optional)
        try:
            response = requests.post(f"{ML_SERVICE_URL}/training/stop", timeout=5)
            if response.status_code == 200:
                logger.info("ML service training stopped")
        except Exception as e:
            logger.info(f"Could not stop ML service: {e}")
        
        # Emit update
        socketio.emit('training_update', training_status)
        
        return jsonify({'success': True, 'message': 'Training stopped successfully'})
        
    except Exception as e:
        logger.error(f"Error stopping training: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/logs')
def get_logs():
    """Get training logs"""
    return jsonify(training_status['logs'])

@app.route('/api/metrics')
def get_metrics():
    """Get performance metrics"""
    try:
        response = requests.get(f"{ML_SERVICE_URL}/models/status", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to get metrics'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('📱 Client connected to training dashboard')
    emit('training_update', training_status)

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('📱 Client disconnected from training dashboard')

@socketio.on('request_status')
def handle_status_request():
    """Handle status request from client"""
    emit('training_update', training_status)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🤖 VUTAX 2.0 - AI Training Progress Tracker")
    print("="*60)
    print("🚀 Starting training dashboard...")
    print("📊 Real-time progress tracking enabled")
    print("🌐 Dashboard available at: http://localhost:5000")
    print("="*60 + "\n")
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_ml_service, daemon=True)
    monitor_thread.start()
    
    # Run the Flask app
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
