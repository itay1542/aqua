def merge_dicts(source, dest):
    for key, value in source.items():
        if isinstance(value, dict):
            deep_val = dest.setdefault(key, {})
            merge_dicts(value, deep_val)
        elif isinstance(value, list):
            deep_val = dest.setdefault(key, [])
            merge_lists(value, deep_val)
        else:
            if dest.setdefault(key, value) != value:
                dest[key] = [dest[key], value]
    return dest


def merge_lists(source_list, dest):
    for item in source_list:
        if __is_last_hierarchy(item) or not isinstance(item, dict) or len(dest) == 0:
            dest.append(item)
        elif isinstance(item, dict):
            to_append = []
            for i, dest_item in enumerate(dest):
                if __are_keys_mergeable(item, dest_item):
                    dest[i] = merge_dicts(item, dest_item)
                else:
                    to_append.append(item)
            dest.append(to_append) if len(to_append) > 0 else None


def __is_last_hierarchy(target_dict):
    for value in target_dict.values():
        return not isinstance(value, list) and not isinstance(value, dict)


def __are_keys_mergeable(source_dict, dest_dict):
    return set(source_dict.keys()).issubset(dest_dict.keys())
