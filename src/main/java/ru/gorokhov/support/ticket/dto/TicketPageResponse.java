package ru.gorokhov.support.ticket.dto;

import java.util.List;

public record TicketPageResponse(
        List<TicketResponse> content, int page, int size, long totalElements, long totalPages) {
    public TicketPageResponse {
        content = List.copyOf(content);
    }
}
