@Query(value = """
    SELECT CASE
        WHEN (
            EXISTS (
                SELECT 1 FROM MERCHANT_RFC r
                WHERE r.MERCHANT_ID = :mId
                  AND r.RECORD_STATUS = 1
                  AND r.AUTH_STATUS = 'REJECTED'
            )
            OR EXISTS (
                SELECT 1 FROM MERCHANT_VVL v
                WHERE v.MERCHANT_ID = :mId
                  AND v.RECORD_STATUS = 1
                  AND v.AUTH_STATUS = 'REJECTED'
            )
        )
        AND NOT EXISTS (
            SELECT 1 FROM MERCHANT_RFC r
            WHERE r.MERCHANT_ID = :mId
              AND r.RECORD_STATUS = 1
              AND r.AUTH_STATUS = 'PENDING'
        )
        AND NOT EXISTS (
            SELECT 1 FROM MERCHANT_VVL v
            WHERE v.MERCHANT_ID = :mId
              AND v.RECORD_STATUS = 1
              AND v.AUTH_STATUS = 'PENDING'
        )
        THEN 1
        ELSE 0
    END
    FROM DUAL
    """, nativeQuery = true)
Boolean isRiskManagementRejected(@Param("mId") String mId);
