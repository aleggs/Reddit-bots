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
  for el in lst: # assumes all items in lst are strings
    s.join(list(filter(str.isalnum, el)))
  return s