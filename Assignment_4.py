@Query(value = """
    SELECT CASE
        WHEN COUNT(DISTINCT CASE
            WHEN STATUS = 'COMPLETED' THEN STEP_CODE
        END) = :stepCount
        THEN 1 ELSE 0
    END
    FROM ONBOARDING_STAGE
    WHERE MERCHANT_MIF_ID = :mifId
    AND STEP_CODE IN (:stepCodes)
    """, nativeQuery = true)
int areStepsCompleted(
        @Param("mifId") String mifId,
        @Param("stepCodes") List<String> stepCodes,
        @Param("stepCount") int stepCount);



public boolean areStepsCompleted(String mifId, List<String> stepCodes) {
    return onboardingStageRepository.areStepsCompleted(
            mifId, stepCodes, stepCodes.size()) == 1;
}



String mifId = onboardingStageDao.getMifId(mId);

onboardingStageService.markStepCompleted(mifId, RISK_MANAGEMENT_RFC_MAKER);
onboardingStageService.markStepCompleted(mifId, RISK_MANAGEMENT_VVL_MAKER);

List<String> steps = List.of(
        RISK_MANAGEMENT_RFC_MAKER,
        RISK_MANAGEMENT_VVL_MAKER
);

if (onboardingStageDao.areStepsCompleted(mifId, steps)) {
    onboardingStageService.markStageCompleted(
            mifId, OnboardingStage.RISK_MANAGEMENT);
}
