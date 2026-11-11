package ru.gorokhov.support.ticket.dto;

import java.time.Instant;
import ru.gorokhov.support.ticket.entity.TicketPriority;
import ru.gorokhov.support.ticket.validation.CreateTicketRequestDeserializer;
import tools.jackson.databind.annotation.JsonDeserialize;

@JsonDeserialize(using = CreateTicketRequestDeserializer.class)
public record CreateTicketRequest(
        String title,
        Long categoryId,
        String description,
        TicketPriority priority,
        Instant dueAt) {}
