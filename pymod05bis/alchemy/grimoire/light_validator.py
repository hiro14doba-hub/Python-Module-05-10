def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients

    allowed = light_spell_allowed_ingredients()
    lower_ingredients = ingredients.lower()

    if any(item in lower_ingredients for item in allowed):
        return f"{ingredients} VALID"
    return f"{ingredients} INVALID"
