package com.epay.transaction.producer;

import com.epay.transaction.dto.TransactionDataDto;
import com.epay.common.logging.LoggerFactoryUtility;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class NspiraSpecificHeaderProducer {

    private final Logger log =
            LoggerFactoryUtility.getLogger(this.getClass());

    private final KafkaTemplate<String, String> kafkaTemplate;

    private final ObjectMapper objectMapper;

    @Value("${spring.kafka.topic.nspiraspecificHeaderTopic}")
    private String nspiraSpecificHeaderTopic;

    public void publishTransactionData(TransactionDataDto transactionDataDto) {

        try {
            String message =
                    objectMapper.writeValueAsString(transactionDataDto);

            kafkaTemplate.send(
                    nspiraSpecificHeaderTopic,
                    transactionDataDto.getSbiOrderRefNum(),
                    message
            );

            log.info(
                    "Transaction data published successfully for key: {}",
                    transactionDataDto.getSbiOrderRefNum()
            );

        } catch (JsonProcessingException e) {

            log.error(
                    "Error while publishing transaction data for key: {}",
                    transactionDataDto.getSbiOrderRefNum(),
                    e
            );

            throw new IllegalStateException(
                    "Failed to publish transaction data to Kafka",
                    e
            );
        }
    }
}
