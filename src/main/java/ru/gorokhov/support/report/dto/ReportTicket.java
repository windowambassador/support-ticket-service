package ru.gorokhov.support.report.dto;

import java.time.Instant;
import org.jspecify.annotations.NullMarked;
import org.jspecify.annotations.Nullable;
import ru.gorokhov.support.ticket.entity.TicketPriority;
import ru.gorokhov.support.ticket.entity.TicketStatus;

@NullMarked
public record ReportTicket(
        TicketStatus status,
        TicketPriority priority,
        Instant createdAt,
        @Nullable Instant dueAt,
        @Nullable Instant closedAt) {}
