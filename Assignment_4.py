public AdminPortalResponse<PricingDto> getPricingByMerchantId(String mid) {

    List<MerchantPaygatewayMapping> mappings =
            mappingRepository.findByMerchantId(mid);

    if (mappings == null || mappings.isEmpty()) {
        throw new AdminPortalException(
                NOT_FOUND_ERROR_CODE,
                MessageFormat.format(NOT_FOUND_ERROR_MESSAGE, mid)
        );
    }

    List<PricingEntity> items = new ArrayList<>();

    for (MerchantPaygatewayMapping mapping : mappings) {

        // Fetch matching payment gateway
        PaygatewayMaster gateway = paygatewayMasterRepository
                .findById(mapping.getPaygatewayId())
                .orElse(null);

        if (gateway == null) {
            continue;
        }

        // Fetch currency using currency code from mapping
        CurrencyMaster currency = null;

        if (mapping.getCurrencyCode() != null
                && !mapping.getCurrencyCode().isBlank()) {

            currency = currencyMasterRepository
                    .findByCurrencyCode(mapping.getCurrencyCode())
                    .orElse(null);
        }

        // Fetch default currency if mapping currency is unavailable
        if (currency == null) {
            currency = currencyMasterRepository
                    .findFirstByIsDefaultTrueAndIsActiveTrue()
                    .orElse(null);
        }

        // Map data into PricingEntity
        PricingEntity item = pricingEntityMapper.toItem(
                mapping,
                gateway,
                currency
        );

        items.add(item);
    }

    // Build response in your existing format
    return AdminPortalResponse.<PricingDto>builder()
            .data(Collections.singletonList(
                    PricingDto.builder()
                            .build(items)
            ))
            .status(SUCCESS_RESPONSE_CODE)
            .build();
}
