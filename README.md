<h2>General description of the app:</h2>
<p>This project is a delivery management system that was created as a part of an Event-Driven Architecture course using React and FastAPI. The app uses Redis as a database to store information about deliveries and events that affect those deliveries. The app consists of several endpoints that allow users to create new deliveries, update the state of existing deliveries by dispatching events, and retrieve the current state of a delivery.</p>
<p>The app uses a set of consumer functions to compute the updated state of a delivery based on the events that have been dispatched for that delivery. These consumer functions are responsible for updating the state of the delivery in Redis and returning the updated state to the client.</p>
<p>The project has been modified to include some minor changes in exception handling, docstrings, and comments to better understand the Redis database operations being performed. There were added entrance tests within the PyTest framework.</p>
<p>The app is still a work in progress and subject to further improvements.</p>
<p>Descriptions for each function:</p>
<p>In <code>app.py</code>:</p>
<ul>
 <li><p><code>get_state(pk: str)</code>: This function retrieves the current state of a delivery with the specified primary key. If the state is not already cached in Redis, it will be built by calling <code>build_state()</code> and then cached for future requests.</p></li>
 <li><p><code>build_state(pk: str)</code>: This function builds the current state of a delivery by aggregating all of the events that have been dispatched for that delivery and applying each event to the initial state. The resulting state is returned as a dictionary.</p></li>
 <li><p><code>create(request: Request)</code>: This function creates a new delivery with the specified budget and notes by parsing the JSON payload in the HTTP request. The new delivery is saved to the Redis database along with an event that describes the creation of the delivery. The initial state of the delivery is returned as a dictionary.</p></li>
 <li><p><code>dispatch(request: Request)</code>: This function dispatches an event to update the state of a delivery. The event is parsed from the JSON payload in the HTTP request, and the current state of the delivery is retrieved from Redis using <code>get_state()</code>. The event is saved to the Redis database, and the new state of the delivery is computed by applying the event to the current state using the appropriate consumer function. The new state is saved to Redis, and then returned as a dictionary.</p></li>
</ul>
<p>In <code>consumers.py</code>:</p>
<ul>
 <li><p><code>create_delivery(state, event)</code>: This function is a consumer function that is called when a new delivery is created. It creates a new delivery and initializes its state with the specified budget and notes. The initial state is returned as a dictionary.</p></li>
 <li><p><code>start_delivery(state, event)</code>: This function is a consumer function that is called when a delivery is started. It updates the state of the delivery to indicate that it is now "active". The updated state is returned as a dictionary.</p></li>
 <li><p><code>pickup_products(state, event)</code>: This function is a consumer function that is called when products are picked up as part of a delivery. It updates the state of the delivery to indicate that the products have been picked up, and reduces the budget by the appropriate amount. The updated state is returned as a dictionary.</p></li>
 <li><p><code>deliver_products(state, event)</code>: This function is a consumer function that is called when products are delivered as part of a delivery. It updates the state of the delivery to indicate that the products have been delivered, and increases the budget by the appropriate amount. The updated state is returned as a dictionary.</p></li>
 <li><p><code>increase_budget(state, event)</code>: This function is a consumer function that is called when the budget for a delivery needs to be increased. It increases the budget by the specified amount, and returns the updated state as a dictionary.</p></li>
</ul>
<p>These functions are called by <code>build_state()</code> and <code>dispatch()</code> in <code>app.py</code> to compute the updated state of a delivery based on the events that have been dispatched for that delivery. Each consumer function takes the current state of the delivery and an event that describes the update, and returns the updated state of the delivery as a dictionary. The consumer functions can also raise <code>HTTPException</code> if there is an error with the update, such as trying to pick up or deliver products when the delivery is already completed.</p>  


<div>
   <div></div>
  </div>
    <div>
     <div>
      <h2>API Documentation</h2>
