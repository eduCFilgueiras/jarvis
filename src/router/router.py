DEV_KEYWORDS = ("codigo", "código", "programacao", "programação", "bug", "projeto")


def route(text: str) -> str:
    input_text = text.lower()

    if any(keyword in input_text for keyword in DEV_KEYWORDS):
        return "dev"

    return "general"
