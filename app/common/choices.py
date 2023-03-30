from model_utils import Choices

TYPE_USER = Choices(
    ("admin", "Administrador"),
    ("customer", "Cliente"),
)

TYPE_STATUS = Choices(
    ("active", "Ativo"),
    ("draft", "Rascunho"),
    ("inactive", "Desativado"),
)

TYPE_DOC = Choices(
    ("cpf", "CPF"),
    ("cnpj", "CNPJ"),
    ("foreing", "Estrangeiro"),
)

STATUS_COMMENT = Choices(
    ("published", "Aprovado"),
    ("review", "Em Revisão"),
    ("blocked", "Bloqueado"),
)
