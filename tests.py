import pytest
from main import BooksCollector

valid_book_names = [
    'П', # 1 символ - допустимое значение
    'Правила инвестирования Уоррена Баффета I' # 40 символов - допустимое значение
]

invalid_book_names = [
    '', # пустое имя - недопустимое значение
    'Великие тайны истории старых стран Европы' # 41 символ - недопустимое значение
]

detective_book = 'Черное эхо'

class TestBooksCollector:

    @pytest.mark.parametrize('valid_book_name', valid_book_names)
    def test_add_new_book_with_valid_name_book_has_been_added(self, valid_book_name):
        collector = BooksCollector()
        collector.add_new_book(valid_book_name)
        assert valid_book_name in collector.books_genre
    
    @pytest.mark.parametrize('valid_book_name', valid_book_names)
    def test_add_new_book_with_valid_name_book_genre_is_empty(self, valid_book_name):
        collector = BooksCollector()
        collector.add_new_book(valid_book_name)
        assert collector.books_genre[valid_book_name] == ''
        
    @pytest.mark.parametrize('invalid_book_name', invalid_book_names)
    def test_add_new_book_with_invalid_name_book_has_not_been_added(self, invalid_book_name):
        collector = BooksCollector()
        collector.add_new_book(invalid_book_name)
        assert invalid_book_name not in collector.books_genre
        
    @pytest.mark.parametrize('book_name', detective_book)
    def test_add_new_book_with_same_name_twice_book_is_not_duplicated(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        assert list(collector.books_genre.keys()).count(book_name) == 1
        
    @pytest.mark.parametrize('book_name', detective_book)
    def test_set_book_genre_with_valid_genre_and_an_existing_book_genre_has_been_assigned(self, book_name):
        collector = BooksCollector()
        expected_genre = 'Детективы'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, expected_genre)
        assert collector.books_genre[book_name] == expected_genre
    
    @pytest.mark.parametrize('book_name', detective_book)
    def test_set_book_genre_with_invalid_genre_and_an_existing_book_genre_has_not_been_assigned(self, book_name):
        collector = BooksCollector()
        invalid_genre = 'Драма'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, invalid_genre)
        assert collector.books_genre[book_name] == ''
    
    @pytest.mark.parametrize('book_name', detective_book)
    def test_set_book_genre_with_valid_genre_and_an_non_existent_book_has_not_been_added_and_genre_has_not_been_assigned(self, book_name):
        collector = BooksCollector()
        collector.set_book_genre(book_name, 'Детективы')
        assert book_name not in collector.books_genre
    
    @pytest.mark.parametrize('book_name', detective_book)
    def test_get_book_genre_of_an_existing_book_genre_is_returned(self, book_name):
        collector = BooksCollector()
        expected_genre = 'Детективы'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, expected_genre)
        assert collector.get_book_genre(book_name) == expected_genre
    
    @pytest.mark.parametrize('book_name', detective_book)
    def test_get_book_genre_of_an_non_existent_book_genre_is_not_returned(self, book_name):
        collector = BooksCollector()
        assert collector.get_book_genre(book_name) is None
    
    @pytest.mark.parametrize('book_name', detective_book)
    def test_get_book_genre_of_an_existing_book_without_genre_genre_is_empty(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert collector.get_book_genre(book_name) == ''
        
    @pytest.mark.parametrize('book_names', ['Хроники нарнии', 'Гарри Поттер'])
    def test_get_books_with_specific_genre_genre_is_assigned_and_an_existing_books_books_are_returned(self, book_names):
        collector = BooksCollector()
        genre = 'Фантастика'
        collector.add_new_book(book_names)
        collector.set_book_genre(book_names, genre)
        assert collector.get_books_with_specific_genre(genre) == [book_names]
    
    @pytest.mark.parametrize('book_names', ['Хроники нарнии', 'Гарри Поттер'])
    def test_get_books_with_specific_genre_an_existing_books_and_wrong_genre_books_are_not_returned(self, book_names):
        collector = BooksCollector()
        genre = 'Фантастика'
        collector.add_new_book(book_names)
        collector.set_book_genre(book_names, genre)
        assert collector.get_books_with_specific_genre('Ужасы') == []
    
    @pytest.mark.parametrize('book_names', ['Хроники нарнии', 'Гарри Поттер'])
    def test_get_books_with_specific_genre_an_existing_books_and_invalid_genre_books_are_not_returned(self, book_names):
        collector = BooksCollector()
        genre = 'Фантастика'
        collector.add_new_book(book_names)
        collector.set_book_genre(book_names, genre)
        assert collector.get_books_with_specific_genre('Драма') == []
        
    def test_get_books_genre_books_not_added_return_empty_vocabulary(self):
        collector = BooksCollector()
        assert collector.get_books_genre() == {}
        
    @pytest.mark.parametrize('book_name', detective_book)
    def test_get_books_genre_book_is_added_without_genre_return_only_book_name_in_vocabulary(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert collector.get_books_genre() == {book_name: ''}
    
    @pytest.mark.parametrize('book_name', detective_book)
    def test_get_books_genre_book_is_added_with_genre_return_book_name_and_genre_in_vocabulary(self, book_name):
        collector = BooksCollector()
        genre = 'Детективы'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_books_genre() == {book_name: genre}
        
    def test_get_books_for_children_with_child_and_adult_book_return_only_child_book(self):
        collector = BooksCollector()
        child_genre = 'Мультфильмы'
        adult_genre = 'Детективы'
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', child_genre)
        collector.add_new_book('Черное эхо')
        collector.set_book_genre('Черное эхо', adult_genre)
        assert collector.get_books_for_children() == ['Гарри Поттер']
    
    @pytest.mark.parametrize('book_name', detective_book)
    def test_add_book_in_favorites_an_existing_book_book_is_added_in_favorites(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.favorites
        
    @pytest.mark.parametrize('book_name', detective_book)
    def test_add_book_in_favorites_an_non_existing_book_book_is_not_added_in_favorites(self, book_name):
        collector = BooksCollector()
        collector.add_book_in_favorites(book_name)
        assert book_name not in collector.favorites
        
    @pytest.mark.parametrize('book_name', detective_book)
    def test_delete_book_from_favorites_book_in_favorites_book_deleted(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.favorites
        
    def test_get_list_of_favorites_books_books_is_not_added(self):
        collector = BooksCollector()
        assert collector.favorites == []
        
    @pytest.mark.parametrize('book_name', detective_book)
    def test_get_list_of_favorites_books_books_is_added(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert collector.favorites == [book_name]