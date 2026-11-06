public List<MerchantVvlRuleDto> getMerchantVvlRuleInfo(String mId) {

    logger.info("Fetching Merchant VVL details for merchantId: {}", mId);

    Map<String, MerchantVvlRuleDto> response = new LinkedHashMap<>();

    // Step 1: Fetch unique currency combinations
    List<UniqueCurrency> currencyCombinations =
            merchantCurrencyCombinationMappingRepository
                    .findUniqueOrderCurrencies(mId);

    for (UniqueCurrency currencyCombination : currencyCombinations) {

        String orderCurrencyCode =
                currencyCombination.getOrderCurrencyCode();

        String currencyCombCode =
                currencyCombination.getCurrencyCombCode();

        // Step 2: Fetch PayModes for each currency combination
        List<PayModeCode> payModes =
                merchantPaymodeMappingRepository.findingPayModeForMerchant(
                        mId, orderCurrencyCode, currencyCombCode);

        if (CollectionUtils.isEmpty(payModes)) {
            continue;
        }

        for (PayModeCode paymode : payModes) {

            String pmCode = paymode.getPaymodeCode();

            // Step 3: Fetch VVL records
            List<MerchantVvlRule> vvlRules =
                    merchantVvlRuleRepository
                            .findByMerchantIdAndPaymodeCodeAndOrderCurrencyCode(
                                    mId, pmCode, orderCurrencyCode);

            if (CollectionUtils.isEmpty(vvlRules)) {

                // Step 4: No VVL configuration - return default DTO
                MerchantVvlRuleDto defaultDto =
                        merchantVvlRuleMapper.toDefaultDto(
                                mId, orderCurrencyCode, pmCode);

                String defaultKey =
                        "DEFAULT_" + orderCurrencyCode + "_" + pmCode;

                response.putIfAbsent(defaultKey, defaultDto);

            } else {

                // Step 5: VVL configuration exists - return actual records
                for (MerchantVvlRule vvlRule : vvlRules) {

                    MerchantVvlRuleDto dto =
                            merchantVvlRuleMapper.toDto(vvlRule);

                    // Prevent duplicate records using database ID
                    String uniqueKey = "VVL_" + vvlRule.getId();

                    response.putIfAbsent(uniqueKey, dto);
                }
            }
        }
    }

    // Step 6: Return unique records
    return new ArrayList<>(response.values());
}
