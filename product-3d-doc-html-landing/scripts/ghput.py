import importlib.util,importlib.machinery,sys,base64,json
ldr=importlib.machinery.SourceFileLoader('apicall','/usr/local/bin/apicall')
spec=importlib.util.spec_from_loader('apicall',ldr); A=importlib.util.module_from_spec(spec); ldr.exec_module(A)
def call(ep,**p):
    s=A.load_spec('github'); base,e,d=A.resolve_endpoint(s,ep)
    params=A.process_params({k:str(v) for k,v in p.items()},e.get('params',{}))
    m,u,h,b=A.build_request(base,e,d,params,{})
    return A.execute_request(m,u,h,b,operation=(e.get('policy') or {}).get('operation'))
if __name__=='__main__':
    owner,repo,path,local,msg=sys.argv[1:6]
    sha=None
    cur=call('contents_get',owner=owner,repo=repo,path=path)
    if isinstance(cur,dict) and cur.get('sha'): sha=cur['sha']
    kw=dict(owner=owner,repo=repo,path=path,message=msg,content=base64.b64encode(open(local,'rb').read()).decode())
    if sha: kw['sha']=sha
    r=call('contents_put',**kw)
    print(json.dumps(r)[:600])
