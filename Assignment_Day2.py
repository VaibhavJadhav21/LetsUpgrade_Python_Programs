SBI ePay – Other Details Header Mapping Enhancement

1. Overview

This enhancement introduces support for receiving and mapping Other Details provided by the transaction service into the SBI ePay transaction report.

The Other Details data can be received in different formats:

- JSON
- Plain String
- Delimiter-separated String

The format of the incoming data is now maintained in the merchant configuration table using the "OtherDetailFormat" field.

Based on this configuration, the listener parses the incoming data and converts it into a common "JsonNode" structure. The parsed data is then used during report generation and header mapping.

The enhancement is designed to work with the existing report header structure. The existing headers are retained, and "OtherDetail" is added as an additional header.

---

2. Existing Flow

Previously, the transaction report was generated using the configured report headers.

The existing report already contains approximately 20 headers.

The enhancement should not replace or modify these existing headers.

Existing Flow

Transaction
    |
    v
Transaction Service
    |
    v
Message / Kafka
    |
    v
Listener
    |
    v
Transaction Processing
    |
    v
Report Generation
    |
    v
Existing Header Mapping
    |
    v
Transaction Report

---

3. New Requirement

The transaction service can now provide an additional field containing merchant-specific information.

This information needs to be:

1. Received by the listener.
2. Parsed according to the merchant's configured format.
3. Converted into a common JSON structure.
4. Flattened/mapped where required.
5. Stored/retrieved using the Other Details configuration.
6. Added to the existing report header mapping.
7. Included as the new "OtherDetail" column in the generated report.

---

4. Other Details Format

The format is configured in the merchant configuration table.

Configuration Field

OtherDetailFormat

Supported values:

JSON
PLAIN STRING
DELIMITER

The listener does not need to assume a fixed format.

Instead, it reads the format from:

merchantInfo.getOtherDetailFormat()

and passes it along with the received data to the parsing method.

Example:

JsonNode parsedData = parseData(
        transactionMessage.getData(),
        merchantInfo.getOtherDetailFormat()
);

---

5. Data Received from Transaction Service

The transaction service producer publishes the Other Details information along with the transaction information.

The message contains the required transaction identifiers and the additional data.

Message Structure

mId
sbiOrderRefNum
data

Where:

Field| Description
"mId"| Merchant ID
"sbiOrderRefNum"| SBI Order Reference Number
"data"| Other Details received from the transaction service

The "data" field is handled as a "JsonNode"/JSON-compatible structure during processing.

---

6. Listener Processing

The listener consumes the message from the transaction service.

The listener performs the following operations:

Receive Message
      |
      v
Get MID
      |
      v
Get SBI Order Reference Number
      |
      v
Get Other Details Data
      |
      v
Fetch Merchant Configuration
      |
      v
Read OtherDetailFormat
      |
      v
Parse Data
      |
      v
Convert to JsonNode
      |
      v
Store / Process Other Details

The important point is that parsing is controlled by the database configuration rather than hard-coded for one particular merchant.

---

7. Parsing Logic

A common parsing method is used for all supported formats.

private JsonNode parseData(JsonNode data, String format) {
    if (data == null || format == null) {
        return NullNode.getInstance();
    }

    switch (format.toUpperCase()) {
        case "JSON":
            return parseJson(data);

        case "PLAIN STRING":
            return parsePlainString(data);

        case "DELIMITER":
            return parseDelimiterData(data);

        default:
            return NullNode.getInstance();
    }
}

This provides a single entry point for processing different types of Other Details.

---

8. JSON Format

When "OtherDetailFormat" is configured as:

JSON

the incoming data is already treated as JSON.

Example:

{
  "Admno": 2477687,
  "GatewayKey": 301,
  "Heads": {
    "CourseAmount": 1,
    "OtherAmount": 0,
    "TransportAmount": 0
  }
}

The JSON structure is retained as a "JsonNode".

Nested objects can then be flattened when required for report/header mapping.

For example:

Admno
GatewayKey
Heads.CourseAmount
Heads.OtherAmount
Heads.TransportAmount

---

9. Plain String Format

When:

OtherDetailFormat = PLAIN STRING

the incoming value is treated as a single value.

Example:

2477687

or:

ABC12345

The value is converted into a JSON representation so that the remaining report-processing flow can work with a common "JsonNode" structure.

Conceptually:

