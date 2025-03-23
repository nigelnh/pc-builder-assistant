from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Define component compatibility relationships
cpu_motherboard_compatibility = Table(
    'cpu_motherboard_compatibility', 
    Base.metadata,
    Column('cpu_id', Integer, ForeignKey('cpus.id')),
    Column('motherboard_id', Integer, ForeignKey('motherboards.id'))
)

class CPU(Base):
    __tablename__ = 'cpus'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    socket = Column(String, nullable=False)
    cores = Column(Integer)
    threads = Column(Integer)
    base_clock = Column(Float)  # GHz
    boost_clock = Column(Float)  # GHz
    tdp = Column(Integer)  # Watts
    price = Column(Float)
    
    compatible_motherboards = relationship(
        "Motherboard",
        secondary=cpu_motherboard_compatibility,
        back_populates="compatible_cpus"
    )

class GPU(Base):
    __tablename__ = 'gpus'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    vram = Column(Integer)  # GB
    memory_type = Column(String)  # GDDR6, etc.
    tdp = Column(Integer)  # Watts
    length = Column(Integer)  # mm
    price = Column(Float)

class Motherboard(Base):
    __tablename__ = 'motherboards'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    socket = Column(String, nullable=False)
    form_factor = Column(String)  # ATX, mATX, etc.
    memory_slots = Column(Integer)
    max_memory = Column(Integer)  # GB
    price = Column(Float)
    
    compatible_cpus = relationship(
        "CPU",
        secondary=cpu_motherboard_compatibility,
        back_populates="compatible_motherboards"
    )

class RAM(Base):
    __tablename__ = 'rams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    capacity = Column(Integer)  # GB
    type = Column(String)  # DDR4, DDR5, etc.
    speed = Column(Integer)  # MHz
    modules = Column(Integer)  # Number of sticks
    price = Column(Float)

class PowerSupply(Base):
    __tablename__ = 'power_supplies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    wattage = Column(Integer)  # Watts
    efficiency = Column(String)  # 80+ Bronze, Gold, etc.
    modular = Column(Boolean)  # Fully, semi, or non-modular
    price = Column(Float)