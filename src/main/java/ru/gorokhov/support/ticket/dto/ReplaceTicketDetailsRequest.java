package ru.gorokhov.support.ticket.dto;

import java.time.Instant;
import ru.gorokhov.support.ticket.entity.TicketPriority;
import ru.gorokhov.support.ticket.validation.ReplaceTicketDetailsRequestDeserializer;
import tools.jackson.databind.annotation.JsonDeserialize;

@JsonDeserialize(using = ReplaceTicketDetailsRequestDeserializer.class)
public record ReplaceTicketDetailsRequest(
        String description, TicketPriority priority, Instant dueAt) {}
