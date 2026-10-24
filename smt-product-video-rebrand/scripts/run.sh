#!/bin/bash
# Pipeline driver.  SMV_PROJECT=<project dir> [SMV_BATCH=batch1] scripts/run.sh <stage> [slug ...]
# stages: lint | tts | prev | sheet | 4k | qc | thumbs | meta | all
# 4K renders take ~6-8 min per 2-min video on 2 CPUs: run in the background, one or two at a time,
# and keep the session alive until done (background jobs die with the session).
set -e
HERE=$(cd "$(dirname "$0")" && pwd); E=$HERE/smv
: "${SMV_PROJECT:?set SMV_PROJECT}"
stage=$1; shift || true
slugs="$@"
[ -z "$slugs" ] && slugs=$(cd $E && python3 -c "import cfg;print(' '.join(v['slug'] for v in cfg.VIDEOS))")
BATCH=${SMV_BATCH:-$(python3 -c "import json;print(json.load(open('$SMV_PROJECT/project.json')).get('default_batch','batch1'))")}
OUT=$SMV_PROJECT/final/$BATCH
NOPROXY="env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u all_proxy"
render() {  # slug tag
  s=$1; tag=$2; d=$SMV_PROJECT/build/$s/$tag
  rm -rf $d; (cd $E && python3 build.py $s $tag > $SMV_PROJECT/build/$s.$tag.prep.log 2>&1) || { echo "E30 prep failed $s (see $s.$tag.prep.log)"; return 1; }
  (cd $d && bash compose.sh > log.txt 2>&1)
  [ -f $d/done.txt ] || { echo "E31 compose failed $s"; return 1; }
  if [ $tag = 4k ]; then cp $d/out.mp4 $OUT/$(cd $E && python3 -c "import cfg;print(cfg.out_name('$s','mp4'))"); cp $d/subs.srt $OUT/$(cd $E && python3 -c "import cfg;print(cfg.out_name('$s','srt'))"); fi
  echo "$s $tag OK $(date +%T)"
}
case $stage in
  lint)   (cd $E && python3 lint.py) ;;
  tts)    (cd $E && $NOPROXY python3 tts.py $slugs) ;;
  prev)   for s in $slugs; do render $s prev; done ;;
  sheet)  for s in $slugs; do bash $HERE/sheet12.sh $SMV_PROJECT/build/$s/prev/out.mp4 $SMV_PROJECT/build/$s.prev.jpg; echo $SMV_PROJECT/build/$s.prev.jpg; done ;;
  4k)     for s in $slugs; do render $s 4k; done ;;
  qc)     for s in $slugs; do bash $HERE/qc.sh $s; done ;;
  thumbs) (cd $E && python3 thumbs.py $slugs) ;;
  meta)   (cd $E && python3 meta.py 4k) ;;
  all)    $0 lint && $0 tts $slugs && $0 prev $slugs && $0 sheet $slugs && $0 4k $slugs && $0 qc $slugs && $0 thumbs $slugs && $0 meta ;;
  *) echo "unknown stage $stage"; exit 1 ;;
esac
