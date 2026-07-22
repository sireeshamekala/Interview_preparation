Google Cloud Pub/Sub - Hands-on Documentation
What is Pub/Sub?
Google Cloud Pub/Sub is a fully managed messaging service that allows applications to communicate with each other asynchronously.
Instead of one application directly calling another application, it sends (publishes) a message to a Topic. Any application that wants the message creates a Subscription and receives it.
This helps applications work independently without depending on each other.
________________________________________
Why do we need Pub/Sub?
Suppose an e-commerce application receives a new order.
After an order is placed, many services need the same information:
•	Email Service
•	SMS Service
•	Inventory Service
•	Billing Service
•	Analytics Service
Without Pub/Sub:
Order Service
      |
      |-----> Email Service
      |
      |-----> Inventory Service
      |
      |-----> Billing Service
Problems:
•	Services are tightly coupled.
•	If one service is unavailable, the order service may fail.
•	Difficult to scale.
With Pub/Sub:
             Order Service
                   |
             Publish Message
                   |
             +--------------+
             | order-topic  |
             +--------------+
              /     |      \
             /      |       \
        Email   Inventory  Billing
Benefits:
•	Loose coupling
•	Better scalability
•	Reliable messaging
•	Easy to add new consumers
________________________________________
Main Components
1. Publisher
The application that sends messages.
Example:
Order Service
Publishes:
Order Created
________________________________________
2. Topic
A Topic is a channel where messages are published.
Example:
order-topic
Publishers send messages to a Topic.
________________________________________
3. Subscription
A Subscription listens to a Topic.
Example:
order-sub
Every subscription receives its own copy of every published message.
________________________________________
4. Subscriber
The application that receives and processes messages.
Example:
•	Email Service
•	Inventory Service
•	Billing Service
________________________________________
Complete Flow
Publisher
    |
    v
Topic
    |
    v
Subscription
    |
    v
Subscriber
________________________________________
Types of Subscriptions
Pull Subscription
The subscriber requests messages from Pub/Sub.
Subscriber

      |

Pull Messages

      |

Pub/Sub
Example:
gcloud pubsub subscriptions pull order-sub --auto-ack
________________________________________
Push Subscription
Pub/Sub automatically sends messages to an HTTP endpoint.
Publisher

      |

Topic

      |

Push Subscription

      |

Cloud Run
No polling is required.
________________________________________
Hands-on Lab 1 – Create a Topic
Create a Topic.
gcloud pubsub topics create order-topic
Verify:
gcloud pubsub topics list
Expected output:
order-topic
________________________________________
Hands-on Lab 2 – Create a Subscription
Create a Subscription.
gcloud pubsub subscriptions create order-sub \
    --topic=order-topic
Verify:
gcloud pubsub subscriptions list
Expected output:
order-sub
________________________________________
Hands-on Lab 3 – Publish a Message
Publish a message to the Topic.
gcloud pubsub topics publish order-topic \
    --message="Order 1001 Created"
Expected output:
messageIds:
- "123456789"
________________________________________
Hands-on Lab 4 – Pull the Message
Receive the published message.
gcloud pubsub subscriptions pull order-sub \
    --auto-ack
Output:
DATA: Order 1001 Created
Here:
•	pull retrieves the message.
•	--auto-ack automatically acknowledges the message after delivery.
________________________________________
Hands-on Lab 5 – Multiple Subscribers
Create additional subscriptions.
gcloud pubsub subscriptions create email-sub \
    --topic=order-topic
gcloud pubsub subscriptions create inventory-sub \
    --topic=order-topic
Architecture:
             order-topic
            /     |      \
           /      |       \
order-sub email-sub inventory-sub
Publish:
gcloud pubsub topics publish order-topic \
    --message="Laptop Ordered"
Pull from each subscription:
gcloud pubsub subscriptions pull email-sub --auto-ack
gcloud pubsub subscriptions pull inventory-sub --auto-ack
Observation:
Each subscription receives the same message independently.
________________________________________
Message Acknowledgement (ACK)
After processing a message successfully, the subscriber sends an ACK.
Publisher

    |

Topic

    |

Subscription

    |

Subscriber

    |

ACK
Pub/Sub removes the message after receiving the ACK.
________________________________________
What happens if ACK is not sent?
If the subscriber does not acknowledge the message:
Receive Message

