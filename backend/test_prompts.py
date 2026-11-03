from backend.app.prompts.templates import get_prompt


modes = [
    "simple",
    "exam",
    "lab",
    "viva",
    "detailed"
]

for mode in modes:

    prompt = get_prompt(mode)

    print("\n" + "=" * 40)
    print("MODE:", mode.upper())
    print("=" * 40)

    print(prompt)

print("\nAll prompt modes loaded successfully!")
