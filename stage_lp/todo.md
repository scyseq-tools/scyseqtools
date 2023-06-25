- redimensionnement des fenêtres (low)
- Fichier de config (low)

- Dans certains modules il y a la variable `application` or on peut utiliser à
  la place `_root()`. Voir ce qui est le plus cohérent et ne pas utiliser les
deux. Faire un choix et homogénéiser (à mon sens plutôt `_root()` tant que l'on
est dans le fonctionnement "bas niveau") Je viens d'essayer mais ça ne semble
pas si simple que ça...

- Dans `encoder` j'ai ajouté des `FIXME` à voir...

- Dans `PlayerControl` il me semble qu'il y a des variables qui sont liées à
  l'application mais qu'elle devraient être plutôt locales au player. Le `mode`
par exemple, c'est bien un état du player et pas de l'application. Comme pour le
temps. Ça devrait être le player qui envoie les info à l'appli et pas le
contraire...
