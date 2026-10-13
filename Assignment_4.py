@Transactional
public List<MerchantRfcDto> updateMerchantRfcInfo(
        String mId, RiskManagementDto riskManagementDto) {

    logger.info("Processing merchant RFC info for mID: {}", mId);

    List<MerchantRfcDto> requestList = riskManagementDto.getMerchantRfcDto();

    if (CollectionUtils.isEmpty(requestList)) {
        return Collections.emptyList();
    }

    Map<UUID, MerchantRfc> existingRecords = merchantRfcRepository
            .findByMerchantId(mId)
            .stream()
            .collect(Collectors.toMap(
                    MerchantRfc::getId,
                    Function.identity()
            ));

    List<MerchantRfc> recordsToSave = requestList.stream()
            .map(request -> prepareMerchantRfc(request, mId, existingRecords))
            .collect(Collectors.toList());

    List<MerchantRfc> savedRecords = merchantRfcRepository.saveAll(recordsToSave);

    logger.info("Merchant RFC info processed successfully for mID: {}", mId);

    return merchantRfcMapper.mapListEntityToResponse(savedRecords);
}

private MerchantRfc prepareMerchantRfc(
        MerchantRfcDto request,
        String mId,
        Map<UUID, MerchantRfc> existingRecords) {

    MerchantRfc entity;

    if (request.getId() != null) {
        entity = existingRecords.get(request.getId());

        if (entity == null) {
            throw new EntityNotFoundException(
                    "Merchant RFC record not found for id: " + request.getId());
        }

        merchantRfcMapper.updateEntityFromRequest(request, entity);

        logger.debug("Merchant RFC record updated. mID: {}, id: {}",
                mId, request.getId());

    } else {
        entity = merchantRfcMapper.mapToListEntity(request);
        entity.setMerchantId(mId);

        logger.debug("New Merchant RFC record created for mID: {}", mId);
    }

    entity.setAuthStatus(MerchantAuthType.PENDING.name());

    return entity;
}
