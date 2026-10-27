@Service
@RequiredArgsConstructor
public class PricingEntityServiceImpl
        implements PricingEntityService {

    private final MerchantPaygatewayMappingRepository mappingRepository;
    private final PaygatewayMasterRepository paygatewayMasterRepository;
    private final ChannelPricingRepository channelPricingRepository;
    private final DefaultChannelPricingRepository defaultChannelPricingRepository;
    private final PricingEntityMapper pricingEntityMapper;

    @Override
    public PricingEntityResponse getPricingEntity(String mid) {

        List<MerchantPaygatewayMapping> mappings =
                mappingRepository.findByMerchantId(mid);

        if (mappings.isEmpty()) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND,
                    "Merchant mapping not found for MID: " + mid
            );
        }

        List<PricingEntityItem> items = new ArrayList<>();

        for (MerchantPaygatewayMapping mapping : mappings) {

            // Fetch matching payment gateway
            PaygatewayMaster gateway =
                    paygatewayMasterRepository
                            .findById(mapping.getPaygatewayId())
                            .orElse(null);

            if (gateway == null) {
                continue;
            }

            // Fetch merchant-specific channel pricing
            List<ChannelPricing> channelPricing =
                    channelPricingRepository
                            .findByMerchantIdAndPaygatewayId(
                                    mid,
                                    mapping.getPaygatewayId()
                            );

            PricingEntityItem item;

            if (channelPricing != null && !channelPricing.isEmpty()) {

                // Merchant-specific pricing available
                item = pricingEntityMapper.toItem(
                        mapping,
                        gateway,
                        channelPricing
                );

            } else {

                // Fetch default channel pricing
                List<DefaultChannelPricing> defaultPricing =
                        defaultChannelPricingRepository
                                .findByPaygatewayId(
                                        mapping.getPaygatewayId()
                                );

                item = pricingEntityMapper.toDefaultItem(
                        mapping,
                        gateway,
                        defaultPricing
                );
            }

            items.add(item);
        }

        return pricingEntityMapper.toResponse(mid, items);
    }
}
