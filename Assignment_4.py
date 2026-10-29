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

        // 1. Fetch matching payment gateway
        PaygatewayMaster gateway = paygatewayMasterRepository
                .findById(mapping.getPaygatewayId())
                .orElse(null);

        if (gateway == null) {
            continue;
        }

        // 2. Fetch merchant-specific channel pricing
        List<ChannelPricingMaster> channelPricing =
                channelPricingMasterRepository
                        .findByMerchantIdAndPaygatewayId(
                                mid,
                                mapping.getPaygatewayId()
                        );

        PricingEntity item;

        if (channelPricing != null && !channelPricing.isEmpty()) {

            // 3. Merchant-specific pricing found
            item = pricingEntityMapper.toItem(
                    mapping,
                    gateway,
                    channelPricing
            );

        } else {

            // 4. Fetch default channel pricing from DB
            List<ChannelPricingMaster> defaultPricing =
                    channelPricingMasterRepository
                            .findByMerchantIdIsNullAndPaygatewayId(
                                    mapping.getPaygatewayId()
                            );

            // 5. Map default pricing
            item = pricingEntityMapper.toDefaultItem(
                    mapping,
                    gateway,
                    defaultPricing
            );
        }

        items.add(item);
    }

    // 6. Map response
    return pricingEntityMapper.toResponse(mid, items);
}
