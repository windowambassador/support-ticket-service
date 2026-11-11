package ru.gorokhov.support.ticket.dto;

import java.time.Instant;
import ru.gorokhov.support.ticket.entity.TicketStatus;
import ru.gorokhov.support.ticket.entity.TicketStatusHistory;

public record StatusHistoryResponse(
        Long id, TicketStatus fromStatus, TicketStatus toStatus, Instant changedAt) {
    public static StatusHistoryResponse from(TicketStatusHistory entry) {
        return new StatusHistoryResponse(
                entry.getId(), entry.getFromStatus(), entry.getToStatus(), entry.getChangedAt());
    }
}
