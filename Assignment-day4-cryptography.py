package com.epay.reporting.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;

import com.epay.reporting.dao.ReportDao;
import com.epay.reporting.dto.ReportHeaderConfigDto;
import com.epay.reporting.dto.ReportManagementDto;
import com.epay.reporting.model.Report;
import com.epay.reporting.model.ReportFile;
import com.epay.reporting.service.FileGeneratorService;

@ExtendWith(MockitoExtension.class)
class ReportServiceTest {

    @InjectMocks
    private ReportService reportService;

    @Mock
    private ReportDao reportDao;

    @Mock
    private FileGeneratorService fileGeneratorService;

    @Mock
    private ReportHeaderConfigDto reportHeaderConfigDto;

    @Mock
    private ReportManagementDto reportManagementDto;

    @Mock
    private ReportFile expectedReportFile;

    @Test
    void mapHeaderAndGenerateReport_shouldGenerateReportSuccessfully() {

        // --------------------------------------------------
        // GIVEN
        // --------------------------------------------------

        Report reportName = Report.TRANSACTION;

        /*
         * Header mapping coming from DB
         *
         * Header       Index
         * ------------------
         * MID          0
         * Transaction  2
         * Amount       4
         */
        Map<String, Integer> headerMapping =
                new LinkedHashMap<>();

        headerMapping.put("MID", 0);
        headerMapping.put("TransactionDate", 2);
        headerMapping.put("Amount", 4);

        when(reportDao.getReportHeaderConfig(reportManagementDto))
                .thenReturn(reportHeaderConfigDto);

        when(reportHeaderConfigDto.getHeaderJson())
                .thenReturn(headerMapping);

        when(reportManagementDto.getFormat())
                .thenReturn("CSV");

        when(reportManagementDto.getMid())
                .thenReturn("123456");

        /*
         * Original file data
         *
         * Index:
         * 0 = MID
         * 1 = unwanted
         * 2 = TransactionDate
         * 3 = unwanted
         * 4 = Amount
         */
        List<List<Object>> fileData = Arrays.asList(

                Arrays.asList(
                        "MID001",
                        "UNWANTED1",
                        "2026-08-31",
                        "UNWANTED2",
                        1000
                ),

                Arrays.asList(
                        "MID002",
                        "UNWANTED3",
                        "2026-08-30",
                        "UNWANTED4",
                        2000
                )
        );

        /*
         * Expected mapped data:
         *
         * Only indexes 0, 2, 4 should be picked.
         */
        List<List<Object>> expectedMappedData = Arrays.asList(

                Arrays.asList(
                        "MID001",
                        "2026-08-31",
                        1000
                ),

                Arrays.asList(
                        "MID002",
                        "2026-08-30",
                        2000
                )
        );

        when(fileGeneratorService.generateFile(
                eq("CSV"),
                eq(reportName),
                eq("123456"),
                eq(Arrays.asList(
                        "MID",
                        "TransactionDate",
                        "Amount"
                )),
                eq(expectedMappedData)
        )).thenReturn(expectedReportFile);

        // --------------------------------------------------
        // WHEN
        // --------------------------------------------------

        ReportFile actualResult =
                ReflectionTestUtils.invokeMethod(
                        reportService,
                        "mapHeaderAndGenerateReport",
                        reportManagementDto,
                        reportName,
                        fileData
                );

        // --------------------------------------------------
        // THEN
        // --------------------------------------------------

        assertNotNull(actualResult);

        assertEquals(expectedReportFile, actualResult);

        // DAO should be called once
        verify(reportDao, times(1))
                .getReportHeaderConfig(reportManagementDto);

        // Header configuration should be fetched
        verify(reportHeaderConfigDto, times(1))
                .getHeaderJson();

        // Report file should be generated with mapped data
        verify(fileGeneratorService, times(1))
                .generateFile(
                        eq("CSV"),
                        eq(reportName),
                        eq("123456"),
                        eq(Arrays.asList(
                                "MID",
                                "TransactionDate",
                                "Amount"
                        )),
                        eq(expectedMappedData)
                );
    }
}
