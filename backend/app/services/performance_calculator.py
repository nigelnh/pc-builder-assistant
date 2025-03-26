"""
Performance Calculator for PC components
This module provides functions to calculate performance scores for different components
and workloads based on more realistic benchmarks and real-world data.
"""

from typing import Dict, Any, Optional, List, Union
import re

# CPU performance scores by model family (normalized to 1-100 scale)
CPU_PERFORMANCE = {
    # Gaming-oriented scores
    "gaming": {
        # Intel
        "i3": 50,
        "i3-12": 60,
        "i3-13": 65,
        "i3-14": 68,
        "i5": 65,
        "i5-12": 75,
        "i5-13": 80,
        "i5-14": 83,
        "i7": 80,
        "i7-12": 85,
        "i7-13": 88,
        "i7-14": 90,
        "i9": 90,
        "i9-12": 92,
        "i9-13": 95,
        "i9-14": 98,
        # AMD
        "ryzen 3": 50,
        "ryzen 5": 70,
        "ryzen 5 5": 75,
        "ryzen 5 7": 83,
        "ryzen 7": 85,
        "ryzen 7 5": 87,
        "ryzen 7 7": 90,
        "ryzen 9": 92,
        "ryzen 9 5": 94,
        "ryzen 9 7": 97,
        "threadripper": 95,
    },
    # Productivity-oriented scores
    "productivity": {
        # Intel
        "i3": 45,
        "i3-12": 55,
        "i3-13": 60,
        "i3-14": 62,
        "i5": 60,
        "i5-12": 70,
        "i5-13": 75,
        "i5-14": 78,
        "i7": 80,
        "i7-12": 85,
        "i7-13": 90,
        "i7-14": 92,
        "i9": 92,
        "i9-12": 94,
        "i9-13": 97,
        "i9-14": 99,
        # AMD
        "ryzen 3": 45,
        "ryzen 5": 65,
        "ryzen 5 5": 70,
        "ryzen 5 7": 78,
        "ryzen 7": 85,
        "ryzen 7 5": 90,
        "ryzen 7 7": 93,
        "ryzen 9": 95,
        "ryzen 9 5": 97,
        "ryzen 9 7": 99,
        "threadripper": 100,
    },
}

# GPU performance scores by model (normalized to 1-100 scale)
GPU_PERFORMANCE = {
    # Gaming-oriented scores
    "gaming": {
        # NVIDIA
        "gtx 1650": 40,
        "gtx 1660": 50,
        "rtx 2060": 60,
        "rtx 2070": 65,
        "rtx 2080": 70,
        "rtx 3050": 55,
        "rtx 3060": 65,
        "rtx 3070": 80,
        "rtx 3080": 90,
        "rtx 3090": 95,
        "rtx 4060": 70,
        "rtx 4070": 85,
        "rtx 4080": 95,
        "rtx 4090": 100,
        # AMD
        "rx 6500": 45,
        "rx 6600": 60,
        "rx 6700": 75,
        "rx 6800": 85,
        "rx 6900": 90,
        "rx 7600": 65,
        "rx 7700": 80,
        "rx 7800": 85,
        "rx 7900": 95,
    },
    # Content creation / productivity scores
    "productivity": {
        # NVIDIA
        "gtx 1650": 35,
        "gtx 1660": 45,
        "rtx 2060": 60,
        "rtx 2070": 70,
        "rtx 2080": 75,
        "rtx 3050": 50,
        "rtx 3060": 65,
        "rtx 3070": 80,
        "rtx 3080": 90,
        "rtx 3090": 98,
        "rtx 4060": 70,
        "rtx 4070": 85,
        "rtx 4080": 95,
        "rtx 4090": 100,
        # AMD
        "rx 6500": 40,
        "rx 6600": 55,
        "rx 6700": 70,
        "rx 6800": 80,
        "rx 6900": 88,
        "rx 7600": 60,
        "rx 7700": 75,
        "rx 7800": 82,
        "rx 7900": 92,
    },
}

