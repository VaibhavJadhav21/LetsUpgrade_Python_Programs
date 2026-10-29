@Service
@RequiredArgsConstructor
public class PricingService {

    private final PricingRepository pricingRepository;

    private final PricingEntityMapper pricingEntityMapper;

    public AdminPortalResponse<PricingDto> getPricingByMerchantId(
            String mid) {

        List<PricingProjection> result =
                pricingRepository.findPricingByMerchantId(mid);

        if (result == null || result.isEmpty()) {
            throw new AdminPortalException(
                    NOT_FOUND_ERROR_CODE,
                    MessageFormat.format(
                            NOT_FOUND_ERROR_MESSAGE,
                            mid
                    )
            );
        }

        List<PricingEntity> items = result.stream()
                .map(pricingEntityMapper::toItem)
                .toList();

        return pricingEntityMapper.toResponse(mid, items);
    }
}





@Mapper(componentModel = "spring")
public interface PricingEntityMapper {

    @Mapping(target = "merchantId", source = "merchantId")
    @Mapping(target = "paygatewayId", source = "paygatewayId")
    @Mapping(target = "aggregatorCode", source = "aggregatorCode")
    @Mapping(target = "currencyCode", source = "currencyCode")
    @Mapping(target = "currencyName", source = "currencyName")
    @Mapping(target = "paymodeCode", source = "paymodeCode")
    @Mapping(target = "meCode", source = "meCode")
    @Mapping(target = "pgMid", source = "pgMid")
    @Mapping(target = "pgTid", source = "pgTid")
    @Mapping(target = "authStatus", source = "authStatus")
    @Mapping(target = "isActive", source = "isActive")
    @Mapping(target = "isTpActive", source = "isTpActive")
    PricingEntity toItem(PricingProjection projection);

    // Tujhya existing PricingDto response structure nusar
    // hi method configure kar.
    AdminPortalResponse<PricingDto> toResponse(
            String mid,
            List<PricingEntity> items);
}







@RestController
@RequestMapping("/api/pricing")
@RequiredArgsConstructor
public class PricingController {

    private final PricingService pricingService;

    @GetMapping("/{mid}")
    public ResponseEntity<AdminPortalResponse<PricingDto>>
            getPricingByMerchantId(
                    @PathVariable String mid) {

        return ResponseEntity.ok(
                pricingService.getPricingByMerchantId(mid)
        );
    }
}







@Repository
public interface PricingRepository
        extends JpaRepository<MerchantPaygatewayMapping, Long> {

    @Query(value = """
        SELECT
            M.MERCHANT_ID       AS merchantId,
            M.PAYGATEWAY_ID     AS paygatewayId,
            PG.AGGREGATOR_CODE  AS aggregatorCode,
            M.CURRENCY_CODE     AS currencyCode,
            CM.CURRENCY_NAME    AS currencyName,
            M.PAYMODE_CODE      AS paymodeCode,
            M.ME_CODE           AS meCode,
            M.PG_MID            AS pgMid,
            M.PG_TID            AS pgTid,
            M.AUTH_STATUS       AS authStatus,
            M.IS_ACTIVE         AS isActive,
            M.IS_TP_ACTIVE      AS isTpActive
        FROM MERCHANT_PAYGATEWAY_MAPPING M
        INNER JOIN PAYGATEWAY_MASTER PG
            ON PG.ID = M.PAYGATEWAY_ID
        LEFT JOIN CURRENCY_MASTER CM
            ON CM.CURRENCY_CODE = M.CURRENCY_CODE
        WHERE M.MERCHANT_ID = :mid
        """, nativeQuery = true)
    List<PricingProjection> findPricingByMerchantId(
            @Param("mid") String mid);
}





public interface PricingProjection {

    String getMerchantId();

    Long getPaygatewayId();

    String getAggregatorCode();

    String getCurrencyCode();

    String getCurrencyName();

    String getPaymodeCode();

    String getMeCode();

    String getPgMid();

    String getPgTid();

    String getAuthStatus();

    String getIsActive();

    String getIsTpActive();
}
