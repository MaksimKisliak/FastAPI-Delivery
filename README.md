<ol>
 <li>A user creates a new delivery by sending a POST request to the <code>/deliveries/create</code> endpoint, with a payload containing the delivery's budget and notes.</li>
<pre><span></span><code>             ┌────────────┐
             │            │
             │   <span>User</span>     │
             │            │
             └────────────┘
                    │
                    │
                    ▼
       ┌───────────────────────┐
       │  <span>/</span>deliveries<span>/</span><span>create</span>   │
       │       endpoint        │
       └───────────────────────┘
                    │
                    │
                    ▼
         ┌─────────────────┐
         │  Delivery Object│
         └─────────────────┘
                    │
                    │
                    ▼
          ┌───────────────┐
          │    Redis      │
          └───────────────┘

</code></pre>
 <li>The app creates a new <code>Delivery</code> object with the specified budget and notes and saves it to Redis as a new hash with a unique primary key. The app also dispatches a <code>CREATE_DELIVERY</code> event for the new delivery and stores it in Redis as a new hash with a unique primary key. The <code>delivery_id</code> field of the event is set to the primary key of the new <code>Delivery</code> object.</li>
<pre><span></span><code>             ┌────────────┐
             │            │
             │    App     │
             │            │
             └────────────┘
                    │
                    │
                    ▼
       ┌───────────────────────┐
       │Create Delivery Object │
       └───────────────────────┘
                    │
                    │
                    ▼
          ┌───────────────┐
          │    Redis      │
          └───────────────┘
                    │
                    │
                    ▼
        ┌──────────────────┐
        │Create</span> Delivery Event
        └──────────────────┘
                    │
                    │
                    ▼
          ┌───────────────┐
          │    Redis      │
          └───────────────┘

</code></pre>
 <li>The <code>create_delivery</code> function is called to update the state of the new delivery based on the <code>CREATE_DELIVERY</code> event. The function creates a new state object with the delivery's ID, budget, notes, and status set to "ready".</li>
<pre><code>             ┌────────────┐
             │            │
             │    App     │
             │            │
             └────────────┘
                    │
                    │
                    ▼
       ┌───────────────────────┐
       │create_delivery()      │
       └───────────────────────┘
                    │
                    │
                    ▼
        ┌──────────────────┐
        │  New State Object│
        └──────────────────┘
                    │
                    │
                    ▼
          ┌───────────────┐
          │    Redis      │
          └───────────────┘

</code></pre>
 <li>The user can retrieve the current status of the delivery by sending a GET request to the <code>/deliveries/{pk}/status</code> endpoint, where <code>{pk}</code> is the primary key of the delivery they want to retrieve. If the delivery's status has been updated by events, the response will contain the updated status. If not, the app will generate the current status by processing all events associated with the delivery and return it to the user:</li>
<pre><span></span><code>             ┌────────────┐
             │            │
             │   User     │
             │            │
             └────────────┘
                    │
                    │
                    ▼
       ┌───────────────────────┐
       │   /deliveries/{pk}/status 
       │         endpoint      │
       └───────────────────────┘
                    │
                    │
                    ▼
          ┌───────────────┐
          │    Redis      │
          └───────────────┘
                    │
                    │
                    ▼
        ┌──────────────────┐
        │Current Delivery Status
        └──────────────────┘

</code></pre>
 <li>If an event is received for a specific delivery, the app retrieves the current state of the delivery from Redis using the <code>delivery_id</code> field of the event. It then dispatches the event to the corresponding handling function, which updates the state of the delivery based on the event.</li>
<pre><span></span><code>             ┌────────────┐
             │            │
             │    App     │
             │            │
             └────────────┘
                    │
                    │
                    ▼
          ┌───────────────┐
          │   Event       │
          └───────────────┘
                    │
                    │
                    ▼
          ┌───────────────┐
          │    Redis      │
          └───────────────┘
                    │
                    │
                    ▼
       ┌───────────────────────┐
       │  Handling Function    │
       └───────────────────────┘
                    │
                    │
                    ▼
        ┌──────────────────┐
        │New State Object  │
        └──────────────────┘
                    │
                    │
                    ▼
          ┌───────────────┐
          │    Redis      │
          └───────────────┘

</code></pre>
 <li>After the delivery's state has been updated by an event, the app saves the new state to Redis under the hash with the primary key matching the delivery's ID.</li>
<pre><span></span><code><span>             ┌────────────┐
             │            │
             │    App     │
             │            │
             └────────────┘
                    │
                    │
                    ▼
          ┌───────────────┐
          │    Redis      │
          └───────────────┘
</span>
</code></pre>
