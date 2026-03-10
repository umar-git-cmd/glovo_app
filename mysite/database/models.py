from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Enum, Date, DateTime, Text
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date, datetime


class RoleChoices(str, PyEnum):
    client = 'client'
    courier = 'courier'
    owner = 'owner'
    admin = 'admin'


class StatusChoices(str, PyEnum):
    pending = 'pending'
    canceled = 'canceled'
    delivered = 'delivered'


class CourierStatusChoices(str, PyEnum):
    busy = 'busy'
    available = 'available'


class UserProfile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.client)
    registered_date: Mapped[date] = mapped_column(Date, default=date.today)

    owner_store: Mapped[List['Store']] = relationship(back_populates='owner', cascade='all, delete-orphan')
    order_client: Mapped[List['Order']] = relationship(back_populates='client', foreign_keys='Order.client_id', cascade='all, delete-orphan')
    order_courier: Mapped[List['Order']] = relationship(back_populates='courier', foreign_keys='Order.courier_id', cascade='all, delete-orphan')
    user_courier_product: Mapped[List['CourierProduct']] = relationship(back_populates='user', cascade='all, delete-orphan')
    client_review: Mapped[List['Review']] = relationship(back_populates='client_review', cascade='all, delete-orphan')


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(40), unique=True)

    category_store: Mapped[List['Store']] = relationship(back_populates='category', cascade='all, delete-orphan')


class Store(Base):
    __tablename__ = 'store'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    store_image: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    category: Mapped[Category] = relationship(back_populates='category_store')
    owner: Mapped[UserProfile] = relationship(back_populates='owner_store')
    store_contact: Mapped[List['Contact']] = relationship(back_populates='store', cascade='all, delete-orphan')
    store_address: Mapped[List['Address']] = relationship(back_populates='address_store', cascade='all, delete-orphan')
    menu_store: Mapped[List['StoreMenu']] = relationship(back_populates='store_menu', cascade='all, delete-orphan')
    product_store: Mapped[List['Product']] = relationship(back_populates='store', cascade='all, delete-orphan')
    store_review: Mapped[List['Review']] = relationship(back_populates='store_review')


class Contact(Base):
    __tablename__ = 'contact'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    contact_name: Mapped[str] = mapped_column(String(32))
    contact_number: Mapped[str] = mapped_column(String(32))

    store: Mapped[Store] = relationship(back_populates='store_contact')


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    address_name: Mapped[str] = mapped_column(String(32))

    address_store: Mapped[Store] = relationship(back_populates='store_address')


class StoreMenu(Base):
    __tablename__ = 'store_menu'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    menu_name: Mapped[str] = mapped_column(String(32))

    store_menu: Mapped[Store] = relationship(back_populates='menu_store')


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    product_name: Mapped[str] = mapped_column(String(50))
    product_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    product_description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    order_product: Mapped[List['Order']] = relationship(back_populates='product', cascade='all, delete-orphan')
    store: Mapped[Store] = relationship(back_populates='product_store')


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.pending)
    delivery_address: Mapped[str] = mapped_column(Text)
    courier_id: Mapped[Optional[int]] = mapped_column(ForeignKey('profile.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    courier_product_current_orders: Mapped[List['CourierProduct']] = relationship(back_populates='current_orders', cascade='all, delete-orphan')
    client: Mapped[UserProfile] = relationship(back_populates='order_client', foreign_keys=[client_id])
    product: Mapped[Product] = relationship(back_populates='order_product')
    courier: Mapped[Optional[UserProfile]] = relationship(back_populates='order_courier', foreign_keys=[courier_id])


class CourierProduct(Base):
    __tablename__ = 'courier_product'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    current_orders_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    courier_status: Mapped[CourierStatusChoices] = mapped_column(Enum(CourierStatusChoices), default=CourierStatusChoices.available)

    current_orders: Mapped[Order] = relationship(back_populates='courier_product_current_orders')
    user: Mapped[UserProfile] = relationship(back_populates='user_courier_product')
    courier_review: Mapped[List['Review']] = relationship(back_populates='courier_review')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    client_client_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    store_review_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    courier_product_id: Mapped[Optional[int]] = mapped_column(ForeignKey('courier_product.id'), nullable=True)
    rating: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    client_review: Mapped[UserProfile] = relationship(back_populates='client_review')
    courier_review: Mapped[Optional[CourierProduct]] = relationship(back_populates='courier_review')
    store_review: Mapped[Store] = relationship(back_populates='store_review')