# Game-specific performance scores for popular GPUs (1-100 scale)
GAME_PERFORMANCE = {
    "RTX 4090": {
        "cyberpunk": 100,
        "fortnite": 100,
        "valorant": 100,
        "minecraft": 100,
        "warzone": 100,
        "call of duty": 100,
        "apex legends": 100,
        "gta": 100,
        "red dead redemption": 100,
        "dota": 100,
    },
    "RTX 4080 Super": {
        "cyberpunk": 92,
        "fortnite": 99,
        "valorant": 99,
        "minecraft": 98,
        "warzone": 95,
        "call of duty": 95,
        "apex legends": 98,
        "gta": 95,
        "red dead redemption": 93,
        "dota": 99,
    },
    "RTX 4070": {
        "cyberpunk": 85,
        "fortnite": 98,
        "valorant": 99,
        "minecraft": 96,
        "warzone": 90,
        "call of duty": 90,
        "apex legends": 95,
        "gta": 90,
        "red dead redemption": 88,
        "dota": 99,
    },
    "RTX 3080": {
        "cyberpunk": 80,
        "fortnite": 95,
        "valorant": 99,
        "minecraft": 93,
        "warzone": 86,
        "call of duty": 87,
        "apex legends": 90,
        "gta": 85,
        "red dead redemption": 83,
        "dota": 99,
    },
    "RTX 3070": {
        "cyberpunk": 72,
        "fortnite": 92,
        "valorant": 98,
        "minecraft": 92,
        "warzone": 83,
        "call of duty": 83,
        "apex legends": 88,
        "gta": 82,
        "red dead redemption": 78,
        "dota": 98,
    },
    "RTX 3060": {
        "cyberpunk": 60,
        "fortnite": 90,
        "valorant": 97,
        "minecraft": 90,
        "warzone": 75,
        "call of duty": 78,
        "apex legends": 85,
        "gta": 75,
        "red dead redemption": 70,
        "dota": 95,
    },
    "RX 7900 XTX": {
        "cyberpunk": 90,
        "fortnite": 97,
        "valorant": 99,
        "minecraft": 95,
        "warzone": 93,
        "call of duty": 92,
        "apex legends": 95,
        "gta": 90,
        "red dead redemption": 90,
        "dota": 98,
    },
    "RX 7800 XT": {
        "cyberpunk": 77,
        "fortnite": 94,
        "valorant": 98,
        "minecraft": 92,
        "warzone": 87,
        "call of duty": 88,
        "apex legends": 92,
        "gta": 84,
        "red dead redemption": 80,
        "dota": 98,
    },
    "RX 6800 XT": {
        "cyberpunk": 75,
        "fortnite": 93,
        "valorant": 98,
        "minecraft": 91,
        "warzone": 85,
        "call of duty": 85,
        "apex legends": 90,
        "gta": 82,
        "red dead redemption": 78,
        "dota": 97,
    },
    "RX 6700 XT": {
        "cyberpunk": 65,
        "fortnite": 90,
        "valorant": 95,
        "minecraft": 88,
        "warzone": 80,
        "call of duty": 80,
        "apex legends": 87,
        "gta": 77,
        "red dead redemption": 73,
        "dota": 95,
    },
    "RX 6600 XT": {
        "cyberpunk": 55,
        "fortnite": 87,
        "valorant": 93,
        "minecraft": 85,
        "warzone": 72,
        "call of duty": 73,
        "apex legends": 82,
        "gta": 70,
        "red dead redemption": 65,
        "dota": 92,
    },
}

# RAM performance impact based on capacity and speed
RAM_PERFORMANCE = {
    "8GB": 60,
    "16GB": 80,
    "32GB": 95,
    "64GB": 100,
    "DDR4": {
        "2666": 70,
        "3000": 75,
        "3200": 80,
        "3600": 85,
        "4000": 90,
    },
    "DDR5": {
        "4800": 85,
        "5200": 90,
        "5600": 92,
        "6000": 95,
        "6400": 97,
        "7200": 100,
    },
}

