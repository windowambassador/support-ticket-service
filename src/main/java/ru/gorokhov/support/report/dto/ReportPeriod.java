package ru.gorokhov.support.report.dto;

import java.time.Instant;

public record ReportPeriod(Instant from, Instant to) {}
