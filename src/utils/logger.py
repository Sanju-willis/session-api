# src\utils\logger.py
import json
import logging

# Force logger configuration
logging.basicConfig(
   level=logging.DEBUG,
   format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
   force=False  # This overrides existing config
)
logger = logging.getLogger(__name__)

def log_state(state, message="State"):
   """Log state data in readable JSON format"""
   if state is None:
       logger.info(f"{message}: None")
       return
   
   # Create safe copy for JSON serialization
   safe_state = state.copy()
   if 'messages' in safe_state:
       safe_state['messages'] = [f"Message(content='{msg.content}')" for msg in safe_state['messages']]
   
   try:
       logger.info(f"{message}: {json.dumps(safe_state, indent=2)}")
   except TypeError:
       logger.info(f"{message}: {safe_state}")  # Fallback to string representation

def log_debug(message):
   """Log debug message"""
   logger.info(message)

def log_error(message):
   """Log error message"""  
   logger.error(message)