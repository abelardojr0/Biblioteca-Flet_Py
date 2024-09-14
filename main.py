import flet as ft  # Importa a biblioteca Flet e a renomeia como `ft`.

# Mock database
books = []  # Cria uma lista vazia para armazenar os livros.

def main(page: ft.Page):
    # Referências para campos de entrada
    title_input = ft.TextField(label="Título")  # Campo para entrada do título do livro.
    author_input = ft.TextField(label="Autor")  # Campo para entrada do autor do livro.

    # Funções de manipulação

    def add_book(e):#esse (e) é uma boa prática, para caso eu queira manipular algo dos eventos.
        # Verifica se os campos de entrada não estão vazios.
        if title_input.value and author_input.value:
            books.append({
                'title': title_input.value,  # Adiciona o título à lista de livros.
                'author': author_input.value  # Adiciona o autor à lista de livros.
            })
            print(books)  # Exibe a lista de livros no console para depuração.
            title_input.value = ""  # Limpa o campo de título.
            author_input.value = ""  # Limpa o campo de autor.
            # Limpa a tela e mostra o menu principal
            page.controls.clear()
            show_main_menu()
            page.update()
        else:
            # Exibe uma mensagem de erro se os campos não forem preenchidos.
            dialog = ft.AlertDialog(
                title=ft.Text("Erro"),  # Título da caixa de diálogo.
                content=ft.Text("Por favor, preencha todos os campos."),  # Mensagem de erro.
                actions=[ft.TextButton("OK", on_click=lambda e: page.overlay.remove(dialog))]  # Botão para fechar a caixa de diálogo.
            )
            page.overlay.append(dialog)  # Adiciona a caixa de diálogo à sobreposição da página.
            page.update()  # Atualiza a página para mostrar a caixa de diálogo.

    def show_all_books(e):
        # Limpa a tela e mostra todos os livros na lista.
        page.controls.clear()  # Limpa todos os controles da página.
        controls = [
            ft.Text("Lista de Livros", size=30, weight=ft.FontWeight.BOLD),  # Título da lista de livros.
            ft.ElevatedButton("Voltar", on_click=lambda e: show_main_menu())  # Botão para voltar ao menu principal.
        ]
        
        if books:
            controls.append(ft.Row(
                controls=[
                    ft.Text("Título", size=20, weight=ft.FontWeight.BOLD, width=200),  # Cabeçalho da coluna "Título".
                    ft.Text("Autor", size=20, weight=ft.FontWeight.BOLD, width=200),  # Cabeçalho da coluna "Autor".
                    ft.Text("Ações", size=20, weight=ft.FontWeight.BOLD)  # Cabeçalho da coluna "Ações".
                ]
            ))

            for book in books:
                controls.append(ft.Row(
                    controls=[
                        ft.Text(book['title'], width=200),  # Exibe o título do livro.
                        ft.Text(book['author'], width=200),  # Exibe o autor do livro.
                        ft.Row(
                            controls=[
                                ft.IconButton(ft.icons.EDIT, on_click=lambda e, book=book: show_edit_book(book)),  # Botão de editar.
                                ft.IconButton(ft.icons.DELETE, on_click=lambda e, book=book: delete_book(book))  # Botão de deletar.
                            ]
                        )
                    ]
                ))
        else:
            controls.append(ft.Text("Nenhum livro encontrado."))  # Mensagem exibida se não houver livros.

        page.add(ft.Column(controls=controls))  # Adiciona todos os controles à página.
        page.update()  # Atualiza a página para refletir as mudanças.

    def show_edit_book(book):
        # Atualiza os campos de entrada com os valores do livro a ser editado.
        title_input.value = book['title']
        author_input.value = book['author']

        def save_book(e):
            # Atualiza o livro com os novos valores dos campos de entrada.
            book['title'] = title_input.value
            book['author'] = author_input.value
            page.controls.clear()  # Limpa todos os controles da página.
            show_main_menu()  # Mostra o menu principal após salvar as alterações.
            page.update()  # Atualiza a página para refletir as mudanças.

        # Limpa a tela e mostra o formulário para edição do livro.
        page.controls.clear()
        page.add(ft.Column(
            controls=[
                ft.Text("Editar Livro", size=30, weight=ft.FontWeight.BOLD),  # Título da página de edição.
                title_input,  # Campo de entrada para o título do livro.
                author_input,  # Campo de entrada para o autor do livro.
                ft.ElevatedButton("Salvar", on_click=save_book),  # Botão para salvar as alterações.
                ft.ElevatedButton("Voltar", on_click=lambda e: show_main_menu())  # Botão para voltar ao menu principal.
            ]
        ))
        page.update()  # Atualiza a página para refletir as mudanças.

    def delete_book(book):
        # Remove o livro da lista e atualiza a exibição.
        books.remove(book)  # Remove o livro da lista de livros.
        show_all_books(None)  # Atualiza a lista de livros.

    def show_add_book(e):
        # Limpa a tela e mostra o formulário para adicionar um novo livro.
        page.controls.clear()
        page.add(ft.Column(
            controls=[
                ft.Text("Adicionar Livro", size=30, weight=ft.FontWeight.BOLD),  # Título da página de adição.
                title_input,  # Campo de entrada para o título do livro.
                author_input,  # Campo de entrada para o autor do livro.
                ft.ElevatedButton("Adicionar", on_click=add_book),  # Botão para adicionar o livro.
                ft.ElevatedButton("Voltar", on_click=lambda e: show_main_menu())  # Botão para voltar ao menu principal.
            ]
        ))
        page.update()  # Atualiza a página para refletir as mudanças.

        # Adiciona um evento para pressionar ENTER e adicionar o livro.
        title_input.on_submit = add_book  # Define a função a ser chamada quando o usuário pressionar ENTER no campo de título.
        author_input.on_submit = add_book  # Define a função a ser chamada quando o usuário pressionar ENTER no campo de autor.

    def show_main_menu():
        # Limpa a tela e mostra o menu principal com opções para adicionar ou visualizar livros.
        page.controls.clear()  # Limpa todos os controles da página.
        page.add(ft.Column(
            controls=[
                ft.Text("Menu Principal", size=30, weight=ft.FontWeight.BOLD),  # Título do menu principal.
                ft.ElevatedButton("Adicionar Livro", on_click=show_add_book),  # Botão para adicionar um livro.
                ft.ElevatedButton("Ver Todos os Livros", on_click=show_all_books)  # Botão para ver todos os livros.
            ]
        ))
        page.update()  # Atualiza a página para refletir as mudanças.
    
    # Inicializa com o menu principal
    show_main_menu()  # Exibe o menu principal quando a aplicação é iniciada.

# Inicia a aplicação
ft.app(target=main)  # Inicia o aplicativo Flet com a função `main` como a função principal.
