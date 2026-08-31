package com.epay.reporting.dao;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.epay.reporting.dto.ReportHeaderConfigDto;
import com.epay.reporting.dto.ReportManagementDto;
import com.epay.reporting.entity.ReportHeaderConfig;
import com.epay.reporting.mapper.ReportHeaderConfigMapper;
import com.epay.reporting.repository.ReportHeaderConfigRepository;

@ExtendWith(MockitoExtension.class)
class ReportDaoTest {

    @InjectMocks
    private ReportDao reportDao;

    @Mock
    private ReportHeaderConfigRepository reportHeaderConfigRepository;

    @Mock
    private ReportHeaderConfigMapper reportHeaderConfigMapper;

    @Test
    void getReportHeaderConfig_shouldReturnReportHeaderConfig() {

        // Given
        ReportManagementDto reportManagementDto =
                mock(ReportManagementDto.class);

        ReportHeaderConfig reportConfig =
                mock(ReportHeaderConfig.class);

        ReportHeaderConfigDto expectedDto =
                mock(ReportHeaderConfigDto.class);

        when(reportManagementDto.getReportTo())
                .thenReturn(ReportType.TRANSACTION);

        when(reportManagementDto.getMid())
                .thenReturn("123456");

        when(reportHeaderConfigRepository.findFirstByMid(
                reportManagementDto.getReportTo().toString(),
                reportManagementDto.getMid()))
                .thenReturn(reportConfig);

        when(reportHeaderConfigMapper.mapEntityToDto(reportConfig))
                .thenReturn(expectedDto);

        // When
        ReportHeaderConfigDto actualDto =
                reportDao.getReportHeaderConfig(reportManagementDto);

        // Then
        assertNotNull(actualDto);
        assertEquals(expectedDto, actualDto);

        verify(reportHeaderConfigRepository, times(1))
                .findFirstByMid(
                        reportManagementDto.getReportTo().toString(),
                        reportManagementDto.getMid());

        verify(reportHeaderConfigMapper, times(1))
                .mapEntityToDto(reportConfig);
    }
}
