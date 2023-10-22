# Mode d'emploi : Lancement du code

Ce guide vous aidera à exécuter le code sans avoir besoin de télécharger des librairies supplémentaires. Suivez ces étapes simples pour obtenir le code assembleur à partir de votre fichier de test.

## Prérequis

- Assurez-vous que Python est bien installé sur votre ordinateur. Vous pouvez vérifier cela en ouvrant un terminal ou une invite de commande et en tapant :

  ```bash
  python --version
  ```

  Cela devrait afficher la version de Python installée.

## Étapes à suivre

1. **Choisir le fichier de test** : Dans le code, repérez la ligne :

    ```python
    with open('test_1.txt', 'r') as file:
    ```

    Remplacez `'test_1.txt'` par le chemin de votre fichier de test. Par exemple, si vous avez un fichier nommé `mon_test.txt`, modifiez la ligne comme suit :

    ```python
    with open('mon_test.txt', 'r') as file:
    ```

2. **Exécution du code** : Une fois que vous avez modifié le chemin du fichier, exécutez le code. Vous verrez le code assembleur affiché dans la console.

3. **Consulter le résultat** : Outre la console, le code assembleur sera également sauvegardé dans un fichier nommé `resultat.s`. Vous pouvez ouvrir ce fichier avec n'importe quel éditeur de texte pour consulter ou modifier le code assembleur généré.