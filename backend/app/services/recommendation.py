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
        
        # Adjust budget allocations based on total budget to prevent exceeding
        # These percentages should add up to <= 90% to leave room for other components
        if budget:
            if budget <= 1000:
                # Budget builds need more conservative component allocation
                cpu_percent = 0.20  # 20% for CPU
                gpu_percent = 0.35  # 35% for GPU
                mb_percent = 0.12   # 12% for motherboard 
                ram_percent = 0.08  # 8% for RAM
                psu_percent = 0.08  # 8% for PSU
            elif budget <= 1500:
                # Mid-range builds
                cpu_percent = 0.22  # 22% for CPU
                gpu_percent = 0.37  # 37% for GPU
                mb_percent = 0.13   # 13% for motherboard
                ram_percent = 0.08  # 8% for RAM
                psu_percent = 0.07  # 7% for PSU
            else:
                # High-end builds can allocate more to CPU and GPU
                cpu_percent = 0.23  # 23% for CPU
                gpu_percent = 0.40  # 40% for GPU
                mb_percent = 0.12   # 12% for motherboard
                ram_percent = 0.09  # 9% for RAM
                psu_percent = 0.06  # 6% for PSU
        else:
            # Default allocations if no budget specified
            cpu_percent = 0.25
            gpu_percent = 0.40
            mb_percent = 0.15
            ram_percent = 0.10
            psu_percent = 0.10
            
        # For gaming builds, allocate more to GPU and less to CPU
        if use_case == "gaming":
            # Adjust for gaming - more GPU, less CPU
            if budget and budget <= 1200:
                # For $1200 gaming builds specifically
                cpu_percent = 0.18  # 18% for CPU (~$216)
                gpu_percent = 0.40  # 40% for GPU (~$480)
                mb_percent = 0.12   # 12% for motherboard (~$144)
                ram_percent = 0.07  # 7% for RAM (~$84)
                psu_percent = 0.06  # 6% for PSU (~$72)
            else:
                # Slight adjustment for other gaming budgets
                cpu_percent -= 0.03
                gpu_percent += 0.03
        
        # For productivity, allocate more to CPU and RAM
        if use_case == "productivity":
            cpu_percent += 0.05
            gpu_percent -= 0.10
            ram_percent += 0.05
        
        # Select CPU based on tier keywords and budget
        cpu_keywords = tier_specs.get("cpu_keywords", [])
        cpus = db.query(CPU).all()
        
        # Filter CPUs by keywords and sort by price
        matching_cpus = []
        for cpu in cpus:
            if any(keyword.lower() in cpu.name.lower() for keyword in cpu_keywords):
                matching_cpus.append(cpu)
        
        # If no match or very few matches (less than 3), use all CPUs
        if len(matching_cpus) < 3:
            matching_cpus = cpus
            
        # Calculate CPU budget
        cpu_budget = (budget * cpu_percent) if budget else None
        selected_cpu = self._select_component_by_price(matching_cpus, cpu_budget)
        
        if selected_cpu:
            selected_components["cpu"] = selected_cpu
            
            # Recalculate remaining budget after CPU selection
            if budget:
                remaining_budget = budget - selected_cpu.price
                # Recalculate percentages for other components based on remaining budget
                if remaining_budget > 0:
                    total_remaining_percent = gpu_percent + mb_percent + ram_percent + psu_percent
                    if total_remaining_percent > 0:
                        adjustment_factor = 1.0 / total_remaining_percent
                        gpu_percent = gpu_percent * adjustment_factor
                        mb_percent = mb_percent * adjustment_factor
                        ram_percent = ram_percent * adjustment_factor
                        psu_percent = psu_percent * adjustment_factor
        
        # Select GPU based on tier keywords and adjusted budget
        gpu_keywords = tier_specs.get("gpu_keywords", [])
        gpus = db.query(GPU).all()
        
        # Filter GPUs by keywords and sort by price
        matching_gpus = []
        for gpu in gpus:
            if any(keyword.lower() in gpu.name.lower() for keyword in gpu_keywords):
                matching_gpus.append(gpu)
        
        # If no match or very few matches, use all GPUs
        if len(matching_gpus) < 3:
            matching_gpus = gpus
            
        # Calculate GPU budget based on remaining budget if CPU was selected
        if budget and "cpu" in selected_components:
            remaining_budget = budget - selected_components["cpu"].price
            gpu_budget = remaining_budget * gpu_percent
        else:
            gpu_budget = (budget * gpu_percent) if budget else None
            
        selected_gpu = self._select_component_by_price(matching_gpus, gpu_budget)
        
        if selected_gpu:
            selected_components["gpu"] = selected_gpu
            
            # Recalculate remaining budget after GPU selection
            if budget:
                # Calculate what's been spent so far
                spent_budget = 0
                for component in selected_components.values():
                    if not isinstance(component, list):  # Skip RAM for now
                        spent_budget += component.price
                
                remaining_budget = budget - spent_budget
                # Recalculate percentages for remaining components
                if remaining_budget > 0:
                    total_remaining_percent = mb_percent + ram_percent + psu_percent
                    if total_remaining_percent > 0:
                        adjustment_factor = 1.0 / total_remaining_percent
                        mb_percent = mb_percent * adjustment_factor
                        ram_percent = ram_percent * adjustment_factor
                        psu_percent = psu_percent * adjustment_factor
        
        # Select Motherboard compatible with CPU with adjusted budget
        if "cpu" in selected_components:
            cpu = selected_components["cpu"]
            motherboards = db.query(Motherboard).all()
            
            # Filter for compatible motherboards
            compatible_motherboards = [
                mb for mb in motherboards 
                if mb.socket == cpu.socket
            ]
            
            if compatible_motherboards:
                # Calculate motherboard budget based on remaining budget
                if budget:
                    spent_budget = 0
                    for component in selected_components.values():
                        if not isinstance(component, list):
                            spent_budget += component.price
                    
                    remaining_budget = budget - spent_budget
                    mb_budget = remaining_budget * mb_percent
                else:
                    mb_budget = (budget * mb_percent) if budget else None
                    
                selected_motherboard = self._select_component_by_price(compatible_motherboards, mb_budget)
                if selected_motherboard:
                    selected_components["motherboard"] = selected_motherboard
                    
                    # Recalculate remaining budget after motherboard selection
                    if budget:
                        spent_budget = 0
                        for component in selected_components.values():
                            if not isinstance(component, list):
                                spent_budget += component.price
                        
                        remaining_budget = budget - spent_budget
                        # Recalculate percentages for RAM and PSU
                        if remaining_budget > 0:
                            total_remaining_percent = ram_percent + psu_percent
                            if total_remaining_percent > 0:
                                adjustment_factor = 1.0 / total_remaining_percent
                                ram_percent = ram_percent * adjustment_factor
                                psu_percent = psu_percent * adjustment_factor
        
        # Select RAM based on capacity requirements and adjusted budget
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
                    # Calculate how many sticks we need
                    needed_sticks = min(ram_capacity // ram.capacity, 4)  # Most motherboards support 4 sticks max
                    if needed_sticks > 0:
                        matching_rams.append([ram] * needed_sticks)
                        break
            
            # If still no match, just take any RAM
            if not matching_rams and rams:
                matching_rams.append([rams[0]])
        
        # Calculate what's been spent so far
        if budget:
            spent_budget = 0
            for component in selected_components.values():
                if not isinstance(component, list):
                    spent_budget += component.price
            
            remaining_budget = budget - spent_budget
            ram_budget = remaining_budget * ram_percent
        else:
            ram_budget = (budget * ram_percent) if budget else None
        
        # Select the RAM set with the best price/capacity ratio within budget
        if matching_rams:
            ram_sets_with_price = []
            for ram_set in matching_rams:
                total_price = sum(ram.price for ram in ram_set)
                total_capacity = sum(ram.capacity for ram in ram_set)
                ram_sets_with_price.append((ram_set, total_price, total_capacity))
            
            # Sort by price
            ram_sets_with_price.sort(key=lambda x: x[1])
            
            # Take the best RAM set within budget
            selected_ram = None
            for ram_set, price, _ in ram_sets_with_price:
                if not ram_budget or price <= ram_budget:
                    selected_ram = ram_set
                    if selected_ram is not ram_sets_with_price[-1][0]:  # If not the best RAM
                        # Try the next one if it fits in budget
                        next_index = ram_sets_with_price.index((ram_set, price, _)) + 1
                        if next_index < len(ram_sets_with_price) and ram_sets_with_price[next_index][1] <= ram_budget:
                            selected_ram = ram_sets_with_price[next_index][0]
                    break
            
            # If we found a RAM set, add it
            if selected_ram:
                selected_components["ram"] = selected_ram
            # If none match budget, take the cheapest
            elif ram_sets_with_price:
                selected_components["ram"] = ram_sets_with_price[0][0]
        
        # Calculate what's been spent so far
        if budget:
            spent_budget = 0
            for component in selected_components.values():
                if isinstance(component, list):  # Handle RAM which is a list
                    spent_budget += sum(ram.price for ram in component)
                else:
                    spent_budget += component.price
            
            remaining_budget = budget - spent_budget
        else:
            remaining_budget = None
        
        # Select Power Supply
        # Calculate power requirements
        base_power = 75  # Base system power
        cpu_power = selected_components.get("cpu").tdp if "cpu" in selected_components else 65
        gpu_power = selected_components.get("gpu").tdp if "gpu" in selected_components else 150
        
        # Add 50% headroom
        total_power = int((base_power + cpu_power + gpu_power) * 1.5)
        
        # Find appropriate PSU
        psus = db.query(PowerSupply).all()
        suitable_psus = [psu for psu in psus if psu.wattage >= total_power]
        
        # Calculate PSU budget from remaining budget
        if budget and remaining_budget is not None:
            psu_budget = remaining_budget * 0.9  # Use up to 90% of remaining budget for PSU
        else:
            psu_budget = (budget * psu_percent) if budget else None
        
        if suitable_psus:
            selected_psu = self._select_component_by_price(suitable_psus, psu_budget)
            if selected_psu:
                selected_components["power_supply"] = selected_psu
        elif psus:
            # If no PSU meets the requirement, take the highest wattage within budget
            within_budget_psus = [psu for psu in psus if not psu_budget or psu.price <= psu_budget]
            if within_budget_psus:
                selected_components["power_supply"] = max(within_budget_psus, key=lambda x: x.wattage)
            else:
                # If none within budget, take the cheapest suitable one
                suitable_psus = sorted(psus, key=lambda x: x.price)
                if suitable_psus:
                    selected_components["power_supply"] = suitable_psus[0]
        
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
        budget_info = nlp_data.get("budget", {})
        
        # Parse budget information
        if isinstance(budget_info, dict):
            target_budget = budget_info.get("value", 1500.0)
            budget_type = budget_info.get("type", "exact")
            
            # Handle different budget types
            if budget_type == "maximum":
                # For "under $X" queries, ensure we stay under budget
                target_budget = target_budget * 0.95  # Target 5% below to ensure we stay under
                price_tolerance = target_budget * 0.05  # Small tolerance
            elif budget_type == "minimum":
                # For "over $X" queries, ensure we meet minimum
                price_tolerance = target_budget * 0.15  # Larger tolerance for minimum budgets
            elif budget_type == "approximate":
                # For "about $X" queries
                price_tolerance = target_budget * budget_info.get("tolerance", 0.1)
            elif budget_type == "range":
                # For range budgets, use the middle value with tolerance equal to half the range
                target_budget = (budget_info.get("range_min", target_budget * 0.8) + 
                                budget_info.get("range_max", target_budget * 1.2)) / 2
                price_tolerance = (budget_info.get("range_max", target_budget * 1.2) - 
                                  budget_info.get("range_min", target_budget * 0.8)) / 2
            else:
                # Default exact budget with 5% tolerance
                price_tolerance = target_budget * 0.05
        else:
            # Legacy support for when budget was just a number
            target_budget = budget_info if budget_info else 1500.0
            price_tolerance = target_budget * 0.1  # 10% tolerance
        
        # Determine use case and performance tier
        use_case = self.determine_use_case(use_case_scores)
        tier = self.determine_tier(target_budget, use_case)
        
        # Check if budget is within the max/min budget for this tier
        tier_budget_min = self.performance_tiers[use_case][tier].get("min_price", 0)
        tier_budget_max = self.performance_tiers[use_case][tier].get("max_price", 999999)
        
        if target_budget < tier_budget_min:
            # If budget is too low for tier, adjust tier down
            if tier == "mid_range" or tier == "high_end":
                tier = "budget" if target_budget < tier_budget_min else tier
        elif target_budget > tier_budget_max:
            # If budget is too high for tier, adjust tier up
            if tier == "budget":
                tier = "mid_range"
            elif tier == "mid_range":
                tier = "high_end"
        
        def is_within_budget(price):
            """Check if price is within acceptable range of target budget"""
            # For maximum budget type, ensure we're always under
            if budget_type == "maximum":
                return price <= target_budget
            # For minimum budget type, ensure we're always over minimum
            elif budget_type == "minimum":
                return price >= target_budget
            # For other budget types, allow tolerance
            else:
                return abs(price - target_budget) <= price_tolerance
        
        # Generate recommendations with budget adherence
        recommended_components = self.select_components(db, use_case, tier, target_budget)
        
        # Calculate total price of components
        total_price = 0
        for component in recommended_components.values():
            if isinstance(component, list):  # Handle RAM which is a list
                total_price += sum(ram.price for ram in component)
            else:
                total_price += component.price
        
        # Apply budget adjustments if needed
        if not is_within_budget(total_price):
            if total_price > target_budget + price_tolerance:
                # Over budget - downgrade components
                recommended_components = self._downgrade_components(db, recommended_components, total_price - target_budget, use_case)
            elif budget_type != "maximum" and total_price < target_budget - price_tolerance:
                # Under budget - upgrade components if not maximum budget type
                # Don't upgrade if it's a "maximum" budget since we want to stay under
                recommended_components = self._upgrade_components(db, recommended_components, target_budget - total_price, use_case)
        
        # Recalculate total after adjustments
        total_price = 0
        for component in recommended_components.values():
            if isinstance(component, list):  # Handle RAM which is a list
                total_price += sum(ram.price for ram in component)
            else:
                total_price += component.price
        
        # Format results
        recommendations = {
            "user_requirements": {
                "use_case": use_case,
                "target_tier": tier,
                "budget": target_budget,
                "budget_type": budget_type if isinstance(budget_info, dict) else "exact"
            },
            "builds": {
                "recommended": {
                    "components": self._format_component_list(recommended_components),
                    "total_price": round(total_price, 2),
                    "compatibility": self.compatibility_checker.check_system_compatibility(recommended_components)["compatible"]
                }
            }
        }
        
        return recommendations

    def _downgrade_components(self, db, components, amount_to_reduce, use_case):
        """Downgrade components to reduce total price by specified amount"""
        if not components:
            return components
        
        # Make a copy to avoid modifying the original
        components = components.copy()
        
        # Priority order for downgrades (most expensive/flexible first)
        downgrade_priority = ["gpu", "cpu", "motherboard", "ram", "power_supply"]
        
        # Keep track of current price
        current_price = 0
        for component in components.values():
            if isinstance(component, list):  # Handle RAM which is a list
                current_price += sum(ram.price for ram in component)
            else:
                current_price += component.price
        
        target_price = current_price - amount_to_reduce
        
        # Try to downgrade components in priority order
        for component_type in downgrade_priority:
            if component_type not in components:
                continue
                
            current_component = components[component_type]
            
            # Handle RAM separately since it's a list
            if component_type == "ram" and isinstance(current_component, list):
                # Get all RAM options and find cheaper alternatives
                all_rams = db.query(RAM).all()
                
                # Calculate current RAM price
                current_ram_price = sum(ram.price for ram in current_component)
                current_capacity = sum(ram.capacity for ram in current_component)
                
                # Find cheaper RAM combinations with similar capacity
                cheaper_ram_options = []
                for ram in all_rams:
                    # Calculate how many sticks we would need
                    needed_sticks = max(1, current_capacity // ram.capacity)
                    if needed_sticks <= 4:  # Most motherboards support up to 4 sticks
                        total_price = ram.price * needed_sticks
                        if total_price < current_ram_price:
                            cheaper_ram_options.append(([ram] * needed_sticks, total_price))
                
                # Sort by price (highest first so we reduce least)
                cheaper_ram_options.sort(key=lambda x: x[1], reverse=True)
                
                # Replace with cheaper option if found
                if cheaper_ram_options:
                    for ram_option, price in cheaper_ram_options:
                        # Calculate new total price if we use this RAM
                        price_diff = current_ram_price - price
                        new_total = current_price - price_diff
                        
                        # Use this RAM if it gets us closer to target without going under
                        if new_total >= target_price:
                            components[component_type] = ram_option
                            current_price = new_total
                            break
                            
                # If we've reached target price, stop downgrading
                if current_price <= target_price + (target_price * 0.05):  # Allow 5% tolerance
                    break
                    
            else:
                # For other component types
                component_model = current_component.__class__
                all_components = db.query(component_model).all()
                
                # Get current component price
                current_component_price = current_component.price
                
                # Find cheaper alternatives
                cheaper_alternatives = [c for c in all_components if c.price < current_component_price]
                
                # For CPU and motherboard, ensure socket compatibility
                if component_type == "motherboard" and "cpu" in components:
                    cheaper_alternatives = [mb for mb in cheaper_alternatives 
                                          if mb.socket == components["cpu"].socket]
                
                # Sort by price (highest first so we reduce least)
                cheaper_alternatives.sort(key=lambda x: x.price, reverse=True)
                
                # Replace with cheaper alternative if found
                if cheaper_alternatives:
                    for alternative in cheaper_alternatives:
                        # Calculate new total price with this alternative
                        price_diff = current_component_price - alternative.price
                        new_total = current_price - price_diff
                        
                        # Use this alternative if it gets us closer to target without going under
                        if new_total >= target_price:
                            components[component_type] = alternative
                            current_price = new_total
                            break
                
                # If we've reached target price, stop downgrading
                if current_price <= target_price + (target_price * 0.05):  # Allow 5% tolerance
                    break
        
        return components
        
    def _upgrade_components(self, db, components, amount_to_add, use_case):
        """Upgrade components to increase total price by specified amount"""
        if not components:
            return components
        
        # Make a copy to avoid modifying the original
        components = components.copy()
        
        # Priority order for upgrades based on use case
        if use_case == "gaming":
            # For gaming, prioritize GPU then CPU
            upgrade_priority = ["gpu", "cpu", "ram", "motherboard", "power_supply"]
        elif use_case == "productivity":
            # For productivity, prioritize CPU then RAM
            upgrade_priority = ["cpu", "ram", "gpu", "motherboard", "power_supply"]
        else:  # content_creation
            # For content creation, balance CPU and GPU
            upgrade_priority = ["gpu", "cpu", "ram", "motherboard", "power_supply"]
        
        # Keep track of current price
        current_price = 0
        for component in components.values():
            if isinstance(component, list):  # Handle RAM which is a list
                current_price += sum(ram.price for ram in component)
            else:
                current_price += component.price
        
        target_price = current_price + amount_to_add
        
        # Try to upgrade components in priority order
        for component_type in upgrade_priority:
            if component_type not in components:
                continue
                
            current_component = components[component_type]
            
            # Handle RAM separately since it's a list
            if component_type == "ram" and isinstance(current_component, list):
                # Get all RAM options and find better alternatives
                all_rams = db.query(RAM).all()
                
                # Calculate current RAM price and capacity
                current_ram_price = sum(ram.price for ram in current_component)
                current_capacity = sum(ram.capacity for ram in current_component)
                
                # Find better RAM combinations (higher capacity or faster)
                better_ram_options = []
                for ram in all_rams:
                    # Look for higher capacity or same capacity with higher speed
                    if ram.capacity > current_component[0].capacity or (
                        ram.capacity == current_component[0].capacity and ram.speed > current_component[0].speed
                    ):
                        # Calculate how many sticks we would need
                        needed_sticks = max(1, min(4, 32 // ram.capacity))  # Aim for 32GB or current
                        total_price = ram.price * needed_sticks
                        if total_price > current_ram_price:
                            better_ram_options.append(([ram] * needed_sticks, total_price))
                
                # Sort by price (lowest first)
                better_ram_options.sort(key=lambda x: x[1])
                
                # Replace with better option if found
                if better_ram_options:
                    for ram_option, price in better_ram_options:
                        # Calculate new total price if we use this RAM
                        price_diff = price - current_ram_price
                        new_total = current_price + price_diff
                        
                        # Use this RAM if it keeps us within budget
                        if new_total <= target_price:
                            components[component_type] = ram_option
                            current_price = new_total
                            break
                            
                # If we've reached target price, stop upgrading
                if current_price >= target_price - (target_price * 0.05):  # Allow 5% tolerance
                    break
                    
            else:
                # For other component types
                component_model = current_component.__class__
                all_components = db.query(component_model).all()
                
                # Get current component price
                current_component_price = current_component.price
                
                # Find better alternatives
                better_alternatives = [c for c in all_components if c.price > current_component_price]
                
                # For motherboard, ensure socket compatibility
                if component_type == "motherboard" and "cpu" in components:
                    better_alternatives = [mb for mb in better_alternatives 
                                         if mb.socket == components["cpu"].socket]
                
                # Sort by price (lowest first)
                better_alternatives.sort(key=lambda x: x.price)
                
                # Replace with better alternative if found
                if better_alternatives:
                    for alternative in better_alternatives:
                        # Calculate new total price with this alternative
                        price_diff = alternative.price - current_component_price
                        new_total = current_price + price_diff
                        
                        # Use this alternative if it keeps us within budget
                        if new_total <= target_price:
                            components[component_type] = alternative
                            current_price = new_total
                            break
                
                # If we've reached target price, stop upgrading
                if current_price >= target_price - (target_price * 0.05):  # Allow 5% tolerance
                    break
        
        return components
    
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