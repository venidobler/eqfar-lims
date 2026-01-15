# 🧪 EQFAR LIMS (Laboratory Information Management System)

Sistema de Gestão de Capacidade e Agendamento de Equipamentos Laboratoriais, desenvolvido para otimizar o fluxo de uso de instrumentos como HPLC e Friabilômetros.

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-sky)

## 🚀 Funcionalidades

- **Dashboard Gantt:** Visualização temporal da ocupação dos equipamentos.
- **Regra Anti-Conflito:** Impede agendamentos simultâneos no mesmo equipamento.
- **Fluxo de Aprovação:** Gestores aprovam ou rejeitam solicitações.
- **Cálculo de Custos:** Estimativa automática baseada nas horas de uso.
- **Interface Responsiva:** Painel administrativo moderno com Sidebar.

## 🛠️ Instalação Local

Pré-requisitos: Python 3.12+, Node.js (para o Tailwind).

1. **Clone o repositório:**
   ```bash```
   git clone [https://github.com/seu-usuario/eqfar-lims.git](https://github.com/seu-usuario/eqfar-lims.git)
   cd eqfar-lims

2. **Crie e ative o ambiente virtual:**
   ```bash```
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate

3. **Instale as dependências:**
  ```bash```
    pip install -r requirements.txt

4. **Configure o Banco de Dados:**
  ```bash```
    python manage.py migrate

5. **Inicie o Tailwind (em um terminal separado):**
  ```bash```
    python manage.py tailwind start

6. **Rode o servidor (no terminal principal):**
  ```bash```
    python manage.py runserver

7. **Acesse: http://127.0.0.1:8000**


## 🤝 Como Contribuir
1. Faça um Fork do projeto

2. Crie uma Branch para sua Feature (git checkout -b feature/IncrivelFeature)

3. Faça o Commit (git commit -m 'feat: Adiciona IncrivelFeature')

4. Faça o Push (git push origin feature/IncrivelFeature)

5. Abra um Pull Request

## 📝 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.