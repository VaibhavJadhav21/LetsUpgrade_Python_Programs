
@Test
void generateReport_ShouldGenerateTransactionReportSuccessfullys() throws Exception {

    // 1. Header Config Data Setup
    ReportHeaderConfigDto reportHeaderConfigDto = new ReportHeaderConfigDto();
    reportHeaderConfigDto.setHeaderJson("{\"Transaction Request Date And Time\": 0}");

    reportManagementDto.setReport(TRANSACTION);

    // 2. Mock DAO Calls
    when(reportManagementDao.updateReportStatus(
            reportManagementId,
            ReportStatus.GENERATION_STARTED))
    .thenReturn(reportManagementDto);

    // HA CALL MISSING HOTA:
    when(reportDao.getReportHeaderConfig(reportManagementDto))
            .thenReturn(reportHeaderConfigDto);

    // 3. Dummy Transaction Data
    List<List<Object>> dummyTransactionList = List.of(
        List.of("dummyValue1", "dummyValue2")
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

    verify(reportDao, times(1)).getReportHeaderConfig(reportManagementDto);
    verify(reportDao, times(1)).getTransaction(reportManagementDto);
}












@Test
void generateReport_ShouldGenerateTransactionReportSuccessfully() {

    // 1. Arrange ReportHeaderConigDto (NullPointer avoid karaynsathi)
    ReportHeaderConfigDto reportHeaderConfigDto = new ReportHeaderConfigDto();
    // Jar HeaderJson string require asel tar:
    reportHeaderConfigDto.setHeaderJson("{}"); 
    
    reportManagementDto.setReport(TRANSACTION);
    reportManagementDto.setReportHeaderConfigDto(reportHeaderConfigDto); // Setup Header Config

    when(reportManagementDao.updateReportStatus(
            reportManagementId,
            ReportStatus.GENERATION_STARTED))
    .thenReturn(reportManagementDto);

    // 2. Dummy transaction data setup (26+ elements or headers as per your service logic)
    List<List<Object>> dummyTransactionList = List.of(
        List.of("val1", "val2", "val3")
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






@Test
void generateReport_ShouldGenerateTransactionReportSuccessfully() {

    // 1. Arrange ReportHeaderConfigDto (NullPointer avoid karaynsathi)
    ReportHeaderConfigDto reportHeaderConfigDto = new ReportHeaderConfigDto();
    // Jar HeaderJson string require asel tar:
    reportHeaderConfigDto.setHeaderJson("{}"); 
    
    reportManagementDto.setReport(TRANSACTION);
    reportManagementDto.setReportHeaderConfigDto(reportHeaderConfigDto); // Setup Header Config

    when(reportManagementDao.updateReportStatus(
            reportManagementId,
            ReportStatus.GENERATION_STARTED))
    .thenReturn(reportManagementDto);

    // 2. Dummy transaction data setup (26+ elements or headers as per your service logic)
    List<List<Object>> dummyTransactionList = List.of(
        List.of("val1", "val2", "val3")
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


// Option 1: Map.ofEntries() vaprun (jar setHeaderJson Map ghet asel)
Map<String, Integer> headerMap = Map.ofEntries(
    Map.entry("Transaction Request Date And Time", 0),
    Map.entry("Transaction Success Date And Time", 1),
    Map.entry("Merchant Order No", 2),
    Map.entry("SBIEPAY ORDER ID", 3),
    Map.entry("Cust Id", 4),
    Map.entry("ATRN", 5),
    Map.entry("Gateway Trace Number", 6),
    Map.entry("Pay Mode Code", 7),
    Map.entry("Gateway Name", 8),
    Map.entry("Pay Proc", 9),
    Map.entry("Transaction Currency", 10),
    Map.entry("Merchant Order Amount", 11),
    Map.entry("Gateway Posting Amount", 12),
    Map.entry("Commission", 13),
    Map.entry("GST", 14),
    Map.entry("Order Status", 15),
    Map.entry("Transaction Status", 16),
    Map.entry("Settlement Status", 17),
    Map.entry("Refund Status", 18),
    Map.entry("Chargeback Status", 19),
    Map.entry("Amount Refunded", 20),
    Map.entry("Amount Chargeback", 21),
    Map.entry("CIN Number", 22),
    Map.entry("Merchant Other Details", 23),
    Map.entry("Settlement Date", 24),
    Map.entry("LFD", 25)
);

// Jar setHeaderJson Map String ghet asel, tar ObjectMapper ne convert kara:
String headerJson = new com.fasterxml.jackson.databind.ObjectMapper().writeValueAsString(headerMap);
reportHeaderConfigDto.setHeaderJson(headerJson);


}
