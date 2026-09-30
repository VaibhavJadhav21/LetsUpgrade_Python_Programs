public List<MerchantRfCResponse> updateMerchantRfCInfo(
        String mid, RiskManagementDto riskManagementDto) {

    List<MerchantRfC> existingRfCList =
            merchantRfCRepository.findByMerchantId(mid);

    if (existingRfCList.isEmpty()) {
        logger.error("Database merchantRfC list is empty for MID: {}", mid);
        throw new AdminPortalException(
                ErrorConstants.VOLUME_ERROR_CODE,
                ErrorConstants.VOLUME_ERROR_MESSAGE);
    }

    List<MerchantRfC> rfCtoList = riskManagementDto.getMerchantRfC();

    if (rfCtoList == null || rfCtoList.isEmpty()) {
        return merchantRfCMapper.mapEntityToResponse(existingRfCList);
    }

    List<MerchantRfC> entitiesToSave =
            merchantRfCMapper.mapToListEntityList(rfCtoList);

    entitiesToSave.forEach(entity -> entity.setMerchantId(mid));

    List<MerchantRfC> savedRfCList =
            merchantRfCRepository.saveAll(entitiesToSave);

    return merchantRfCMapper.mapEntityToResponse(savedRfCList);
}
