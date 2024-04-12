# Project2_BookScrap
 https://openclassrooms.com/fr/paths/879/projects/832/mission
Ce projet python permet de récuperer les données des livres présent sur https://books.toscrape.com/ (Ou sur un site ayant la même configuration).

## Installation
Cloner le projet git.
pip install -requirments.txt

## Utilisation
python main.py [nom_de_dossier]
Démarre le script sur la page https://books.toscrape.com/, parcourt tout les livres présent dans toute les catégories et enregistre leurs données dans un fichier CSV et leur image dans un dossier [nom de dossier] ("scrapped" par défaut si [nom de dossier] n'est pas défini), trié par catégories.