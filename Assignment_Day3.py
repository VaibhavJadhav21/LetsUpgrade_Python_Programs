Other Details Publisher – Order Creation API

Summary

As part of the Order Creation API enhancement, an Other Details publisher has been integrated into the order creation flow.

Whenever an order is created successfully, the Order Creation API prepares the Other Details information available in the request/order data and publishes it along with the required transaction identifiers.

The publisher message contains the following three fields:

mId
sbiOrderRefNum
data

Where:

- mId – Merchant ID associated with the order.
- sbiOrderRefNum – SBI Order Reference Number generated/associated with the order.
- data – Other Details received during order creation, represented as "JsonNode".

Order Creation Flow

Order Creation API
        |
        v
Validate Request
        |
        v
Create Order
        |
        v
Prepare Other Details
        |
        v
Create Publisher DTO
        |
        +-------------------------+
        |           |             |
        v           v             v
      mId    sbiOrderRefNum      data
        |           |             |
        +-----------+-------------+
                    |
                    v
             Publish Message
                    |
                    v
              Kafka Topic
                    |
                    v
             Consumer/Listener

Publisher DTO

The publisher DTO contains:

private String mId;
private String sbiOrderRefNum;
private JsonNode data;

Using "JsonNode" for "data" allows the API to publish dynamic Other Details without defining separate DTOs for merchant-specific fields.

For example, SBI Other Details may contain:

{
  "Admno": 2477687,
  "GatewayKey": 301,
  "Heads": {
    "CourseAmount": 1,
    "OtherAmount": 0,
    "TransportAmount": 0
  }
}

The complete structure is passed as "data" to the publisher.

Responsibility of the Order Creation API

The Order Creation API is responsible for:

1. Creating the order.
2. Collecting the required transaction identifiers.
3. Preparing the Other Details data.
4. Creating the publisher DTO.
5. Publishing the message.

The API does not perform report header mapping or flattening.

Downstream Processing

After publication, the consumer/listener processes the message.

The consumer:

- Retrieves the merchant configuration.
- Reads "OtherDetailFormat".
- Determines whether the data is "JSON", "PLAIN STRING", or "DELIMITER".
- Parses the data into the required structure.
- Stores the Other Details.
- Makes the data available for transaction report generation.

This keeps the Order Creation API lightweight while allowing the downstream service to handle format-specific processing.

Key Design Point

The publisher is triggered as part of the Order Creation API flow, ensuring that the Other Details associated with the newly created order are published at the time of order creation.

The publisher follows a common message structure:

mId + sbiOrderRefNum + data

and uses "JsonNode" for flexible Other Details handling.

This approach avoids hard-coding merchant-specific fields in the Order Creation API and allows the downstream processing flow to support different Other Details formats through configuration.
