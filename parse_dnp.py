matchers = {}
dup = set()

def warn(msg, line):
    print(f'[warn] {msg} at line {line}')

class Matcher:
    alias = None
    user = None
    iden = None
    def __init__(self, predicatee, line) -> None:
        if len(predicatee) == 0:
            # This should never happen... but just in
            # case a cosmic bit flip or similar occurs,
            raise RuntimeError('null data was passed onto Matcher')

        # Probably in format predicatee=alias
        if '=' in predicatee:
            separator = predicatee.rindex('=')
            alias = predicatee[separator + 1:]
            predicatee = predicatee[:separator]
            self.alias = alias
            pass

        # Probably in format username#0000
        if '#' in predicatee:
            index = predicatee.rindex('#')
            discrim = predicatee[index + 1:]
            name = predicatee[:index]

            # Discriminator must be all base-10 numbers
            if not discrim.isdigit():
                warn(f'discriminator {discrim} was not numeric', line)
                return

            # ...#0000 length check
            if len(discrim) != 4:
                warn(f'discriminator {discrim} too short or long (l={len(discrim)})', line)
                return

            # Usernames can't be shorter than 2 or longer than 32
            if not 2 <= len(name) <= 32:
                warn(f'username {name} too short or long (l={len(name)})', line)
                return
            
            self.user = f'{name}#{discrim}'
            pass # '#' in predicatee

        # If not in previous format and length < 3,
        # it is neither a username-tag combination
        # nor an ID nor a ping format because an ID,
        # <@0..., and <@!... are always >=3
        if len(predicatee) < 3:
            warn(f'line does not follow format (l={predicatee}, expected >=3)', line)
            return
        
        if predicatee[:2] == '<@':
            predicatee = predicatee[2:]

            # Starts with <@!
            if predicatee[0] == '!':
                predicatee = predicatee[1:]

            index = predicatee.find('>')
            # Invalid format <@[!]...
            if index == -1:
                warn(f'ping format does not close angle brackets', line)
                return

            # ID did not match \d{17, 18}
            identifier = predicatee[:index]
            if not identifier.isdigit() or not 17 <= len(identifier) <= 18:
                warn(f'ping format has invalid id (not all digits or not 17 <= length <= 18)', line)
                return

            self.iden = identifier
            pass # == '<@'

        if not self.iden and not self.user:
            if not predicatee.isdigit() or not 17 <= len(predicatee) <= 18:
                warn(f'id-only format has invalid id (not all digits or not 17 <= length <= 18)', line)
                return
            
            self.iden = predicatee
            pass

        if self.iden != None and self.user != None:
            warn('identifier and user are both set', line)
            self.alias = None
            self.iden = None
            self.user = None
            return

        if self.iden or self.user:
            thing = self.iden or self.user
            if thing in dup:
                warn(f'duplicate entry {thing} detected', line)
                self.alias = None
                self.iden = None
                self.user = None
                return
            
            dup.add(thing)
            return # Passed all checks

        warn('format not recognized', line)
        pass #__init__

def parse():
    with open('do-not-ping.txt', 'r') as dnp:
        lines = [x.strip() for x in dnp.readlines()]
        for index in range(len(lines)):
            line = lines[index]
            if line.find('#') == 0 or len(line) == 0:
                continue

            matcher = Matcher(line, index + 1)
            thing = matcher.iden or matcher.user
            if thing:
                matchers[thing] = matcher.alias
                continue
        pass
    return matchers