<div>
 <div>
  <div></div>
 </div>
 <div>
  <div>
   <div>
    <div>
     <ol>
      <li><p><strong>Create new delivery</strong>: Creates a new delivery with the specified budget and notes. Returns the ID, budget, notes, and status of the newly created delivery.</p></li>
      <li><p><strong>Start delivery</strong>: Starts the specified delivery. Returns the ID, budget, notes, and status of the delivery after it has been started.</p></li>
      <li><p><strong>Pick up products</strong>: Records the purchase of products for the specified delivery, and updates the delivery's budget and status accordingly. Returns the ID, budget, notes, status, purchase price, and remaining quantity of the delivery after the products have been picked up.</p></li>
      <li><p><strong>Deliver products</strong>: Records the delivery of products for the specified delivery, and updates the delivery's budget, quantity, and status accordingly. Returns the ID, budget, notes, status, purchase price, sell price, and remaining quantity of the delivery after the products have been delivered.</p></li>
      <li><p><strong>Get delivery state</strong>: Retrieves the current state of the specified delivery, including its ID, budget, notes, status, purchase price, sell price, and remaining quantity.</p></li>
      <li><p><strong>Increase budget</strong>: Before pickup (if something extra needs to be delivered) increases the specified delivery budget by the specified amount and updates the delivery status accordingly. Returns identifier, budget, notes and delivery status after budget increase..</p></li>
     </ol>
    </div>
   </div>
  </div>
  <div>
   <div></div>
  </div>
 </div>
</div>
<p>Link to a raw Postman documentaion - <a>https://documenter.getpostman.com/view/25720495/2s93Jushe4</a></p>
      <h3>Create new delivery</h3>
      <p><strong>POST</strong> <code>/deliveries/create</code></p>
      <p>Create a new delivery.</p>
      <h4>Request Body</h4>
      <table>
       <thead>
        <tr>
         <th>Name</th>
         <th>Type</th>
         <th>Description</th>
        </tr>
       </thead>
       <tbody>
        <tr>
         <td>type</td>
         <td>string</td>
         <td>The type of event. Must be <code>CREATE_DELIVERY</code>.</td>
        </tr>
        <tr>
         <td>data</td>
         <td>object</td>
         <td>The data of the event.</td>
        </tr>
        <tr>
         <td>data.budget</td>
         <td>integer</td>
         <td>The budget of the delivery.</td>
        </tr>
        <tr>
         <td>data.notes</td>
         <td>string</td>
         <td>The notes of the delivery.</td>
        </tr>
       </tbody>
      </table>
      <h4>Response Body</h4>
      <table>
       <thead>
        <tr>
         <th>Name</th>
         <th>Type</th>
         <th>Description</th>
        </tr>
       </thead>
       <tbody>
        <tr>
         <td>id</td>
         <td>string</td>
         <td>The ID of the delivery.</td>
        </tr>
        <tr>
         <td>budget</td>
         <td>integer</td>
         <td>The budget of the delivery.</td>
        </tr>
        <tr>
         <td>notes</td>
         <td>string</td>
         <td>The notes of the delivery.</td>
        </tr>
        <tr>
         <td>status</td>
         <td>string</td>
         <td>The status of the delivery. Must be <code>ready</code>.</td>
        </tr>
       </tbody>
      </table>
      <h4>Example Request</h4>
      <pre>
