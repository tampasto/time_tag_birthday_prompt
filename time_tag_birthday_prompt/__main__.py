from . import __doc__ as init_doc, PrimaryPrompt


print(init_doc)

primary_prompt = PrimaryPrompt(tag_end_prompt='')

print('Defined time tags in JSON\n-------------------------', end='')
primary_prompt.print_time_tags()

print('Defined birthdays in JSON\n-------------------------', end='')
primary_prompt.print_birthdays()
