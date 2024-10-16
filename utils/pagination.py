def get_page_range(current_page, total_pages):
    page_range = []

    # Добавляем "Предыдущая", если это не первая страница
    if current_page > 1:
        page_range.append("Предыдущая")

    # Добавляем первую страницу
    if total_pages > 1:
        page_range.append(1)

    # Добавляем многоточие, если текущая страница далеко от первой
    if current_page > 3:
        page_range.append("...")

    # Добавляем страницы слева от текущей
    for page in range(max(2, current_page - 2), min(total_pages, current_page + 3)):
        page_range.append(page)

    # Добавляем многоточие, если текущая страница далеко от последней
    if current_page < total_pages - 2:
        page_range.append("...")

    # Добавляем последнюю страницу
    if total_pages > 1:
        page_range.append(total_pages)

        # Добавляем "Следующая", если это не последняя страница
    if current_page < total_pages:
        page_range.append("Следующая")

    return page_range