Plain String
     |
     v
JsonNode
     |
     v
OtherDetail Mapping

---

10. Delimiter Format

When:

OtherDetailFormat = DELIMITER

the incoming value is interpreted using the configured delimiter.

The agreed implementation uses a pipe ("|") delimiter.

Example:

2477687|301|ABC123

The values are parsed according to their position.

Example logical representation:

0 -> 2477687
1 -> 301
2 -> ABC123

The parsed values are then converted into a JSON structure.

Using one delimiter keeps the parsing logic consistent and avoids ambiguity between comma-separated and pipe-separated input.

---

11. Why JsonNode Is Used

"JsonNode" is used as the common representation because the incoming Other Details can have different structures.

For example:

JSON

{
  "Admno": 2477687,
  "GatewayKey": 301
}

Plain String

ABC123

Delimiter

2477687|301|ABC123

Instead of maintaining separate DTO structures for each input format, all formats are normalized into a "JsonNode".

This allows the report-generation logic to process the data consistently.

---

12. Other Details Storage

A dedicated table is introduced to store Other Details received from the transaction service.

Proposed Table Structure

Column| Description
"ID"| Unique identifier
"MID"| Merchant ID
"SBI_ORDER_REF_NUM"| SBI Order Reference Number
"JSON"| Original/processed Other Details JSON
"FLATTEN_JSON"| Flattened representation of Other Details

The stored data can subsequently be retrieved during report generation.

---

13. Flatten JSON

Nested JSON is flattened so that individual fields can be mapped to report headers.

For example:

Input

{
  "Admno": 2477687,
  "GatewayKey": 301,
  "Heads": {
    "CourseAmount": 1,
    "OtherAmount": 0,
    "TransportAmount": 0
  }
}

Flattened Structure

Admno = 2477687
GatewayKey = 301
Heads.CourseAmount = 1
Heads.OtherAmount = 0
Heads.TransportAmount = 0

The flattened structure makes it possible to identify individual values while performing header mapping.

---

14. Report Header Configuration

The existing report header configuration table is:

REPORT_HEADER_CONFIG

The enhancement introduces the new mapping:

OTHER_DETAIL

The existing report headers remain unchanged.

For example:

Existing Header 1
Existing Header 2
...
Existing Header 20
OtherDetail

Therefore:

Existing headers + OtherDetail

are used for report generation.

---

15. Other Detail Header

The new report header is:

OtherDetail

Its mapping is configured through:

OTHER_DETAIL

The new header does not replace any existing header.

If the report already contains 20 headers, the resulting configuration contains:

20 Existing Headers
+
1 OtherDetail Header
=
21 Headers

The "OtherDetail" header uses the special mapping/index configuration instead of a hard-coded transaction-data index.

---

16. Header Mapping Logic

During report generation, the system first loads the configured headers.

Existing header values are populated exactly as before.

After the existing header values are prepared, the Other Details value is added.

Conceptually:

Existing Transaction Data
        |
        v
Existing Header Mapping
        |
        +------------------+
        |                  |
        v                  v
Existing Headers       OtherDetail
                           |
                           v
                  Parsed Other Details
                           |
                           v
                    Header JSON

This ensures that existing report functionality is not impacted.

---

17. Header JSON

The final header JSON contains the existing headers plus the new Other Details mapping.

Example conceptual structure:

{
  "Header1": "value1",
  "Header2": "value2",
  "Header3": "value3",
  "...": "...",
  "OtherDetail": "mappedValue"
}

If the Other Details contain multiple fields, the corresponding configured mappings can be populated from the flattened JSON.

---

18. Merchant-Specific Mapping

The enhancement supports merchant-specific Other Details.

For example, one merchant may send:

JSON

while another merchant may send:

PLAIN STRING

and another merchant may send:

DELIMITER

The system determines the correct parsing strategy using:

OtherDetailFormat

from the merchant configuration.

Therefore, the implementation does not require separate code changes for every merchant.

---

19. Example – SBI Data

Sample SBI Other Details structure:

{
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
  }
}

The JSON is received by the transaction service and published to the listener.

The listener reads the merchant's configured:

OtherDetailFormat = JSON

The data is then parsed into "JsonNode".

Nested values can be flattened and used for header mapping.

---

