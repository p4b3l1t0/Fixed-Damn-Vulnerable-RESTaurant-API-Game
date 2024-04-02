import base64

import requests
from apis.menu import schemas
from db.models import MenuItem
from fastapi import HTTPException


ALLOWED_DOMAINS = {"example.com", "images.example.com"}

def is_url_allowed(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme in ["http", "https"] and parsed_url.netloc in ALLOWED_DOMAINS:
            return True
        else:
            return False
    except Exception:
        return False

def _image_url_to_base64(image_url: str):
    if not is_url_allowed(image_url):
        raise HTTPException(status_code=400, detail="Invalid image URL")

    try:
        response = requests.get(image_url, timeout=5)
        return base64.b64encode(response.content).decode()
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="Error retrieving image")


def create_menu_item(
    db,
    menu_item: schemas.MenuItemCreate,
):
    menu_item_dict = menu_item.dict()
    image_url = menu_item_dict.pop("image_url", None)
    db_item = MenuItem(**menu_item_dict)

    if image_url:
        db_item.image_base64 = _image_url_to_base64(image_url)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def update_menu_item(
    db,
    item_id: int,
    menu_item: schemas.MenuItemCreate,
):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Menu Item not found")

    menu_item_dict = menu_item.dict()
    image_url = menu_item_dict.pop("image_url", None)

    for key, value in menu_item_dict.items():
        setattr(db_item, key, value)

    if image_url:
        db_item.image_base64 = _image_url_to_base64(image_url)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_menu_item(db, item_id: int):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="MenuItem not found")

    db.delete(db_item)
    db.commit()