def match_cpu_model(cpu_name: str) -> str:
    """
    Match a CPU name to the closest model in our performance database
    """
    cpu_name = cpu_name.lower()
    
    # Check for Intel CPUs
    if "intel" in cpu_name or "core" in cpu_name or "i3" in cpu_name or "i5" in cpu_name or "i7" in cpu_name or "i9" in cpu_name:
        # Check generation
        for gen in ["14", "13", "12", "11", "10"]:
            if f"i9-{gen}" in cpu_name:
                return f"i9-{gen}"
            if f"i7-{gen}" in cpu_name:
                return f"i7-{gen}"
            if f"i5-{gen}" in cpu_name:
                return f"i5-{gen}"
            if f"i3-{gen}" in cpu_name:
                return f"i3-{gen}"
        
        # Fallback to general model
        if "i9" in cpu_name:
            return "i9"
        if "i7" in cpu_name:
            return "i7"
        if "i5" in cpu_name:
            return "i5"
        if "i3" in cpu_name:
            return "i3"
    
    # Check for AMD CPUs
    if "amd" in cpu_name or "ryzen" in cpu_name:
        # Check generation
        for gen in ["7", "5", "3"]:
            if f"ryzen 9 {gen}" in cpu_name or f"r9-{gen}" in cpu_name:
                return f"ryzen 9 {gen}"
            if f"ryzen 7 {gen}" in cpu_name or f"r7-{gen}" in cpu_name:
                return f"ryzen 7 {gen}"
            if f"ryzen 5 {gen}" in cpu_name or f"r5-{gen}" in cpu_name:
                return f"ryzen 5 {gen}"
            if f"ryzen 3 {gen}" in cpu_name or f"r3-{gen}" in cpu_name:
                return f"ryzen 3 {gen}"
        
        # Fallback to general model
        if "ryzen 9" in cpu_name or "r9" in cpu_name:
            return "ryzen 9"
        if "ryzen 7" in cpu_name or "r7" in cpu_name:
            return "ryzen 7"
        if "ryzen 5" in cpu_name or "r5" in cpu_name:
            return "ryzen 5"
        if "ryzen 3" in cpu_name or "r3" in cpu_name:
            return "ryzen 3"
        if "threadripper" in cpu_name:
            return "threadripper"
    
    # Default fallback
    return "i5"

def match_gpu_model(gpu_name: str) -> str:
    """
    Match a GPU name to the closest model in our performance database
    """
    gpu_name = gpu_name.lower()
    
    # NVIDIA GPUs
    if "nvidia" in gpu_name or "geforce" in gpu_name or "rtx" in gpu_name or "gtx" in gpu_name:
        # Check for RTX 40 series
        for model in ["4090", "4080", "4070", "4060"]:
            if f"rtx {model}" in gpu_name or f"rtx{model}" in gpu_name:
                return f"rtx {model}"
        
        # Check for RTX 30 series
        for model in ["3090", "3080", "3070", "3060", "3050"]:
            if f"rtx {model}" in gpu_name or f"rtx{model}" in gpu_name:
                return f"rtx {model}"
        
        # Check for RTX 20 series
        for model in ["2080", "2070", "2060"]:
            if f"rtx {model}" in gpu_name or f"rtx{model}" in gpu_name:
                return f"rtx {model}"
        
        # Check for GTX
        for model in ["1660", "1650"]:
            if f"gtx {model}" in gpu_name or f"gtx{model}" in gpu_name:
                return f"gtx {model}"
    
    # AMD GPUs
    if "amd" in gpu_name or "radeon" in gpu_name or "rx" in gpu_name:
        # Check for RX 7000 series
        for model in ["7900", "7800", "7700", "7600"]:
            if f"rx {model}" in gpu_name or f"rx{model}" in gpu_name:
                return f"rx {model}"
        
        # Check for RX 6000 series
        for model in ["6900", "6800", "6700", "6600", "6500"]:
            if f"rx {model}" in gpu_name or f"rx{model}" in gpu_name:
                return f"rx {model}"
    
    # Default fallback
    return "rtx 3060"

