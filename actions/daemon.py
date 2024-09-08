import subprocess
import os
import signal
import psutil
import threading
import time

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "daemon",
            "author": "Kai",
            "version": "0.7",
            "features": [],
            "group": "",
            "description": "",
        }

    def __help__(self, ctx):
        return """
            Daemon manager.

            start <name>
            send <name> <text>
            list
        """

    def find_process_by_name(self, process_name):
        """
        Find a running process by name.

        :param process_name: The name of the process to find (case-insensitive).
        :return: A list of psutil.Process objects matching the name.
        """
        found_processes = []
        for proc in psutil.process_iter(['name', 'exe', 'cmdline']):
            if proc.info.get("cmdline"):
                if len(proc.info["cmdline"]) == 2:
                    dn = proc.info["cmdline"][1].split("/")[-1]
                    if proc.info["cmdline"][0] == self.ctx.touch_config("system.runner", "python3") and process_name == dn:
                        found_processes.append(proc)

            try:
                # Check if process name matches
                if process_name.lower() in proc.name().lower():
                    found_processes.append(proc)
                elif proc.exe():
                    # Check if the executable name matches
                    if process_name.lower() in proc.exe().lower():
                        found_processes.append(proc)
                elif proc.cmdline():
                    # Check if the command line contains the process name
                    if any(process_name.lower() in cmd.lower() for cmd in proc.cmdline()):
                        found_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return found_processes

    def __run__(self, ctx):
        cmd, ln = ctx.cmdsplit()
        ddir = ctx.aos_dir+"daemons/"
        ldir = ctx.aos_dir+"logs/"

        if not os.path.exists(ddir):
            return ctx.writeln("Daemon directory does not exist.")

        if not os.path.exists(ldir):
            os.mkdir(ldir)

        procs = ctx.get_data()

        match cmd:
            case "list" | "ls":
                p = ctx.touch_config("daemon.names", [])

                for filename in os.listdir(ddir):
                    dn = filename.split(".")[0]
                    if dn in p:
                        #ctx.writeln(f"[yellow]{filename}[/yellow] (Running (Test query))")
                        prs = self.find_process_by_name(filename)
                        #print(prs)
                        if len(prs) > 0:
                            ctx.writeln(f"[green]{filename}[/green] (Running)")
                        else:
                            ctx.writeln(f"[red]{filename}[/red] (Dead)")
                            p.remove(dn)
                            if os.path.exists(f"/tmp/{dn}"):
                                os.remove(f"/tmp/{dn}")
                                ctx.writeln("Cleaning up", f"/tmp/{dn}")
                            ctx.set_config("daemon.names", p)
                    else:
                        ctx.writeln(f"[yellow]{filename}[/yellow] (Not running)")

            case "run" | "start":
                if " " in ln: return self.writeln("Spaces not allowed.")
                if not ln: return self.writeln("No name given.")
                ctx.run_daemon(ln)

            case "log":
                pass

            case "send" | "talk" | "say":
                if " " not in ln:
                    return ctx.writeln("Invalid format, requires: <daemon_name> <text>")

                dname = ln.split(" ")[0]
                text = " ".join(ln.split(" ")[1:])

                def got_reply(text):
                    ctx.write_panel(f"{text}", dname)
                    ctx.end_pipe_listen()

                ctx.get_pipe_reply(dname, text, got_reply)

            case "stop" | "kill":
                pass #TODO maybe do the same as ls finding the process and use psutil to kill, then cleanup tmp?

        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass
