@Transactional
public List<MerchantEntity> updateMerchant(
        String mId,
        List<MerchantUpdateRequestDto> requestList) {

    List<MerchantEntity> existingRecords =
            merchantRepository.findByMId(mId);

    if (CollectionUtils.isEmpty(existingRecords)) {
        throw new ResourceNotFoundException(
                "No records found for mId: " + mId);
    }

    Map<Long, MerchantEntity> existingById =
            existingRecords.stream()
                    .collect(Collectors.toMap(
                            MerchantEntity::getId,
                            Function.identity()));

    for (MerchantUpdateRequestDto request : requestList) {

        MerchantEntity existing =
                existingById.get(request.getId());

        if (existing == null) {
            throw new ResourceNotFoundException(
                    "Record not found for id: " + request.getId());
        }

        merchantMapper.updateEntityFromRequest(request, existing);
    }

    return merchantRepository.saveAll(existingRecords);
}
