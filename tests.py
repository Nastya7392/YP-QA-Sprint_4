import pytest

from main import BooksCollector

VALID_BOOK_NAMES = [
    'П',  # 1 символ - допустимое значение
    'Правила инвестирования Уоррена Баффета I'  # 40 символов - допустимое значение
]

INVALID_BOOK_NAMES = [
    '',  # пустое имя - недопустимое значение
    'Великие тайны истории старых стран Европы'  # 41 символ - недопустимое значение
]

DETECTIVE_BOOK = 'Черное эхо'
FANTASY_BOOKS = ['Хроники нарнии', 'Гарри Поттер']

@pytest.fixture
def collector():
    return BooksCollector()

class TestBooksCollector:

    @pytest.mark.parametrize('book_name', VALID_BOOK_NAMES)
    def test_add_new_book_valid_name_adds_book(self, collector, book_name):
        collector.add_new_book(book_name)

        assert book_name in collector.get_books_genre()
        assert collector.get_books_genre()[book_name] == ''

    @pytest.mark.parametrize('book_name', INVALID_BOOK_NAMES)
    def test_add_new_book_invalid_name_does_not_add_book(self, collector, book_name):
        collector.add_new_book(book_name)

        assert book_name not in collector.get_books_genre()

    def test_add_new_book_duplicate_name_keeps_single_entry(self, collector):
        collector.add_new_book(DETECTIVE_BOOK)
        collector.add_new_book(DETECTIVE_BOOK)

        assert list(collector.get_books_genre().keys()).count(DETECTIVE_BOOK) == 1

    def test_set_book_genre_valid_data_sets_genre(self, collector):
        collector.add_new_book(DETECTIVE_BOOK)
        collector.set_book_genre(DETECTIVE_BOOK, 'Детективы')

        assert collector.get_book_genre(DETECTIVE_BOOK) == 'Детективы'

    def test_set_book_genre_invalid_genre_keeps_empty_genre(self, collector):
        collector.add_new_book(DETECTIVE_BOOK)
        collector.set_book_genre(DETECTIVE_BOOK, 'Драма')

        assert collector.get_book_genre(DETECTIVE_BOOK) == ''

    def test_set_book_genre_missing_book_does_not_add_book(self, collector):
        collector.set_book_genre(DETECTIVE_BOOK, 'Детективы')

        assert DETECTIVE_BOOK not in collector.get_books_genre()

    def test_get_book_genre_existing_book_returns_genre(self, collector):
        collector.add_new_book(DETECTIVE_BOOK)
        collector.set_book_genre(DETECTIVE_BOOK, 'Детективы')

        assert collector.get_book_genre(DETECTIVE_BOOK) == 'Детективы'

    def test_get_book_genre_missing_book_returns_none(self, collector):
        assert collector.get_book_genre(DETECTIVE_BOOK) is None

    def test_get_book_genre_book_without_genre_returns_empty_string(self, collector):
        collector.add_new_book(DETECTIVE_BOOK)

        assert collector.get_book_genre(DETECTIVE_BOOK) == ''

    @pytest.mark.parametrize('book_name', FANTASY_BOOKS)
    def test_get_books_with_specific_genre_returns_books_with_genre(self, collector, book_name):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, 'Фантастика')

        assert collector.get_books_with_specific_genre('Фантастика') == [book_name]

    @pytest.mark.parametrize('book_name', FANTASY_BOOKS)
    def test_get_books_with_specific_genre_wrong_genre_returns_empty_list(self, collector, book_name):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, 'Фантастика')

        assert collector.get_books_with_specific_genre('Ужасы') == []

    @pytest.mark.parametrize('book_name', FANTASY_BOOKS)
    def test_get_books_with_specific_genre_invalid_genre_returns_empty_list(self, collector, book_name):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, 'Фантастика')

        assert collector.get_books_with_specific_genre('Драма') == []

    def test_get_books_genre_empty_collector_returns_empty_dict(self, collector):
        assert collector.get_books_genre() == {}

    def test_get_books_genre_book_without_genre_returns_dict(self, collector):
        collector.add_new_book(DETECTIVE_BOOK)

        assert collector.get_books_genre() == {DETECTIVE_BOOK: ''}

    def test_get_books_genre_book_with_genre_returns_dict(self, collector):
        collector.add_new_book(DETECTIVE_BOOK)
        collector.set_book_genre(DETECTIVE_BOOK, 'Детективы')

        assert collector.get_books_genre() == {DETECTIVE_BOOK: 'Детективы'}

    def test_get_books_for_children_returns_only_children_books(self, collector):
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Мультфильмы')

        collector.add_new_book(DETECTIVE_BOOK)
        collector.set_book_genre(DETECTIVE_BOOK, 'Детективы')

        assert collector.get_books_for_children() == ['Гарри Поттер']

    def test_add_book_in_favorites_existing_book_adds_book(self, collector):
        collector.add_new_book(DETECTIVE_BOOK)
        collector.add_book_in_favorites(DETECTIVE_BOOK)

        assert DETECTIVE_BOOK in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_missing_book_does_not_add_book(self, collector):
        collector.add_book_in_favorites(DETECTIVE_BOOK)

        assert DETECTIVE_BOOK not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_removes_book(self, collector):
        collector.add_new_book(DETECTIVE_BOOK)
        collector.add_book_in_favorites(DETECTIVE_BOOK)
        collector.delete_book_from_favorites(DETECTIVE_BOOK)

        assert DETECTIVE_BOOK not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books_empty_returns_empty_list(self, collector):
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_returns_added_books(self, collector):
        collector.add_new_book(DETECTIVE_BOOK)
        collector.add_book_in_favorites(DETECTIVE_BOOK)

        assert collector.get_list_of_favorites_books() == [DETECTIVE_BOOK]
