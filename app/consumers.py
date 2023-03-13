import json
from fastapi import HTTPException


def create_delivery(state, event):
    """
    Create a new delivery and initialize its state with the specified budget and notes.

    Parameters:
        - state (dict): The current state of the delivery.
        - event (Event): The event that triggered the creation of the delivery.

    Returns:
        - A dictionary containing the initial state of the new delivery.

    """
    data = json.loads(event.data)
    return {
        "id": event.delivery_id,
        "budget": int(data["budget"]),
        "notes": data["notes"],
        "status": "ready"
    }


def start_delivery(state, event):
    """
    Start a delivery and update its state to 'active'.

    Parameters:
        - state (dict): The current state of the delivery.
        - event (Event): The event that triggered the start of the delivery.

    Returns:
        - A dictionary containing the updated state of the delivery.

    Raises:
        - HTTPException: If the delivery is already started.

    """
    if state['status'] != 'ready':
        raise HTTPException(status_code=400, detail="Delivery already started")

    return state | {
        "status": "active"
    }


def pickup_products(state, event):
    """
    Update the state of a delivery to indicate that products have been picked up.

    Parameters:
        - state (dict): The current state of the delivery.
        - event (Event): The event that triggered the update.

    Returns:
        - A dictionary containing the updated state of the delivery.

    Raises:
        - HTTPException: If the delivery is already completed or there is not enough budget to complete the pickup.

    """
    data = json.loads(event.data)
    new_budget = state["budget"] - int(data['purchase_price']) * int(data['quantity'])

    if state["status"] == 'completed':
        raise HTTPException(status_code=400, detail="Delivery already competed")

    if new_budget < 0:
        raise HTTPException(status_code=400, detail="Not enough budget")

    return state | {
        "budget": new_budget,
        "purchase_price": int(data['purchase_price']),
        "quantity": int(data['quantity']),
        "status": "collected"
    }


def deliver_products(state, event):
    """
    Update the state of a delivery to indicate that products have been delivered.

    Parameters:
        - state (dict): The current state of the delivery.
        - event (Event): The event that triggered the update.

    Returns:
        - A dictionary containing the updated state of the delivery.

    Raises:
        - HTTPException: If the delivery is already completed or there is not enough quantity to complete the delivery.

    """
    data = json.loads(event.data)
    new_quantity = state["quantity"] - int(data['quantity'])

    if state["status"] == 'completed':
        raise HTTPException(status_code=400, detail="Not enough quantity")

    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Not enough quantity")

    new_budget = state["budget"] + int(data['sell_price']) * int(data['quantity'])

    return state | {
        "budget": new_budget,
        "sell_price": int(data['sell_price']),
        "quantity": new_quantity,
        "status": "completed"
    }


def increase_budget(state, event):
    """
    Increase the budget of a delivery.

    Parameters:
        - state (dict): The current state of the delivery.
        - event (Event): The event that triggered the budget increase.

    Returns:
        - A dictionary containing the updated state of the delivery.

    Raises:
        - HTTPException: If the delivery is not active.

    """
    if state["status"] != "active":
        raise HTTPException(status_code=400, detail="delivery has either not started or has already been completed")
    data = json.loads(event.data)
    state['budget'] += int(data['budget'])
    return state


CONSUMERS = {
    "CREATE_DELIVERY": create_delivery,
    "START_DELIVERY": start_delivery,
    "PICKUP_PRODUCTS": pickup_products,
    "DELIVER_PRODUCTS": deliver_products,
    "INCREASE_BUDGET": increase_budget,
}
