public List<MerchantVvlRuleDto> getMerchantVvlRuleInfo(String mId) {

    logger.info("Fetching VVL details for merchantId: {}", mId);

    List<MerchantVvlRuleDto> result = new ArrayList<>();

    // 1. Fetch currency combinations using MID
    List<MerchantCurrencyCombination> currencyCombinations =
            merchantCurrencyCombinationRepository
                    .findByMerchantId(mId);

    if (CollectionUtils.isEmpty(currencyCombinations)) {
        return result;
    }

    /*
     * Keeps only unique:
     * ORDER_CURRENCY + PAYMODE
     *
     * Example:
     * INR + CC
     * INR + UPI
     * USD + CC
     */
    Set<String> processedCombinations = new HashSet<>();

    // 2. Process merchant currency combinations
    for (MerchantCurrencyCombination combination : currencyCombinations) {

        String currencyCombCode =
                combination.getCurrencyCombCode();

        if (currencyCombCode == null) {
            continue;
        }

        // 3. Find currency combination master
        Optional<CurrencyCombinationMaster> masterOptional =
                currencyCombinationMasterRepository
                        .findByCurrencyCombCode(currencyCombCode);

        if (masterOptional.isEmpty()) {
            continue;
        }

        CurrencyCombinationMaster master =
                masterOptional.get();

        String orderCurrency =
                master.getOrderCurrencyCode();

        if (orderCurrency == null) {
            continue;
        }

        // 4. Find paymodes for this currency combination
        List<CurrencyCombPaymodeMapping> paymodeMappings =
                currencyCombPaymodeMappingRepository
                        .findByCurrencyCombCode(currencyCombCode);

        if (CollectionUtils.isEmpty(paymodeMappings)) {
            continue;
        }

        // 5. Process unique paymodes
        for (CurrencyCombPaymodeMapping paymodeMapping
                : paymodeMappings) {

            String paymodeCode =
                    paymodeMapping.getPaymodeCode();

            if (paymodeCode == null) {
                continue;
            }

            /*
             * Avoid duplicate:
             *
             * INR-INR + CC
             * INR-USD + CC
             *
             * Both can produce:
             *
             * INR + CC
             */
            String uniqueKey =
                    orderCurrency + "|" + paymodeCode;

            if (!processedCombinations.add(uniqueKey)) {
                continue;
            }

            // 6. Check VVL data using MID
            Optional<MerchantVvlRule> vvlOptional =
                    merchantVvlRuleRepository
                            .findByMerchantIdAndOrderCurrencyCodeAndPaymodeCode(
                                    mId,
                                    orderCurrency,
                                    paymodeCode
                            );

            if (vvlOptional.isPresent()) {

                // VVL data available
                result.add(
                        merchantVvlRuleMapper.toDto(
                                vvlOptional.get()
                        )
                );

            } else {

                // VVL data not available
                // Return default DTO
                result.add(
                        createDefaultVvlDto(
                                mId,
                                orderCurrency,
                                paymodeCode
                        )
                );
            }
        }
    }

    logger.info(
            "VVL details fetched successfully for merchantId={}, count={}",
            mId,
            result.size()
    );

    return result;
}
