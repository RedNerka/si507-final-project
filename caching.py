import json

def openCache(CACHENAME):
    try:
        cache_file=open(CACHENAME, 'r')
        cache_contents=cache_file.read()
        cache_dict=json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict={}
    return cache_dict

def writeCache(cache_dict,CACHENAME):
    dumped_cache=json.dumps(cache_dict)
    fw=open(CACHENAME,"w")
    fw.write(dumped_cache)
    fw.close() 