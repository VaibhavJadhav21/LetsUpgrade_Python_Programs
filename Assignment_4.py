public MerchantInfoDto updateMerchantInfo(String mId, RiskManagementDto riskManagementDto) {
    // 1. Fetch existing entity or throw exception
    MerchantInfo existingMerchantInfo = merchantInfoRepository.findById(mId)
        .orElseThrow(() -> new AdminPortalException(NOT_FOUND_ERROR_CODE, MessageFormat.format(..., mId)));

    // 2. Map fields from DTO (extracting merchantInfoDto) into the existing entity
    merchantInfoMapper.mapDtoToEntityForUpdate(riskManagementDto.getMerchantInfoDto(), existingMerchantInfo);

    // 3. Save the updated entity
    MerchantInfo saveMerchantInfo = merchantInfoRepository.save(existingMerchantInfo);
    
    logger.info("merchantInfo entity saved successfully. mID: {}", mId);
    
    // 4. Return mapped response DTO
    return merchantInfoMapper.entityToMerchantInfoDTO(saveMerchantInfo);
}
