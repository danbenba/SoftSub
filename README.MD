# 🎬 Ajout de sous-titres soft à un fichier MKV

Ce script Python permet d'intégrer un fichier de **sous-titres `.srt`** en tant que **piste soft-sub** dans une vidéo au format `.mkv`, à l'aide de `mkvmerge` (inclus dans [MKVToolNix](https://mkvtoolnix.download/)).

---

## 📦 Prérequis

- Python 3.7 ou plus
- `mkvmerge` disponible dans le **PATH système** (via [MKVToolNix](https://mkvtoolnix.download/))
- Installer les dépendances Python nécessaires :

```bash
pip install rich tqdm
```

---

## 🛠️ Fonctionnalités

- Détection automatique de `mkvmerge`
- Barre de progression animée et élégante grâce à `rich`
- Confirmation si le fichier de sortie existe déjà
- Ajout de sous-titres **soft-sub** (non gravés dans l’image)
- Langue et nom de piste personnalisables

---

## 🚀 Utilisation

```bash
python soft_sub.py <video.mkv> <sous-titres.srt> <output.mkv> [code_langue] [nom_piste]
```

### 📌 Exemple

```bash
python soft_sub.py "film.mkv" "francais.srt" "film_final.mkv" fra "[French]"
```

- `film.mkv` : fichier vidéo source
- `francais.srt` : fichier de sous-titres
- `film_final.mkv` : nouveau fichier avec les sous-titres intégrés
- `fra` : code de langue (ISO 639-2)
- `[French]` : nom personnalisé pour la piste de sous-titres

---

## ✅ Résultat

- Un fichier `.mkv` avec les sous-titres **intégrés en soft-sub**, que vous pouvez activer ou désactiver dans votre lecteur vidéo (VLC, MPV, etc.).
- Le fichier original n’est **pas modifié**.
- Si le fichier de sortie existe déjà, vous serez invité à confirmer avant son remplacement.

---

## 🧪 Testé avec

- Windows 10 / 11
- Python 3.11
- MKVToolNix v90.0
- Lecteurs : VLC, MPV, Kodi

---

## 🔧 Dépannage

- **mkvmerge introuvable ?**
  > Assurez-vous que MKVToolNix est installé et que le dossier contenant `mkvmerge` est bien dans le `PATH`.

- **Permission refusée ?**
  > Fermez les lecteurs vidéo utilisant le fichier, ou exécutez le terminal en administrateur.

- **Problème d'encodage ?**
  > Vérifiez que votre fichier `.srt` est bien encodé en UTF-8.

---

## 🧠 Notes

- Ce script ajoute uniquement **des sous-titres soft** (non incrustés).
- Pour ajouter plusieurs pistes de sous-titres, le script doit être modifié ou appelé plusieurs fois.

---

## 📜 Licence

Ce projet est open-source — faites-en bon usage !
