public List<MerchantVvlRuleDto> getMerchantVvlRuleInfo(String mId) {

    logger.info("Fetching Merchant VVL details for merchantId: {}", mId);

    Map<String, MerchantVvlRuleDto> response = new LinkedHashMap<>();

    // Step 1: Fetch currency combinations
    List<UniqueCurrency> currencyCombinations =
            merchantCurrencyCombinationMappingRepository
                    .findUniqueOrdersCurrencies(mId);

    if (CollectionUtils.isEmpty(currencyCombinations)) {
        return new ArrayList<>();
    }

    // Step 2: Fetch all VVL records only once
    List<MerchantVvlRule> allVvlRules =
            merchantVvlRuleRepository.findByMerchantId(mId);

    // Step 3: Group VVL records by currency and payment mode
    Map<String, List<MerchantVvlRule>> vvlRulesMap =
            allVvlRules.stream()
                    .collect(Collectors.groupingBy(
                            rule -> getVvlKey(
                                    rule.getOrderCurrencyCode(),
                                    rule.getPaymodeCode()
                            )
                    ));

    // Step 4: Process currency combinations
    for (UniqueCurrency currency : currencyCombinations) {

        String orderCurrencyCode = currency.getOrderCurrencyCode();
        String currencyCombCode = currency.getCurrencyCombCode();

        // Step 5: Fetch payment modes
        List<PayModeCode> payModes =
                merchantPaymodeMappingRepository
                        .findingPayModeForMerchant(
                                mId,
                                orderCurrencyCode,
                                currencyCombCode
                        );

        if (CollectionUtils.isEmpty(payModes)) {
            continue;
        }

        for (PayModeCode payMode : payModes) {

            String pmCode = payMode.getPaymodeCode();

            // Step 6: Get VVL records from Map (No DB call)
            List<MerchantVvlRule> vvlRules =
                    vvlRulesMap.getOrDefault(
                            getVvlKey(orderCurrencyCode, pmCode),
                            Collections.emptyList()
                    );

            if (CollectionUtils.isEmpty(vvlRules)) {

                // Step 7: Prepare default DTO
                MerchantVvlRuleDto defaultDto =
                        merchantVvlRuleMapper.toDefaultDto(
                                mId,
                                orderCurrencyCode,
                                pmCode
                        );

                String defaultKey =
                        "DEFAULT_" + orderCurrencyCode + "_" + pmCode;

                response.putIfAbsent(defaultKey, defaultDto);

                continue;
            }

            // Step 8: Process existing VVL records
            // Move your existing ELSE block logic here.
            // Keep your existing DTO mapping and response key logic.
        }
    }

    return new ArrayList<>(response.values());
}

private String getVvlKey(String currencyCode, String pmCode) {
    return currencyCode + "_" + pmCode;
}
