Transaction Service – Other Details Publisher

1. Purpose

The Publisher is implemented in the Transaction Service to send Other Details information to the downstream service responsible for processing and storing the data.

The main purpose of the publisher is to transfer the following information:

- Merchant ID ("mId")
- SBI Order Reference Number ("sbiOrderRefNum")
- Other Details data ("data")

The publisher does not perform the report mapping itself. Its responsibility is to package the transaction information into a message and publish it to the configured messaging topic.

---

2. Publisher Flow

The overall publisher flow is:

Transaction Processing
        |
        v
Other Details Available
        |
        v
Create Publisher DTO
        |
        +----------------------+
        |                      |
        v                      v
       mId              sbiOrderRefNum
        |                      |
        +----------+-----------+
                   |
                   v
                 data
                   |
                   v
          Publish Message
                   |
                   v
              Kafka Topic
                   |
                   v
             Consumer/Listener

The publisher is therefore the entry point for transferring Other Details from the Transaction Service to the downstream processing service.

---

3. Publisher DTO

A dedicated DTO is used for the message.

The DTO contains three fields:

private String mId;
private String sbiOrderRefNum;
private JsonNode data;

Field Description

Field| Type| Description
"mId"| String| Merchant identifier
"sbiOrderRefNum"| String| SBI order reference number used to identify the transaction
"data"| JsonNode| Other Details received/generated for the transaction

Using "JsonNode" for "data" allows the publisher to send flexible Other Details without creating a separate DTO for every merchant-specific structure.

---

4. Why JsonNode Is Used for Data

The Other Details structure can differ from merchant to merchant.

For example, SBI can provide nested JSON:

{
  "Admno": 2477687,
  "GatewayKey": 301,
  "Heads": {
    "CourseAmount": 1,
    "OtherAmount": 0,
    "TransportAmount": 0
  }
}

Instead of converting this into a fixed Java object, the publisher keeps the structure as a "JsonNode".

This provides the following benefits:

- Supports dynamic fields.
- Supports nested JSON.
- Avoids creating merchant-specific DTOs.
- Preserves the original structure.
- Allows the consumer to process the data according to "OtherDetailFormat".

---

5. Publisher Trigger

The publisher is invoked when the Transaction Service has Other Details that need to be transferred.

The transaction processing flow identifies the relevant transaction information and prepares the publisher request.

Conceptually:

OtherDetailPublisherDto message =
        new OtherDetailPublisherDto(
                transaction.getMid(),
                transaction.getSbiOrderRefNum(),
                otherDetails
        );

The message is then passed to the Kafka publisher.

---

6. Message Creation

The publisher creates a message containing the three required values:

mId
sbiOrderRefNum
data

Example:

{
  "mId": "123456",
  "sbiOrderRefNum": "SBIORD123456",
  "data": {
    "Admno": 2477687,
    "GatewayKey": 301,
    "Heads": {
      "CourseAmount": 1,
      "OtherAmount": 0
    }
  }
}

The complete "data" object is kept as JSON rather than extracting individual fields at the publisher level.

---

7. Kafka Publishing

Once the DTO is prepared, the publisher sends the message to the configured Kafka topic.

Conceptually:

kafkaTemplate.send(topic, message);

The publisher is responsible only for publishing the message.

The downstream listener is responsible for:

1. Receiving the message.
2. Fetching merchant configuration.
3. Reading "OtherDetailFormat".
4. Parsing the data.
5. Storing the Other Details.
6. Making the data available for report generation.

---

8. Separation of Responsibility

The implementation follows a clear separation of responsibilities.

Transaction Service / Publisher

Responsible for:

Prepare Data
     ↓
Create DTO
     ↓
Publish Message

Consumer / Listener

Responsible for:

Consume Message
     ↓
Read Merchant Configuration
     ↓
Identify OtherDetailFormat
     ↓
Parse Data
     ↓
Store Other Details

Report Generation

Responsible for:

Fetch Other Details
     ↓
Flatten / Map Data
     ↓
Map to OtherDetail Header
     ↓
Generate Report

This prevents report-specific logic from being introduced into the Transaction Service publisher.

---

9. Handling Different Data Formats

The publisher does not need separate publishing logic for:

- JSON
- Plain String
- Delimiter

The publisher sends the available data in the common "data" field.

The actual format is determined using merchant configuration.

For example:

Merchant Configuration
        |
        v
OtherDetailFormat = JSON
        |
        v
Consumer parses JSON

or:

Merchant Configuration
        |
        v
OtherDetailFormat = PLAIN STRING
        |
        v
Consumer parses plain string

or:

Merchant Configuration
        |
        v
OtherDetailFormat = DELIMITER
        |
        v
Consumer parses delimiter data

This keeps the publisher simple and makes the solution configuration-driven.

---

10. Example – SBI JSON Data

For the SBI use case, the publisher can send:

{
  "mId": "123456",
  "sbiOrderRefNum": "SBI123456789",
  "data": {
    "Admno": 2477687,
    "GatewayKey": 301,
    "Heads": {
      "CourseAmount": 1,
      "OtherAmount": 0,
      "TransportAmount": 0,
      "MaterialAmount": 0,
      "UniformAmnt": 0,
      "UniformFeeS": 0,
      "Ino": 0,
      "Exam": 0
    },
    "ApexId": "ABC123",
    "AcademicYear": "2026",
    "AppSource": "SBI"
  }
}

The publisher sends this message without changing the nested structure.

The consumer can then flatten the required fields for report mapping.

---

11. Benefits of the Publisher Design

The new publisher design provides:

- Loose coupling between Transaction Service and report processing.
- Dynamic data support through "JsonNode".
- Merchant-specific flexibility.
- No hard-coded Other Details fields.
- No report-specific parsing logic in Transaction Service.
- Easy extension if additional Other Details fields are introduced.
- Consistent message structure across different merchants.

---

12. End-to-End Publisher and Consumer Flow

                    TRANSACTION SERVICE
                           |
                           v
                  Transaction Completed
                           |
                           v
                   Other Details Found
                           |
                           v
                Create Publisher DTO
                           |
              +------------+------------+
              |            |            |
              v            v            v
             mId     sbiOrderRefNum     data
              |            |            |
              +------------+------------+
                           |
                           v
                    Kafka Publisher
                           |
                           v
                      Kafka Topic
                           |
                           v
                    Other Details
                       Listener
                           |
                           v
                Fetch Merchant Info
                           |
                           v
                  OtherDetailFormat
                           |
              +------------+------------+
              |            |            |
             JSON      PLAIN STRING   DELIMITER
              |            |            |
              +------------+------------+
                           |
                           v
                       JsonNode
                           |
                           v
                 Store Other Details
                           |
                           v
                  Report Generation
                           |
                           v
                 Existing Headers
                           +
                    OtherDetail
                           |
                           v
                    Final Report

13. Key Design Decision

The important design decision is that format-specific processing is not performed by the publisher.

The publisher has a simple responsibility:

«Publish "mId", "sbiOrderRefNum", and "data" as a single message.»

The consumer uses the merchant's "OtherDetailFormat" configuration to determine how the "data" should be interpreted.

This keeps the Transaction Service independent of merchant-specific report requirements and makes the overall implementation easier to maintain and extend.
