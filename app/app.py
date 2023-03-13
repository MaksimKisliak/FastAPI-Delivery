import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

from app.consumers import CONSUMERS

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get('ALLOW_ORIGINS')],
    allow_methods=['*'],
    allow_headers=['*'])

redis = get_redis_connection(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    password=os.environ.get('REDIS_PASSWORD'),
)


class Delivery(HashModel):
    budget: int = 0
    notes: str = ''

    class Meta:
        database = redis


class Event(HashModel):
    delivery_id: str = None
    type: str
    data: str

    class Meta:
        database = redis


@app.get('/deliveries/{pk}/status')
async def get_state(pk: str):
    """
    Retrieve the current state of a delivery by its primary key.

    Parameters:
        - pk (str): The primary key of the delivery.

    Returns:
        - A dictionary containing the current state of the delivery.

    """
    state = redis.get(f'delivery:{pk}')

    if state is not None:
        return json.loads(state)

    state = build_state(pk)
    redis.set(f'delivery:{pk}', json.dumps(state))
    return state


def build_state(pk: str):
    """
    Build the current state of a delivery by its primary key.

    Parameters:
        - pk (str): The primary key of the delivery.

    Returns:
        - A dictionary containing the current state of the delivery.

    """
    pks = Event.all_pks()
    all_events = [Event.get(pk) for pk in pks]
    events = [event for event in all_events if event.delivery_id == pk]
    state = {}

    for event in events:
        state = CONSUMERS[event.type](state, event)

    return state


@app.post('/deliveries/create')
async def create(request: Request):
    """
    Create a new delivery with the specified budget and notes.

    Parameters:
        - request (Request): The HTTP request containing the JSON payload with the budget and notes.

    Returns:
        - A dictionary containing the initial state of the new delivery.

    """
    body = await request.json()
    # Create a redis Hash object
    delivery = Delivery(budget=body['data']['budget'], notes=body['data']['notes']).save()
    # Create a redis Hash object
    event = Event(delivery_id=delivery.pk, type=body['type'], data=json.dumps(body['data'])).save()
    state = CONSUMERS[event.type]({}, event)
    # Create a redis string
    redis.set(f'delivery:{delivery.pk}', json.dumps(state))
    return state


@app.post('/event')
async def dispatch(request: Request):
    """
    Dispatch an event to update the state of a delivery.

    Parameters:
        - request (Request): The HTTP request containing the JSON payload with the delivery ID, type of event,
        and event data.

    Returns:
        - A dictionary containing the updated state of the delivery.

    """
    body = await request.json()
    delivery_id = body['delivery_id']
    state = await get_state(delivery_id)
    event = Event(delivery_id=delivery_id, type=body['type'], data=json.dumps(body['data'])).save()
    new_state = CONSUMERS[event.type](state, event)
    # Update the redis string with the new values
    redis.set(f'delivery:{delivery_id}', json.dumps(new_state))
    return new_state
