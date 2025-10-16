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

def monitor_ml_service():
    """Monitor ML service for training updates"""
    while True:
        try:
            response = requests.get(f"{ML_SERVICE_URL}/training/status", timeout=5)
            if response.status_code == 200:
                ml_status = response.json()
                
                # Update training status
                if ml_status.get('is_training', False):
                    progress = ml_status.get('progress', 0)
                    stage = ml_status.get('current_stage', 'training')
                    
                    # Calculate ETA
                    eta_minutes = 0
                    if progress > 0:
                        # Rough estimate: 30 minutes total training time
                        remaining_progress = 100 - progress
                        eta_minutes = int((remaining_progress / 100) * 30)
                    
                    training_status.update({
                        'is_training': True,
                        'progress': progress,
                        'current_stage': stage,
                        'model_type': ml_status.get('model_type', 'analytical'),
                        'eta_minutes': eta_minutes,
                        'estimated_completion': (datetime.now() + timedelta(minutes=eta_minutes)).strftime('%H:%M') if eta_minutes > 0 else None
                    })
                    
                    # Add log entry
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
                    
                    socketio.emit('training_update', training_status)
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
                        socketio.emit('training_update', training_status)
            
            time.sleep(3)  # Check every 3 seconds
            
        except Exception as e:
            logger.debug(f"ML service monitoring error: {e}")
            time.sleep(10)  # Wait longer on error

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
        
        # Send request to ML service
        response = requests.post(f"{ML_SERVICE_URL}/training/start", 
                               json={'model_type': model_type}, 
                               timeout=10)
        
        if response.status_code == 200:
            training_status.update({
                'start_time': datetime.now().isoformat(),
                'model_type': model_type,
                'logs': []
            })
            return jsonify({'success': True, 'message': f'Started training {model_type} model'})
        else:
            return jsonify({'success': False, 'message': 'Failed to start training'}), 500
            
    except Exception as e:
        logger.error(f"Error starting training: {e}")
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