<code>POST /deliveries/create HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "type": "CREATE_DELIVERY",
    "data": {
        "budget": 600,
        "notes": "BigMac, Coca cola and fries"
    }
}
</code>
</pre>
<h4>Example Response</h4>
<pre>
<code>HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "01GVDFM78ZXGT1ENB78F6BMDQW",
    "budget": 600,
    "notes": "BigMac, Coca cola and fries",
    "status": "ready"
}
</code>
</pre>
<h3>Start delivery</h3>
<p><strong>POST</strong> <code>/event</code></p>
<p>Start a delivery.</p>
<h4>Request Body</h4>
<table>
<thead>
<tr>
<th>Name</th>
<th>Type</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>type</td>
<td>string</td>
<td>The type of event. Must be <code>START_DELIVERY</code>.</td>
</tr>
<tr>
<td>delivery_id</td>
<td>string</td>
<td>The ID of the delivery to start.</td>
</tr>
<tr>
<td>data</td>
<td>object</td>
<td>The data of the event.</td>
</tr>
</tbody>
</table>
<h4>Response Body</h4>
<table>
<thead>
<tr>
<th>Name</th>
<th>Type</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>id</td>
<td>string</td>
<td>The ID of the delivery.</td>
</tr>
<tr>
<td>budget</td>
<td>integer</td>
<td>The budget of the delivery.</td>
</tr>
<tr>
<td>notes</td>
<td>string</td>
<td>The notes of the delivery.</td>
</tr>
<tr>
<td>status</td>
<td>string</td>
<td>The status of the delivery. Must be <code>active</code>.</td>
</tr>
</tbody>
</table>
<h4>Example Request</h4>
<pre>
<code>POST /event HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "type": "START_DELIVERY",
    "delivery_id": "01GVDFM78ZXGT1ENB78F6BMDQW",
    "data": {}
}
</code>
</pre>
<h4>Example Response</h4>
<pre>
<code>HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "01GVDFM78ZXGT1ENB78F6BMDQW",
    "budget": 600,
    "notes": "BigMac, Coca cola and fries",
    "status": "active"
}
</code>
</pre>
  <div>
   <div>
    <div>
     <div>
      <h3>Pick up products</h3>
      <p><strong>POST</strong> <code>/event</code></p>
      <p>Pick up products for a delivery.</p>
      <h4>Request Body</h4>
      <table>
       <thead>
        <tr>
         <th>Name</th>
         <th>Type</th>
         <th>Description</th>
        </tr>
       </thead>
       <tbody>
        <tr>
         <td>type</td>
         <td>string</td>
         <td>The type of event. Must be <code>PICKUP_PRODUCTS</code>.</td>
        </tr>
        <tr>
         <td>delivery_id</td>
         <td>string</td>
         <td>The ID of the delivery to pick up products for.</td>
        </tr>
        <tr>
         <td>data</td>
         <td>object</td>
         <td>The data of the event.</td>
        </tr>
        <tr>
         <td>data.purchase_price</td>
         <td>integer</td>
         <td>The purchase price of the products.</td>
        </tr>
        <tr>
         <td>data.quantity</td>
         <td>integer</td>
         <td>The quantity of the products.</td>
        </tr>
       </tbody>
      </table>
      <h4>Response Body</h4>
      <table>
       <thead>
        <tr>
         <th>Name</th>
         <th>Type</th>
         <th>Description</th>
        </tr>
       </thead>
       <tbody>
        <tr>
         <td>id</td>
         <td>string</td>
         <td>The ID of the delivery.</td>
        </tr>
        <tr>
         <td>budget</td>
         <td>integer</td>
         <td>The budget of the delivery.</td>
        </tr>
        <tr>
         <td>notes</td>
         <td>string</td>
         <td>The notes of the delivery.</td>
        </tr>
        <tr>
         <td>status</td>
         <td>string</td>
         <td>The status of the delivery. Must be <code>collected</code>.</td>
        </tr>
        <tr>
         <td>purchase_price</td>
         <td>integer</td>
         <td>The purchase price of the products.</td>
        </tr>
        <tr>
         <td>quantity</td>
         <td>integer</td>
         <td>The quantity of the products.</td>
        </tr>
       </tbody>
      </table>
      <h4>Example Request</h4>
      <pre>
