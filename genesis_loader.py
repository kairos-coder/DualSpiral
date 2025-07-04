# spiral_core/genesis_loader.py
import json
import os
import logging

logger = logging.getLogger(__name__)

class GenesisLoader:
    """
    Handles loading and managing parameters from genesis_params.json.
    This acts as the central source of truth for all configurable parameters
    of the Spiral Engine, including fixed pulse intervals and dynamic thresholds.
    """
    def __init__(self, file_path='genesis_params.json'):
        # Determine the project root dynamically
        # This assumes genesis_params.json is in the directory above spiral_core
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir) # Go up one level from spiral_core

        self.file_path = os.path.join(project_root, file_path)
        self.params = {}
        self._load_params()
        logger.info(f"GenesisLoader initialized, loading params from: {self.file_path}")

    def _load_params(self):
        """Loads parameters from the JSON file."""
        if not os.path.exists(self.file_path):
            logger.error(f"Genesis parameters file not found at: {self.file_path}")
            # Create a default if it doesn't exist to prevent errors,
            # though the user should ideally create it manually based on README.
            self.params = self._get_default_params()
            self._save_params() # Save the default params
            logger.warning("Created default genesis_params.json. Please review and customize it.")
        else:
            try:
                with open(self.file_path, 'r') as f:
                    self.params = json.load(f)
            except json.JSONDecodeError as e:
                logger.critical(f"Error decoding genesis_params.json: {e}")
                raise
            except Exception as e:
                logger.critical(f"An unexpected error occurred loading genesis_params.json: {e}")
                raise

    def _save_params(self):
        """Saves current parameters back to the JSON file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.params, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving genesis_params.json: {e}")

    def get_params(self):
        """Returns the currently loaded parameters. Refreshes from file to get latest."""
        self._load_params() # Always reload to get the latest from disk
        return self.params

    def update_params(self, new_params):
        """Updates parameters with a dictionary and saves them."""
        self.params.update(new_params)
        self._save_params()
        logger.debug("Genesis parameters updated and saved.")

    def _get_default_params(self):
        """Returns a basic set of default parameters for initial creation."""
        # This should match the structure provided in the README
        return {
            "current_generation": 0,
            "max_generations": 100,

            "mnemo_archive_path": "mnemo_archive/",
            "kairos_raw_path": "kairos_raw_output/",
            "kairos_processed_path": "kairos_processed_output/",
            "aion_output_path": "aion_output/",
            "nyx_graveyard_path": "nyx_graveyard/",
            "lethe_graveyard_path": "lethe_graveyard/",
            "tartarus_abyss_path": "tartarus_abyss/",
            "log_dir": "logs/",

            "apollo_pulse_interval": 2.618,
            "kairos_pulse_interval": 0.618,
            "aion_pulse_interval": 1.047,
            "kronos_pulse_interval": 1.618,
            "erebus_pulse_interval": 1.618,
            "nyx_pulse_interval": 0.955,
            "tartarus_pulse_interval": 0.618,

            "base_code_units_per_generation": 1,

            "initial_spiral_growth_factor": 1.0,
            "min_spiral_growth_factor": 0.5,
            "max_spiral_growth_factor": 5.0,

            "initial_complexity_bias": 0.5,
            "min_complexity_bias": 0.1,
            "max_complexity_bias": 0.9,

            "initial_erebus_chaos_intensity": 0.001,
            "min_erebus_chaos_intensity": 0.0001,
            "max_erebus_chaos_intensity": 0.1,

            "initial_erebus_deletion_chance": 0.01,
            "min_erebus_deletion_chance": 0.001,
            "max_erebus_deletion_chance": 0.5,

            "initial_nyx_obscurity_chance": 0.005,
            "min_nyx_obscurity_chance": 0.0005,
            "max_nyx_obscurity_chance": 0.1,
            "nyx_recovery_chance": 0.1, # Static for now

            "initial_tartarus_decay_window_seconds": 3600.0,
            "min_tartarus_decay_window_seconds": 60.0,
            "max_tartarus_decay_window_seconds": 36000.0,

            "current_spiral_growth_factor": 1.0,
            "current_complexity_bias": 0.5,
            "current_erebus_chaos_intensity": 0.001,
            "current_erebus_deletion_chance": 0.01,
            "current_nyx_obscurity_chance": 0.005,
            "current_tartarus_decay_window_seconds": 3600.0
        }
