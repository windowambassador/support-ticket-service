package ru.gorokhov.support.ticket.validation;

import java.util.Set;
import ru.gorokhov.support.common.json.StrictJsonObject;
import ru.gorokhov.support.common.validation.ApiDateTime;
import ru.gorokhov.support.ticket.dto.ReplaceTicketDetailsRequest;
import ru.gorokhov.support.ticket.entity.TicketPriority;
import tools.jackson.core.JsonParser;
import tools.jackson.databind.DeserializationContext;
import tools.jackson.databind.ValueDeserializer;

public class ReplaceTicketDetailsRequestDeserializer
        extends ValueDeserializer<ReplaceTicketDetailsRequest> {
    private static final Set<String> FIELDS = Set.of("description", "priority", "dueAt");

    @Override
    public ReplaceTicketDetailsRequest deserialize(
            JsonParser parser, DeserializationContext context) {
        var fields = new StrictJsonObject(parser.readValueAsTree(), FIELDS);
        fields.require("description", "priority", "dueAt");
        var description = fields.string("description");
        var priority = fields.enumValue("priority", TicketPriority.class);
        var dueAt = fields.string("dueAt");
        return new ReplaceTicketDetailsRequest(
                description, priority, dueAt == null ? null : ApiDateTime.parse(dueAt, "dueAt"));
    }
}
