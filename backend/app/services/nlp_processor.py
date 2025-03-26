import spacy
import re
from typing import Dict, List, Optional, Tuple

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
        
        # Improved budget patterns
        self.budget_patterns = [
            # Exact budget pattern (e.g., "$1500", "1500 dollars", "budget of $1500")
            r"(?:budget|price|cost|spend|spending)\s+(?:is|of)?\s*\$?(\d+(?:,\d+)?(?:\.\d+)?)|(?:looking to spend|would spend|planning to spend)\s+\$?(\d+(?:,\d+)?(?:\.\d+)?)",
            
            # Approximate budget pattern (e.g., "about $1500", "around $1500")
            r"(?:about|around|approximately|roughly|close to)\s+\$?(\d+(?:,\d+)?(?:\.\d+)?)",
            
            # Upper limit pattern (e.g., "under $1500", "less than $1500")
            r"(?:under|below|less than|at most|maximum of|no more than|up to|not more than)\s+\$?(\d+(?:,\d+)?(?:\.\d+)?)",
            
            # Lower limit pattern (e.g., "over $1500", "more than $1500")
            r"(?:over|above|more than|at least|minimum of|starting from|starting at)\s+\$?(\d+(?:,\d+)?(?:\.\d+)?)",
            
            # Range pattern (e.g., "between $1000 and $1500")
            r"between\s+\$?(\d+(?:,\d+)?(?:\.\d+)?)\s+(?:and|to|[-])\s+\$?(\d+(?:,\d+)?(?:\.\d+)?)",
            
            # Fallback for standalone dollar amounts with optional budget context
            r"(?:budget|build)(?:[^$]*?)\$(\d+(?:,\d+)?(?:\.\d+)?)",
            r"\$(\d+(?:,\d+)?(?:\.\d+)?)",
            r"(\d+(?:,\d+)?(?:\.\d+)?)\s*(?:dollars|usd)"
        ]
        
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
    
    def extract_budget(self, text: str) -> Dict[str, float]:
        """Extract budget information from text with improved pattern matching
        
        Returns:
            A dictionary with keys:
            - value: The numeric budget value
            - type: 'exact', 'approximate', 'maximum', 'minimum', or 'range'
            - range_min: Lower value in a range (if applicable)
            - range_max: Upper value in a range (if applicable)
            - tolerance: Percentage tolerance for approximate values
        """
        text = text.lower()
        result = {
            "value": 1500.0,  # Default value
            "type": "exact",  # Default type
            "tolerance": 0.0   # Default tolerance (percentage)
        }
        
        # Check for budget patterns in order of specificity
        for i, pattern in enumerate(self.budget_patterns):
            matches = re.search(pattern, text)
            if matches:
                # Handle different patterns
                if i == 0:  # Exact budget
                    # Get the first non-None group
                    for group in matches.groups():
                        if group:
                            result["value"] = float(group.replace(',', ''))
                            result["type"] = "exact"
                            result["tolerance"] = 0.0
                            break
                elif i == 1:  # Approximate budget
                    result["value"] = float(matches.group(1).replace(',', ''))
                    result["type"] = "approximate"
                    result["tolerance"] = 0.07  # 7% tolerance for "about" and "around" (was 10%)
                elif i == 2:  # Upper limit
                    result["value"] = float(matches.group(1).replace(',', ''))
                    result["type"] = "maximum"
                    # Setting maximum a bit below the stated limit to ensure we stay under budget
                    result["value"] = result["value"] * 0.97  # Target 3% below maximum
                    result["tolerance"] = 0.0
                elif i == 3:  # Lower limit
                    result["value"] = float(matches.group(1).replace(',', ''))
                    result["type"] = "minimum"
                    # Setting minimum a bit above the stated minimum to ensure we're over the budget
                    result["value"] = result["value"] * 1.05  # Target 5% above minimum
                    result["tolerance"] = 0.0
                elif i == 4:  # Range
                    min_val = float(matches.group(1).replace(',', ''))
                    max_val = float(matches.group(2).replace(',', ''))
                    # Use the middle of the range as the target value
                    result["value"] = (min_val + max_val) / 2
                    result["type"] = "range"
                    result["range_min"] = min_val
                    result["range_max"] = max_val
                    result["tolerance"] = (max_val - min_val) / 2 / result["value"]  # Tolerance as percentage
                else:  # Fallback patterns (standalone dollar amounts)
                    result["value"] = float(matches.group(1).replace(',', ''))
                    result["type"] = "exact"
                    result["tolerance"] = 0.05  # Allow 5% flexibility for standalone dollar amounts
                
                return result
        
        # No match found, return default
        return result
    
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
            "use_case": self.extract_use_case(text),
            "mentioned_games": self._extract_game_mentions(text)
        }
        
        return result
    
    def _extract_game_mentions(self, text: str) -> List[str]:
        """Extract mentioned games from text"""
        text = text.lower()
        mentioned_games = []
        
        for game in self.popular_games:
            if game in text:
                mentioned_games.append(game)
        
        return mentioned_games
    
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