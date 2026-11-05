Set<String> processedPayModes = new HashSet<>();

for (UniqueCurrency currencyCombination : currencyCombinations) {

    String orderCurrencyCode = currencyCombination.getOrderCurrencyCode();
    String currencyCombCode = currencyCombination.getCurrencyCombCode();

    List<PayModeCode> payModes =
            merchantPaymodeMappingRepository.findingPayModeForMerchant(
                    mId, orderCurrencyCode, currencyCombCode);

    for (PayModeCode paymode : payModes) {

        String pmCode = paymode.getPaymodeCode();

        // Avoid processing the same currency + paymode combination again
        String uniqueKey = orderCurrencyCode + "_" + currencyCombCode + "_" + pmCode;

        if (!processedPayModes.add(uniqueKey)) {
            continue;
        }

        List<MerchantVvlRule> vvlRule =
                merchantVvlRuleRepository.findByMerchantIdAndPaymodeCode(mId, pmCode);

        if (ObjectUtils.isEmpty(vvlRule)) {

            response.add(
                    merchantVvlRuleMapper.toDefaultDto(mId, orderCurrencyCode, pmCode));

        } else {

            // Remove duplicate records using their database ID
            Map<UUID, MerchantVvlRule> uniqueRules = vvlRule.stream()
                    .collect(Collectors.toMap(
                            MerchantVvlRule::getId,
                            Function.identity(),
                            (existing, duplicate) -> existing,
                            LinkedHashMap::new
                    ));

            uniqueRules.values().forEach(rule ->
                    response.add(merchantVvlRuleMapper.toDto(rule)));
        }
    }
}

return response;
