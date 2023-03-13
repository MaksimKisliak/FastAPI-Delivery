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
