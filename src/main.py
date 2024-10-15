# Organização de ideias
"""
/src
│
├── main.py                  # Ponto de entrada do sistema
├── admin_flow.py            # Controle e funcionalidades para o Administrador
├── vendor_flow.py           # Controle e funcionalidades para o Vendedor/Gestor
├── user_flow.py             # Controle e funcionalidades para o Usuário comum
├── classes/
│   ├── vending_machine.py    # Classe Vending Machine
│   ├── product.py            # Classe Produto
│   ├── problem_report.py      # Classe para Reports de Problemas
│   ├── review.py             # Classe para Avaliações
│   └── user.py               # Classe para Usuários (Administrador, Vendedor, Usuário)
"""

# Pseudocodigo do loop principal
'''
from admin_flow import admin_actions
from vendor_flow import vendor_actions
from user_flow import user_actions

def main():
    while True:
        user_type = identificar_usuario()  # Exemplo de login ou seleção de tipo de usuário
        
        if user_type == "Administrador":
            admin_actions()  # Chama as ações do administrador definidas no módulo admin_flow.py
        elif user_type == "Vendedor":
            vendor_actions()  # Chama as ações do vendedor no módulo vendor_flow.py
        elif user_type == "Usuario":
            user_actions()  # Chama as ações do usuário no módulo user_flow.py
        elif user_type == "Sair":
            break  # Finaliza o programa
'''
