def formatar_reais(valor):
    """Formata um valor numérico como moeda brasileira, por exemplo R$ 1.250,00."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"