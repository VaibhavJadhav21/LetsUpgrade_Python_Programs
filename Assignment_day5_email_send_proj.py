public void processOtherDetails(OtherDetailsDto otherDetailsDto) {

    JsonNode data = otherDetailsDto.getOtherDetails();

    String otherDetailsFormat =
            merchantInfoDao.getOtherDetailsFormatForMid(otherDetailsDto.getMid());

    if (data == null || data.isNull()) {
        log.warn("Other Details data is null for Mid: {}", otherDetailsDto.getMid());
        return;
    }

    if (otherDetailsFormat == null || otherDetailsFormat.isBlank()) {
        log.warn("Other Details format is not configured for Mid: {}",
                otherDetailsDto.getMid());
        return;
    }

    try {

        String flattenJson;

        switch (otherDetailsFormat.trim().toUpperCase()) {

            case "JSON":
                flattenJson = flattenJson(data);
                break;

            case "DELIMITER": {
                String value = data.asText();

                String[] values = value.split("\\|", -1);

                ObjectNode node = objectMapper.createObjectNode();

                for (int i = 0; i < values.length; i++) {
                    node.put(String.valueOf(i), values[i].trim());
                }

                flattenJson = flattenJson(node);
                break;
            }

            case "PLAIN STRING": {
                ObjectNode node = objectMapper.createObjectNode();

                node.put("0", data.asText());

                flattenJson = flattenJson(node);
                break;
            }

            default:
                throw new IllegalArgumentException(
                        "Unsupported Other Details format: " + otherDetailsFormat);
        }

        OtherDetailsInfo otherDetailsInfo = new OtherDetailsInfo();

        otherDetailsInfo.setMid(otherDetailsDto.getMid());
        otherDetailsInfo.setSbiOrderRefNumber(
                otherDetailsDto.getSbiOrderRefNumber());
        otherDetailsInfo.setOtherDetailsJson(
                otherDetailsDto.getOtherDetails().toString());
        otherDetailsInfo.setFlattenJson(flattenJson);

        // save
        otherDetailsInfoRepository.save(otherDetailsInfo);

    } catch (Exception e) {
        log.error("Error while processing Other Details for Mid: {}",
                otherDetailsDto.getMid(), e);

        throw new IllegalArgumentException(
                "Unable to process Other Details", e);
    }
}
