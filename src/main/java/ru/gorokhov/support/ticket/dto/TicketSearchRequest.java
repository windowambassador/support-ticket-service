package ru.gorokhov.support.ticket.dto;

import ru.gorokhov.support.ticket.entity.TicketPriority;
import ru.gorokhov.support.ticket.entity.TicketStatus;

public record TicketSearchRequest(
        TicketStatus status,
        TicketPriority priority,
        Long categoryId,
        Boolean overdue,
        int page,
        int size) {
    public long offset() {
        return (long) page * size;
    }
}
