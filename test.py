from parse_dnp import parse

print('>>> Do-Not-Ping Test Suite v1 <<<')
print('-> Testing syntax / error checking:')
matchers = parse(True)

print('')
print('-> Testing parser results:')
def FAIL(msg): print(f'\t[FAIL] {msg}')
def PASS(msg): print(f'\t[PASS] {msg}')

# Matchers
if '559210445991444480' in matchers: PASS('IDs functional')
else: FAIL('IDs are parsed incorrectly')

if '343451476137607179' in matchers: PASS('ping format parsing functional')
else: FAIL('ping-format IDs are parsed incorrectly')

if 'Odd Stranger#7957' in matchers: PASS('username-tags functional')
else: FAIL('username-tag combos are parsed incorrectly')

# Aliases
if 'Odd Stranger#7957' in matchers and matchers['Odd Stranger#7957'] == 'Sophie':
    PASS('aliases functional')
else:
    FAIL('aliases are parsed incorrectly')

print('')
print('-> Testing on a valid file (should be no warnings):')
parse()

print('>>> Testing Complete <<<')
