from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime
import enum

from ..database import Base

class OrderStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class PaymentStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"

class PrintStyle(str, enum.Enum):
    engraving = "engraving"
    cutting = "cutting"
    marking = "marking"
    relief = "relief"

class Material(str, enum.Enum):
    pine = "pine"
    oak = "oak"
    cedar = "cedar"
    mahogany = "mahogany"
    walnut = "walnut"

class PrintOrder(Base):
    __tablename__ = "print_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Order details
    description = Column(Text, nullable=False)
    material = Column(Enum(Material), nullable=False)
    width = Column(Float, nullable=False)  # in cm
    height = Column(Float, nullable=False)  # in cm
    depth = Column(Float, nullable=True)   # in cm
    
    # Print specifications
    print_style = Column(Enum(PrintStyle), nullable=False)
    dimensions = Column(JSON, nullable=False)  # {width, height, depth}
    quantity = Column(Integer, default=1)
    color_preferences = Column(JSON, nullable=True)  # preferencias de color
    
    # File information
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    
    # Pricing
    base_price = Column(Float, nullable=False)
    material_cost = Column(Float, nullable=False)
    shipping_cost = Column(Float, default=0.0)
    total_price = Column(Float, nullable=False)
    
    # Status and tracking
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    tracking_updates = Column(JSON, default=list)  # historial de seguimiento
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estimated_completion = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="print_orders")
    progress = relationship("OrderProgress", back_populates="order", cascade="all, delete-orphan")

class OrderProgress(Base):
    __tablename__ = "order_progress"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("print_orders.id"), nullable=False)
    
    # Progress details
    status = Column(Enum(OrderStatus), nullable=False)
    description = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Additional info
    notes = Column(Text, nullable=True)
    completed_by = Column(String, nullable=True)  # user or system
    
    # Relationships
    order = relationship("PrintOrder", back_populates="progress")