<code>POST /event HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "type": "PICKUP_PRODUCTS",
    "delivery_id": "01GVDFM78ZXGT1ENB78F6BMDQW",
    "data": {
        "purchase_price": 200,
        "quantity": 3
    }
}
</code>
</pre>
<h4>Example Response</h4>
<pre>
<code>HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "01GVDFM78ZXGT1ENB78F6BMDQW",
    "budget": 0,
    "notes": "BigMac, Coca cola and fries",
    "status": "collected",
    "purchase_price": 200,
    "quantity": 3
}
</code>
</pre>
    <div>
     <div>
      <h3>Deliver products</h3>
      <p><strong>POST</strong> <code>/event</code></p>
      <p>Deliver products for a delivery.</p>
      <h4>Request Body</h4>
      <table>
       <thead>
        <tr>
         <th>Name</th>
         <th>Type</th>
         <th>Description</th>
        </tr>
       </thead>
       <tbody>
        <tr>
         <td>type</td>
         <td>string</td>
         <td>The type of event. Must be <code>DELIVER_PRODUCTS</code>.</td>
        </tr>
        <tr>
         <td>delivery_id</td>
         <td>string</td>
         <td>The ID of the delivery to deliver products for.</td>
        </tr>
        <tr>
         <td>data</td>
         <td>object</td>
         <td>The data of the event.</td>
        </tr>
        <tr>
         <td>data.sell_price</td>
         <td>integer</td>
         <td>The sell price of the products.</td>
        </tr>
        <tr>
         <td>data.quantity</td>
         <td>integer</td>
         <td>The quantity of the products.</td>
        </tr>
       </tbody>
      </table>
      <h4>Response Body</h4>
      <table>
       <thead>
        <tr>
         <th>Name</th>
         <th>Type</th>
         <th>Description</th>
        </tr>
       </thead>
       <tbody>
        <tr>
         <td>id</td>
         <td>string</td>
         <td>The ID of the delivery.</td>
        </tr>
        <tr>
         <td>budget</td>
         <td>integer</td>
         <td>The budget of the delivery.</td>
        </tr>
        <tr>
         <td>notes</td>
         <td>string</td>
         <td>The notes of the delivery.</td>
        </tr>
        <tr>
         <td>status</td>
         <td>string</td>
         <td>The status of the delivery. Must be <code>completed</code>.</td>
        </tr>
        <tr>
         <td>purchase_price</td>
         <td>integer</td>
         <td>The purchase price of the products.</td>
        </tr>
        <tr>
         <td>quantity</td>
         <td>integer</td>
         <td>The remaining quantity of the products.</td>
        </tr>
        <tr>
         <td>sell_price</td>
         <td>integer</td>
         <td>The sell price of the products.</td>
        </tr>
       </tbody>
      </table>
      <h4>Example Request</h4>
      <pre>
<code>POST /event HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "type": "DELIVER_PRODUCTS",
    "delivery_id": "01GVDFM78ZXGT1ENB78F6BMDQW",
    "data": {
        "sell_price": 250,
        "quantity": 3
    }
}
</code>
</pre>
<h4>Example Response</h4>
<pre>
<code>HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "01GVDFM78ZXGT1ENB78F6BMDQW",
    "budget": 750,
    "notes": "BigMac, Coca cola and fries",
    "status": "completed",
    "purchase_price": 200,
    "quantity": 0,
    "sell_price": 250
}
</code>
</div>
</div></pre>

