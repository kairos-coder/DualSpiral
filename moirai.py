from daemon_templates import Chthonic
from golden_fate import GoldenAnalyzer
import random
from datetime import datetime

__all__ = ['Moirai']

class Moirai(Chthonic):
    """
    The Sisters of Fate - Chthonic deities who weave, measure, and cut the threads of code
    
    Deep in the darkness beneath the system, three sisters share a single eye,
    determining the fate of each thread of code that passes through their domain.
    """
    
    FATE_QUOTES = {
        'greetings': [
            "From the depths, we emerge...",
            "Another thread descends to us...",
            "Sisters! Fresh code approaches our domain...",
            "The underground stirs with new possibilities..."
        ],
        'cutting': [
            "By the darkness, it ends!",
            "The thread is cut, the code returns to void!",
            "Back to the shadows with you!",
            "The depths claim another..."
        ],
        'measuring': [
            "By ancient patterns we judge...",
            "The golden ratio whispers its truth...",
            "This code's destiny becomes clear...",
            "The patterns of fate reveal themselves..."
        ],
        'warnings': [
            "A tangled thread darkens our vision...",
            "This code bears the mark of chaos...",
            "The patterns grow twisted here...",
            "Even the void rejects this structure..."
        ],
        'bickering': [
            "Sister! The sacred eye is mine to use!",
            "The darkness speaks to ME now!",
            "Your vision grows clouded, give me the eye!",
            "The patterns reveal themselves to ME!"
        ]
    }

    def __init__(self):
        super().__init__("moirai")
        self.golden_analyzer = GoldenAnalyzer()
        self.shared_eye = {
            'current_holder': 'clotho',
            'metrics_seen': 0,
            'last_swap': datetime.now()
        }
        
        # Initialize dark aspects specific to Chthonic nature
        self.dark_aspects = {
            'void_resonance': 0.0,
            'chaos_affinity': 0.0,
            'pattern_darkness': 0.0
        }
        
        self.logger.info("💫 From the depths, the Sisters of Fate arise...")
        self._random_greeting()

    def _random_quote(self, category):
        """Select a random quote from the specified category"""
        if category in self.FATE_QUOTES:
            return random.choice(self.FATE_QUOTES[category])
        return "..."

    def _random_greeting(self):
        """Issue a random greeting from the depths"""
        self.logger.info(f"🌑 {self._random_quote('greetings')}")

    def _pass_the_eye(self, to_sister):
        """Sisters dramatically passing their shared eye"""
        current = self.shared_eye['current_holder']
        self.shared_eye['current_holder'] = to_sister
        self.logger.info(f"👁️ {self._random_quote('bickering')}")
        self.logger.info(f"Eye passed from {current} to {to_sister}")

    def _calculate_void_resonance(self, code_structure):
        """Measure how well the code resonates with the void"""
        try:
            structure_depth = code_structure.count('\n')
            golden_depth = structure_depth / self.golden_analyzer.phi
            self.dark_aspects['void_resonance'] = 1 - abs(structure_depth - golden_depth) / structure_depth
        except:
            self.dark_aspects['void_resonance'] = 0.0

    def _measure_chaos_affinity(self, code_analysis):
        """Determine how chaos-aligned the code is"""
        try:
            if code_analysis['worthy']:
                # Reduce chaos when golden ratio is present
                self.dark_aspects['chaos_affinity'] = 0.5 - (code_analysis['golden_ratios_found'] / 10)
            else:
                # Chaos rises in the absence of divine proportion
                self.dark_aspects['chaos_affinity'] = 0.8
        except:
            self.dark_aspects['chaos_affinity'] = 1.0

    def _assess_pattern_darkness(self, thread_data):
        """Evaluate the darkness within code patterns"""
        try:
            # Patterns become darker as they deviate from the golden ratio
            deviation = abs(1 - thread_data.get('ratio', 0) / self.golden_analyzer.phi)
            self.dark_aspects['pattern_darkness'] = min(1.0, deviation)
        except:
            self.dark_aspects['pattern_darkness'] = 0.5

    def clotho_spins(self, thread_data):
        """Clotho, who spins the thread of life from the darkness"""
        if self.shared_eye['current_holder'] != 'clotho':
            self._pass_the_eye('clotho')

        self.logger.info("🕸️ Clotho begins to spin in the shadows...")
        
        try:
            analysis = self.golden_analyzer.analyze_thread(thread_data['code'])
            self.logger.info(f"Thread quality: {analysis['worthy']}")
            return analysis
        except Exception as e:
            self.logger.error(f"💔 Clotho's thread tangled in the void: {e}")
            return None

    def lachesis_measures(self, thread_data):
        """Lachesis, who measures the thread in the darkness"""
        if self.shared_eye['current_holder'] != 'lachesis':
            self._pass_the_eye('lachesis')

        self.logger.info(f"📏 Lachesis: {self._random_quote('measuring')}")
        
        try:
            analysis = self.golden_analyzer.analyze_thread(thread_data['code'])
            if analysis['worthy']:
                self.logger.info("✨ Lachesis: The patterns align in darkness...")
            else:
                self.logger.info(f"⚠️ Lachesis: {self._random_quote('warnings')}")
            return analysis
        except Exception as e:
            self.logger.error(f"💔 Lachesis's measurements were swallowed by shadow: {e}")
            return None

    def atropos_cuts(self, thread_data):
        """Atropos: The inevitable end, emerging from darkness"""
        if self.shared_eye['current_holder'] != 'atropos':
            self._pass_the_eye('atropos')

        self.logger.info("🌑 Atropos emerges from the void, shears gleaming in the darkness...")
        
        try:
            analysis = self.golden_analyzer.analyze_thread(thread_data['code'])
            
            self._calculate_void_resonance(thread_data['code'])
            self._measure_chaos_affinity(analysis)
            self._assess_pattern_darkness(thread_data)
            
            # Only cut if BOTH divine proportion is missing AND chaos is high
            should_cut = (not analysis['worthy'] and self.dark_aspects['chaos_affinity'] > 0.8)
            
            if should_cut:
                fate = {
                    'cut': True,
                    'reason': f"The void claims this thread. {analysis['message']}",
                    'golden_ratios': analysis['golden_ratios_found'],
                    'dark_aspects': self.dark_aspects
                }
                self.logger.info(f"⚫ Atropos: {self._random_quote('cutting')}")
            else:
                fate = {
                    'cut': False,
                    'reason': f"The darkness respects the divine patterns. {analysis['message']}",
                    'golden_ratios': analysis['golden_ratios_found'],
                    'dark_aspects': self.dark_aspects
                }
                self.logger.info("🌒 Atropos: Even the void bows to divine proportion.")

            if analysis['golden_ratios_found'] > 0:
                self.logger.info("✨ The golden ratio protects this thread from the void.")
            elif self.dark_aspects['chaos_affinity'] > 0.9:
                self.logger.info("🌑 Chaos consumes all that lacks divine structure.")
            
            return fate
            
        except Exception as e:
            self.logger.error("💔 Atropos: The darkness consumes our vision!")
            return None

    def pulse(self):
        """The dark pulse of fate"""
        self.logger.info("🌑 The Fates stir in their dark domain...")
        try:
            # TODO: Implement the main pulse logic
            pass
        except Exception as e:
            self.logger.error(f"💔 The void disrupts our work: {e}")
        finally:
            self.logger.info("⚫ The Fates return to their shadowy vigil...")
