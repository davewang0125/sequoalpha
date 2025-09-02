from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from ..models.print_order import PrintOrder, OrderProgress, OrderStatus, PaymentStatus
from ..schemas.print_order import PrintOrderCreate, PrintOrderUpdate, OrderProgressCreate
import os
import uuid
from datetime import datetime, timedelta

class PrintOrderCRUD:
    
    def create_order(self, db: Session, order_data: PrintOrderCreate, user_id: int, file_path: str) -> PrintOrder:
        """Crear una nueva orden de impresión"""
        # Calcular precio basado en dimensiones y cantidad
        total_price = self._calculate_price(order_data.dimensions, order_data.quantity, order_data.material_type)
        
        db_order = PrintOrder(
            user_id=user_id,
            file_name=order_data.file_name,
            file_path=file_path,
            file_size=order_data.file_size,
            material_type=order_data.material_type,
            dimensions=order_data.dimensions,
            quantity=order_data.quantity,
            print_style=order_data.print_style,
            color_preferences=order_data.color_preferences,
            contact_name=order_data.contact_name,
            contact_email=order_data.contact_email,
            contact_phone=order_data.contact_phone,
            shipping_address=order_data.shipping_address,
            customer_notes=order_data.customer_notes,
            total_price=total_price,
            tax_amount=total_price * 0.16,  # 16% IVA
            shipping_cost=self._calculate_shipping(order_data.dimensions, order_data.quantity),
            estimated_delivery=datetime.now() + timedelta(days=7)  # 7 días estimados
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # Crear primer progreso
        self.create_progress(db, db_order.id, OrderStatus.PENDING, "Orden creada exitosamente")
        
        return db_order
    
    def get_order(self, db: Session, order_id: int) -> Optional[PrintOrder]:
        """Obtener una orden por ID"""
        return db.query(PrintOrder).filter(PrintOrder.id == order_id).first()
    
    def get_user_orders(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[PrintOrder]:
        """Obtener todas las órdenes de un usuario"""
        return db.query(PrintOrder).filter(PrintOrder.user_id == user_id).order_by(desc(PrintOrder.created_at)).offset(skip).limit(limit).all()
    
    def get_all_orders(self, db: Session, skip: int = 0, limit: int = 100) -> List[PrintOrder]:
        """Obtener todas las órdenes (para admin)"""
        return db.query(PrintOrder).order_by(desc(PrintOrder.created_at)).offset(skip).limit(limit).all()
    
    def update_order(self, db: Session, order_id: int, order_update: PrintOrderUpdate) -> Optional[PrintOrder]:
        """Actualizar una orden"""
        db_order = self.get_order(db, order_id)
        if not db_order:
            return None
        
        update_data = order_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        
        db.commit()
        db.refresh(db_order)
        return db_order
    
    def delete_order(self, db: Session, order_id: int) -> bool:
        """Eliminar una orden"""
        db_order = self.get_order(db, order_id)
        if not db_order:
            return False
        
        # Eliminar archivo físico si existe
        if os.path.exists(db_order.file_path):
            os.remove(db_order.file_path)
        
        db.delete(db_order)
        db.commit()
        return True
    
    def create_progress(self, db: Session, order_id: int, status: OrderStatus, description: str, updated_by: Optional[int] = None) -> OrderProgress:
        """Crear una actualización de progreso"""
        progress = OrderProgress(
            order_id=order_id,
            status=status,
            description=description,
            updated_by=updated_by
        )
        
        db.add(progress)
        db.commit()
        db.refresh(progress)
        
        # Actualizar el estado de la orden
        order = self.get_order(db, order_id)
        if order:
            order.status = status
            db.commit()
        
        return progress
    
    def get_order_progress(self, db: Session, order_id: int) -> List[OrderProgress]:
        """Obtener el historial de progreso de una orden"""
        return db.query(OrderProgress).filter(OrderProgress.order_id == order_id).order_by(OrderProgress.created_at).all()
    
    def add_tracking_update(self, db: Session, order_id: int, tracking_update: dict) -> Optional[PrintOrder]:
        """Agregar una actualización de seguimiento"""
        db_order = self.get_order(db, order_id)
        if not db_order:
            return None
        
        if not db_order.tracking_updates:
            db_order.tracking_updates = []
        
        db_order.tracking_updates.append(tracking_update)
        db.commit()
        db.refresh(db_order)
        return db_order
    
    def get_orders_by_status(self, db: Session, status: OrderStatus, skip: int = 0, limit: int = 100) -> List[PrintOrder]:
        """Obtener órdenes por estado"""
        return db.query(PrintOrder).filter(PrintOrder.status == status).order_by(desc(PrintOrder.created_at)).offset(skip).limit(limit).all()
    
    def get_orders_by_payment_status(self, db: Session, payment_status: PaymentStatus, skip: int = 0, limit: int = 100) -> List[PrintOrder]:
        """Obtener órdenes por estado de pago"""
        return db.query(PrintOrder).filter(PrintOrder.payment_status == payment_status).order_by(desc(PrintOrder.created_at)).offset(skip).limit(limit).all()
    
    def _calculate_price(self, dimensions: dict, quantity: int, material_type: str) -> float:
        """Calcular precio basado en dimensiones, cantidad y tipo de material"""
        base_price_per_cm2 = {
            "pino": 0.05,
            "roble": 0.08,
            "cedro": 0.07,
            "caoba": 0.10,
            "nogal": 0.09
        }
        
        area = dimensions['width'] * dimensions['height']
        base_price = area * base_price_per_cm2.get(material_type.lower(), 0.06)
        
        # Descuento por cantidad
        if quantity >= 10:
            discount = 0.15
        elif quantity >= 5:
            discount = 0.10
        elif quantity >= 3:
            discount = 0.05
        else:
            discount = 0
        
        total_price = base_price * quantity * (1 - discount)
        return round(total_price, 2)
    
    def _calculate_shipping(self, dimensions: dict, quantity: int) -> float:
        """Calcular costo de envío"""
        volume = dimensions['width'] * dimensions['height'] * dimensions['depth']
        base_shipping = 5.0  # Envío base
        
        if volume > 1000:  # más de 1000 cm³
            base_shipping += 3.0
        if quantity > 1:
            base_shipping += (quantity - 1) * 2.0
        
        return round(base_shipping, 2)

print_order_crud = PrintOrderCRUD()
