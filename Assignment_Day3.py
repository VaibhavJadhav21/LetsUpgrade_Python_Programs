Other Details Listener – Summary

Overview

A dedicated listener has been implemented to consume the Other Details message published from the Order Creation API.

The listener receives the following information:

mId
sbiOrderRefNum
data

The primary responsibility of the listener is to process the received "data" according to the merchant-specific "OtherDetailFormat" configuration and persist the processed information for further use in transaction reports.

Listener Flow

Kafka Topic
     |
     v
Other Details Listener
     |
     v
Receive Message
     |
     +----------------------------+
     |            |               |
     v            v               v
    mId     sbiOrderRefNum       data
     |            |               |
     +------------+---------------+
                  |
                  v
          Fetch Merchant Info
                  |
                  v
        Read OtherDetailFormat
                  |
       +----------+----------+
       |          |          |
       v          v          v
      JSON    PLAIN STRING  DELIMITER
       |          |          |
       +----------+----------+
                  |
                  v
              Parse Data
                  |
                  v
               JsonNode
                  |
                  v
        Store Other Details

Format-Based Processing

The listener does not assume a fixed format for the incoming data.

It retrieves "OtherDetailFormat" from the merchant configuration.

Supported formats are:

JSON
PLAIN STRING
DELIMITER

The format is passed to the common parsing logic:

JsonNode parsedData = parseData(
        transactionMessage.getData(),
        merchantInfo.getOtherDetailFormat()
);

The parsing logic uses a "switch" based on the configured format.

JSON Processing

For JSON data, the listener retains the original JSON structure as a "JsonNode".

For example:

{
  "Admno": 2477687,
  "GatewayKey": 301,
  "Heads": {
    "CourseAmount": 1,
    "OtherAmount": 0
  }
}

Nested data can subsequently be flattened for report/header mapping while retaining the original JSON structure.

Example flattened keys:

Admno
GatewayKey
Heads.CourseAmount
Heads.OtherAmount

Persistence

After parsing, the listener stores the Other Details against the transaction using:

- Merchant ID
- SBI Order Reference Number
- Original/processed JSON
- Flattened JSON

This allows the information to be retrieved later during transaction report generation.

Key Responsibilities

The listener is responsible for:

1. Consuming the Other Details message.
2. Extracting "mId", "sbiOrderRefNum", and "data".
3. Fetching the merchant configuration.
4. Reading "OtherDetailFormat".
5. Parsing the incoming data based on the configured format.
6. Converting the result into "JsonNode".
7. Creating the required flattened representation for mapping.
8. Persisting the Other Details.
9. Ensuring the processed information is available for report generation.

Design Benefit

The listener provides a common processing layer for different merchants and data formats.

The Order Creation API only publishes the data, while the listener handles format-specific processing and persistence.

This provides a clean separation:

Order Creation API
       |
       | Publish
       v
Kafka
       |
       | Consume
       v
Listener
       |
       | Parse + Store
       v
Other Details
       |
       | Map
       v
Transaction Report
