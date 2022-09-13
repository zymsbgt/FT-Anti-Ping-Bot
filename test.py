from parse_dnp import parse

matchers = parse()

# Matchers
if '559210445991444480' in matchers: print('IDs functional')
else: print('IDs are parsed incorrectly')

if '343451476137607179' in matchers: print('ping format parsing functional')
else: print('ping-format IDs are parsed incorrectly')

if 'Odd Stranger#7957' in matchers: print('username-tags functional')
else: print('username-tag combos are parsed incorrectly')

# Aliases
if 'Odd Stranger#7957' in matchers and matchers['Odd Stranger#7957'] == 'Sophie':
    print('aliases functional')
else:
    print('aliases are parsed incorrectly')
