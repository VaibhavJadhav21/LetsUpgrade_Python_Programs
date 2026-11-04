public List<MerchantRfcDto> getMerchantRfcInfo(String mId) {
    logger.info("msg: fetching MerchantRfcDetail. Calling database."); //[span_1](start_span)[span_1](end_span)
    
    // 1. Saglya unique currencies fetch karne
    List<String> currencies = merchantCurrencyCombinationMappingRepository.findUniqueOrderCurrencies(mId); //[span_2](start_span)[span_2](end_span)
    List<MerchantRfcDto> response = new ArrayList<>(); //[span_3](start_span)[span_3](end_span)
    
    // 2. Pratyek currency sathi loop firvane
    for (String currency : currencies) {
        List<MerchantRfc> config = merchantRfcRepository.findByMerchantIdAndOrderCurrencyCode(mId, currency); //[span_4](start_span)[span_4](end_span)
        
        // 3. Jar database madhe ya currency sathi data nasel, tr default DTO call hovun add hoil
        if (ObjectUtils.isEmpty(config)) {
            response.add(merchantRfcMapper.toDefaultDto(mId, currency));
        } else {
            // 4. Jar table madhe data milala, tar sagglya entries sathi toDto call hoil (multiple entries handle karnyasathi)
            for (MerchantRfc rfcData : config) {
                response.add(merchantRfcMapper.toDto(rfcData));
            }
        }
    }
    
    return response; //[span_5](start_span)[span_5](end_span)
}
