import sys

from packages import Package, parse

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'usage: %s old new' % sys.argv[0]
        sys.exit(1)

    old = parse(sys.argv[1])
    new = parse(sys.argv[2])

    # we only care about the package name for new and missing packages
    Package.compare = Package.COMPARE_NAME
    new_packages = new - old
    missing_packages = old - new
    in_both = old.intersection(new)

    changes = {}

    # we want to compare versions for upgrades
    Package.compare = Package.COMPARE_VERSION
    changes['version'] = in_both - old

    # now states
    Package.compare = Package.COMPARE_STATE
    changes['state'] = in_both - old

    # now arch
    Package.compare = Package.COMPARE_ARCH
    changes['arch'] = in_both - old

    if new_packages:
        print 'New packages:'
        for p in new_packages:
            print ' * %s (%s)' % (p.name, p.version)
        print ''

    if missing_packages:
        print 'Packages now absent:'
        for p in missing_packages:
            print ' * %s' % p.name
        print ''

    for member, packages in changes.items():
        if packages:
            print '%s changed:' % member.title()
            for p in packages:
                o = old.lookup(p)
                print ' * %s (now %s, was %s)' % (p.name, getattr(p, member), getattr(o, member))
            print ''
