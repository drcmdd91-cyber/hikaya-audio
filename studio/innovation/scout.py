#!/usr/bin/env python3
"""Read-only GitHub discovery. Produces candidate reports; never installs code."""
import datetime,json,os,pathlib,urllib.parse,urllib.request
BASE="https://api.github.com/search/repositories"
def search(q,limit,token):
    params=urllib.parse.urlencode({"q":q+" archived:false","sort":"updated","order":"desc","per_page":limit})
    req=urllib.request.Request(BASE+"?"+params,headers={"Accept":"application/vnd.github+json","User-Agent":"hikaya-innovation-scout",**({"Authorization":"Bearer "+token} if token else {})})
    with urllib.request.urlopen(req,timeout=25) as r:return json.load(r).get("items",[])
def main():
    base=pathlib.Path(__file__).parent
    config=json.loads((base/"queries.json").read_text())
    output=pathlib.Path(os.environ.get("SCOUT_OUTPUT","studio/innovation/reports"))
    output.mkdir(parents=True,exist_ok=True)
    token=os.environ.get("GH_TOKEN","")
    results={}; errors=[]
    for query in config["queries"]:
        try:
            for r in search(query,config["max_results_per_query"],token):
                if r.get("stargazers_count",0)<config["min_stars"]:continue
                name=r["full_name"]
                results[name]={"repository":name,"url":r["html_url"],"description":r.get("description"),"stars":r.get("stargazers_count",0),"updated_at":r.get("updated_at"),"license_spdx":(r.get("license") or {}).get("spdx_id","UNVERIFIED"),"found_by":query,"status":"CANDIDATE_UNTESTED","commercial_use":"UNVERIFIED","arabic_support":"UNVERIFIED","security_review":"PENDING","benchmark":"PENDING"}
        except Exception as e:errors.append({"query":query,"error":str(e)})
    ranked=sorted(results.values(),key=lambda r:(r["stars"],r["updated_at"] or ""),reverse=True)
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report={"generated_at":stamp,"candidates":ranked,"errors":errors,"note":"Discovery only; licenses and capabilities not verified"}
    (output/"latest.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    lines=["# Innovation scout — "+stamp,"","Candidates are **not installed or verified**.",""]
    for r in ranked:lines.append(f"- [{r['repository']}]({r['url']}) — ★{r['stars']} — license: {r['license_spdx']} — {r['found_by']}")
    if errors:lines+=["","## Search errors"]+[f"- {e['query']}: {e['error']}" for e in errors]
    (output/"latest.md").write_text("\n".join(lines)+"\n")
    print(f"Found {len(ranked)} candidates, {len(errors)} search errors")
    if errors and not ranked:raise SystemExit(1)
if __name__=="__main__":main()