def match_gpu_for_game_performance(gpu_name: str) -> str:
    """
    Match a GPU to the best available model in our game performance database
    """
    gpu_name = gpu_name.lower()
    
    # Try to match the exact GPU model
    possible_matches = {
        "rtx 4090": "RTX 4090",
        "rtx 4080": "RTX 4080 Super",
        "rtx 3080": "RTX 3080",
        "rtx 3070": "RTX 3070",
        "rtx 3060": "RTX 3060",
        "rx 7900": "RX 7900 XTX",
        "rx 7800": "RX 7800 XT",
        "rx 6800": "RX 6800 XT",
        "rx 6700": "RX 6700 XT",
        "rx 6600": "RX 6600 XT",
    }
    
    for match_key, result in possible_matches.items():
        if match_key in gpu_name:
            return result
    
    # If no match, return a reasonable default
    if "40" in gpu_name or "7900" in gpu_name:
        return "RTX 4080 Super"
    elif "30" in gpu_name or "6800" in gpu_name:
        return "RTX 3080"
    elif "20" in gpu_name or "6700" in gpu_name:
        return "RTX 3070"
    elif "1660" in gpu_name or "6600" in gpu_name:
        return "RTX 3060"
    
    return "RTX 3060"  # Default

def calculate_ram_score(components: Dict[str, Any]) -> float:
    """
    Calculate a performance score for RAM based on capacity and speed
    """
    if "ram" not in components:
        return 70  # Default score
    
    ram = components["ram"]
    
    # Convert to list if not already
    if not isinstance(ram, list):
        ram = [ram]
    
    # Extract total capacity
    total_capacity = 0
    for ram_stick in ram:
        if "capacity" in ram_stick:
            # If capacity is directly specified
            total_capacity += ram_stick["capacity"]
        elif "name" in ram_stick:
            # Try to extract from name
            name = ram_stick["name"].lower()
            for capacity in ["8gb", "16gb", "32gb", "64gb"]:
                if capacity in name:
                    total_capacity += int(capacity.replace("gb", ""))
                    break
    
    # Get base score from capacity
    capacity_score = 0
    if total_capacity >= 64:
        capacity_score = RAM_PERFORMANCE["64GB"]
    elif total_capacity >= 32:
        capacity_score = RAM_PERFORMANCE["32GB"]
    elif total_capacity >= 16:
        capacity_score = RAM_PERFORMANCE["16GB"]
    elif total_capacity >= 8:
        capacity_score = RAM_PERFORMANCE["8GB"]
    else:
        capacity_score = 50  # Low capacity
    
    # Try to determine RAM speed
    speed_score = 0
    for ram_stick in ram:
        ram_name = ram_stick.get("name", "").lower()
        ram_specs = ram_stick.get("specs", "").lower()
        ram_info = ram_name + " " + ram_specs
        
        # Check for DDR type
        ddr_type = "DDR4"  # Default
        if "ddr5" in ram_info:
            ddr_type = "DDR5"
        
        # Extract speed
        speeds = RAM_PERFORMANCE[ddr_type]
        for speed_str in speeds.keys():
            if speed_str in ram_info:
                speed_score = max(speed_score, speeds[speed_str])
        
        # If no specific speed found, use a reasonable default
        if speed_score == 0:
            speed_score = 80 if ddr_type == "DDR5" else 75
    
    # Combine capacity and speed (weighted 60/40)
    return (capacity_score * 0.6) + (speed_score * 0.4)

