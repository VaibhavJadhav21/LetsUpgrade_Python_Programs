@Test
void generateReport_ShouldBuildTransactionReport() {
    UUID reportManagementId = UUID.randomUUID();

    ReportManagementDto dto = new ReportManagementDto();
    dto.setId(reportManagementId);
    dto.setReport(ReportType.TRANSACTION);

    when(reportManagementDao.updateReportStatus(
            reportManagementId, ReportStatus.GENERATION_STARTED))
            .thenReturn(dto);

    when(reportDao.getTransactionReportData(dto))
            .thenReturn(transactionReportData);

    reportService.generateReport(reportManagementId);

    verify(reportDao).getTransactionReportData(dto);
    verify(reportManagementDao).updateReportStatus(
            reportManagementId, ReportStatus.GENERATION_STARTED);
}




@Test
void generateReport_ShouldBuildSettlementReport() {
    UUID reportManagementId = UUID.randomUUID();

    ReportManagementDto dto = new ReportManagementDto();
    dto.setId(reportManagementId);
    dto.setReport(ReportType.SETTLEMENT);

    when(reportManagementDao.updateReportStatus(
            reportManagementId, ReportStatus.GENERATION_STARTED))
            .thenReturn(dto);

    when(reportDao.getSettlementReportData(dto))
            .thenReturn(settlementReportData);

    reportService.generateReport(reportManagementId);

    verify(reportDao).getSettlementReportData(dto);
    verify(reportManagementDao).updateReportStatus(
            reportManagementId, ReportStatus.GENERATION_STARTED);
}
