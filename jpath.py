########################################################################
#
#   jpath-py 
#   An XPath-like querying interface for JSON objects
#
#   author: Vasileios Mitrousis  
#   email: vamitrou@gmail.com
# 
#   The software is given as is, no guarantees from the author
#   Licenced under Apache 2.0 licence
#
########################################################################


debug = False


# This function will accept a JSON document and a path /x/y/z[4]/*
# and will return you the actual value of the key(s)
def get_dict_value(doc, path, leaf=None):
    if len(path.strip()) == 0:
        return doc
    path_splits = path.split('/')
    for i, key in enumerate(path_splits):
        if debug: print 'key processing: ' + key
        if not doc:
            return None

        if '[' in key and ']' in key and i != len(path_splits)-1:
            # array element
            if debug: print 'array element'
            idx = int(key[key.index('[')+1:key.index(']')])
            key = key[:key.index('[')]
            if debug: print 'key stripped: ' + key
            if not doc.get(key):
                return None

            if isinstance(doc[key], list):
                if debug: print 'is an array'
                if idx >= len(doc[key]):
                    # index out of bounds
                    if debug: print 'out of bounds'
                    return None
                doc = doc[key][idx]
            else:
                # single object, accept 0 index only
                if debug: print 'single object'
                if idx > 0:
                    return None
                doc = doc[key]
        elif key == '*':
            # '*' has 2 meanings. The whole array,
            # or the whole object if it is the last key
            if debug: print 'wildcard key'
            if i == len(path_splits) - 1:
                # it is the last element, push the whole object
                if debug: print 'last element'
            else:
                # '*' requires the whole array in this case
                if debug: print 'getting the whole array'
                if isinstance(doc, list):
                    if debug: print 'is type of array'
                else:
                    if debug: print 'is not type of array, constructing it manually'
                    doc = [doc]
                idx = -1
                item_arr = []
                recon_path = '/'.join(path_splits[i+1:])
                if  ']' == recon_path[-1]:
                    # we need indexed result
                    if debug: print 'getting indexed result'
                    idx = int(recon_path[recon_path.index('[')+1:recon_path.index(']')])
                    recon_path = recon_path[:recon_path.index('[')]

                for k, item in enumerate(doc):
                    val = get_dict_value(item, recon_path, leaf)
                    if val:
                        item_arr.append(val)

                if idx != -1:
                    if idx < len(item_arr):
                        return item_arr[idx]
                    return None

                return item_arr
        else:
            if debug: print 'normal key: ' + key
            if isinstance(doc, list):
                if debug: print 'pointing to an array'
                print "Warning: '%s' array was detected but not expected. Returning first item." % path_splits[i-1]
                if len(doc) > 0:
                    doc = doc[0][key]
            else:
                if debug: print 'getting object normaly'
                doc = doc.get(key)

            if i == len(path_splits) - 1:
                if debug: print 'it is the last component'
                if isinstance(doc, list):
                    if debug: print 'it is a list, generate a @Val array'
                    try:
                        doc = [d[leaf] for d in doc if d]
                    except:
                        print "1,", doc
                        #raw_input()
                else:
                    if debug: print 'final object @Val'
                    if doc and leaf:
                        try:
                            doc = doc[leaf]
                        except Exception, e:
                            print 'jpath_error:', e
                            #raw_input()
    return doc


