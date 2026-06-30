# Limites et securite des RAG

Un RAG reduit les hallucinations mais ne les supprime pas. Le modele peut mal interpreter un passage, ignorer une source importante ou melanger des informations incompatibles.

Les risques principaux sont l'injection de prompt dans les documents, l'exposition d'informations sensibles, la recuperation de documents non pertinents et la confiance excessive dans une reponse fluide.

Pour limiter ces risques, il faut filtrer les documents, separer les instructions systeme du contenu documentaire, citer les sources et refuser de repondre quand le corpus ne contient pas l'information.

Les pistes d'amelioration incluent des embeddings plus puissants, un reranker, une evaluation humaine, une meilleure observabilite et une politique de securite documentaire.
