package com.epay.reporting.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import java.util.Collections;
import java.util.UUID;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.epay.reporting.dao.ReportDao;
import com.epay.reporting.dao.ReportManagementDao;
import com.epay.reporting.dto.ReportManagementDto;
import com.epay.reporting.enums.ReportStatus;
import com.epay.reporting.enums.ReportType;

@ExtendWith(MockitoExtension.class)
class ReportServiceTest {

    @InjectMocks
    private ReportService reportService;

    @Mock
    private ReportManagementDao reportManagementDao;

    @Mock
    private ReportDao reportDao;

    /*
     * Add other @Mock dependencies of ReportService here
     * if they are present in your actual constructor.
     *
     * Example:
     *
     * @Mock
     * private ScrollFileService scrollFileService;
     *
     * @Mock
     * private ReportHeaderService reportHeaderService;
     */

    private UUID reportManagementId;
    private ReportManagementDto reportManagementDto;

    @BeforeEach
    void setUp() {
        reportManagementId = UUID.randomUUID();

        reportManagementDto = new ReportManagementDto();
        reportManagementDto.setId(reportManagementId);
    }

    // =========================================================
    // TRANSACTION REPORT
    // =========================================================

    @Test
    void generateReport_ShouldGenerateTransactionReportSuccessfully() {

        // Arrange
        reportManagementDto.setReport(ReportType.TRANSACTION);

        when(reportManagementDao.updateReportStatus(
                reportManagementId,
                ReportStatus.GENERATION_STARTED))
                .thenReturn(reportManagementDto);

        when(reportDao.getTransactionReportData(reportManagementDto))
                .thenReturn(Collections.emptyList());

        // Act
        reportService.generateReport(reportManagementId);

        // Assert
        verify(reportManagementDao, times(1))
                .updateReportStatus(
                        reportManagementId,
                        ReportStatus.GENERATION_STARTED);

        verify(reportDao, times(1))
                .getTransactionReportData(reportManagementDto);
    }

    // =========================================================
    // SETTLEMENT REPORT
    // =========================================================

    @Test
    void generateReport_ShouldGenerateSettlementReportSuccessfully() {

        // Arrange
        reportManagementDto.setReport(ReportType.SETTLEMENT);

        when(reportManagementDao.updateReportStatus(
                reportManagementId,
                ReportStatus.GENERATION_STARTED))
                .thenReturn(reportManagementDto);

        when(reportDao.getSettlementReportData(reportManagementDto))
                .thenReturn(Collections.emptyList());

        // Act
        reportService.generateReport(reportManagementId);

        // Assert
        verify(reportManagementDao, times(1))
                .updateReportStatus(
                        reportManagementId,
                        ReportStatus.GENERATION_STARTED);

        verify(reportDao, times(1))
                .getSettlementReportData(reportManagementDto);
    }



@Test
void generateReport_ShouldGenerateTransactionReportSuccessfully() {

    // Arrange
    reportManagementDto.setReport(TRANSACTION);

    when(reportManagementDao.updateReportStatus(
            reportManagementId,
            ReportStatus.GENERATION_STARTED))
    .thenReturn(reportManagementDto);

    // List<List<Object>> dummy data context sathi mock kela ahe
    List<List<Object>> dummyTransactionList = List.of(
        List.of("dummyField1", "dummyField2", "dummyField3")
    );

    when(reportDao.getTransaction(reportManagementDto))
            .thenReturn(dummyTransactionList);

    // Act
    reportService.generateReport(reportManagementId);

    // Assert
    verify(reportManagementDao, times(1))
            .updateReportStatus(
                    reportManagementId,
                    ReportStatus.GENERATION_STARTED);

    verify(reportDao, times(1)).getTransaction(reportManagementDto);
}

}
