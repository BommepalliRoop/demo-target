from jinja2 import Template, sandbox  # noqa: F401  sandbox imported for later use, not used yet


def render_greeting(name: str) -> str:
    """Return a greeting for the given name."""
    return Template("Hello {{ name }}!").render(name=name)
