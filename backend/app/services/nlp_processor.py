import spacy
import re
from typing import Dict, List, Optional

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    print("Downloading spaCy model...")
    spacy.cli.download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")

class NLPProcessor:
    def __init__(self):
        # Component type keywords
        self.component_types = {
            "cpu": ["cpu", "processor", "intel", "amd", "ryzen", "core", "i3", "i5", "i7", "i9"],
            "gpu": ["gpu", "graphics card", "video card", "nvidia", "geforce", "rtx", "gtx", "radeon", "rx", "graphics"],
            "motherboard": ["motherboard", "mobo", "mainboard"],
            "ram": ["ram", "memory", "ddr4", "ddr5"],
            "power_supply": ["power supply", "psu", "power"],
        }
        
        # Popular games (for gaming use case detection)
        self.popular_games = [
            "cyberpunk", "fortnite", "call of duty", "cod", "warzone", "apex legends",
            "battlefield", "minecraft", "valorant", "league of legends", "pubg", "gta",
            "grand theft auto", "doom", "overwatch", "destiny", "rainbow six", "halo",
            "assassin's creed", "far cry", "skyrim", "witcher", "dark souls", "elden ring"
        ]
        
        # Component brand keywords
        self.component_brands = {
            "cpu": {
                "intel": ["intel", "core", "i3", "i5", "i7", "i9"],
                "amd": ["amd", "ryzen", "threadripper"]
            },
            "gpu": {
                "nvidia": ["nvidia", "geforce", "rtx", "gtx"],
                "amd": ["amd", "radeon", "rx"]
            },
            "motherboard": {
                "asus": ["asus", "rog", "tuf"],
                "msi": ["msi"],
                "gigabyte": ["gigabyte", "aorus"],
                "asrock": ["asrock"]
            },
            "ram": {
                "corsair": ["corsair", "vengeance"],
                "g.skill": ["g.skill", "ripjaws", "trident"],
                "kingston": ["kingston", "fury"],
                "crucial": ["crucial", "ballistix"]
            },
            "power_supply": {
                "corsair": ["corsair"],
                "evga": ["evga"],
                "seasonic": ["seasonic"],
                "thermaltake": ["thermaltake"],
                "be quiet": ["be quiet"]
            }
        }
        
        # Budget pattern - improved to catch approximate values
        self.budget_pattern = r"(?:budget|price|cost|around|about|approximately)\s+(?:is|of)?\s*\$?(\d+(?:,\d+)?(?:\.\d+)?)|(\d+(?:,\d+)?(?:\.\d+)?)\s*(?:dollars|usd)"
        
        # Gaming phrases pattern
        self.gaming_phrases = [
            r"(?:run|play)\s+\w+\s+(?:at|on)\s+(?:max|high|ultra|maximum)\s+(?:settings|graphics|quality)",
            r"gaming\s+pc",
            r"play\s+games",
            r"for\s+gaming",
            r"max\s+fps",
            r"high\s+frame\s+rates?",
            r"max\s+settings"
        ]
        
        # Use case patterns with weighted scoring
        self.use_cases = {
            "gaming": ["gaming", "game", "fps", "play", "gamer", "settings", "max settings", "ultra"],
            "productivity": ["productivity", "work", "office", "multitasking"],
            "content_creation": ["content creation", "video editing", "streaming", "rendering"],
            "budget_build": ["budget", "cheap", "affordable", "low cost"],
            "high_end": ["high end", "premium", "enthusiast", "high performance"]
        }
    
    def extract_component_mentions(self, text: str) -> Dict[str, List[str]]:
        """Extract component type mentions from text"""
        text = text.lower()
        doc = nlp(text)
        
        component_mentions = {comp_type: [] for comp_type in self.component_types}
        
        # Extract component mentions using spaCy entities and pattern matching
        for token in doc:
            for comp_type, keywords in self.component_types.items():
                for keyword in keywords:
                    if keyword in token.text.lower():
                        # Find the full span that might contain model numbers
                        span = self._extract_component_span(doc, token.i)
                        if span and span not in component_mentions[comp_type]:
                            component_mentions[comp_type].append(span)
        
        return component_mentions
    
    def extract_budget(self, text: str) -> Optional[float]:
        """Extract budget from text with improved pattern matching"""
        text = text.lower()
        
        # First try the main budget pattern
        matches = re.findall(self.budget_pattern, text)
        if matches:
            # Process matches from the regex groups
            for match in matches:
                # Match could be in either group
                budget_str = next((m for m in match if m), None)
                if budget_str:
                    # Remove commas and convert to float
                    return float(budget_str.replace(',', ''))
        
        # Fallback: try to find any number after words like "budget", "around", etc.
        budget_mentions = re.findall(r"(?:budget|price|cost|around|about|approximately).*?(\d+)", text)
        if budget_mentions:
            return float(budget_mentions[0].replace(',', ''))
        
        return None
    
    def extract_use_case(self, text: str) -> Dict[str, float]:
        """Extract use case preferences from text with improved gaming detection"""
        text = text.lower()
        
        use_case_scores = {use_case: 0.0 for use_case in self.use_cases}
        
        # Check for direct mentions of use cases
        for use_case, keywords in self.use_cases.items():
            for keyword in keywords:
                if keyword in text:
                    use_case_scores[use_case] += 1.0
        
        # Check for gaming-specific patterns
        for pattern in self.gaming_phrases:
            if re.search(pattern, text):
                use_case_scores["gaming"] += 2.0  # Higher weight for gaming phrases
        
        # Check for specific game mentions
        for game in self.popular_games:
            if game in text:
                use_case_scores["gaming"] += 1.5  # Bonus for mentioning specific games
                break
        
        # Check for "max settings" or similar gaming quality indicators
        if re.search(r"(?:max|high|ultra)\s+(?:settings|quality|graphics)", text):
            use_case_scores["gaming"] += 1.5
            use_case_scores["high_end"] += 1.0  # Max settings implies high-end
        
        # Normalize scores
        total_score = sum(use_case_scores.values())
        if total_score > 0:
            for use_case in use_case_scores:
                use_case_scores[use_case] /= total_score
        
        return use_case_scores
    
    def _extract_component_span(self, doc, token_idx: int) -> Optional[str]:
        """Extract a span of text that might contain a component mention"""
        start_idx = max(0, token_idx - 2)
        end_idx = min(len(doc), token_idx + 4)
        
        # Extract a window around the token and clean it
        span = doc[start_idx:end_idx].text.strip()
        return span if span else None

    def process_query(self, text: str) -> Dict:
        """Process a natural language query and extract relevant information"""
        # Correct common typos in game names before processing
        text = self._correct_game_typos(text)
        
        result = {
            "component_mentions": self.extract_component_mentions(text),
            "budget": self.extract_budget(text),
            "use_case": self.extract_use_case(text)
        }
        
        return result
    
    def _correct_game_typos(self, text: str) -> str:
        """Correct common typos in game names"""
        corrections = {
            "cyberbunk": "cyberpunk",
            "fortnight": "fortnite",
            "war zone": "warzone",
            "mine craft": "minecraft",
            "grand theft auto 5": "gta",
            "gta 5": "gta",
            "gta v": "gta"
        }
        
        for typo, correction in corrections.items():
            text = re.sub(r'\b' + re.escape(typo) + r'\b', correction, text, flags=re.IGNORECASE)
        
        return text