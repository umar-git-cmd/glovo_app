from fastapi import FastAPI
from mysite.api import user, store_menu, store, review, product, order, courier_product, contact, category, address
import uvicorn
glovo_app = FastAPI()

glovo_app.include_router(user.user_router)
glovo_app.include_router(store_menu.store_menu_router)
glovo_app.include_router(store.store_router)
glovo_app.include_router(review.review_router)
glovo_app.include_router(product.product_router)
glovo_app.include_router(order.order_router)
glovo_app.include_router(courier_product.courierProduct_router)
glovo_app.include_router(contact.contact_router)
glovo_app.include_router(category.category_router)
glovo_app.include_router(address.address_router)




if __name__ == '__main__':
    uvicorn.run(glovo_app, host='127.0.0.1', port=8000)


