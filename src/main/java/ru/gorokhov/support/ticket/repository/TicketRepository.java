package ru.gorokhov.support.ticket.repository;

import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;
import ru.gorokhov.support.ticket.entity.Ticket;

public interface TicketRepository extends JpaRepository<Ticket, UUID> {}
