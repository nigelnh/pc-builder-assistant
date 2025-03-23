# PC Builder Component Database

This database contains information about PC components for the PC Builder Assistant project.

## Database Schema

### CPU

- id: Primary key
- name: Full component name
- brand: Manufacturer (Intel, AMD)
- model: Model number/name
- socket: CPU socket type (LGA1700, AM4)
- cores: Number of cores
- threads: Number of threads
- base_clock: Base clock speed in GHz
- boost_clock: Boost clock speed in GHz
- tdp: Thermal Design Power in Watts
- price: Price in USD

### GPU

- id: Primary key
- name: Full component name
- brand: Manufacturer (NVIDIA, AMD)
- model: Model number/name
- vram: Video memory in GB
- memory_type: Memory type (GDDR6, etc.)
- tdp: Thermal Design Power in Watts
- length: Card length in mm
- price: Price in USD

### Motherboard

- id: Primary key
- name: Full component name
- brand: Manufacturer
- model: Model number/name
- socket: CPU socket type (LGA1700, AM4)
- form_factor: Form factor (ATX, mATX, etc.)
- memory_slots: Number of memory slots
- max_memory: Maximum memory capacity in GB
- price: Price in USD

### RAM

- id: Primary key
- name: Full component name
- brand: Manufacturer
- model: Model number/name
- capacity: Memory capacity in GB
- type: Memory type (DDR4, DDR5)
- speed: Memory speed in MHz
- modules: Number of modules/sticks
- price: Price in USD

### Power Supply

- id: Primary key
- name: Full component name
- brand: Manufacturer
- model: Model number/name
- wattage: Power output in Watts
- efficiency: Efficiency rating (80+ Bronze, Gold, etc.)
- modular: Whether the PSU is modular
- price: Price in USD

## Compatibility Relationships

- CPU to Motherboard: Many-to-many relationship based on socket type
