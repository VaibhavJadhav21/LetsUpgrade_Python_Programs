Business Logic – Point Wise
Order Creation: Other Details are captured during the Order Creation API.
Publish Data: The API publishes MID, SBI Order Reference Number, and Other Details data.
Consume Message: The listener consumes the published message.
Fetch Configuration: Listener fetches OtherDetailFormat from merchant configuration.
Identify Format: Data is processed based on the configured format:
JSON
Plain String
Delimiter
Parse Data: The received data is converted into a common JsonNode structure.
Flatten Data: Nested JSON fields are flattened where required for easy header mapping.
Store Data: Original JSON and flattened JSON are stored in the Other Details table against MID and SBI Order Reference Number.
Report Mapping: During transaction report generation, the stored Other Details are fetched and mapped dynamically to the OtherDetail header.
Existing Headers: Existing transaction report headers remain unchanged; OtherDetail is added as an additional header.
