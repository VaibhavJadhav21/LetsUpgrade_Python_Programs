public List<MerchantRfcDto> getMerchantRfcInfo(String mId) {

    Logger.info("Fetching MerchantRfcDetail. Calling database.");

    List<String> currencies =
            merchantCurrencyCombinationMappingRepository.findUniqueOrderCurrencies(mId);

    List<MerchantRfcDto> response = new ArrayList<>();

    for (String currency : currencies) {

        List<MerchantRfc> config =
                merchantRfcRepository.findByMerchantIdAndOrderCurrencyCode(mId, currency);

        if (config != null && !config.isEmpty()) {

            for (MerchantRfc rfcData : config) {
                response.add(merchantRfcMapper.toDto(rfcData));
            }
        }
    }

    return response;
}