20. End-to-End Flow

                Transaction Service
                       |
                       |
                       v
                Kafka Producer
                       |
                       | mId
                       | sbiOrderRefNum
                       | data
                       v
                    Listener
                       |
                       v
             Fetch Merchant Info
                       |
                       v
              OtherDetailFormat
                       |
             +---------+---------+
             |         |         |
             v         v         v
            JSON   PLAIN STRING  DELIMITER
             |         |         |
             +---------+---------+
                       |
                       v
                   JsonNode
                       |
                       v
              Flatten / Process
                       |
                       v
             Other Details Table
                       |
                       v
             Report Generation
                       |
                       v
          Existing Header Mapping
                       |
                       v
              Add OtherDetail
                       |
                       v
              Final Report File

---

21. Scheduler Changes

The scheduler/report-generation flow has been updated to support the new Other Details information.

During report generation:

1. Existing transaction data is fetched.
2. Existing header mapping is performed.
3. Other Details are retrieved using the required transaction identifiers.
4. Other Details are converted/processed as required.
5. The "OtherDetail" header is populated.
6. The final report is generated.

The existing scheduler functionality remains unchanged apart from the additional Other Details processing.

---

22. Database Changes

The enhancement requires database configuration changes for:

Merchant Configuration

OtherDetailFormat

Supported values:

JSON
PLAIN STRING
DELIMITER

Report Header Configuration

REPORT_HEADER_CONFIG

with:

OTHER_DETAIL

mapping.

Other Details Table

Stores:

MID
SBI_ORDER_REF_NUM
JSON
FLATTEN_JSON

Liquibase scripts should be maintained for the required table/column changes.

---

23. Error Handling

The implementation should handle the following cases:

Null Data

If Other Details data is not available:

No OtherDetail value

should be added rather than causing the complete report generation to fail.

Missing Format

If "OtherDetailFormat" is unavailable, the system should not attempt to apply an incorrect parser.

Unsupported Format

If an unsupported format is configured, the data should be handled safely and logged.

Invalid JSON

For JSON format, malformed JSON should be handled through exception handling and appropriate logging.

Invalid Delimiter Data

If delimiter-based data does not contain the expected number of values, the parser should handle the available values without breaking the entire transaction processing flow.

---

24. Important Implementation Points

Existing Headers Must Be Preserved

The enhancement is additive.

Existing headers
      +
OtherDetail

No existing header should be replaced.

Avoid Hard-Coded Data Indexes

The Other Details mapping should not depend on hard-coded values such as:

rowData.get(26)

Instead, the index/mapping should be determined from the configured header mapping.

Single Delimiter

Only the agreed delimiter should be used for delimiter-based input:

|

Common Data Type

The parsed result should be represented using:

JsonNode

This keeps JSON, plain-string, and delimiter processing consistent.

---

25. Benefits

The enhancement provides:

- Merchant-specific Other Details support.
- Support for multiple input formats.
- Configuration-driven parsing.
- No impact on existing report headers.
- Flexible JSON/nested-data mapping.
- Reusable parsing logic.
- Better separation between transaction processing and report mapping.
- Ability to introduce additional merchant-specific fields without changing the core report structure.

---

26. Testing Scenarios

The following scenarios should be covered during testing.

Scenario| Expected Result
Valid JSON| JSON parsed successfully
Nested JSON| Nested fields flattened correctly
Plain String| Value converted and mapped
Pipe-delimited data| Values parsed according to position
Null data| Processing should not fail
Missing format| Safe handling
Invalid JSON| Error handled/logged
Invalid delimiter input| Safe handling
Existing 20 headers| All existing headers remain unchanged
OtherDetail configured| New header populated
OtherDetail not available| Existing report generation continues
Multiple merchants| Each merchant uses its configured format

---

27. Summary

The SBI ePay enhancement introduces a configuration-driven Other Details Header Mapping mechanism.

The transaction service publishes Other Details along with:

MID
SBI Order Reference Number
Data

The listener retrieves the merchant's "OtherDetailFormat" and parses the data as:

JSON
PLAIN STRING
DELIMITER

The parsed information is normalized into "JsonNode", flattened where required, and stored/retrieved through the Other Details mechanism.

During report generation, the existing headers are retained and the new:

OtherDetail

header is added using the "OTHER_DETAIL" configuration.

This makes the solution flexible for SBI and other merchants while avoiding hard-coded field indexes and unnecessary changes to the existing report-generation logic.
