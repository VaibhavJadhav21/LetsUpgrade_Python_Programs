public List<MerchantVvlRuleDto> getMerchantVvlRuleInfo(String mId) {

    logger.info("Fetching Merchant VVL details for merchantId: {}", mId);

    List<MerchantVvlRuleDto> response = new ArrayList<>();

    List<UniqueCurrency> currencyCombinations =
            merchantCurrencyCombinationMappingRepository
                    .findUniqueOrderCurrencies(mId);

    for (UniqueCurrency currencyCombination : currencyCombinations) {

        String orderCurrencyCode =
                currencyCombination.getOrderCurrencyCode();

        String currencyCombCode =
                currencyCombination.getCurrencyCombCode();

        // Fetch PayModes for each currency combination
        List<PayModeCode> payModes =
                merchantPaymodeMappingRepository.findingPayModeForMerchant(
                        mId, orderCurrencyCode, currencyCombCode);

        for (PayModeCode paymode : payModes) {

            String pmCode = paymode.getPaymodeCode();

            List<MerchantVvlRule> vvlRules =
                    merchantVvlRuleRepository
                            .findByMerchantIdAndPaymodeCodeAndOrderCurrencyCode(
                                    mId, pmCode, orderCurrencyCode);

            if (CollectionUtils.isEmpty(vvlRules)) {

                // No VVL configuration: return default DTO
                response.add(
                        merchantVvlRuleMapper.toDefaultDto(
                                mId, orderCurrencyCode, pmCode));

            } else {

                // VVL configuration exists: return actual DTOs
                for (MerchantVvlRule vvlRule : vvlRules) {
                    response.add(
                            merchantVvlRuleMapper.toDto(vvlRule));
                }
            }
        }
    }

    return response;
}
