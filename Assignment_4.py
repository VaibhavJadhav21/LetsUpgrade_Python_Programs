public void validateRiskManagementRfcInfo(
        String mId,
        List<MerchantRfcRequestDto> merchantRfcDto) {

    errorDtoList = new ArrayList<>();

    if (CollectionUtils.isEmpty(merchantRfcDto)) {
        throw new AdminPortalException(
                INVALID_ERROR_CODE, "RFC details cannot be empty");
    }

    Set<UUID> requestIds = new HashSet<>();

    for (MerchantRfcRequestDto rfcInfoData : merchantRfcDto) {

        // Existing validations
        validateRfcInfoMandatoryFields(rfcInfoData);
        validateLeadingAndTrailingSpaceRfcFields(rfcInfoData);

        // Duplicate ID validation
        if (rfcInfoData.getId() != null
                && !requestIds.add(rfcInfoData.getId())) {

            throw new AdminPortalException(
                    INVALID_ERROR_CODE, "Duplicate RFC ID found");
        }
    }

    // ID and Version validation
    validateRfcIdAndVersion(mId, merchantRfcDto);

    // Pending record validation
    validatePendingRfcRecords(mId, merchantRfcDto);

    throwIfErrors();
}




private void validateRfcIdAndVersion(
        String mId,
        List<MerchantRfcRequestDto> requestList) {

    List<MerchantRfc> existingRecords =
            riskManagementDao.getMerchantRfcRecords(mId);

    Map<UUID, MerchantRfc> existingMap =
            existingRecords.stream()
                    .collect(Collectors.toMap(
                            MerchantRfc::getId,
                            Function.identity()
                    ));

    for (MerchantRfcRequestDto dto : requestList) {

        if (dto.getId() != null) {

            MerchantRfc existing = existingMap.get(dto.getId());

            if (existing == null) {
                throw new AdminPortalException(
                        INVALID_ERROR_CODE,
                        "Invalid RFC ID");
            }

            if (!Objects.equals(
                    existing.getVersion(), dto.getVersion())) {

                throw new AdminPortalException(
                        INVALID_ERROR_CODE,
                        "RFC version mismatch");
            }
        }
    }
}





private void validatePendingRfcRecords(
        String mId,
        List<MerchantRfcRequestDto> requestList) {

    for (MerchantRfcRequestDto dto : requestList) {

        // Duplicate pending check only for new records
        if (dto.getId() == null) {

            boolean alreadyExists =
                    riskManagementDao.existsPendingRfc(
                            mId,
                            dto.getOrderCurrencyCode()
                    );

            if (alreadyExists) {
                throw new AdminPortalException(
                        INVALID_ERROR_CODE,
                        "Pending RFC already exists for this merchant and currency");
            }
        }
    }
}





