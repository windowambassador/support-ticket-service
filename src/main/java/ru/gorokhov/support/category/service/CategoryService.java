package ru.gorokhov.support.category.service;

import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gorokhov.support.category.dto.CategoryResponse;
import ru.gorokhov.support.category.entity.Category;
import ru.gorokhov.support.category.repository.CategoryRepository;
import ru.gorokhov.support.common.error.ApiException;

@Service
@Transactional(readOnly = true)
public class CategoryService {
    private final CategoryRepository repository;

    public CategoryService(CategoryRepository repository) {
        this.repository = repository;
    }

    public List<CategoryResponse> getAll() {
        return repository.findAllByOrderByIdAsc().stream().map(CategoryResponse::from).toList();
    }

    public Category getRequired(long id) {
        return repository
                .findById(id)
                .orElseThrow(() -> ApiException.validation("categoryId", "Категория не найдена."));
    }
}
