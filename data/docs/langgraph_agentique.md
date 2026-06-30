# LangGraph et approche agentique

LangGraph permet de construire des applications LLM sous forme de graphe d'etats. Chaque noeud realise une action precise, par exemple analyser la question, rechercher des documents, evaluer les resultats, reformuler la requete ou generer une reponse.

Contrairement a un agent pret a l'emploi, un graphe explicite rend la boucle de raisonnement controlable. Le developpeur definit le state, les transitions, les conditions d'arret et la memoire. Cette approche facilite le debogage, l'evaluation et l'ajout d'outils.

Dans un Agentic RAG, l'agent ne se contente pas d'une recherche unique. Il peut planifier, choisir un outil, verifier si le contexte est suffisant, relancer une recherche avec une requete reformulee, puis produire une reponse argumentee.

La memoire peut conserver l'historique des questions, les documents deja recuperes et les decisions prises par le graphe. Elle permet d'ameliorer les conversations multi-tours.
