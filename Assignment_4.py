@Query("""
    SELECT DISTINCT c.orderCurrencyCode
    FROM MerchantCurrencyCombinationMapping m
    JOIN CurrencyCombinationMaster c
      ON c.currencyCombCode = m.currencyCombCode
    WHERE m.merchantId = :merchantId
      AND m.authStatus = 'Y'
      AND c.isActive = 'Y'
""")
List<String> findUniqueOrderCurrencies(
        @Param("merchantId") String merchantId);



public RfcFetchResponse fetchRfc(String merchantId) {

    List<String> currencies =
            mappingRepository.findUniqueOrderCurrencies(merchantId);

    List<RfcResponse> response = new ArrayList<>();

    for (String currency : currencies) {

        Optional<MerchantRfcRuleConfig> config =
                rfcRepository
                    .findByMerchantIdAndOrderCurrencyCodeAndAuthStatus(
                            merchantId,
                            currency,
                            "Y");

        if (config.isPresent()) {
            response.add(mapToResponse(config.get()));
        } else {
            response.add(getDefaultRfc(currency));
        }
    }

    return RfcFetchResponse.builder()
            .merchantId(merchantId)
            .rfc(response)
            .build();
}

