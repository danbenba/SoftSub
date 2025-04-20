#!/usr/bin/env python3
import subprocess
import sys
import shutil
import re
import os

from rich import print as rprint
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.prompt import Confirm
import logging

print("------------------------------------")
print ("Custom SoftSub MKVToolNix")
print ("Version 1.1 - danbenba Productions")
print("------------------------------------")

# CHEMIN PERSONNALISÉ VERS MKVMERGE (définir ici si binaire hors PATH)
# Exemple : "/usr/local/bin/mkvmerge"
MKVMERGE_PATH = None  # ou chemin complet vers mkvmerge

# Console et logger
console = Console()
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("soft_sub")

def add_soft_subtitle(
    input_mkv: str,
    subtitle_file: str,
    output_mkv: str,
    lang_code: str = "fra",
    track_name: str = "[French]",
    mkvmerge_exe: str = None
):
    # Détermine l'exécutable mkvmerge à utiliser
    exe = mkvmerge_exe or MKVMERGE_PATH or shutil.which("mkvmerge")
    if not exe or not shutil.which(exe) and not os.path.isfile(exe):
        logger.error("❌ mkvmerge introuvable : installez MKVToolNix, ajoutez-le au PATH, ou définissez MKVMERGE_PATH.")
        sys.exit(1)

    # Vérification et confirmation d'écrasement
    if os.path.exists(output_mkv):
        if not Confirm.ask(f"Le fichier [bold]{output_mkv}[/] existe déjà. Voulez-vous l'écraser ?"):
            logger.info("❌ Opération annulée par l'utilisateur.")
            sys.exit(0)
        try:
            os.remove(output_mkv)
            logger.info(f"🗑️  Ancien fichier supprimé : {output_mkv}")
        except Exception as e:
            logger.error(f"❌ Impossible de supprimer le fichier existant : {e}")
            sys.exit(1)

    # Construction de la commande mkvmerge
    cmd = [
        exe,
        "-o", output_mkv,
        input_mkv,
        "--language", f"0:{lang_code}",
        "--track-name", f"0:{track_name}",
        subtitle_file
    ]

    logger.info(f"\n🔧 Démarrage du muxing de [bold]{input_mkv}[/] avec [bold]{subtitle_file}[/]\n")
    logger.debug(f"Commande complète : {' '.join(cmd)}")

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    prog_re = re.compile(r"Progress: (\d+(?:\.\d+)?)%")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=20),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task("Muxing…", total=100)
        for line in proc.stderr:
            m = prog_re.search(line)
            if m:
                percent = float(m.group(1))
                progress.update(task, completed=percent)
        proc.wait()

    if proc.returncode != 0:
        logger.error(f"❌ Erreur durant le muxing (code {proc.returncode})")
        sys.exit(proc.returncode)

    console.print(f"\n✅ Sous‑titres soft ajoutés dans [bold green]{output_mkv}[/]\n")


if __name__ == "__main__":
    argc = len(sys.argv)
    if not (4 <= argc <= 7):
        rprint("[bold yellow]Usage :[/] python soft_sub.py input.mkv subtitles.srt output.mkv [lang_code] [track_name] [mkvmerge_path]")
        rprint("Exemple : python soft_sub.py film.mkv subs.srt film_out.mkv fra \"[French]\" /usr/local/bin/mkvmerge")
        sys.exit(1)

    input_mkv  = sys.argv[1]
    subtitle   = sys.argv[2]
    output_mkv = sys.argv[3]
    lang_code  = sys.argv[4] if argc >= 5 else "fra"
    track_name = sys.argv[5] if argc >= 6 else "[French]"
    mkvmerge_path = sys.argv[6] if argc == 7 else None

    add_soft_subtitle(input_mkv, subtitle, output_mkv, lang_code, track_name, mkvmerge_path)
