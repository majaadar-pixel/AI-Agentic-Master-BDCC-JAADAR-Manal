# Fondamentaux des systemes RAG

Un systeme RAG, ou Retrieval-Augmented Generation, combine un moteur de recherche documentaire avec un modele de langage. Le principe est de recuperer des passages pertinents dans une base de connaissances puis de les fournir au modele pour produire une reponse contextualisee.

Les etapes principales sont la collecte des documents, le nettoyage, le decoupage en fragments, la vectorisation, l'indexation, la recherche et la generation. Le decoupage doit conserver assez de contexte pour que les passages soient utiles, tout en restant assez court pour eviter le bruit.

La vectorisation transforme les textes en representations numeriques. Dans un prototype local, une vectorisation TF-IDF peut suffire pour des corpus pedagogiques. Dans un systeme de production, on utilise souvent des embeddings denses specialises.

Un bon RAG cite ses sources, limite les hallucinations et reconnait les limites de son corpus. Il doit aussi mesurer la pertinence des documents recuperes et la fidelite de la reponse.
