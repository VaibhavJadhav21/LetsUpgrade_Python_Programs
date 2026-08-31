package com.epay.reporting.service;

import com.epay.reporting.dao.ReportDao;
import com.epay.reporting.dto.ReportHeaderConfigDto;
import com.epay.reporting.dto.ReportManagementDto;
import com.epay.reporting.enums.ReportFormat; // तुमच्या प्रोजेक्टनुसार पॅकेज तपासा
import com.epay.reporting.model.Report;
import com.epay.reporting.model.ReportFile;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ReportServiceTest {

    @Mock
    private ReportDao reportDao;

    @Mock
    private FileGeneratorService fileGeneratorService;

    @InjectMocks
    private ReportService reportService;

    @Test
    void testMapHeaderAndGenerateReport_Success() {
        // 1. Setup Input Data
        ReportManagementDto dto = new ReportManagementDto();
        dto.setmId(UUID.randomUUID());
        dto.setFormat(ReportFormat.CSV); // योग्य तो फॉरमॅट सेट करा

        Report reportName = new Report();

        List<List<Object>> fileData = List.of(
            List.of("Val1", "Val2")
        );

        // Mock ReportHeaderConfigDto
        ReportHeaderConfigDto configDto = new ReportHeaderConfigDto();
        // headerMapping मध्ये इमेज १ नुसार String key आणि Integer index व्हॅल्यू सेट केली आहे
        configDto.setHeaderJson(Map.of("Header1", 0, "Header2", 1)); 

        // 2. Stub Mock Calls (इथे NPE येत होता, तो असा सॉल्व्ह होईल)
        when(reportDao.getReportHeaderConfig(dto)).thenReturn(configDto);

        when(fileGeneratorService.generateFile(
                any(), any(), any(), any(), any()
        )).thenReturn(new ReportFile());

        // 3. Execute Method 
        // जर mapHeaderAndGenerateReport ही 'private' असेल, तर हिला कॉल करणाऱ्या सार्वजनिक (public) मेथडद्वारे टेस्ट करा.
        ReportFile result = reportService.mapHeaderAndGenerateReport(dto, reportName, fileData);

        // 4. Assertions
        assertNotNull(result);
    }
}
