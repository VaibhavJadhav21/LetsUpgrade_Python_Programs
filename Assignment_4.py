@Mapper(componentModel = "spring")
public interface PricingEntityMapper {

    @Mapping(
        target = "pricingEntities",
        source = "items"
    )
    PricingEntityResponse toResponse(
            String mid,
            List<PricingEntityItem> items
    );

    @Mapping(
        target = "paygatewayId",
        source = "mapping.paygatewayId"
    )
    @Mapping(
        target = "aggregatorCode",
        source = "gateway.aggregatorCode"
    )
    @Mapping(
        target = "currencyCode",
        source = "mapping.currencyCode"
    )
    @Mapping(
        target = "paymodeCode",
        source = "mapping.paymodeCode"
    )
    @Mapping(
        target = "meCode",
        source = "mapping.meCode"
    )
    @Mapping(
        target = "pgMid",
        source = "mapping.pgMid"
    )
    @Mapping(
        target = "pgTid",
        source = "mapping.pgTid"
    )
    @Mapping(
        target = "pricingSource",
        constant = "MERCHANT"
    )
    @Mapping(
        target = "pricingDetails",
        source = "pricing"
    )
    PricingEntityItem toItem(
            MerchantPaygatewayMapping mapping,
            PaygatewayMaster gateway,
            List<ChannelPricing> pricing
    );

    @Mapping(
        target = "paygatewayId",
        source = "mapping.paygatewayId"
    )
    @Mapping(
        target = "aggregatorCode",
        source = "gateway.aggregatorCode"
    )
    @Mapping(
        target = "currencyCode",
        source = "mapping.currencyCode"
    )
    @Mapping(
        target = "paymodeCode",
        source = "mapping.paymodeCode"
    )
    @Mapping(
        target = "meCode",
        source = "mapping.meCode"
    )
    @Mapping(
        target = "pgMid",
        source = "mapping.pgMid"
    )
    @Mapping(
        target = "pgTid",
        source = "mapping.pgTid"
    )
    @Mapping(
        target = "pricingSource",
        constant = "DEFAULT"
    )
    @Mapping(
        target = "pricingDetails",
        source = "pricing"
    )
    PricingEntityItem toDefaultItem(
            MerchantPaygatewayMapping mapping,
            PaygatewayMaster gateway,
            List<DefaultChannelPricing> pricing
    );
}
