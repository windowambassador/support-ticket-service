package ru.gorokhov.support.ticket.dto;

import java.time.Instant;
import ru.gorokhov.support.ticket.entity.TicketPriority;

public record CreateTicketRequest(
        String title,
        Long categoryId,
        String description,
        TicketPriority priority,
        Instant dueAt) {}
