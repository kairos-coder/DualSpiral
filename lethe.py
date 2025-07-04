# spiral_core/lethe.py

import os
import json
import time
import random
import logging
from datetime import datetime

# CHANGE START: Ensuring absolute import is correct
from spiral_core.daemon_templates import Chthonic, BaseDaemon
# CHANGE END

class Lethe(Chthonic): 
    """
    Lethe Daemon - The River of Oblivion.
    Injects chaotic "oblivion noise" into Hephaestus's forge to test code resilience.
    """
    def __init__(self):
        super().__init__("lethe") 
        self.logger.info("Lethe Daemon initialized as the chaos injector.")

        self.lethe_chaos_logs_path = self.params.get('lethe_chaos_logs_path', 'lethe_chaos_logs/')
        self.hephaestus_forge_path = self.params.get('hephaestus_forge_path', 'hephaestus_forge/')

        os.makedirs(self.lethe_chaos_logs_path, exist_ok=True)
        os.makedirs(self.hephaestus_forge_path, exist_ok=True)


    def pulse(self):
        """
        Lethe's main pulse function.
        Injects "oblivion" chaos into Hephaestus's forge.
        """
        self.logger.info("Lethe: Chaos injection pulse initiated.")

        # Identify active Hephaestus sandbox directories
        active_sandboxes = [d for d in os.listdir(self.hephaestus_forge_path) 
                            if os.path.isdir(os.path.join(self.hephaestus_forge_path, d)) and d.startswith("experiment_")]

        if not active_sandboxes:
            self.logger.info("Lethe: No active Hephaestus sandboxes found to inject chaos into.")
            return

        # Choose a random sandbox to target
        target_sandbox_name = random.choice(active_sandboxes)
        target_sandbox_path = os.path.join(self.hephaestus_forge_path, target_sandbox_name)

        chaos_id = os.urandom(4).hex()
        chaos_types = ["data_corruption_sim", "state_reset_sim", "memory_leak_sim", "transient_file_loss_sim"]
        chosen_chaos_type = random.choice(chaos_types)

        self.logger.info(f"Lethe: Injecting '{chosen_chaos_type}' chaos (ID: {chaos_id}) into sandbox: {target_sandbox_name}")

        chaos_marker_file = os.path.join(target_sandbox_path, f"chaos_marker_{chaos_id}.txt")
        chaos_data = {
            "chaos_type": chosen_chaos_type,
            "intensity": self.params.get("lethe_chaos_intensity", 0.5), 
            "timestamp": datetime.now().isoformat(),
            "target_sandbox": target_sandbox_name
        }
        
        try:
            # Attempt to create the chaos marker file
            with open(chaos_marker_file, 'w', encoding='utf-8') as f:
                json.dump(chaos_data, f, indent=4)
            self.logger.info(f"Lethe: Chaos marker created at {chaos_marker_file}")

            # Log the chaos event in Lethe's own logs
            chaos_log_filename = f"chaos_event_{chaos_id}.json"
            chaos_log_filepath = os.path.join(self.lethe_chaos_logs_path, chaos_log_filename)
            with open(chaos_log_filepath, 'w', encoding='utf-8') as f:
                json.dump(chaos_data, f, indent=4)
            self.logger.info(f"Lethe: Chaos event logged to {chaos_log_filepath}")

        except FileNotFoundError:
            self.logger.warning(f"Lethe: Target sandbox '{target_sandbox_name}' disappeared before chaos injection. Skipping.")
        except Exception as e:
            self.logger.error(f"Lethe: Error injecting chaos into {target_sandbox_name}: {e}", exc_info=True)

        self.logger.info("Lethe: Chaos injection pulse completed.")

if __name__ == '__main__':
    lethe_daemon = Lethe()
    lethe_daemon.run_daemon()

