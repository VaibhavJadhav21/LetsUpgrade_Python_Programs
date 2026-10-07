package com.epay.admin.portal.repository;

import com.epay.admin.portal.entity.MerchantVvlRule;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface MerchantVvlRuleRepository
        extends JpaRepository<MerchantVvlRule, UUID> {

    Optional<MerchantVvlRule> findByMerchantIdAndOrderCurrencyCodeAndPaymodeCode(
            String merchantId,
            String orderCurrencyCode,
            String paymodeCode
    );
}







package com.epay.admin.portal.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface MerchantCurrencyCombinationRepository
        extends JpaRepository<MerchantCurrencyCombinationEntity, String> {

    @Query(value = """
        SELECT DISTINCT
               mccm.CURRENCY_COMB_CODE
        FROM MERCHANT_CURRENCY_COMBINATION_MAPPING mccm
        INNER JOIN CURRENCY_COMBINATION_MASTER ccm
            ON ccm.CURRENCY_COMB_CODE = mccm.CURRENCY_COMB_CODE
        WHERE mccm.MERCHANT_ID = :merchantId
        """, nativeQuery = true)
    List<String> findCurrencyCombinationCodesByMerchantId(
            @Param("merchantId") String merchantId
    );
}












package com.epay.admin.portal.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface MerchantPaymodeMappingRepository
        extends JpaRepository<MerchantPaymodeMappingEntity, String> {

    @Query(value = """
        SELECT DISTINCT mp.PAYMODE_CODE
        FROM MERCHANT_PAYMODE_MAPPING mp
        WHERE mp.MERCHANT_ID = :merchantId
        """, nativeQuery = true)
    List<String> findPaymodesByMerchantId(
            @Param("merchantId") String merchantId
    );
}









package com.epay.admin.portal.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface CurrencyCombPaymodeMappingRepository
        extends JpaRepository<CurrencyCombPaymodeMappingEntity, String> {

    @Query(value = """
        SELECT DISTINCT cpm.PAYMODE_CODE
        FROM CURRENCY_COMB_PAYMODE_MAPPING cpm
        WHERE cpm.CURRENCY_COMB_CODE = :currencyCombCode
        """, nativeQuery = true)
    List<String> findPaymodesByCurrencyCombination(
            @Param("currencyCombCode") String currencyCombCode
    );
}




















package com.epay.admin.portal.service;

import com.epay.admin.portal.dto.admin.MerchantVvlRuleDto;
import com.epay.admin.portal.entity.MerchantVvlRule;
import com.epay.admin.portal.mapper.MerchantVvlRuleMapper;
import com.epay.admin.portal.repository.CurrencyCombPaymodeMappingRepository;
import com.epay.admin.portal.repository.MerchantCurrencyCombinationRepository;
import com.epay.admin.portal.repository.MerchantPaymodeMappingRepository;
import com.epay.admin.portal.repository.MerchantVvlRuleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class MerchantVvlRuleService {

    private final MerchantCurrencyCombinationRepository
            merchantCurrencyCombinationRepository;

    private final MerchantPaymodeMappingRepository
            merchantPaymodeMappingRepository;

    private final CurrencyCombPaymodeMappingRepository
            currencyCombPaymodeMappingRepository;

    private final MerchantVvlRuleRepository
            merchantVvlRuleRepository;

    private final MerchantVvlRuleMapper
            merchantVvlRuleMapper;


    public List<MerchantVvlRuleDto> fetchVvlRules(String merchantId) {

        List<MerchantVvlRuleDto> response = new ArrayList<>();

        /*
         * Step 1:
         * Get unique currency combinations mapped to merchant
         */
        List<String> currencyCombinations =
                merchantCurrencyCombinationRepository
                        .findCurrencyCombinationCodesByMerchantId(merchantId);

        if (currencyCombinations == null ||
                currencyCombinations.isEmpty()) {
            return response;
        }


        /*
         * Step 2:
         * Loop each currency combination
         */
        for (String currencyCombination : currencyCombinations) {

            String orderCurrency =
                    getOrderCurrency(currencyCombination);


            /*
             * Step 3:
             * Get paymodes applicable for this
             * currency combination
             */
            List<String> currencyPaymodes =
                    currencyCombPaymodeMappingRepository
                            .findPaymodesByCurrencyCombination(
                                    currencyCombination
                            );


            /*
             * Step 4:
             * Get merchant level paymodes
             */
            List<String> merchantPaymodes =
                    merchantPaymodeMappingRepository
                            .findPaymodesByMerchantId(merchantId);


            /*
             * Step 5:
             * Find intersection of merchant paymodes
             * and currency combination paymodes
             */
            List<String> applicablePaymodes =
                    currencyPaymodes.stream()
                            .filter(merchantPaymodes::contains)
                            .distinct()
                            .toList();


            /*
             * Step 6:
             * Loop each applicable paymode
             */
            for (String paymode : applicablePaymodes) {

                MerchantVvlRule vvlRule =
                        merchantVvlRuleRepository
                                .findByMerchantIdAndOrderCurrencyCodeAndPaymodeCode(
                                        merchantId,
                                        orderCurrency,
                                        paymode
                                )
                                .orElse(null);


                /*
                 * Step 7:
                 * If VVL already defined,
                 * populate response from DB
                 */
                if (vvlRule != null) {

                    response.add(
                            merchantVvlRuleMapper.toDto(vvlRule)
                    );

                } else {

                    /*
                     * Step 8:
                     * If VVL not defined,
                     * populate default values
                     */
                    response.add(
                            buildDefaultVvlRule(
                                    merchantId,
                                    orderCurrency,
                                    paymode
                            )
                    );
                }
            }
        }

        return response;
    }


    private String getOrderCurrency(String currencyCombination) {

        if (currencyCombination == null ||
                currencyCombination.isBlank()) {
            return null;
        }

        /*
         * Example:
         *
         * INR-INR -> INR
         * INR-USD -> INR
         * USD-INR -> USD
         */

        int separatorIndex = currencyCombination.indexOf("-");

        if (separatorIndex > 0) {
            return currencyCombination.substring(
                    0,
                    separatorIndex
            );
        }

        return currencyCombination;
    }


    private MerchantVvlRuleDto buildDefaultVvlRule(
            String merchantId,
            String orderCurrency,
            String paymode
    ) {

        return MerchantVvlRuleDto.builder()
                .id(null)
                .aggregatorId(null)
                .merchantId(merchantId)
                .orderCurrencyCode(orderCurrency)
                .vvlIsActive("N")
                .paymodeCode(paymode)
                .volvelCheckAllowed("N")
                .dailyTxnAmtLimit(BigDecimal.ZERO)
                .weeklyTxnAmtLimit(BigDecimal.ZERO)
                .monthlyTxnAmtLimit(BigDecimal.ZERO)
                .quarterlyTxnAmtLimit(BigDecimal.ZERO)
                .halfYearlyTxnAmtLimit(BigDecimal.ZERO)
                .annualTxnAmtLimit(BigDecimal.ZERO)
                .resetApplicable("N")
                .resetDays(null)
                .authStatus(null)
                .makerComment(null)
                .checkerComment(null)
                .isSubmitted("N")
                .build();
    }
}





















