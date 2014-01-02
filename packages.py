class Package:
    COMPARE_NAME = 1
    COMPARE_VERSION = 2
    COMPARE_STATE = 4
    COMPARE_ARCH = 8
    COMPARE_ALL = COMPARE_NAME | COMPARE_VERSION | COMPARE_STATE | COMPARE_ARCH

    compare = COMPARE_ALL

    def __init__(self, name, version, state, arch):
        self.name = name
        self.version = version
        self.state = state # probably should be more than a string
        self.arch = arch

    def __repr__(self):
        return 'Package(name=%s, version=%s, state=%s, arch=%s)' % (self.name, self.version, self.state, self.arch)

    def __hash__(self):
        cls = self.__class__
        tohash = [self.name]

        if cls.compare & cls.COMPARE_VERSION:
            tohash.append(self.version)

        if cls.compare & cls.COMPARE_STATE:
            tohash.append(self.state)

        if cls.compare & cls.COMPARE_ARCH:
            tohash.append(self.arch)

        return hash(tuple(tohash))

    def __eq__(self, b):
        cls = self.__class__

        if self.name != b.name:
            return False

        if cls.compare & cls.COMPARE_VERSION \
          and self.version != b.version:
            return False

        if cls.compare & cls.COMPARE_STATE \
          and self.state != b.state:
            return False

        if cls.compare & cls.COMPARE_ARCH \
          and self.arch != b.arch:
            return False

        return True

class Packages(list):
    def intersection(self, other):
        return self.__class__(set(self).intersection(other))

    def __sub__(self, other):
        return self.__class__(set(self).difference(other))

    def lookup(self, other):
        for package in self:
            if package.name == other.name:
                return package

        return None

def parse(filename):
    f = open(filename, 'r')

    out = []
    for line in f.readlines():
        if not line[0].isalpha() or line[0].isupper():
            continue

        parts = line.split()
        state = parts[0]
        name = parts[1]
        version = parts[2]
        arch = parts[3]

        out.append(Package(name, version, state, arch))

    f.close()

    return Packages(out)
