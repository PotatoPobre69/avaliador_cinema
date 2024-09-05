from colorama import Fore, Back, Style
import getpass
import os
import random
import re
import string

if not os.path.exists("users"):
    os.makedirs("users")
if not os.path.exists("movies"):
    os.makedirs("movies")

class User:
    def __init__(self, user_name, user_login, user_email, user_password):
        self.user_name = user_name
        self.user_login = user_login
        self.user_email = user_email
        self.user_password = user_password

    def __str__(self) -> str:
        return (
            f"Nome:     {self.user_name}\n"
            f"Login:    {self.user_login}\n"
            f"Email:    {self.user_email}\n"
        )

    def save_info(self):
        with open(f"users/{self.user_login}.txt", "w") as user_file:
            user_file.write(f"Nome:     {self.user_name}\n")
            user_file.write(f"Login:    {self.user_login}\n")
            user_file.write(f"Email:    {self.user_email}\n")
            user_file.write(f"Senha:    {self.user_password}\n")

    @classmethod
    def load_info(cls):
        try:
            with open(f"users/{cls.user_login}.txt", "r") as user_file:
                lines = user_file.readlines()
                if len(lines) == 4:
                    user_name = lines[0].strip()
                    user_login = lines[1].strip()
                    user_email = lines[2].strip()
                    user_password = lines[3].strip()
                    return cls(user_name, user_login, user_email, user_password)
        except FileNotFoundError:
            print(f"Usuário '{user_login}' não encontrado.")
        return None

    @classmethod
    def get_user(cls) -> "User":
        while True:
            user_name = input("Digite seu nome completo (todos os nomes precisam começar com letra maiúscula): ")
            if cls(user_name, "", "", "").validate_user_name():
                print("Nome Válido!")
                break
            else:
                print("Nome Inválido! Certifique-se que todos os nomes começam com letras maiúsculas.")

        while True:
            user_login = input("Digite seu login (deve ter entre 3 e 16 caracteres, sem espaços e sem letras maiúsculas): @")
            if os.path.exists(f"users/{user_login}.txt"):
                print("Erro: Login já existe.")
            elif cls("", user_login, "", "").validate_user_login():
                print("Login Válido")
                break
            else:
                print("Login Inválido! Deve ter entre 3 e 16 caracteres, sem espaços e sem letras maiúsculas.")

        while True:
            user_email = input("Digite seu endereço de email: ")
            if cls("", "", user_email, "").validate_user_email():
                print("Email Válido")
                break
            else:
                print("Email Inválido! Verifique o formato.")

        while True:
            user_password = getpass.getpass("Digite sua senha (deve ter pelo menos 8 caracteres, com letras maiúsculas, minúsculas, números e caracteres especiais): ")
            if cls("", "", "", user_password).validate_user_password():
                print("Senha Válida")
                break
            else:
                print("Senha Inválida. Deve ter pelo menos 8 caracteres, com letras maiúsculas, minúsculas, números e caracteres especiais.")

        return cls(user_name, user_login, user_email, user_password)

    def validate_user_name(self) -> bool:
        return self.user_name.istitle()

    def validate_user_login(self) -> bool:
        upper = any(i in string.ascii_uppercase for i in self.user_login)
        space = any(i in string.whitespace for i in self.user_login)

        if 3 <= len(self.user_login) <= 16:
            return not (upper or space)
        return False

    def validate_user_email(self) -> bool:
        validacao = r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,7}"

        if len(self.user_email) <= 255:
            local_part = self.user_email.split('@')[0]
            if 0 < len(local_part) < 64:
                return bool(re.fullmatch(validacao, self.user_email))
        return False

    def validate_user_password(self) -> bool:
        lower = any(i in string.ascii_lowercase for i in self.user_password)
        upper = any(i in string.ascii_uppercase for i in self.user_password)
        number = any(i in string.digits for i in self.user_password)
        spchar = any(i in string.punctuation for i in self.user_password)
        space = any(i in string.whitespace for i in self.user_password)

        if len(self.user_password) >= 8:
            return lower and upper and number and spchar and not space
        return False


