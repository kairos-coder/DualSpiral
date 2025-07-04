# spiral_core/tartarus.py

import os
import time
import logging
import json
from datetime import datetime, timedelta
import shutil 

# Changed to absolute import
from spiral_core.daemon_templates import Chthonic, BaseDaemon 

class Tartarus(Chthonic): 
    """
    Tartarus Daemon - The Abyss.
    Manages the deep, irretrievable decay and destruction of code units
    that have fallen into disuse or are deemed irrelevant over time. It cleanses
    the system's memory, creating space and driving the necessity for new creation.
    Its activity frequency (pulse_interval) is fixed, but its decay window (how quickly
    it acts on old files) is dynamically scaled by Apollo.
    """
    def __init__(self):
        super().__init__("tartarus") 
        self.logger.info("Tartarus Daemon initialized as the abyss.")

        self.lethe_graveyard_path = self.params.get('lethe_graveyard_path', 'lethe_graveyard/')
        self.tartarus_abyss_path = self.params.get('tartarus_abyss_path', 'tartarus_abyss/')
        
        os.makedirs(self.lethe_graveyard_path, exist_ok=True)
        os.makedirs(self.tartarus_abyss_path, exist_ok=True)

        self.decay_window_seconds = self.params.get('current_tartarus_decay_window_seconds', 3600.0)


    def pulse(self):
        """
        Tartarus's main pulse function.
        Scans the Lethe Graveyard for files older than the decay window and moves them to the Abyss.
        """
        self.logger.info(f"Tartarus Pulse: Scanning Lethe Graveyard for decay (window: {self.decay_window_seconds}s).")

        # Get a list of files. This list might become stale due to race conditions.
        files_in_graveyard = [f for f in os.listdir(self.lethe_graveyard_path) if f.endswith('.py')]

        if not files_in_graveyard:
            self.logger.info("Tartarus: No files found in Lethe Graveyard to decay.")
            return

        decayed_count = 0
        now = datetime.now()

        for filename in files_in_graveyard:
            filepath = os.path.join(self.lethe_graveyard_path, filename)
            
            try:
                # Robustness: Check if file exists before getting mtime
                if not os.path.exists(filepath):
                    self.logger.debug(f"Tartarus: File disappeared before age check: {os.path.basename(filepath)}. Skipping.")
                    continue

                mod_timestamp = os.path.getmtime(filepath)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)

                if (now - mod_datetime).total_seconds() > self.decay_window_seconds:
                    destination_filepath = os.path.join(self.tartarus_abyss_path, filename)
                    shutil.move(filepath, destination_filepath)
                    self.logger.info(f"Tartarus: Decayed '{filename}' (moved to Abyss).")
                    decayed_count += 1
                else:
                    self.logger.debug(f"Tartarus: Skipping '{filename}', too new for decay.")

            except FileNotFoundError:
                self.logger.warning(f"Tartarus: File disappeared during processing: {filename}. Skipping.")
                continue # Continue to the next file
            except Exception as e:
                self.logger.error(f"Tartarus: Error processing file '{filename}': {e}", exc_info=True)
        
        self.logger.info(f"Tartarus pulse completed. Decayed {decayed_count} files.")


if __name__ == '__main__':
    tartarus_daemon = Tartarus()
    tartarus_daemon.run_daemon()

