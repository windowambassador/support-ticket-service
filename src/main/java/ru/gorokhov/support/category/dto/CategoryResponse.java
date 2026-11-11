package ru.gorokhov.support.category.dto;

import ru.gorokhov.support.category.entity.Category;

public record CategoryResponse(long id, String name) {
    public static CategoryResponse from(Category category) {
        return new CategoryResponse(category.getId(), category.getName());
    }
}
