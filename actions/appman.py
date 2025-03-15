import os, json, subprocess, shutil, sys, textwrap, re, requests
from thefuzz import fuzz, process
import shlex, importlib
import importlib.util as ilu
from urllib.parse import urlparse

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "appman",
            "author": "Kaiser",
            "version": "0.0",
            "features": [],
            "group": "system",
    }

    def __help__(self, ctx):
        return """ App Manager
        Commands:
            run <appname>
                Runs the command specified.

            show <appname>
                Show information on app.

            list
                Print list of known applications

            edit
                Open list in code editor

            dirs
                Show directory list

            launchers
                Show launcher list"""

    def __run__(self, ctx):
        cmd, line = ctx.cmdsplit()

        data = ctx.get_data("appman", fmt="toml")

        min_match = ctx.touch_config("appman.min_match", 90)
    
        match cmd:
            case "run":
                def run_app(name, *args):
                    if name == "appman": return ctx.writeln("Infinite recursion!")
                    
                    app = ctx.get_data(name, fmt="toml")
                    cwd = app.get("cwd") or os.getcwd()
                    launcher = app.get('launcher') or None
                    if launcher == None: return ctx.writeln("No launcher specified.")
                    
                    args = list(app.get("args", [])) + list(args)
                    print("Running", name, args)
                    
                    p = None
                    try:
                        p = subprocess.run([launcher, *args], cwd=cwd)
                    except PermissionError:
                        ctx.writeln("Permissions Error: Could not run application.")

                    if p != None:
                        if ctx.touch_config("appman.show_result"):
                            ctx.writeln(f":right_arrow: Application exit: [blue]{p.args}[/blue] (Return code: "+str(p.returncode)+")")
                    
                to_run = line.split(" ")[0]
            
                matches = []

                for filename in os.listdir(ctx.data_path()):
                    fmt = filename.split(".")[0]
                    m = fuzz.ratio(line.lower(), fmt.lower())

                    if min_match < m or fmt.lower().startswith(to_run.lower()) or \
                    to_run.lower() in fmt.lower():
                        matches.append(fmt)

                args = ctx.lines[2:]

                if len(matches) == 0:
                    ctx.say("No matches found.")

                elif len(matches) == 1:
                    ctx.writeln(f":right_arrow: Launching {matches[0]}")
                    run_app(matches[0], *args)

                else:
                    ctx.say("Too many matches, select one: ")
                    for i, m in enumerate(matches):
                        ctx.writeln(f"{i}. {m}")

                    app = ctx.g.choose("Select: ", *matches)
                    ctx.writeln(f":right_arrow: Launching {app}")
                    run_app(app, *args)

            case "get":
                def download(url):
                    if url != "Cancel" and url != "":
                        ctx.writeln(f":right_arrow: Preparing download of {url}")
                        filename = os.path.basename(urlparse(url).path)
                        ctx.writeln(f":right_arrow: Filename: {filename}")

                        dl_path = data["Paths"].get("Download Path") or "~/Downloads"
                        dl_path = os.path.expanduser(dl_path)
                        if os.path.exists(dl_path+"/"+filename):
                            ctx.writeln(":right_arrow: File already exists, skipping download.")
                        else:
                            ctx.writeln(f":right_arrow: Downloading file in to {dl_path}")
                            exit_code = ctx.download_file(url, dl_path+"/"+filename)
                            if exit_code == 0:
                                ctx.writeln(f":right_arrow: Saved to {dl_path}{filename}")

                        ext = os.path.splitext(filename)[1][1:]
                        ctx.writeln(f":right_arrow: Finding installer recipe for {ext}...")

                        cmd = data.get("Executables", {}).get(ext)
                        if cmd:
                            cmd = cmd.replace("%FILE%", f"{dl_path}/{filename}").replace("//", "/")
                            ctx.writeln(f":right_arrow: Running {cmd}")
                            exit_code = ctx.subproc(cmd)
                            if exit_code == 0 and os.path.exists(f"{dl_path}/{filename}"):
                                ctx.writeln(f":right_arrow: Deleting download file")
                                os.remove(f"{dl_path}/{filename}")
                        else:
                            ctx.writeln(f":right_arrow: No executor found for {cmd}")



                if line == "appman": print("You already have this.")
                d = ctx.get_data(line, fmt = "toml", skip_validate = True)
                if not d: return ctx.writeln("Recipe not found.")

                if d.get("protocol", "direct") == "html":
                    if not d.get("url"): return ctx.writeln("Recipe is missing a `url` key.")
                    if not d.get("filetype"): return ctx.writeln("Recipe is missing a `filetype` key to filter scanned files.")
                    url = d['url']
                    filetype = d['filetype']
                    ctx.writeln(f"Searching {url} for {filetype} files.")
                    content = requests.get(url).text
                    urls = re.findall(rf'https?://\S+\.{filetype}', content)

                    if len(urls) == 0:
                        ctx.writeln("No matching files found in service.")
                    elif len(urls) == 1:
                        download(urls[0])
                    else:
                        urls.append("Cancel")
                        download(ctx.g.choose("Multiple files found, choose one:", *urls))

                elif d.get("protocol", "direct") == "direct":
                    if not d.get("url"): return ctx.writeln("Recipe is missing a `url` key.")
                    url = d['url']
                    v = ctx.get_flag("v") or d['version']
                    download(url.replace("%version%", v))

            case "edit":
                if line != "":
                    ctx.edit_code(ctx.data_path()+line+".toml")
                else:
                    ctx.edit_code(ctx.data_path()+"appman.toml")

            case "list" | "ls":
                for filename in os.listdir(ctx.data_path()):
                    ctx.writeln("* "+filename)


        return ctx
