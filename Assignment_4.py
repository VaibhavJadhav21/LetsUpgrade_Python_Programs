@Query(value = """
    SELECT CASE
        WHEN (
            EXISTS (
                SELECT 1 FROM MERCHANT_RFC
                WHERE MERCHANT_ID = :mId
                  AND RECORD_STATUS = '1'
                  AND AUTH_STATUS = 'REJECTED'
            )
            OR
            EXISTS (
                SELECT 1 FROM MERCHANT_VVL
                WHERE MERCHANT_ID = :mId
                  AND RECORD_STATUS = '1'
                  AND AUTH_STATUS = 'REJECTED'
            )
        )
        AND NOT EXISTS (
            SELECT 1 FROM MERCHANT_RFC
            WHERE MERCHANT_ID = :mId
              AND RECORD_STATUS = '1'
              AND AUTH_STATUS = 'PENDING'
        )
        AND NOT EXISTS (
            SELECT 1 FROM MERCHANT_VVL
            WHERE MERCHANT_ID = :mId
              AND RECORD_STATUS = '1'
              AND AUTH_STATUS = 'PENDING'
        )
        THEN 1
        ELSE 0
    END
    FROM DUAL
    """, nativeQuery = true)
Integer isRiskManagementRejected(@Param("mId") String mId);