<div>
 <div>
  <div>
   <div></div>
  </div>
  <div>
   <div>
    <div>
     <div>
      <h3>Get delivery state</h3>
      <p><strong>GET</strong> <code>/deliveries/{pk}/status</code></p>
      <p>Get the current state of a delivery.</p>
      <h4>Path Parameters</h4>
      <table>
       <thead>
        <tr>
         <th>Name</th>
         <th>Type</th>
         <th>Description</th>
        </tr>
       </thead>
       <tbody>
        <tr>
         <td>pk</td>
         <td>string</td>
         <td>The ID of the delivery.</td>
        </tr>
       </tbody>
      </table>
      <h4>Response Body</h4>
      <table>
       <thead>
        <tr>
         <th>Name</th>
         <th>Type</th>
         <th>Description</th>
        </tr>
       </thead>
       <tbody>
        <tr>
         <td>id</td>
         <td>string</td>
         <td>The ID of the delivery.</td>
        </tr>
        <tr>
         <td>budget</td>
         <td>integer</td>
         <td>The budget of the delivery.</td>
        </tr>
        <tr>
         <td>notes</td>
         <td>string</td>
         <td>The notes of the delivery.</td>
        </tr>
        <tr>
         <td>status</td>
         <td>string</td>
         <td>The status of the delivery.</td>
        </tr>
        <tr>
         <td>purchase_price</td>
         <td>integer</td>
         <td>The purchase price of the products.</td>
        </tr>
        <tr>
         <td>quantity</td>
         <td>integer</td>
         <td>The remaining quantity of the products.</td>
        </tr>
        <tr>
         <td>sell_price</td>
         <td>integer</td>
         <td>The sell price of the products.</td>
        </tr>
       </tbody>
      </table>
      <h4>Example Request</h4>
      <pre>
<code>GET /deliveries/01GVDFM78ZXGT1ENB78F6BMDQW/status HTTP/1.1
Host: localhost:8000
</code>
</pre>
      <h4>Example Response</h4>
      <pre>
<code>HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "01GVDFM78ZXGT1ENB78F6BMDQW",
    "budget": 750,
    "notes": "BigMac, Coca cola and fries",
    "status": "completed",
    "purchase_price": 200,
    "quantity": 0,
    "sell_price": 250
}
</code>
        </div>
       </div></pre>

<div>
 <div>
  <div>
   <div></div>
  </div>
  <div>
   <div>
    <div>
     <div>
      <h3>Increase budget</h3>
      <p><strong>POST</strong> <code>/event</code></p>
      <p>Increase the budget of a delivery.</p>
      <h4>Request Body</h4>
      <table>
       <thead>
        <tr>
         <th>Name</th>
         <th>Type</th>
         <th>Description</th>
        </tr>
       </thead>
       <tbody>
        <tr>
         <td>type</td>
         <td>string</td>
         <td>The type of event. Must be <code>INCREASE_BUDGET</code>.</td>
        </tr>
        <tr>
         <td>delivery_id</td>
         <td>string</td>
         <td>The ID of the delivery to increase the budget for.</td>
        </tr>
        <tr>
         <td>data</td>
         <td>object</td>
         <td>The data of the event.</td>
        </tr>
        <tr>
         <td>data.budget</td>
         <td>integer</td>
         <td>The amount to increase the budget by.</td>
        </tr>
       </tbody>
      </table>
      <h4>Response Body</h4>
      <table>
       <thead>
        <tr>
         <th>Name</th>
         <th>Type</th>
         <th>Description</th>
        </tr>
       </thead>
       <tbody>
        <tr>
         <td>id</td>
         <td>string</td>
         <td>The ID of the delivery.</td>
        </tr>
        <tr>
         <td>budget</td>
         <td>integer</td>
         <td>The budget of the delivery, after the increase.</td>
        </tr>
        <tr>
         <td>notes</td>
         <td>string</td>
         <td>The notes of the delivery.</td>
        </tr>
        <tr>
         <td>status</td>
         <td>string</td>
         <td>The status of the delivery. Must be <code>active</code>.</td>
        </tr>
       </tbody>
      </table>
      <h4>Example Request</h4>
      <pre>
<code>POST /event HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "type": "INCREASE_BUDGET",
    "delivery_id": "01GVDBB3PG55CBZRJCTPWNN2PV",
    "data": {
        "budget": 500
    }
}
</code>
</pre>
  <h4>Example Response</h4>
<pre>
<code>HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "01GVDBB3PG55CBZRJCTPWNN2PV",
    "budget": 1100,
    "notes": "BigMac, Coca cola and fries",
    "status": "active"
}
</code>
</pre>
