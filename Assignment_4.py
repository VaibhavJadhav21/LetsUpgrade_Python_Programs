public List<MerchantVvlRuleDto> getMerchantVvlRuleInfo(String mId) {

    logger.info("Fetching Merchant VVL details for merchantId: {}", mId);

    List<MerchantVvlRuleDto> result = new ArrayList<>();

    /*
     * Step 1:
     * Get merchant information using mId.
     *
     * We need AGGREGATOR_CODE because
     * MERCHANT_CURRENCY_COMBINATION_MAPPING contains
     * AGGREGATOR_CODE, not MERCHANT_ID.
     */
    MerchantInfoDto merchantInfo = getMerchantInfo(mId);

    if (merchantInfo == null || merchantInfo.getAggregatorCode() == null) {
        logger.warn("Aggregator code not found for merchantId: {}", mId);
        return result;
    }

    String aggregatorCode = merchantInfo.getAggregatorCode();

    logger.info(
            "Aggregator code {} found for merchantId {}",
            aggregatorCode,
            mId
    );

    /*
     * Step 2:
     * Get currency combination + paymode mapping.
     *
     * Table:
     * MERCHANT_CURRENCY_COMBINATION_MAPPING
     *
     * AGGREGATOR_CODE
     * CURRENCY_COMB_CODE
     * PAYMODE_CODE
     */
    List<MerchantCurrencyCombinationMapping> mappings =
            merchantCurrencyCombinationMappingRepository
                    .findByAggregatorCode(aggregatorCode);

    if (mappings == null || mappings.isEmpty()) {
        logger.info(
                "No currency/paymode mapping found for aggregatorCode: {}",
                aggregatorCode
        );
        return result;
    }

    /*
     * Step 3:
     * We need UNIQUE:
     *
     * ORDER_CURRENCY_CODE + PAYMODE_CODE
     *
     * because multiple currency combinations can have
     * same order currency.
     *
     * Example:
     *
     * INR-INR -> CC
     * INR-USD -> CC
     *
     * Both give:
     *
     * INR + CC
     *
     * So return only one.
     */
    Set<String> processedCombination = new HashSet<>();

    /*
     * Step 4:
     * Process every mapping.
     */
    for (MerchantCurrencyCombinationMapping mapping : mappings) {

        String currencyCombCode = mapping.getCurrencyCombCode();
        String paymodeCode = mapping.getPaymodeCode();

        if (currencyCombCode == null || paymodeCode == null) {
            continue;
        }

        /*
         * Step 5:
         * Get ORDER_CURRENCY_CODE from
         * CURRENCY_COMBINATION_MASTER
         */
        Optional<CurrencyCombinationMaster> masterOptional =
                currencyCombinationMasterRepository
                        .findByCurrencyCombCode(currencyCombCode);

        if (masterOptional.isEmpty()) {
            logger.warn(
                    "Currency combination not found: {}",
                    currencyCombCode
            );
            continue;
        }

        CurrencyCombinationMaster master =
                masterOptional.get();

        String orderCurrencyCode =
                master.getOrderCurrencyCode();

        if (orderCurrencyCode == null) {
            continue;
        }

        /*
         * Step 6:
         * Create unique key.
         *
         * Example:
         * INR + CC = INR|CC
         * USD + CC = USD|CC
         * USD + UPI = USD|UPI
         */
        String uniqueKey =
                orderCurrencyCode + "|" + paymodeCode;

        /*
         * If already processed, don't add duplicate DTO.
         */
        if (!processedCombination.add(uniqueKey)) {
            logger.debug(
                    "Skipping duplicate combination: {}",
                    uniqueKey
            );
            continue;
        }

        /*
         * Step 7:
         * Check VVL table.
         *
         * VVL table contains:
         *
         * MERCHANT_ID
         * ORDER_CURRENCY_CODE
         * PAYMODE_CODE
         */
        Optional<MerchantVvlRule> vvlRuleOptional =
                merchantVvlRuleRepository
                        .findByMerchantIdAndOrderCurrencyCodeAndPaymodeCode(
                                mId,
                                orderCurrencyCode,
                                paymodeCode
                        );

        /*
         * Step 8:
         * If VVL data exists -> return actual VVL data.
         */
        if (vvlRuleOptional.isPresent()) {

            MerchantVvlRule vvlRule =
                    vvlRuleOptional.get();

            logger.info(
                    "VVL data found for merchantId={}, currency={}, paymode={}",
                    mId,
                    orderCurrencyCode,
                    paymodeCode
            );

            result.add(
                    merchantVvlRuleMapper.toDto(vvlRule)
            );

        } else {

            /*
             * Step 9:
             * VVL data doesn't exist.
             *
             * Create default DTO using:
             * merchantId
             * orderCurrency
             * paymode
             */
            logger.info(
                    "VVL data not found. Creating default DTO for merchantId={}, currency={}, paymode={}",
                    mId,
                    orderCurrencyCode,
                    paymodeCode
            );

            MerchantVvlRuleDto defaultDto =
                    createDefaultVvlDto(
                            mId,
                            orderCurrencyCode,
                            paymodeCode
                    );

            result.add(defaultDto);
        }
    }

    logger.info(
            "Merchant VVL details fetched successfully. Total records: {}",
            result.size()
    );

    return result;
}