def calculate_cpu_score(components: Dict[str, Any], workload: str = "gaming") -> float:
    """
    Calculate a CPU performance score based on the CPU model and workload type
    """
    if "cpu" not in components:
        return 65  # Default score
    
    cpu = components["cpu"]
    cpu_name = cpu.get("name", "")
    
    # Match to our database
    cpu_model = match_cpu_model(cpu_name)
    
    # Get score based on workload
    performance_db = CPU_PERFORMANCE.get(workload, CPU_PERFORMANCE["gaming"])
    return performance_db.get(cpu_model, 65)  # Default score if not found

def calculate_gpu_score(components: Dict[str, Any], workload: str = "gaming") -> float:
    """
    Calculate a GPU performance score based on the GPU model and workload type
    """
    if "gpu" not in components:
        return 50  # Default score
    
    gpu = components["gpu"]
    gpu_name = gpu.get("name", "")
    
    # Match to our database
    gpu_model = match_gpu_model(gpu_name)
    
    # Get score based on workload
    performance_db = GPU_PERFORMANCE.get(workload, GPU_PERFORMANCE["gaming"])
    return performance_db.get(gpu_model, 60)  # Default score if not found

def calculate_game_specific_performance(components: Dict[str, Any], games: List[str]) -> float:
    """
    Calculate game-specific performance based on mentioned games
    """
    if not games or "gpu" not in components:
        return 70  # Default score
    
    gpu = components["gpu"]
    gpu_name = gpu.get("name", "")
    
    # Match to our game performance database
    gpu_model = match_gpu_for_game_performance(gpu_name)
    
    # Get scores for mentioned games
    game_scores = []
    for game in games:
        game = game.lower()
        if gpu_model in GAME_PERFORMANCE and game in GAME_PERFORMANCE[gpu_model]:
            game_scores.append(GAME_PERFORMANCE[gpu_model][game])
        else:
            # Fallback to a reasonable default if game not found
            game_scores.append(75)
    
    # Return average score
    return sum(game_scores) / len(game_scores) if game_scores else 70

