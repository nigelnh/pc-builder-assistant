from typing import Dict, List, Optional, Union, Tuple
from sqlalchemy.orm import Session

from app.models.components import CPU, GPU, Motherboard, RAM, PowerSupply
from app.services.compatibility import CompatibilityChecker

class RecommendationEngine:
    def __init__(self):
        self.compatibility_checker = CompatibilityChecker()
        
        # Performance tiers for different use cases
        self.performance_tiers = {
            "gaming": {
                "budget": {
                    "cpu_keywords": ["i5", "ryzen 5"],
                    "gpu_keywords": ["rtx 3060", "rx 6600"],
                    "ram_capacity": 16,
                    "min_price": 700,
                    "max_price": 1000
                },
                "mid_range": {
                    "cpu_keywords": ["i7", "ryzen 7"],
                    "gpu_keywords": ["rtx 3070", "rtx 4060 ti", "rx 6700"],
                    "ram_capacity": 32,
                    "min_price": 1000,
                    "max_price": 1600
                },
                "high_end": {
                    "cpu_keywords": ["i9", "ryzen 9"],
                    "gpu_keywords": ["rtx 3080", "rtx 3090", "rtx 4070", "rtx 4080", "rx 6800", "rx 6900"],
                    "ram_capacity": 32,
                    "min_price": 1600,
                    "max_price": 3000
                }
            },
            "productivity": {
                "budget": {
                    "cpu_keywords": ["i5", "ryzen 5"],
                    "gpu_keywords": ["rtx 3050", "integrated"],
                    "ram_capacity": 16,
                    "min_price": 600,
                    "max_price": 900
                },
                "mid_range": {
                    "cpu_keywords": ["i7", "ryzen 7"],
                    "gpu_keywords": ["rtx 3060", "rx 6600"],
                    "ram_capacity": 32,
                    "min_price": 900,
                    "max_price": 1400
                },
                "high_end": {
                    "cpu_keywords": ["i9", "ryzen 9"],
                    "gpu_keywords": ["rtx 3070", "rtx 4060", "rx 6700"],
                    "ram_capacity": 64,
                    "min_price": 1400,
                    "max_price": 2500
                }
            },
            "content_creation": {
                "budget": {
                    "cpu_keywords": ["i7", "ryzen 7"],
                    "gpu_keywords": ["rtx 3060", "rx 6600"],
                    "ram_capacity": 32,
                    "min_price": 1000,
                    "max_price": 1500
                },
                "mid_range": {
                    "cpu_keywords": ["i7", "ryzen 9"],
                    "gpu_keywords": ["rtx 3070", "rtx 4060 ti", "rx 6700"],
                    "ram_capacity": 32,
                    "min_price": 1500,
                    "max_price": 2200
                },
                "high_end": {
                    "cpu_keywords": ["i9", "ryzen 9"],
                    "gpu_keywords": ["rtx 3080", "rtx 3090", "rtx 4070", "rtx 4080", "rx 6800", "rx 6900"],
                    "ram_capacity": 64,
                    "min_price": 2200,
                    "max_price": 3500
                }
            }
        }
    
    def determine_use_case(self, use_case_scores: Dict[str, float]) -> str:
        """Determine the primary use case based on scores"""
        if not use_case_scores:
            return "gaming"  # Default to gaming if no scores
        
        # Get the use case with the highest score
        primary_use_case = max(use_case_scores.items(), key=lambda x: x[1])[0]
        
        # Map to one of our three main categories
        if primary_use_case in ["gaming"]:
            return "gaming"
        elif primary_use_case in ["productivity", "budget_build"]:
            return "productivity"
        elif primary_use_case in ["content_creation", "high_end"]:
            return "content_creation"
        else:
            return "gaming"  # Default fallback
    
    def determine_tier(self, budget: Optional[float], use_case: str) -> str:
        """Determine the performance tier based on budget and use case"""
        if not budget:
            return "mid_range"  # Default to mid-range if no budget specified
        
        use_case_tiers = self.performance_tiers.get(use_case, self.performance_tiers["gaming"])
        
        # Determine tier based on budget
        if budget <= use_case_tiers["budget"]["max_price"]:
            return "budget"
        elif budget <= use_case_tiers["mid_range"]["max_price"]:
            return "mid_range"
        else:
            return "high_end"
    
    def select_components(
        self, 
        db: Session, 
        use_case: str, 
        tier: str, 
        budget: Optional[float] = None
    ) -> Dict[str, Union[CPU, GPU, Motherboard, List[RAM], PowerSupply]]:
        """Select appropriate components based on use case, tier, and budget"""
        # Get tier specifications
        tier_specs = self.performance_tiers.get(use_case, {}).get(tier, {})
        
        # Initialize result with placeholders
        selected_components = {}
        
        # Select CPU based on tier keywords
        cpu_keywords = tier_specs.get("cpu_keywords", [])
        cpus = db.query(CPU).all()
        
        # Filter CPUs by keywords and sort by price
        matching_cpus = []
        for cpu in cpus:
            if any(keyword.lower() in cpu.name.lower() for keyword in cpu_keywords):
                matching_cpus.append(cpu)
        
        # If no match, use all CPUs
        if not matching_cpus:
            matching_cpus = cpus
            
        # Sort by price, with mid-tier CPUs first
        cpu_budget = (budget * 0.25) if budget else None
        selected_cpu = self._select_component_by_price(matching_cpus, cpu_budget)
        
        if selected_cpu:
            selected_components["cpu"] = selected_cpu
        
        # Select GPU based on tier keywords
        gpu_keywords = tier_specs.get("gpu_keywords", [])
        gpus = db.query(GPU).all()
        
        # Filter GPUs by keywords and sort by price
        matching_gpus = []
        for gpu in gpus:
            if any(keyword.lower() in gpu.name.lower() for keyword in gpu_keywords):
                matching_gpus.append(gpu)
        
        # If no match, use all GPUs
        if not matching_gpus:
            matching_gpus = gpus
            
        # Sort by price, with mid-tier GPUs first
        gpu_budget = (budget * 0.4) if budget else None
        selected_gpu = self._select_component_by_price(matching_gpus, gpu_budget)
        
        if selected_gpu:
            selected_components["gpu"] = selected_gpu
        
        # Select Motherboard compatible with CPU
        if "cpu" in selected_components:
            cpu = selected_components["cpu"]
            motherboards = db.query(Motherboard).all()
            
            # Filter for compatible motherboards
            compatible_motherboards = [
                mb for mb in motherboards 
                if mb.socket == cpu.socket
            ]
            
            if compatible_motherboards:
                # Select a mid-price motherboard
                mb_budget = (budget * 0.15) if budget else None
                selected_motherboard = self._select_component_by_price(compatible_motherboards, mb_budget)
                if selected_motherboard:
                    selected_components["motherboard"] = selected_motherboard
        
        # Select RAM based on capacity requirements
        ram_capacity = tier_specs.get("ram_capacity", 16)
        rams = db.query(RAM).all()
        
        # Try to find RAM that matches our capacity target
        matching_rams = []
        for ram in rams:
            # Check if this single RAM meets our target
            if ram.capacity == ram_capacity and ram.modules >= 1:
                matching_rams.append([ram])
            # Or check if two of these would meet our target
            elif ram.capacity * 2 == ram_capacity and ram.modules >= 2:
                matching_rams.append([ram, ram])
        
        # If no perfect match, try combinations
        if not matching_rams and rams:
            # For simplicity, just take the first RAM that has the right capacity per stick
            for ram in rams:
                if ram.capacity in [8, 16, 32] and ram.modules >= 1:
                    # Calculate how many we need
                    needed_sticks = ram_capacity // ram.capacity
                    if needed_sticks <= 4:  # Most motherboards support 4 sticks max
                        matching_rams.append([ram] * needed_sticks)
                        break
            
            # If still no match, just take any RAM
            if not matching_rams:
                matching_rams.append([rams[0]])
        
        # Select the RAM set with the best price/capacity ratio
        if matching_rams:
            ram_sets_with_price = []
            for ram_set in matching_rams:
                total_price = sum(ram.price for ram in ram_set)
                total_capacity = sum(ram.capacity for ram in ram_set)
                ram_sets_with_price.append((ram_set, total_price, total_capacity))
            
            # Sort by price/capacity ratio
            ram_sets_with_price.sort(key=lambda x: x[1]/x[2])
            
            # Take the best value RAM set
            ram_budget = (budget * 0.1) if budget else None
            for ram_set, price, _ in ram_sets_with_price:
                if not ram_budget or price <= ram_budget:
                    selected_components["ram"] = ram_set
                    break
            
            # If none match budget, take the cheapest
            if "ram" not in selected_components and ram_sets_with_price:
                selected_components["ram"] = ram_sets_with_price[0][0]
        
        # Select Power Supply
        # Calculate power requirements
        base_power = 75  # Base system power
        cpu_power = selected_components.get("cpu").tdp if "cpu" in selected_components else 65
        gpu_power = selected_components.get("gpu").tdp if "gpu" in selected_components else 150
        
        # Add 50% headroom
        total_power = (base_power + cpu_power + gpu_power) * 1.5
        
        # Find appropriate PSU
        psus = db.query(PowerSupply).all()
        suitable_psus = [psu for psu in psus if psu.wattage >= total_power]
        
        if suitable_psus:
            psu_budget = (budget * 0.1) if budget else None
            selected_psu = self._select_component_by_price(suitable_psus, psu_budget)
            if selected_psu:
                selected_components["power_supply"] = selected_psu
        elif psus:
            # If no PSU meets the requirement, take the highest wattage
            selected_components["power_supply"] = max(psus, key=lambda x: x.wattage)
        
        return selected_components
    
    def _select_component_by_price(self, components, budget=None):
        """Select a component based on price, prioritizing mid-range if no budget"""
        if not components:
            return None
            
        # Sort by price
        components_by_price = sorted(components, key=lambda x: x.price)
        
        if not budget:
            # If no budget, aim for a mid-range component
            middle_index = len(components_by_price) // 2
            return components_by_price[middle_index]
        
        # Find components within budget
        within_budget = [c for c in components_by_price if c.price <= budget]
        
        if within_budget:
            # Get the best component within budget
            return within_budget[-1]
        
        # If nothing is in budget, get the cheapest
        return components_by_price[0]
    
    def generate_recommendations(self, db: Session, nlp_data: Dict) -> Dict:
        """Generate PC build recommendations based on NLP analysis"""
        # Extract data from NLP result
        use_case_scores = nlp_data.get("use_case", {})
        budget = nlp_data.get("budget")
        
        # Determine primary use case and tier
        use_case = self.determine_use_case(use_case_scores)
        tier = self.determine_tier(budget, use_case)
        
        # Generate three recommendations: budget, recommended (target), and high-end
        recommendations = {}
        
        # 1. Budget version (one tier down or the same if already budget)
        budget_tier = "budget"
        budget_components = self.select_components(
            db, 
            use_case, 
            budget_tier,
            budget * 0.8 if budget else None
        )
        budget_price = sum(
            c.price for c in budget_components.values() 
            if not isinstance(c, list)
        ) + sum(
            sum(r.price for r in rams) for rams in 
            [budget_components.get('ram', [])] if rams
        )
        
        # 2. Recommended version (target tier)
        recommended_components = self.select_components(
            db, 
            use_case, 
            tier,
            budget
        )
        recommended_price = sum(
            c.price for c in recommended_components.values() 
            if not isinstance(c, list)
        ) + sum(
            sum(r.price for r in rams) for rams in 
            [recommended_components.get('ram', [])] if rams
        )
        
        # 3. High-end version (one tier up or the same if already high-end)
        high_end_tier = "high_end"
        high_end_components = self.select_components(
            db, 
            use_case, 
            high_end_tier,
            budget * 1.2 if budget else None
        )
        high_end_price = sum(
            c.price for c in high_end_components.values() 
            if not isinstance(c, list)
        ) + sum(
            sum(r.price for r in rams) for rams in 
            [high_end_components.get('ram', [])] if rams
        )
        
        # Format results
        recommendations = {
            "user_requirements": {
                "use_case": use_case,
                "target_tier": tier,
                "budget": budget
            },
            "builds": {
                "budget": {
                    "components": self._format_component_list(budget_components),
                    "total_price": round(budget_price, 2),
                    "compatibility": self.compatibility_checker.check_system_compatibility(budget_components)["compatible"]
                },
                "recommended": {
                    "components": self._format_component_list(recommended_components),
                    "total_price": round(recommended_price, 2),
                    "compatibility": self.compatibility_checker.check_system_compatibility(recommended_components)["compatible"]
                },
                "high_end": {
                    "components": self._format_component_list(high_end_components),
                    "total_price": round(high_end_price, 2),
                    "compatibility": self.compatibility_checker.check_system_compatibility(high_end_components)["compatible"]
                }
            }
        }
        
        return recommendations
    
    def _format_component_list(self, components: Dict) -> Dict[str, Dict]:
        """Format component dictionary for API response"""
        result = {}
        
        if "cpu" in components:
            cpu = components["cpu"]
            result["cpu"] = {
                "id": cpu.id,
                "name": cpu.name,
                "brand": cpu.brand,
                "model": cpu.model,
                "price": cpu.price
            }
        
        if "gpu" in components:
            gpu = components["gpu"]
            result["gpu"] = {
                "id": gpu.id,
                "name": gpu.name,
                "brand": gpu.brand,
                "model": gpu.model,
                "price": gpu.price
            }
        
        if "motherboard" in components:
            mb = components["motherboard"]
            result["motherboard"] = {
                "id": mb.id,
                "name": mb.name,
                "brand": mb.brand,
                "model": mb.model,
                "price": mb.price
            }
        
        if "ram" in components and components["ram"]:
            rams = components["ram"]
            result["ram"] = [{
                "id": ram.id,
                "name": ram.name,
                "brand": ram.brand,
                "capacity": ram.capacity,
                "price": ram.price
            } for ram in rams]
        
        if "power_supply" in components:
            psu = components["power_supply"]
            result["power_supply"] = {
                "id": psu.id,
                "name": psu.name,
                "brand": psu.brand,
                "model": psu.model,
                "wattage": psu.wattage,
                "price": psu.price
            }
        
        return result