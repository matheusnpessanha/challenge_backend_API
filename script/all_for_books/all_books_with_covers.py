import requests
import json
import base64

def get_books():
    url = "https://anapioficeandfire.com/api/books"
    response = requests.get(url)
    
    if response.status_code == 200:
        books = response.json()
        return books
    else:
        print(f"Erro ao obter livros: {response.status_code}")
        return []
    
def get_character_name(character_url):
    response = requests.get(character_url)
    if response.status_code == 200:
        character = response.json()
        return character.get("name")  
    else:
        print(f"Erro ao obter personagem da URL {character_url}: {response.status_code}")
        return None

def get_book_cover_base64(isbn):
    cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
    response = requests.get(cover_url)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    else:
        print(f"Erro ao obter capa para ISBN {isbn}: {response.status_code}")
        return None

def save_books_with_covers(data):
    with open('books_with_characters.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("Dados salvos no arquivo 'books_with_characters.json'.")

def main():
    books = get_books()
    books_with_covers = []

    for book in books:
        title = book.get('name')
        isbn = book.get('isbn')
        cover_base64 = None

        if isbn:
            print(f"Obtendo capa para o livro: {title}")
            cover_base64 = get_book_cover_base64(isbn)

        pov_character_names = []
        for character_url in book.get("povCharacters", []):
            character_name = get_character_name(character_url)
            if character_name:
                pov_character_names.append(character_name)

        books_with_covers.append({
            'name': title,
            'isbn': isbn,
            'numberOfPages': book.get('numberOfPages'),
            'released': book.get('released'),
            'povCharacters': pov_character_names,  
            'cover_base64': cover_base64
        })

    save_books_with_covers(books_with_covers)

if __name__ == "__main__":
    main()