class Movie:
    def __init__(self, movie_id, movie_name, movie_director, movie_tags, movie_rating, movie_comments):
        self.movie_id = movie_id
        self.movie_name = movie_name
        self.movie_director = movie_director
        self.movie_tags = movie_tags
        self.movie_rating = movie_rating
        self.movie_comments = movie_comments

    def __str__(self) -> str:
        return (
            f"Nome do Filme:        {self.movie_name} ({self.movie_rating:.1f}) - #{self.movie_id}\n"
            f"Diretor do Filme:     {self.movie_director}\n"
            f"Categorias:           {self.movie_tags}\n"
            f"Comentários:          {self.movie_comments}\n"
        )

    def save_info(self):
        with open(f"movies/{self.movie_id}.txt", "w") as movie_file:
            movie_file.write(f"{Back.RED}{Fore.WHITE}{Style.DIM}Nome do Filme:{Style.RESET_ALL}       {self.movie_name}\n")
            movie_file.write(f"{Back.RED}{Fore.WHITE}{Style.DIM}Diretor do Filme:{Style.RESET_ALL}    {self.movie_director}\n")
            movie_file.write(f"{Back.RED}{Fore.WHITE}{Style.DIM}Categorias:{Style.RESET_ALL}          {', '.join(self.movie_tags)}\n")
            movie_file.write(f"{Back.RED}{Fore.WHITE}{Style.DIM}Nota:{Style.RESET_ALL}                {self.movie_rating}\n")
            movie_file.write(f"{Back.RED}{Fore.WHITE}{Style.DIM}Comentários:{Style.RESET_ALL}         {self.movie_comments}\n")
            movie_file.write(f"{Back.RED}{Fore.WHITE}{Style.DIM}#{self.movie_id}\n")

    @classmethod
    def get_movie(cls) -> "Movie":
        while True:
            movie_name = input("Digite o nome do Filme (todos os nomes precisam começar com letra maiúscula): ")
            if cls("", movie_name, "", "", "", "").validate_movie_name():
                print("Filme Válido")
                break
            else:
                print("Filme Inválido! Certifique-se que todas as palavras começam com letras maiúsculas.")

        while True:
            movie_director = input("Digite o nome do Diretor do Filme (todos os nomes precisam começar com letra maiúscula): ")
            if cls("", "", movie_director, "", "", "").validate_movie_director():
                print("Diretor Válido")
                break
            else:
                print("Diretor Inválido! Certifique-se que todas as palavras começam com letras maiúsculas.")

        movie_tags = cls.get_movie_tags()

        while True:
            movie_rating = float(input("Digite a nota do Filme (nota de 0.1 à 10): "))
            if cls("", "", "", "", movie_rating, "").validate_movie_rating():
                print("Nota Adicionada")
                break
            else:
                print("Nota Inválida! Utilize apenas números de 0.1 à 10.")

        movie_comments = input("Digite seu comentário sobre o filme (máximo de 500 caracteres): ")
        movie_id = cls.generate_movie_id()

        return cls(movie_id, movie_name, movie_director, movie_tags, movie_rating, movie_comments)

    @staticmethod
    def generate_movie_id(LENGTH=10) -> str:
        characters = string.ascii_letters + string.digits
        return "".join(random.choices(characters, k=LENGTH))

    @staticmethod
    def get_movie_tags():
        switch_tag = {
            "1": "Ação",
            "2": "Aventura",
            "3": "Cinema de Arte",
            "4": "Chanchada",
            "5": "Comédia",
            "6": "Comédia de Ação",
            "7": "Comédia de Terror",
            "8": "Comédia Dramática",
            "9": "Comédia Romântica",
            "10": "Dança",
            "11": "Documentário",
            "12": "Docuficção",
            "13": "Drama",
            "14": "Espionagem",
            "15": "Faroeste",
            "16": "Fantasia",
            "17": "Fantasia Científica",
            "18": "Ficção Científica",
            "19": "Filmes com truques",
            "20": "Filmes de Guerra",
            "21": "Mistério",
            "22": "Musical",
            "23": "Filme Policial",
            "24": "Romance",
            "25": "Terror",
            "26": "Thriller"
        }

        movie_tags = []
        while True:
            print("Adicione os gêneros do filme, digite o número do gênero desejado no terminal:")
            for key, tag in switch_tag.items():
                print(f"{key} - {tag}")
            print("0 - Sair")

            movie_tag = input("Escolha o número do gênero: ")

            if movie_tag == "0":
                print("Finalizando a seleção de gêneros.")
                break
            elif movie_tag in switch_tag:
                tag = switch_tag[movie_tag]
                if tag not in movie_tags:
                    movie_tags.append(tag)
                    print(f"Gênero '{tag}' adicionado.")
                else:
                    print(f"Gênero '{tag}' já foi adicionado.")
            else:
                print("Opção inválida. Por favor, escolha um número entre 1 e 26, ou 0 para sair.")

        return movie_tags

    def validate_movie_name(self):
        return self.movie_name.istitle()

    def validate_movie_director(self):
        return self.movie_director.istitle()

    def validate_movie_rating(self):
        return 0.1 <= self.movie_rating <= 10

    def validate_movie_comments(self):
        return len(self.movie_comments) <= 500


# Console para interagir com o sistema de filmes:
def rating_console():
    while True:
        print("Bem-vindo ao Algoritmo avaliador_cinema.py")
        print("Escolha:\n1 - Catálogo de Filmes\n2 - Adicionar Filme ao Catálogo\n3 - Avaliar Filme\n4 - Meu Perfil\n5 - Sair")
        option = input("Digite o número da opção desejada: ")

        if option == "1":
            print("\nCatálogo")

            movie_files = os.listdir("movies")
            if not movie_files:
                print("Nenhum filme cadastrado ainda.")
            else:
                for movie_file in movie_files:
                    with open(f"movies/{movie_file}", "r") as file:
                        print(file.read())
        elif option == "2":
            print("\nAdicione um Filme: ")
            new_movie = Movie.get_movie()
            new_movie.save_info()
            print(f"Filme '{new_movie.movie_name}' adicionado ao catálogo.")
        elif option == "3":
            print("\nAvalie o filme: ")
            

        elif option == "5":
            print("\nSaindo...")
            break

def main():
    while True:
        print("Bem-vindo ao Algoritmo avaliador_cinema.py, caso não tenha uma conta ainda, registre-se e se torne um Avaliador\nEscolha:\n1 - Registrar-se\n2 - Já tenho uma conta\n3 - Sair")
        option = input("Digite o número da opção desejada: ")

        if option == "1":
            new_user = User.get_user()
            new_user.save_info()
            print("\nCadastro concluído com sucesso.")
            rating_console()
        elif option == "2":
            login = input("Digite seu login: @")
            password = getpass.getpass("Digite sua senha: ")

            user = User.load_info(login)
            if user and user.user_password == password:
                print("\nLogin bem-sucedido!")
                print(user)
                rating_console()
            else:
                print("Login ou senha inválidos.")
        elif option == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha 1, 2 ou 3.")

if __name__ == "__main__":
    main()
