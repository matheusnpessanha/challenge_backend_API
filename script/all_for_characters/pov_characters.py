import json
import requests

def get_books():
    url = "https://anapioficeandfire.com/api/books"
    response = requests.get(url)
    
    if response.status_code == 200:
        books = response.json()
        return books
    else:
        print(f"Erro ao obter livros: {response.status_code}")
        return []

def get_character_details(character_url):
    response = requests.get(character_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter detalhes do personagem da URL {character_url}: {response.status_code}")
        return None

def save_pov_characters(pov_characters):
    with open('pov_characters.json', 'w') as json_file:
        json.dump(pov_characters, json_file, indent=4)
    print("Dados dos personagens POV salvos no arquivo 'pov_characters.json'.")

def main():
    books = get_books()  
    pov_characters_list = []
    added_character_urls = set()  
    
    book_urls_to_names = {book["url"]: book["name"] for book in books}
    
    for book in books:
        pov_urls = book.get("povCharacters", [])
        
        for url in pov_urls:
            if url not in added_character_urls:
                character = get_character_details(url)
                if character:
                    pov_books = []
                    for book_url in character.get("povBooks", []):
                        if book_url in book_urls_to_names:
                            pov_books.append(book_urls_to_names[book_url])
                        else:
                            print(f"URL do livro {book_url} não encontrada no dicionário.")
                    
                    pov_character_data = {
                        "name": character.get("name"),
                        "gender": character.get("gender"),
                        "culture": character.get("culture"),
                        "born": character.get("born"),
                        "died": character.get("died"),
                        "titles": character.get("titles", []),
                        "povBooks": pov_books,  
                        "tvSeries": character.get("tvSeries", [])
                    }
                    
                    pov_characters_list.append(pov_character_data)
                    added_character_urls.add(url)  
                else:
                    print(f"Erro ao obter detalhes do personagem da URL {url}.")
            else:
                print(f"Personagem com URL {url} já foi adicionado.")

    if pov_characters_list:
        save_pov_characters(pov_characters_list)
    else:
        print("Nenhum personagem POV encontrado.")
        
if __name__ == "__main__":
    main()
