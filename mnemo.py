import multiprocessing
import time
import os
from datetime import datetime

from common_utils import (
    setup_logging, set_cpu_affinity, # <--- Ensure set_cpu_affinity is imported
    DATA_TYPE_KEY, DATA_CONTENT_KEY, DATA_PULSE_KEY, DATA_STATUS_KEY,
    LETHE_STATUS_MESSAGE_KEY, LETHE_ERROR_MESSAGE_KEY
)

# Setup logging for Mnemo
logger = setup_logging("Mnemo")

class Mnemo:
    def __init__(self, apollo_to_mnemo_q, mnemo_to_lethe_q, mnemo_log_q, kronos_log_q, lethe_to_apollo_feedback_q, script_dirs):
        self.apollo_to_mnemo_q = apollo_to_mnemo_q
        self.mnemo_to_lethe_q = mnemo_to_lethe_q
        self.mnemo_log_q = mnemo_log_q
        self.kronos_log_q = kronos_log_q
        self.lethe_to_apollo_feedback_q = lethe_to_apollo_feedback_q
        self.running_event = None
        self.cpu_affinity = None
        self.script_dirs = script_dirs
        self.log_file_path = os.path.join(self.script_dirs["active_scripts"], "mnemo_activity_log.txt") # Updated for active_scripts
        self._ensure_log_file_exists()
        logger.info("Initialized.")

    def _ensure_log_file_exists(self):
        """Ensures the mnemo activity log file and its directory exist."""
        log_dir = os.path.dirname(self.log_file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        # The file will be created when first written to if it doesn't exist.

    def run(self, cpu_affinity, running_event):
        self.cpu_affinity = cpu_affinity
        self.running_event = running_event
        set_cpu_affinity(os.getpid(), self.cpu_affinity, logger) # <--- CORRECTED: Added os.getpid()
        logger.info(f"Starting on PID {os.getpid()} (assigned CPU {self.cpu_affinity}).")

        while self.running_event.is_set():
            # Process content from Apollo
            if not self.apollo_to_mnemo_q.empty():
                data = self.apollo_to_mnemo_q.get()
                self._save_and_relay(data)

            # Process logs from Kronos (for logging purposes)
            if not self.kronos_log_q.empty():
                log_message = self.kronos_log_q.get()
                self._log_activity(f"Received from Kronos: {log_message}")

            # Process messages from Lethe (could be logs or feedback)
            if not self.mnemo_log_q.empty():
                message = self.mnemo_log_q.get()
                # Check if it's a structured feedback message from Lethe
                if isinstance(message, dict) and message.get("source") == "Lethe":
                    logger.info(f"Received feedback from Lethe: Status={message.get(LETHE_STATUS_MESSAGE_KEY)}")
                    self.lethe_to_apollo_feedback_q.put(message) # Relay to Apollo
                else:
                    self._log_activity(f"Received from Lethe: {message}")

            time.sleep(0.1)
        logger.info("Shutting down.")

    def _save_and_relay(self, data):
        data_type = data.get(DATA_TYPE_KEY)
        generated_content = data.get(DATA_CONTENT_KEY)
        original_pulse = data.get(DATA_PULSE_KEY) # Get the original pulse type

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_extension = "py" if data_type == "python_script" else "txt"
        file_name = f"{data_type}_{timestamp}.{file_extension}"

        target_dir = ""
        if data_type == "python_script":
            target_dir = self.script_dirs["active_scripts"]
        elif data_type == "seo_content":
            target_dir = self.script_dirs["active_seo_keywords"]
        else:
            logger.error(f"Unknown data type '{data_type}' for saving and relaying.")
            return

        file_path = os.path.join(target_dir, file_name)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(generated_content)
            logger.info(f"Saved {file_name} to {file_path}")

            # Prepare data to send to Lethe (now includes full path and original pulse)
            data_for_lethe = {
                DATA_TYPE_KEY: data_type,
                DATA_CONTENT_KEY: file_path, # Send the full path
                DATA_PULSE_KEY: original_pulse # Pass the original pulse
            }
            self.mnemo_to_lethe_q.put(data_for_lethe)
            self._log_activity(f"Saved {file_name} for Lethe.")

        except Exception as e:
            logger.error(f"Error saving {file_name}: {e}")

    def _log_activity(self, message):
        """Logs activity to the Mnemo-specific log file."""
        try:
            with open(self.log_file_path, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}] Mnemo: {message}\n")
            logger.info(f"Logged Mnemo activity to {self.log_file_path.split('/')[-1]}")
        except Exception as e:
            logger.error(f"Failed to write to Mnemo activity log file {self.log_file_path}: {e}")
