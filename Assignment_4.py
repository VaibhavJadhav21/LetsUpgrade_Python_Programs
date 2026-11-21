@Mapping(target = "version", ignore = true)
@Mapping(target = "recordStatus", constant = "1")
@Mapping(target = "aggregatorCode", constant = "SBI_EPAY")
@Mapping(target = "mid", source = "mid")
MerchantRfc mapRfcDtoToEntity(
        MerchantRfcRequestDto merchantRfcDto,
        String mid);

default List<MerchantRfc> mapRfcDtoListToEntityList(
        List<MerchantRfcRequestDto> merchantRfcDto,
        String mid) {

    return merchantRfcDto.stream()
            .map(dto -> mapRfcDtoToEntity(dto, mid))
            .toList();
}
