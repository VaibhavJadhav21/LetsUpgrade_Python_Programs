package com.epay.admin.portal.dao;

import com.epay.admin.portal.dto.admin.MerchantInfoDto;
import com.epay.admin.portal.dto.admin.MerchantRfcDto;
import com.epay.admin.portal.dto.admin.RiskManagementDto;
import com.epay.admin.portal.entity.admin.MerchantInfo;
import com.epay.admin.portal.entity.admin.MerchantRfc;
import com.epay.admin.portal.exception.AdminPortalException;
import com.epay.admin.portal.exception.ErrorConstants;
import com.epay.admin.portal.mapper.admin.MerchantInfoMapper;
import com.epay.admin.portal.mapper.admin.MerchantRfcMapper;
import com.epay.admin.portal.repository.admin.MerchantInfoRepository;
import com.epay.admin.portal.repository.admin.MerchantRfcRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.text.MessageFormat;
import java.util.List;

@Service
public class RiskManagementDao {

    private static final Logger logger = LoggerFactory.getLogger(RiskManagementDao.class);

    private final MerchantInfoRepository merchantInfoRepository;
    private final MerchantRfcRepository merchantRfcRepository;
    private final MerchantInfoMapper merchantInfoMapper;
    private final MerchantRfcMapper merchantRfcMapper;

    public RiskManagementDao(MerchantInfoRepository merchantInfoRepository,
                               MerchantRfcRepository merchantRfcRepository,
                               MerchantInfoMapper merchantInfoMapper,
                               MerchantRfcMapper merchantRfcMapper) {
        this.merchantInfoRepository = merchantInfoRepository;
        this.merchantRfcRepository = merchantRfcRepository;
        this.merchantInfoMapper = merchantInfoMapper;
        this.merchantRfcMapper = merchantRfcMapper;
    }

    @Transactional
    public MerchantInfoDto updateMerchantInfo(String mId, RiskManagementDto riskManagementDto) {
        MerchantInfo existingMerchantInfo = merchantInfoRepository.findById(mId)
                .orElseThrow(() -> new AdminPortalException(
                        ErrorConstants.NOT_FOUND_ERROR_CODE,
                        MessageFormat.format("Merchant Info not found for mID: {0}", mId)
                ));

        if (riskManagementDto.getMerchantInfoDto() != null) {
            merchantInfoMapper.mapDtoToEntityForUpdate(
                    riskManagementDto.getMerchantInfoDto(), 
                    existingMerchantInfo
            );
        }

        MerchantInfo savedMerchantInfo = merchantInfoRepository.save(existingMerchantInfo);
        logger.info("MerchantInfo entity saved successfully. mID: {}", mId);

        return merchantInfoMapper.entityToMerchantInfoDTO(savedMerchantInfo);
    }

    @Transactional
    public List<MerchantRfcDto> updateMerchantRfcInfo(String mId, RiskManagementDto riskManagementDto) {
        List<MerchantRfc> existingRfcList = merchantRfcRepository.findByMerchantId(mId);

        if (existingRfcList.isEmpty()) {
            logger.error("Database MerchantRfc list is empty for mID: {}", mId);
            throw new AdminPortalException(
                    ErrorConstants.VOLUME_ERROR_CODE, 
                    ErrorConstants.VOLUME_ERROR_MESSAGE
            );
        }

        List<MerchantRfcDto> rfcDtoList = riskManagementDto.getMerchantRfcDto();
        if (rfcDtoList == null || rfcDtoList.isEmpty()) {
            return merchantRfcMapper.mapEntityToResponse(existingRfcList);
        }

        List<MerchantRfc> entitiesToSave = merchantRfcMapper.mapDtoListToEntityList(rfcDtoList);
        entitiesToSave.forEach(entity -> entity.setMerchantId(mId));

        List<MerchantRfc> savedRfcList = merchantRfcRepository.saveAll(entitiesToSave);
        logger.info("MerchantRfc entities saved successfully. mID: {}", mId);

        return merchantRfcMapper.mapEntityToResponse(savedRfcList);
    }
}
