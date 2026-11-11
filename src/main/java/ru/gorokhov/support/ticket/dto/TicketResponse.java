package ru.gorokhov.support.ticket.dto;

import java.time.Instant;
import java.util.UUID;
import ru.gorokhov.support.category.dto.CategoryResponse;
import ru.gorokhov.support.ticket.entity.TicketPriority;
import ru.gorokhov.support.ticket.entity.TicketStatus;

public record TicketResponse(
        UUID id,
        String title,
        String description,
        CategoryResponse category,
        TicketPriority priority,
        TicketStatus status,
        Instant createdAt,
        Instant dueAt,
        Instant closedAt,
        boolean overdue) {}
