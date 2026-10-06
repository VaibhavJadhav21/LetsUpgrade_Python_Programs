@Entity
@Table(name = "MERCHANT_CURRENCY_COMBINATION_MAPPING")
public class MerchantCurrencyCombinationMapping {

    @Id
    @Column(name = "ID")
    private String id;

    @Column(name = "AGGREGATOR_CODE")
    private String aggregatorCode;

    @Column(name = "CURRENCY_COMB_CODE")
    private String currencyCombCode;

    @Column(name = "PAYMODE_CODE")
    private String paymodeCode;

    // getters and setters
}




@Entity
@Table(name = "CURRENCY_COMBINATION_MASTER")
public class CurrencyCombinationMaster {

    @Id
    private String currencyCombCode;

    @Column(name = "ORDER_CURRENCY_CODE")
    private String orderCurrencyCode;

    @Column(name = "PAYMENT_CURRENCY_CODE")
    private String paymentCurrencyCode;

    // getters and setters
}


@Entity
@Table(name = "MERCHANT_PAYMODE_MAPPING")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class MerchantPaymodeMapping {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ID")
    private Long id;

    @Column(name = "MERCHANT_ID")
    private String merchantId;

    @Column(name = "CURRENCY_COMB_CODE")
    private String currencyCombCode;

    @Column(name = "PAYMODE_CODE")
    private String paymodeCode;

    @Column(name = "CREATED_AT")
    private LocalDateTime createdAt;

    @Column(name = "UPDATED_AT")
    private LocalDateTime updatedAt;

    @Column(name = "CREATED_BY")
    private String createdBy;

    @Column(name = "UPDATED_BY")
    private String updatedBy;
}




@Repository
public interface MerchantPaymodeMappingRepository
        extends JpaRepository<MerchantPaymodeMapping, Long> {

    List<MerchantPaymodeMapping> findByMerchantId(String merchantId);

    List<MerchantPaymodeMapping> findByMerchantIdAndCurrencyCombCode(
            String merchantId,
            String currencyCombCode);
}




@Repository
public interface CurrencyCombinationMasterRepository
        extends JpaRepository<CurrencyCombinationMaster, String> {

    Optional<CurrencyCombinationMaster>
    findByCurrencyCombCode(String currencyCombCode);
}



@Repository
public interface MerchantCurrencyCombinationMappingRepository
        extends JpaRepository<MerchantCurrencyCombinationMapping, String> {

    List<MerchantCurrencyCombinationMapping>
    findByAggregatorCode(String aggregatorCode);
}





