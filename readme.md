# 🕹️ Mon Jeu en Python

Bienvenue dans le projet **Mon Jeu en Python** ! Ce jeu est conçu pour offrir une expérience immersive et amusante. Ce README fournit une vue d'ensemble de la structure du projet et des instructions pour exécuter le jeu.

## 🌟 Fonctionnalités du Jeu

- **Gestion des règles du jeu du YINSH** : Profitez d'une expérience de jeu réelle, comme sur un plateau !
- **Jouez contre une IA** : Profitez d'une IA crée par nos soins pour pouvoir jouer contre elle !
- **Multijoueur** : Jouez avec vos amis et défiez-les dans des compétitions palpitantes. (pas completement fonctionnel)

## 📂 Structure du Projet

Le projet comprend 7 fichiers principaux qui assurent le bon fonctionnement du jeu :

Mon_Jeu
│
├── main.py # Fichier principal qui lance le jeu
├── start_interface.py # Gère le démarage de l'interface
├── game_interface.py # Gère la gestion des règles du jeu et celle de l'interface
├── action.py # Contient la logique des deplacements possibles
├── update_game.py # Contient toutes les fonctions qui mettent a jour le jeu / le plateau (deplacement d'un pion (suppression d'un pour en mettre un autre, etc...))
├── valid_move.py # Gère les mouvements possibles des markers / anneaux
└── winning.py # Gère les conditions de victoire.
