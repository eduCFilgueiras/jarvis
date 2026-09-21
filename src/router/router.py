DEV_KEYWORDS = (
    "codigo",
    "código",
    "programacao",
    "programação",
    "bug",
    "corrigir",
    "implementar",
    "alterar arquivo",
    "escrever arquivo",
    "executar teste",
)


def route(text: str) -> str:
    input_text = text.lower()

    if any(keyword in input_text for keyword in DEV_KEYWORDS):
        return "dev"

    return "general"
