from pathlib import Path
import os,json,subprocess,gzip,base64,hashlib,zipfile,tempfile,shutil
root=Path.cwd();repo=os.environ['GITHUB_REPOSITORY'];sha=os.environ['GITHUB_SHA'];env=dict(os.environ);env['GH_REPO']=repo;event=json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text());url=event['inputs']['artifact_url'];assert url.startswith('https://release-assets.githubusercontent.com/');print('::add-mask::'+url,flush=True)
def run(args,cwd=None):
 p=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True)
 if p.returncode:raise RuntimeError(args[0]+' failed: '+p.stderr[-1200:].replace(url,'[masked]'))
 return p.stdout
app=root/'assembled';run(['git','init',str(app)]);run(['git','fetch','--depth=1','https://github.com/Chevey339/kelivo.git','b1702b3a9ff35656c682a0818a9b44d8a8b72454'],app);run(['git','checkout','--detach','FETCH_HEAD'],app)
b=''.join(p.read_text().strip() for p in sorted((root/'archive/source-delta').glob('part-*.b64')));patch=root/'source.patch';patch.write_bytes(gzip.decompress(base64.b64decode(b)));run(['git','apply','--index',str(patch)],app);tree=run(['git','write-tree'],app).strip();assert tree=='6f8a7a7a193a2606baf0741827c9550a6359e20a',tree;print('Exact validated application source tree verified:',tree,flush=True)
shutil.copyfile(app/'README.md',app/'README_UPSTREAM.md')
for name in ['README.md','BUILDING_GLASS.md','VALIDATION_GLASS.md']:shutil.copyfile(root/name,app/name)
(app/'tools').mkdir(exist_ok=True)
for p in (root/'archive/build-tools').glob('*.py'):shutil.copyfile(p,app/'tools'/p.name)
files=[]
for p in sorted(app.rglob('*')):
 if '.git' in p.relative_to(app).parts or not p.is_file():continue
 files.append({'path':str(p.relative_to(app)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(app/'SOURCE_MANIFEST.json').write_text(json.dumps({'algorithm':'sha256','source_tree':tree,'files':files},ensure_ascii=False,indent=2)+'\n')
source=root/'Kelivo-Glass-1.3.2-glass13.3-source.zip'
with zipfile.ZipFile(source,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(app.rglob('*')):
  if '.git' not in p.relative_to(app).parts and p.is_file():z.write(p,str(p.relative_to(app)))
with zipfile.ZipFile(source) as z:
 assert z.testzip() is None
 for item in files:assert hashlib.sha256(z.read(item['path'])).hexdigest()==item['sha256']
apk=root/'Kelivo-Glass-1.3.2-glass13.3-arm64.apk';run(['curl','-fsSL','--connect-timeout','20','--max-time','180','-o',str(apk),url]);expected='bfd1053ece7fed49153a26ae0e1a7ac4b9b028c674b858c66843624689233b37';assert apk.stat().st_size==60609994;assert hashlib.sha256(apk.read_bytes()).hexdigest()==expected
rel=json.loads(run(['gh','release','view','glass13.3','--json','id,isDraft,tagName']));assert rel['isDraft'];run(['gh','release','upload','glass13.3',str(apk),str(source),'--clobber'])
with tempfile.TemporaryDirectory() as tmp:
 run(['gh','release','download','glass13.3','--dir',tmp,'--pattern',apk.name,'--pattern',source.name])
 for p in [apk,source]:assert hashlib.sha256((Path(tmp)/p.name).read_bytes()).hexdigest()==hashlib.sha256(p.read_bytes()).hexdigest()
receipt={'source_tree':tree,'docs_commit':sha,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_bytes':source.stat().st_size,'apk_sha256':expected,'apk_bytes':apk.stat().st_size,'files':len(files)+1};(root/'archive-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');run(['gh','release','upload','glass13.3',str(root/'archive-receipt.json'),'--clobber']);print('Both uploaded archives fully downloaded and verified:',json.dumps(receipt),flush=True)
