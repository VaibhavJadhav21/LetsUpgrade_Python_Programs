} else {

    boolean alreadyExists =
            merchantRfcRepository
                    .existsByMerchantIdAndOrderCurrencyCodeAndAuthStatus(
                            mId,
                            requestDto.getOrderCurrencyCode(),
                            MerchantAuthType.PENDING.name()
                    );

    if (alreadyExists) {
        throw new BusinessException(
                "Pending RFC already exists for this merchant and currency: "
                        + requestDto.getOrderCurrencyCode()
        );
    }

    merchantRfc = merchantRfcMapper.mapDtoListToEntityList(requestDto);

    merchantRfc.setAuthStatus(MerchantAuthType.PENDING.name());
    merchantRfc.setAggregatorCode(SBI_AGGREGATOR_CODE);
    merchantRfc.setIsActive("Y");
    merchantRfc.setMerchantId(mId);

    Logger.info("New Merchant RFC record created. mID: {}", mId);
}
