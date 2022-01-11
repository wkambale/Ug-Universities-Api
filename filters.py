import json
import sys


def _university_filter(src, scope, out):
    """
    Search the data for a single university by name
    :arg src: source dictionary
    :arg scope: source selector
    """

    def filter(entry, item):
        matching = entry["name"]

        if item == matching or item == matching.lower() or item == matching.upper():
            return True

        else:
            return False

    return [entry for entry in src if filter(entry, scope)]


def university_filter(src, scopes):
    """
    Either make multiple data searches or
    execute one. {NEEDS IMPROVEMENT, O(kN) => O(n)}
    :arg src: source dictionary
    :arg scopes: source selectors
    """
    out = []

    if type(scopes) is list:
        [out.extend(_university_filter(src, scope, out)) for scope in scopes]
    else:
        out = _university_filter(src, scopes, out)

    return out


def main():
    args = []
    temp_arg = ""
    first_word = True

    # Retrieve universities (seperated by commas)
    for arg in sys.argv[1:]:
        temp_arg += arg if first_word else " " + arg
        first_word = False

        if arg[-1] == ",":
            args.append(temp_arg[:-1])
            temp_arg = ""
            first_word = True

    if temp_arg:
        args.append(temp_arg)

    if not args:
        return

    # Load the json
    src = None
    with open("./uganda-universities-domains.json") as src_file:
        src = json.load(src_file)

    if src is None:
        return

    # Write the filtered result
    with open("./filtered-uganda-universities-domains.json", "w") as dest_file:
        json.dump(university_filter(src, args), dest_file)


if __name__ == "__main__":
    main()