↓

No ACK

↓

Retry

↓

Retry

↓

Retry
Pub/Sub keeps attempting delivery until the retry policy or dead-letter policy is reached.
________________________________________
Dead Letter Topic (DLT)
A Dead Letter Topic stores messages that repeatedly fail processing.
Architecture:
Publisher

    |

order-topic

    |

order-sub

    |

Processing Failed

    |

Retry 1

Retry 2

Retry 3

Retry 4

Retry 5

    |

dead-letter-topic

    |

dead-letter-sub
________________________________________
Hands-on – Create Dead Letter Topic
Create the Dead Letter Topic.
gcloud pubsub topics create dead-letter-topic
Create a subscription for it.
gcloud pubsub subscriptions create dead-letter-sub \
    --topic=dead-letter-topic
Find your Project Number.
gcloud projects describe PROJECT_ID \
    --format="value(projectNumber)"
Grant the Pub/Sub service account permission to publish to the dead-letter topic.
gcloud pubsub topics add-iam-policy-binding dead-letter-topic \
--member="serviceAccount:service-PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com" \
--role="roles/pubsub.publisher"
Create the main subscription with a Dead Letter Policy.
gcloud pubsub subscriptions create order-sub \
    --topic=order-topic \
    --dead-letter-topic=dead-letter-topic \
    --max-delivery-attempts=5
Publish a message.
gcloud pubsub topics publish order-topic \
    --message="Order-1001"
Run a subscriber that intentionally does not acknowledge the message.
Observe:
Delivery Attempt : 1

Delivery Attempt : 2

Delivery Attempt : 3

Delivery Attempt : 4

Delivery Attempt : 5
After the fifth failed delivery, the message is automatically moved to the Dead Letter Topic.
Verify:
gcloud pubsub subscriptions pull dead-letter-sub --auto-ack
Output:
DATA: Order-1001
________________________________________
Push Subscription
Instead of the subscriber pulling messages, Pub/Sub pushes them automatically.
Architecture:
Publisher

    |

Topic

    |

Push Subscription

    |

Cloud Run

    |

Process Message
Steps:
1.	Create a Topic.
2.	Deploy a Cloud Run service.
3.	Create a Push Subscription.
4.	Publish a message.
5.	Cloud Run receives the message automatically.
No manual pull is required.
________________________________________
Pull vs Push Subscription
Pull Subscription	Push Subscription
Subscriber requests messages	Pub/Sub sends messages automatically
Polling required	No polling
Used by Dataflow and custom applications	Used with Cloud Run, Cloud Functions, Webhooks
Subscriber controls when to receive	Pub/Sub controls delivery
________________________________________
Common Use Cases
•	Microservices communication
•	Real-time streaming
•	IoT data ingestion
•	Event-driven applications
•	Notifications
•	Data pipelines
•	Cloud Run integration
•	Cloud Functions integration
•	Dataflow streaming pipelines
•	BigQuery streaming
________________________________________
Pub/Sub with Dataflow
Applications

      |

Pub/Sub

      |

Dataflow

      |

Transform

      |

BigQuery
________________________________________
Pub/Sub with Cloud Run
Publisher

      |

Topic

      |

Push Subscription

      |

Cloud Run

      |

Business Logic
________________________________________
Pub/Sub with Airflow
Airflow DAG

      |

Publish Message

      |

Pub/Sub

      |

Cloud Run / Dataflow
________________________________________
Key Interview Points
•	Pub/Sub is a fully managed messaging service.
•	It enables asynchronous communication between applications.
•	Publishers send messages to Topics.
•	Subscribers receive messages through Subscriptions.
•	One Topic can have multiple Subscriptions.
•	Every Subscription receives its own copy of the message.
•	Messages are removed only after acknowledgment.
•	If a message is not acknowledged, Pub/Sub retries delivery.
•	After the configured maximum delivery attempts, the message can be routed to a Dead Letter Topic.
•	Pull subscriptions require consumers to request messages.
•	Push subscriptions automatically deliver messages to an HTTP endpoint such as Cloud Run or Cloud Functions.
•	Pub/Sub is widely used with Dataflow, BigQuery, Cloud Run, Cloud Functions, and Composer (Airflow) to build scalable event-driven data pipelines.
