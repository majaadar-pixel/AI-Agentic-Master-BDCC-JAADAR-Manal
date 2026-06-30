# Architecture du projet

Le projet est organise autour d'un corpus local, d'un index vectoriel et d'un graphe LangGraph. Le corpus est place dans `data/docs`. L'index est construit au demarrage a partir des fichiers Markdown.

Le state du graphe contient la question, la requete de recherche, les documents recuperes, le score de pertinence, la reponse, les sources, le nombre d'iterations et l'historique memoire.

Les noeuds principaux sont `plan`, `retrieve`, `grade`, `rewrite`, `generate` et `finalize`. Le noeud `grade` decide si les documents sont suffisants. Si le score est faible, le graphe passe par `rewrite` puis relance la recherche.

Cette architecture respecte l'approche Agentic RAG car elle utilise des outils, une decision conditionnelle, une memoire et une boucle de correction au lieu d'une simple chaine lineaire.
