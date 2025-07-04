# spiral_core/nyx.py

import os
import json
import time
import random
import logging
from datetime import datetime
import re 
import shutil 

# Changed to absolute import
from spiral_core.daemon_templates import Chthonic, BaseDaemon 

class Nyx(Chthonic): 
    """
    Nyx Daemon - The Obscurer.
    Introduces obscurity and decay into the Mnemo Archive, forcing evolution.
    It randomly corrupts or obscures small parts of archived code.
    Its activity frequency (pulse_interval) is fixed, but its intensity
    (obscurity_chance, min_file_age_seconds) is dynamically scaled by Apollo.
    """
    def __init__(self):
        super().__init__("nyx") 
        self.logger.info("Nyx Daemon initialized as the obscurer.")

        self.nyx_graveyard_path = self.params.get('nyx_graveyard_path', 'nyx_graveyard/')
        self.mnemo_archive_path = self.params.get('mnemo_archive_path', 'mnemo_archive/')
        
        os.makedirs(self.nyx_graveyard_path, exist_ok=True)
        os.makedirs(self.mnemo_archive_path, exist_ok=True)


    def should_obscure_file(self, filepath: str) -> bool:
        """
        Decides if a file should be obscured based on chance, age, and content complexity.
        Uses parameters loaded from genesis_params.json via BaseDaemon.
        """
        nyx_obscurity_chance = self.params.get("nyx_obscurity_chance", 0.3)
        nyx_min_file_age_seconds = self.params.get("nyx_min_file_age_seconds", 60)

        try:
            # Robustness: Check if file exists before getting mtime
            if not os.path.exists(filepath):
                self.logger.debug(f"Nyx: File disappeared before age check: {os.path.basename(filepath)}. Skipping.")
                return False

            file_age = time.time() - os.path.getmtime(filepath)
            if file_age < nyx_min_file_age_seconds:
                self.logger.info(f"Skipping {os.path.basename(filepath)}: too new ({file_age:.1f}s old).")
                return False

            if random.random() > nyx_obscurity_chance:
                self.logger.info(f"Skipping {os.path.basename(filepath)}: random chance prevented obscuring.")
                return False

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            complexity_indicators = [
                r"\bfor\s+\w+\s+in\b",     
                r"\bclass\s+\w+:",         
                r"\bimport\s+\w+",         
                r"hephaestus",             
                r"lethe",                  
                r"apollo"                  
            ]

            resistance_score = 0
            for pattern in complexity_indicators:
                if re.search(pattern, content):
                    resistance_score += 1
            
            if resistance_score > 0:
                adjusted_obscurity_chance = nyx_obscurity_chance * (1 - (resistance_score * 0.15)) 
                adjusted_obscurity_chance = max(0.05, adjusted_obscurity_chance) 
                
                if random.random() > adjusted_obscurity_chance:
                    self.logger.info(f"Skipping {os.path.basename(filepath)}: contains complexity indicators (resistance score: {resistance_score}, adjusted chance: {adjusted_obscurity_chance:.2f}).")
                    return False
                else:
                    self.logger.info(f"Decision to obscure {os.path.basename(filepath)} despite complexity (adjusted chance: {adjusted_obscurity_chance:.2f}).")

        except FileNotFoundError:
            self.logger.warning(f"Nyx: File disappeared during should_obscure_file check: {os.path.basename(filepath)}. Skipping.")
            return False
        except Exception as e:
            self.logger.error(f"Nyx: Error reading or analyzing {filepath} for obscurity: {e}. Defaulting to skipping decision.", exc_info=True)
            return False

        return True 

    def obscure_file(self, filepath: str, graveyard_path: str) -> bool:
        """
        Simulates obscuring a file by moving it to the graveyard.
        """
        filename = os.path.basename(filepath)
        new_filepath = os.path.join(graveyard_path, filename)
        try:
            os.makedirs(graveyard_path, exist_ok=True)
            shutil.move(filepath, new_filepath) 
            self.logger.info(f"Obscured (moved to graveyard): {filename}")
            return True
        except FileNotFoundError:
            self.logger.warning(f"Nyx: File disappeared before obscuring: {filename}. Skipping.")
            return False
        except Exception as e:
            self.logger.error(f"Nyx: Failed to obscure file {filename}: {e}", exc_info=True)
            return False

    def pulse(self):
        """
        Nyx's main pulse function.
        Scans Mnemo's archive for code to obscure based on its heuristics.
        """
        self.logger.info("Nyx Pulse: Scanning Mnemo Archive for obscurity targets.")
        
        if not os.path.exists(self.mnemo_archive_path):
            self.logger.warning(f"Mnemo archive path '{self.mnemo_archive_path}' does not exist. Nothing to obscure.")
            return

        # Get a list of files. This list might become stale due to race conditions.
        files_in_archive = [f for f in os.listdir(self.mnemo_archive_path) if f.endswith('.py')]
        
        obscured_count = 0
        for filename in files_in_archive:
            filepath = os.path.join(self.mnemo_archive_path, filename)
            # Each operation on the file needs to check if it still exists
            if self.should_obscure_file(filepath): 
                if self.obscure_file(filepath, self.nyx_graveyard_path):
                    obscured_count += 1
        
        self.logger.info(f"Nyx pulse completed. Obscured {obscured_count} files.")


if __name__ == '__main__':
    nyx_daemon = Nyx()
    nyx_daemon.run_daemon()

