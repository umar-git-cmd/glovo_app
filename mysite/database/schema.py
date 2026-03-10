from pydantic import BaseModel
from .models import StatusChoices, RoleChoices, CourierStatusChoices
from typing import Optional
from datetime import date, datetime

class UserProfileInputSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str
    email: str
    password: str

class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    role: RoleChoices
    registered_date: date

class CategoryInputSchema(BaseModel):
    category_name: str

class CategoryOutSchema(BaseModel):
    id: int
    category_name: str


class StoreInputSchema(BaseModel):
    store_image: Optional[str] = None
    description: str
    category_id: int
    owner_id: int

class StoreOutSchema(BaseModel):
    id: int
    category_image: Optional[str] = None
    description: str
    created_date: date
    category_id: int
    owner_id: int


class ContactInputSchema(BaseModel):
    contact_name: str
    contact_number: str
    store_id: int


class ContactOutSchema(BaseModel):
    id: int
    contact_name: str
    contact_number: str
    store_id: int

class AddressInputSchema(BaseModel):
    address_name: str
    store_id: int


class AddressOutSchema(BaseModel):
    id: int
    address_name: str
    store_id: int

class StoreMenuInputSchema(BaseModel):
    menu_name: str
    store_id: int

class StoreMenuOutSchema(BaseModel):
    id: int
    menu_name: str
    store_id: int


class ProductInputSchema(BaseModel):
    product_name: str
    product_image: Optional[str] = None
    product_description: str
    price: int
    quantity: int
    store_id: int


class ProductOutSchema(BaseModel):
    id: int
    product_name: str
    product_image: Optional[str] = None
    product_description: str
    price: int
    quantity: int
    store_id: int


class OrderInputSchema(BaseModel):
    status: StatusChoices
    delivery_address: str
    client_id: int
    product_id: int
    courier_id: int


class OrderOutSchema(BaseModel):
    id: int
    status: StatusChoices
    delivery_address: str
    created_at: datetime
    client_id: int
    product_id: int
    courier_id: int


class CourierProductInputSchema(BaseModel):
    courier_status: CourierStatusChoices
    user_id: int
    current_orders_id: int

class CourierProductOutSchema(BaseModel):
    id: int
    courier_status: CourierStatusChoices
    user_id: int
    current_orders_id: int


class ReviewInputSchema(BaseModel):
    rating: int
    text: str
    client_client_id: int
    store_review_id: int
    courier_product_id: int

class ReviewOutSchema(BaseModel):
    id: int
    rating: int
    text: str
    created_date: datetime
    client_client_id: int
    store_review_id: int
    courier_product_id: int


class UserLoginShema(BaseModel):
    username: str
    password: str