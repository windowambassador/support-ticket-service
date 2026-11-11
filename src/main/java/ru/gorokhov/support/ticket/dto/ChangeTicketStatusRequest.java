package ru.gorokhov.support.ticket.dto;

import ru.gorokhov.support.ticket.entity.TicketStatus;
import ru.gorokhov.support.ticket.validation.ChangeTicketStatusRequestDeserializer;
import tools.jackson.databind.annotation.JsonDeserialize;

@JsonDeserialize(using = ChangeTicketStatusRequestDeserializer.class)
public record ChangeTicketStatusRequest(TicketStatus status) {}