def calculate_overall_performance(components: Dict[str, Any], 
                                 use_case: str = "gaming",
                                 mentioned_games: Optional[List[str]] = None) -> Dict[str, float]:
    """
    Calculate overall performance metrics for a PC build
    
    Args:
        components: Dictionary of PC components
        use_case: Primary use case ("gaming", "productivity", "content_creation")
        mentioned_games: List of specific games mentioned by the user
    
    Returns:
        Dictionary with performance scores for different categories
    """
    # Map content_creation to productivity for our scoring system
    workload = "productivity" if use_case in ["productivity", "content_creation"] else "gaming"
    
    # Get component scores
    cpu_score = calculate_cpu_score(components, workload)
    gpu_score = calculate_gpu_score(components, workload)
    ram_score = calculate_ram_score(components)
    storage_score = calculate_storage_score(components)
    
    # Enhanced gaming performance calculation with real-world benchmark weighting
    # For modern games, GPU typically matters more than CPU, but CPU bottlenecks can limit performance
    gaming_gpu_weight = 0.65  # GPU is most important for gaming (increased from 0.60)
    gaming_cpu_weight = 0.25  # CPU still important but less so than GPU
    gaming_ram_weight = 0.07  # RAM has some impact for gaming
    gaming_storage_weight = 0.03  # Fast storage affects load times but not FPS as much
    
    # Calculate Gaming Score with bottleneck consideration
    # Apply bottleneck penalty if CPU score is significantly lower than GPU score
    gpu_gaming_score = calculate_gpu_score(components, "gaming")
    cpu_gaming_score = calculate_cpu_score(components, "gaming")
    
    # Check for CPU bottleneck
    cpu_bottleneck_penalty = 0
    if gpu_gaming_score > cpu_gaming_score + 20:  # If GPU is much better than CPU
        # Calculate bottleneck penalty based on disparity
        cpu_bottleneck_penalty = min((gpu_gaming_score - cpu_gaming_score) * 0.01 * gpu_gaming_score, 10)
    
    gaming_score = (
        (cpu_gaming_score * gaming_cpu_weight) +
        (gpu_gaming_score * gaming_gpu_weight) +
        (ram_score * gaming_ram_weight) +
        (storage_score * gaming_storage_weight)
    ) - cpu_bottleneck_penalty
    
    # Enhanced productivity performance with real-world benchmark weighting
    # For productivity, CPU typically matters more, but GPU acceleration is increasingly important
    productivity_cpu_weight = 0.55  # CPU is most important (slightly reduced from 0.60)
    productivity_gpu_weight = 0.25  # GPU more important for modern productivity apps
    productivity_ram_weight = 0.15  # RAM is more important for multitasking
    productivity_storage_weight = 0.05  # Storage speed affects application loading and file operations
    
    productivity_score = (
        (calculate_cpu_score(components, "productivity") * productivity_cpu_weight) +
        (calculate_gpu_score(components, "productivity") * productivity_gpu_weight) +
        (ram_score * productivity_ram_weight) +
        (storage_score * productivity_storage_weight)
    )
    
    # Calculate content creation performance (balanced approach with RAM emphasis)
    content_cpu_weight = 0.40
    content_gpu_weight = 0.40
    content_ram_weight = 0.15  # RAM important for content creation
    content_storage_weight = 0.05  # Storage speed for working with large files
    
    content_score = (
        (calculate_cpu_score(components, "productivity") * content_cpu_weight) +
        (calculate_gpu_score(components, "productivity") * content_gpu_weight) +
        (ram_score * content_ram_weight) +
        (storage_score * content_storage_weight)
    )
    
    # Calculate game-specific performance if games are mentioned
    game_specific_score = None
    if mentioned_games and use_case == "gaming":
        game_specific_score = calculate_game_specific_performance(components, mentioned_games)
        # Blend game-specific score with general gaming score (70/30 mix)
        gaming_score = (game_specific_score * 0.7) + (gaming_score * 0.3)
    
    # Calculate overall score based on use case with increased specificity
    if use_case == "gaming":
        overall_score = gaming_score
    elif use_case == "productivity":
        overall_score = productivity_score
    elif use_case == "content_creation":
        overall_score = content_score
    else:
        # Weighted balanced score for general use
        overall_score = (gaming_score * 0.4) + (productivity_score * 0.4) + (content_score * 0.2)
    
    # Return comprehensive performance metrics
    result = {
        "gaming": round(gaming_score),
        "productivity": round(productivity_score),
        "content_creation": round(content_score),
        "overall": round(overall_score)
    }
    
    # Add game-specific score if available
    if game_specific_score is not None:
        result["game_specific"] = round(game_specific_score)
    
    return result

# Helper function to calculate storage score
def calculate_storage_score(components: Dict[str, Any]) -> float:
    """Calculate a storage performance score based on storage type and capacity"""
    if "storage" not in components:
        return 50  # Default score
    
    storage = components["storage"]
    storage_type = storage.get("type", "").lower() if isinstance(storage, dict) else ""
    
    # Assign base scores by storage type
    if "nvme" in storage_type:
        base_score = 90
    elif "ssd" in storage_type:
        base_score = 75
    elif "hdd" in storage_type:
        base_score = 40
    else:
        base_score = 60
    
    # Adjust for capacity
    capacity = storage.get("capacity", 0) if isinstance(storage, dict) else 0
    if isinstance(capacity, str):
        # Extract numeric part if it's a string like "1TB" or "500GB"
        capacity_match = re.search(r'(\d+)', capacity)
        if capacity_match:
            capacity_value = float(capacity_match.group(1))
            # Convert to GB if in TB
            if "tb" in capacity.lower():
                capacity_value *= 1000
            capacity = capacity_value
    
    # Capacity adjustment
    if capacity >= 2000:  # 2TB or more
        capacity_bonus = 10
    elif capacity >= 1000:  # 1TB
        capacity_bonus = 5
    elif capacity >= 500:  # 500GB
        capacity_bonus = 0
    else:
        capacity_bonus = -5  # Penalty for small storage
    
    return min(base_score + capacity_bonus, 100) 