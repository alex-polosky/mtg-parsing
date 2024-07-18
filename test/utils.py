def normalize_for_compare(obj: object) -> dict:
    normed = {}
    for k, v in vars(obj).items():
        match k:
            case '_state':
                cache = vars(v).get('fields_cache')
                if not cache:
                    continue
                for rel, rel_obj in cache.items():
                    normed[rel] = normalize_for_compare(rel_obj)
            case 'id' | 'uuid' | 'created' | 'updated' | 'reported':
                continue
            case s if s.endswith('_id'):
                continue
            case _:
                normed[k] = v
    return normed
