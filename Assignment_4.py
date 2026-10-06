// 5. Get paymodes from MERCHANT_PAYMODE_MAPPING
List<MerchantPaymodeMapping> paymodeMappings =
        merchantPaymodeMappingRepository
                .findByMerchantIdAndCurrencyCombCode(
                        mId,
                        currencyCombCode
                );

if (CollectionUtils.isEmpty(paymodeMappings)) {
    continue;
}

// 6. Process unique paymodes
Set<String> uniquePaymodes = paymodeMappings.stream()
        .map(MerchantPaymodeMapping::getPaymodeCode)
        .filter(Objects::nonNull)
        .collect(Collectors.toCollection(LinkedHashSet::new));

for (String paymodeCode : uniquePaymodes) {

    String uniqueKey =
            orderCurrency + "|" + paymodeCode;

    if (!processedCombinations.add(uniqueKey)) {
        continue;
    }

    // VVL check
    Optional<MerchantVvlRule> vvlOptional =
            merchantVvlRuleRepository
                    .findByMerchantIdAndOrderCurrencyCodeAndPaymodeCode(
                            mId,
                            orderCurrency,
                            paymodeCode
                    );

    if (vvlOptional.isPresent()) {

        result.add(
                merchantVvlRuleMapper.toDto(
                        vvlOptional.get()
                )
        );

    } else {

        result.add(
                createDefaultVvlDto(
                        mId,
                        orderCurrency,
                        paymodeCode
                )
        );
    }
}
