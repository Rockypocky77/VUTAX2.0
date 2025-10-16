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
from datetime import datetime
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
    'current_stage': '',
    'model_type': '',
    'start_time': None,
    'estimated_completion': None,
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
        data = request.get_json()
        model_type = data.get('model_type', 'analytical')
        
        if training_status['is_training']:
            return jsonify({'error': 'Training already in progress'}), 400
        
        # Start training in background thread
        training_thread = threading.Thread(
            target=trigger_ml_training,
            args=(model_type,),
            daemon=True
        )
        training_thread.start()
        
        return jsonify({'message': f'Training started for {model_type} model'})
        
    except Exception as e:
        logger.error(f"Error starting training: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop-training', methods=['POST'])
def stop_training():
    """Stop current training (if possible)"""
    try:
        # In a real implementation, this would send a stop signal to the ML service
        training_status['is_training'] = False
        training_status['progress'] = 0.0
        training_status['current_stage'] = 'Training stopped'
        
        # Emit update to connected clients
        socketio.emit('training_update', training_status)
        
        return jsonify({'message': 'Training stop requested'})
        
    except Exception as e:
        logger.error(f"Error stopping training: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs')
def get_logs():
    """Get training logs"""
    return jsonify({'logs': training_status['logs']})

@app.route('/api/metrics')
def get_metrics():
    """Get model performance metrics"""
    try:
        # Try to get latest metrics from ML service
        response = requests.get(f'{ML_SERVICE_URL}/models/status', timeout=5)
        if response.status_code == 200:
            ml_metrics = response.json()
            training_status['metrics'].update(ml_metrics)
    except Exception as e:
        logger.warning(f"Could not fetch ML metrics: {e}")
    
    return jsonify(training_status['metrics'])

def trigger_ml_training(model_type: str):
    """Trigger training in ML service and monitor progress"""
    try:
        # Update status
        training_status['is_training'] = True
        training_status['model_type'] = model_type
        training_status['start_time'] = datetime.now().isoformat()
        training_status['progress'] = 0.0
        training_status['current_stage'] = 'Initializing training...'
        
        add_log(f"Starting {model_type} model training...")
        
        # Emit initial update
        socketio.emit('training_update', training_status)
        
        # Simulate training progress monitoring
        # In a real implementation, this would communicate with the ML service
        simulate_training_progress(model_type)
        
    except Exception as e:
        logger.error(f"Error in training trigger: {e}")
        training_status['is_training'] = False
        add_log(f"Training failed: {str(e)}")
        socketio.emit('training_update', training_status)

def simulate_training_progress(model_type: str):
    """Simulate training progress for demonstration"""
    stages = [
        ("Collecting training data...", 30),
        ("Engineering features...", 50),
        ("Training model...", 80),
        ("Validating performance...", 90),
        ("Deploying model...", 100)
    ]
    
    try:
        for stage, target_progress in stages:
            training_status['current_stage'] = stage
            add_log(f"Stage: {stage}")
            
            # Gradually increase progress to target
            current_progress = training_status['progress']
            while current_progress < target_progress:
                current_progress += 1
                training_status['progress'] = current_progress
                
                # Emit progress update
                socketio.emit('training_update', training_status)
                
                # Simulate work time
                time.sleep(0.5)  # Adjust speed for demo
                
                if not training_status['is_training']:  # Check if stopped
                    return
        
        # Training completed
        training_status['is_training'] = False
        training_status['current_stage'] = 'Training completed successfully!'
        
        # Update metrics (simulated)
        if model_type == 'analytical':
            training_status['metrics']['analytical_model'].update({
                'accuracy': round(0.75 + (0.15 * time.time() % 1), 3),
                'last_trained': datetime.now().isoformat(),
                'training_count': training_status['metrics']['analytical_model']['training_count'] + 1
            })
        else:
            training_status['metrics']['chatbot_model'].update({
                'quality_score': round(0.80 + (0.15 * time.time() % 1), 3),
                'last_trained': datetime.now().isoformat(),
                'training_count': training_status['metrics']['chatbot_model']['training_count'] + 1
            })
        
        add_log(f"{model_type.title()} model training completed successfully!")
        socketio.emit('training_update', training_status)
        
    except Exception as e:
        logger.error(f"Error in training simulation: {e}")
        training_status['is_training'] = False
        training_status['current_stage'] = f'Training failed: {str(e)}'
        add_log(f"Training failed: {str(e)}")
        socketio.emit('training_update', training_status)

def add_log(message: str):
    """Add log message with timestamp"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'message': message
    }
    training_status['logs'].append(log_entry)
    
    # Keep only last 100 log entries
    if len(training_status['logs']) > 100:
        training_status['logs'] = training_status['logs'][-100:]
    
    logger.info(message)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected to training tracker')
    emit('training_update', training_status)

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected from training tracker')

@socketio.on('request_update')
def handle_update_request():
    """Handle client request for status update"""
    emit('training_update', training_status)

# Background thread to monitor ML service
def monitor_ml_service():
    """Monitor ML service for training updates"""
    while True:
        try:
            if not training_status['is_training']:
                # Check if ML service is training
                response = requests.get(f'{ML_SERVICE_URL}/models/status', timeout=5)
                if response.status_code == 200:
                    ml_status = response.json()
                    
                    # Update our status if ML service is training
                    if ml_status.get('is_training', False):
                        training_status.update({
                            'is_training': True,
                            'progress': ml_status.get('progress', 0),
                            'current_stage': ml_status.get('current_stage', ''),
                            'model_type': 'analytical'  # Default
                        })
                        socketio.emit('training_update', training_status)
            
            time.sleep(10)  # Check every 10 seconds
            
        except Exception as e:
            logger.debug(f"ML service monitoring error: {e}")
            time.sleep(30)  # Wait longer on error

# Start monitoring thread
monitor_thread = threading.Thread(target=monitor_ml_service, daemon=True)
monitor_thread.start()

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run the Flask app
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
