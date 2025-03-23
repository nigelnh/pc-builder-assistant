from typing import Dict, List, Tuple, Optional, Union
from sqlalchemy.orm import Session

from app.models.components import CPU, GPU, Motherboard, RAM, PowerSupply

class CompatibilityChecker:
    def __init__(self):
        # Power requirements by GPU model (approximate TDP in watts)
        self.gpu_power_requirements = {
            # NVIDIA RTX 30 series
            "rtx 3050": 130,
            "rtx 3060": 170, 
            "rtx 3060 ti": 200,
            "rtx 3070": 220,
            "rtx 3070 ti": 290,
            "rtx 3080": 320,
            "rtx 3080 ti": 350,
            "rtx 3090": 350,
            "rtx 3090 ti": 450,
            
            # NVIDIA RTX 40 series
            "rtx 4060": 115,
            "rtx 4060 ti": 160,
            "rtx 4070": 200,
            "rtx 4070 ti": 285,
            "rtx 4080": 320,
            "rtx 4090": 450,
            
            # AMD RX 6000 series
            "rx 6600": 132,
            "rx 6600 xt": 160,
            "rx 6700 xt": 230,
            "rx 6800": 250,
            "rx 6800 xt": 300,
            "rx 6900 xt": 300,
            
            # AMD RX 7000 series
            "rx 7600": 165,
            "rx 7700 xt": 245,
            "rx 7800 xt": 263,
            "rx 7900 xt": 315,
            "rx 7900 xtx": 355
        }
        
        # Socket compatibility mappings
        self.socket_compatibility = {
            # Intel
            "lga1700": ["12th Gen Intel", "13th Gen Intel"],
            "lga1200": ["10th Gen Intel", "11th Gen Intel"],
            "lga1151": ["8th Gen Intel", "9th Gen Intel"],
            
            # AMD
            "am4": ["Ryzen 3000", "Ryzen 5000"],
            "am5": ["Ryzen 7000"]
        }
        
        # Minimum recommended PSU wattage with headroom
        self.psu_headroom = 1.5  # 50% headroom for future upgrades and efficiency
    
    def check_cpu_motherboard_compatibility(self, cpu: CPU, motherboard: Motherboard) -> Dict:
        """Check if CPU and motherboard are compatible based on socket"""
        is_compatible = cpu.socket == motherboard.socket
        
        return {
            "compatible": is_compatible,
            "reason": "Socket types match" if is_compatible else f"Socket mismatch: CPU requires {cpu.socket}, motherboard has {motherboard.socket}"
        }
    
    def check_power_requirements(self, components: Dict[str, Union[CPU, GPU, List[RAM], PowerSupply]]) -> Dict:
        """Check if power supply is adequate for components"""
        cpu = components.get("cpu")
        gpu = components.get("gpu")
        psu = components.get("power_supply")
        
        if not all([cpu, gpu, psu]):
            return {
                "compatible": False,
                "reason": "Missing components for power check"
            }
        
        # Calculate estimated power requirements
        base_power = 75  # Base system power (motherboard, drives, fans)
        cpu_power = cpu.tdp if hasattr(cpu, "tdp") else 65  # Default to 65W if not specified
        gpu_power = gpu.tdp if hasattr(gpu, "tdp") else 0
        
        # Get GPU power from lookup table if available and not in component data
        if gpu_power == 0:
            gpu_model_lower = gpu.model.lower() if hasattr(gpu, "model") else ""
            for model, power in self.gpu_power_requirements.items():
                if model in gpu_model_lower:
                    gpu_power = power
                    break
        
        total_power = base_power + cpu_power + gpu_power
        recommended_power = total_power * self.psu_headroom
        
        is_compatible = psu.wattage >= recommended_power
        
        return {
            "compatible": is_compatible,
            "calculated_power": total_power,
            "recommended_power": recommended_power,
            "available_power": psu.wattage,
            "reason": f"Power supply is adequate" if is_compatible else 
                      f"Insufficient power: System needs ~{int(recommended_power)}W, power supply provides {psu.wattage}W"
        }
    
    def check_ram_compatibility(self, motherboard: Motherboard, ram: List[RAM]) -> Dict:
        """Check RAM compatibility with motherboard"""
        if not ram:
            return {
                "compatible": False,
                "reason": "No RAM specified"
            }
        
        # Check number of modules vs slots
        total_modules = sum(r.modules for r in ram if hasattr(r, "modules"))
        is_slot_compatible = total_modules <= motherboard.memory_slots
        
        # Check total capacity vs max supported
        total_capacity = sum(r.capacity for r in ram if hasattr(r, "capacity"))
        is_capacity_compatible = total_capacity <= motherboard.max_memory
        
        # Check RAM type (simplistic - would need more sophisticated logic in real app)
        ram_types = set(r.type for r in ram if hasattr(r, "type"))
        is_type_compatible = len(ram_types) == 1  # All RAM should be same type
        
        is_compatible = is_slot_compatible and is_capacity_compatible and is_type_compatible
        
        reasons = []
        if not is_slot_compatible:
            reasons.append(f"Too many RAM modules ({total_modules}) for available slots ({motherboard.memory_slots})")
        if not is_capacity_compatible:
            reasons.append(f"Total RAM capacity ({total_capacity}GB) exceeds motherboard maximum ({motherboard.max_memory}GB)")
        if not is_type_compatible:
            reasons.append(f"Mixed RAM types detected ({', '.join(ram_types)})")
        
        return {
            "compatible": is_compatible,
            "reasons": reasons if reasons else ["RAM is compatible with motherboard"]
        }
    
    def get_compatible_components(self, db: Session, component_type: str, component_id: int) -> List[Dict]:
        """Get all compatible components of a certain type for a given component"""
        if component_type == "cpu" and component_id:
            cpu = db.query(CPU).filter(CPU.id == component_id).first()
            if cpu:
                compatible_motherboards = cpu.compatible_motherboards
                return [
                    {
                        "id": mb.id,
                        "name": mb.name,
                        "brand": mb.brand,
                        "model": mb.model,
                        "socket": mb.socket,
                        "form_factor": mb.form_factor,
                        "memory_slots": mb.memory_slots,
                        "max_memory": mb.max_memory,
                        "price": mb.price
                    } for mb in compatible_motherboards
                ]
        
        elif component_type == "motherboard" and component_id:
            mb = db.query(Motherboard).filter(Motherboard.id == component_id).first()
            if mb:
                compatible_cpus = mb.compatible_cpus
                return [
                    {
                        "id": cpu.id,
                        "name": cpu.name,
                        "brand": cpu.brand,
                        "model": cpu.model,
                        "socket": cpu.socket,
                        "cores": cpu.cores,
                        "threads": cpu.threads,
                        "base_clock": cpu.base_clock,
                        "boost_clock": cpu.boost_clock,
                        "tdp": cpu.tdp,
                        "price": cpu.price
                    } for cpu in compatible_cpus
                ]
        
        return []
    
    def check_system_compatibility(self, components: Dict[str, Union[CPU, GPU, Motherboard, List[RAM], PowerSupply]]) -> Dict:
        """Check overall system compatibility"""
        results = {
            "compatible": True,
            "compatibility_checks": {}
        }
        
        # Check CPU-Motherboard compatibility
        if "cpu" in components and "motherboard" in components:
            cpu_mb_check = self.check_cpu_motherboard_compatibility(components["cpu"], components["motherboard"])
            results["compatibility_checks"]["cpu_motherboard"] = cpu_mb_check
            if not cpu_mb_check["compatible"]:
                results["compatible"] = False
        
        # Check power requirements
        power_check = self.check_power_requirements(components)
        results["compatibility_checks"]["power"] = power_check
        if not power_check["compatible"]:
            results["compatible"] = False
        
        # Check RAM compatibility
        if "motherboard" in components and "ram" in components:
            ram_check = self.check_ram_compatibility(components["motherboard"], components["ram"])
            results["compatibility_checks"]["ram"] = ram_check
            if not ram_check["compatible"]:
                results["compatible"] = False
        
        return results