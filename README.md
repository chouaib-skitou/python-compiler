
# Mode d'emploi : Lancement du code

Ce guide vous aidera à exécuter le code sans avoir besoin de télécharger des librairies supplémentaires. Suivez ces étapes simples pour obtenir le code assembleur à partir de votre fichier de test.

## Prérequis

- Assurez-vous que Python est bien installé sur votre ordinateur. Vous pouvez vérifier cela en ouvrant un terminal ou une invite de commande et en tapant :

  ```bash
  python --version
  ```

  Cela devrait afficher la version de Python installée.

## Étapes à suivre

1. **Exécution du code avec le fichier de test** : Pour compiler un fichier, utilisez la commande suivante dans votre terminal ou invite de commande, en remplaçant `nom_du_fichier.c` par le chemin de votre fichier de test :

   ```bash
   python chemin_vers_main.py nom_du_fichier.c
   ```

   Par exemple, si vous souhaitez compiler `test_1.c` et que votre script est situé à `c:\Users\pc_su\Desktop\Polytech Paris-Saclay\APP4\Compilation\python-compiler\main.py`, utilisez :

   ```bash
   python -u "c:\Users\pc_su\Desktop\Polytech Paris-Saclay\APP4\Compilation\python-compiler\main.py" test_1.c
   ```

2. **Consulter le résultat** : Après exécution, le code assembleur sera afficher dans la console.

