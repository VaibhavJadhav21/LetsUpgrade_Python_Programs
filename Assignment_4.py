@Query(value = """
    SELECT CASE WHEN EXISTS (
        SELECT 1
        FROM MERCHANT_VVL
        WHERE MERCHANT_ID = :mId
          AND AUTH_STATUS = 'APPROVED'
          AND RECORD_STATUS = '1'
    )
    THEN 1 ELSE 0 END
    FROM DUAL
    """, nativeQuery = true)
Boolean existsApprovedRecord(@Param("mId") String mId);



public boolean isAnyVvlRecordApproved(String mId) {
    return Boolean.TRUE.equals(
            merchantVvlRepository.existsApprovedRecord(mId));
}
