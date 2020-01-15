def flatten(lst):
    out = []
    for item in lst:
        if isinstance(item, (list, tuple)):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out


def remove_dupes(lst):
    new_lst = []
    [new_lst.append(i) for i in lst if i not in new_lst]
    return new_lst


# turns a list of strings into one alphanumeric string
def list_to_alnum(lst):
    s = ""
    for el in lst:  # assumes all items in lst are strings
        s.join(list(filter(str.isalnum, el)))
    return s


def remove_spaces(string):
    return "".join(filter(lambda x: x != " ", string))


def to_alnum(string):
    return "".join(filter(str.isalnum, string))


def all_in_one(lst):
    lst = remove_dupes(flatten(lst))
    lst = [to_alnum(item) for item in lst]
    return lst


def list_to_string(lst):
    return "".join(lst)


def title_filter(title, brands, models):
    title = remove_spaces(title)
    brand, model = '', ''
    for br in brands:
        if br.lower() in title.lower():
            brand = br
    for mdl in models:
        if mdl.lower() in title.lower():
            model = mdl
    return (brand, model)
            