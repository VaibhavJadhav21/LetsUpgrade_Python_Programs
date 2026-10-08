package com.yourpackage.dao;

import com.yourpackage.dto.MerchantRfcDto;
import com.yourpackage.dto.RiskManagementDto;
import com.yourpackage.entity.MerchantRfc;
import com.yourpackage.exception.AdminPortalException;
import com.yourpackage.mapper.MerchantRfcMapper;
import com.yourpackage.repository.MerchantRfcRepository;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.function.Function;
import java.util.stream.Collectors;

import static com.yourpackage.constants.ErrorConstants.NOT_FOUND_ERROR_CODE;
import static com.yourpackage.constants.ErrorConstants.NOT_FOUND_ERROR_MESSAGE;

@Component
@RequiredArgsConstructor
public class RiskManagementDao {

    private static final Logger logger =
            LoggerFactory.getLogger(RiskManagementDao.class);

    private final MerchantRfcRepository merchantRfcRepository;
    private final MerchantRfcMapper merchantRfcMapper;


    public List<MerchantRfcDto> updateMerchantRfcInfo(
            String mId,
            RiskManagementDto riskManagementDto) {

        logger.info("Updating merchant RFC info for mID: {}", mId);

        List<MerchantRfcDto> requestList =
                riskManagementDto.getMerchantRfcDto();

        if (CollectionUtils.isEmpty(requestList)) {
            return List.of();
        }

        /*
         * Fetch all existing records for this MID.
         * One MID can have multiple MerchantRfc records.
         */
        List<MerchantRfc> existingRecords =
                merchantRfcRepository.findByMerchantId(mId);

        /*
         * Create Map<UUID, MerchantRfc> for quick lookup.
         */
        Map<UUID, MerchantRfc> existingById =
                existingRecords.stream()
                        .collect(Collectors.toMap(
                                MerchantRfc::getId,
                                Function.identity()
                        ));

        List<MerchantRfc> recordsToSave = new ArrayList<>();

        for (MerchantRfcDto requestDto : requestList) {

            MerchantRfc merchantRfc;

            /*
             * ID present and record exists
             * --------------------------------
             * UPDATE existing record
             */
            if (requestDto.getId() != null
                    && existingById.containsKey(requestDto.getId())) {

                merchantRfc = existingById.get(requestDto.getId());

                merchantRfcMapper.updateEntityFromRequest(
                        requestDto,
                        merchantRfc
                );

                logger.info(
                        "Merchant RFC record updated. mID: {}, id: {}",
                        mId,
                        requestDto.getId()
                );

            } else {

                /*
                 * ID is null OR ID does not exist
                 * --------------------------------
                 * CREATE new record
                 */
                merchantRfc =
                        merchantRfcMapper.mapDtoListToEntityList(requestDto);

                /*
                 * Make sure new record is associated
                 * with the requested merchant.
                 */
                merchantRfc.setMerchantId(mId);

                logger.info(
                        "New Merchant RFC record created. mID: {}",
                        mId
                );
            }

            recordsToSave.add(merchantRfc);
        }

        /*
         * Save all INSERT + UPDATE records in one call.
         */
        List<MerchantRfc> savedRecords =
                merchantRfcRepository.saveAll(recordsToSave);

        logger.info(
                "Merchant RFC info updated successfully. mID: {}",
                mId
        );

        return merchantRfcMapper.mapListEntityToResponse(savedRecords);
    }
}
