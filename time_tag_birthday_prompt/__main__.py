from . import __doc__ as init_doc, package_name, __version__, PrimaryPrompt
import argparse


def print_birthdays():
    print('Defined birthdays in JSON\n=========================', end='')
    primary_prompt.print_birthdays()


def print_time_tags():
    print('Defined time tags in JSON\n=========================', end='')
    primary_prompt.print_time_tags()


parser = argparse.ArgumentParser(
    prog=package_name,
    description=('Add time tags to interactive mode prompt and birthday '
                 'reminders to Python startup.')
    )
parser.add_argument(
    '-v', '--version', action='store_true',
    help='Version information.'
    )
parser.add_argument(
    '-t', '--time-tags', action='store_true',
    help='Show all time tags defined in JSON.'
    )
parser.add_argument(
    '-b', '--birthdays', action='store_true',
    help='Show all birthdays defined in JSON.'
    )
parser.add_argument(
    '-d', '--doc', action='store_true',
    help='Show package documentation.'
    )
args = parser.parse_args()


prepend = '\n'
primary_prompt = None

if args.version:
    print(f'\n{package_name} {__version__}')
    prepend = '\n'

if args.time_tags:
    print(prepend, end='')
    primary_prompt = PrimaryPrompt(tag_end_prompt='')
    print_time_tags()
    prepend = ''

if args.birthdays:
    print(prepend, end='')
    if not primary_prompt:
        primary_prompt = PrimaryPrompt(tag_end_prompt='')
    print_birthdays()
    prepend = ''

if args.doc:
    print(prepend, end='')
    if not primary_prompt:
        primary_prompt = PrimaryPrompt(tag_end_prompt='')
    print('Documentation\n=============')
    print(init_doc.strip())
    prepend = ''

if not (args.version or args.time_tags or args.birthdays or args.doc):
    print()
    parser.print_help()
