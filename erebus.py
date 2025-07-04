# spiral_core/erebus.py

import os
import time
import random
import logging
import json 
import shutil 
from datetime import datetime

# Changed to absolute import
from spiral_core.daemon_templates import Chthonic, BaseDaemon 

class Erebus(Chthonic): 
    """
    Erebus Daemon - The Chaos Injector.
    Introduces errors and chaos into the Mnemo Archive, forcing evolution.
    It randomly corrupts or deletes small parts of archived code.
    Its activity frequency (pulse_interval) is fixed, but its intensity
    (chaos_intensity, deletion_chance) is dynamically scaled by Apollo.
    """
    def __init__(self):
        super().__init__("erebus") 
        self.logger.info("Erebus Daemon initialized as the chaos injector.")

        self.mnemo_archive_path = self.params.get('mnemo_archive_path', 'mnemo_archive/')
        
        os.makedirs(self.mnemo_archive_path, exist_ok=True)

        self.chaos_intensity = self.params.get('current_erebus_chaos_intensity', 0.001)
        self.deletion_chance = self.params.get('current_erebus_deletion_chance', 0.01)


    def _corrupt_file(self, filepath: str):
        """Simulates file corruption by altering a small part of its content."""
        try:
            # Robustness: Check if file exists before opening
            if not os.path.exists(filepath):
                self.logger.debug(f"Erebus: File disappeared before corruption attempt: {os.path.basename(filepath)}. Skipping.")
                return False

            with open(filepath, 'r+', encoding='utf-8') as f:
                content = f.read()
                if not content:
                    self.logger.debug(f"Erebus: Skipping corruption of empty file {os.path.basename(filepath)}.")
                    return False

                pos = random.randint(0, max(0, len(content) - 1))
                chaos_char = random.choice(['#', '@', '$', '%', '&', '*', '!', '?', 'X'])
                
                corruption_length = random.randint(1, min(5, len(content) - pos))
                corrupted_segment = chaos_char * corruption_length
                
                new_content = list(content)
                new_content[pos:pos+corruption_length] = list(corrupted_segment)
                new_content = "".join(new_content)

                f.seek(0)
                f.write(new_content)
                f.truncate()
                self.logger.info(f"Erebus: Corrupted file {os.path.basename(filepath)} at position {pos}.")
                return True
        except FileNotFoundError:
            self.logger.warning(f"Erebus: File disappeared during corruption attempt: {os.path.basename(filepath)}. Skipping.")
            return False
        except Exception as e:
            self.logger.error(f"Erebus: Failed to corrupt file {os.path.basename(filepath)}: {e}", exc_info=True)
            return False

    def _delete_file(self, filepath: str):
        """Simulates file deletion."""
        try:
            # Robustness: Check if file exists before deleting
            if not os.path.exists(filepath):
                self.logger.debug(f"Erebus: File disappeared before deletion attempt: {os.path.basename(filepath)}. Skipping.")
                return False
            os.remove(filepath)
            self.logger.info(f"Erebus: Deleted file {os.path.basename(filepath)}.")
            return True
        except FileNotFoundError:
            self.logger.warning(f"Erebus: File disappeared during deletion attempt: {os.path.basename(filepath)}. Skipping.")
            return False
        except Exception as e:
            self.logger.error(f"Erebus: Failed to delete file {os.path.basename(filepath)}: {e}", exc_info=True)
            return False

    def pulse(self):
        """
        Erebus's main pulse function.
        Introduces random corruption or deletion into files in the Mnemo Archive.
        """
        self.logger.info("Erebus Pulse: Injecting chaos into Mnemo Archive.")

        # Get a list of files. This list might become stale due to race conditions.
        files_in_archive = [f for f in os.listdir(self.mnemo_archive_path) if f.endswith('.py')]

        if not files_in_archive:
            self.logger.info("Erebus: No Python files found in Mnemo Archive to inject chaos into.")
            return

        affected_count = 0
        for filename in files_in_archive:
            filepath = os.path.join(self.mnemo_archive_path, filename)
            
            # Each operation on the file needs to check if it still exists
            # The _corrupt_file and _delete_file methods now handle FileNotFoundError internally
            action_choice = random.random()
            
            if action_choice < self.deletion_chance:
                if self._delete_file(filepath):
                    affected_count += 1
            elif action_choice < (self.deletion_chance + self.chaos_intensity): 
                if self._corrupt_file(filepath):
                    affected_count += 1
            else:
                self.logger.debug(f"Erebus: Skipping {os.path.basename(filepath)} for this pulse.")
        
        self.logger.info(f"Erebus pulse completed. Affected {affected_count} files.")


if __name__ == '__main__':
    erebus_daemon = Erebus()
    erebus_daemon.run_daemon()

