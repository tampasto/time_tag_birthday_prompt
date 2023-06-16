from . import __doc__, PrimaryPrompt


print(__doc__)

print('\nDefined birthdays:')
primary_prompt = PrimaryPrompt()
primary_prompt.print_birthdays()

print('\nDefined time tags:')
primary_prompt.print_time_tags()
