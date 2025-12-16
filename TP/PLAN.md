# Tests unitaires

## Tests sur PointSet
- accepter les pointSet vide sans produire d'erreurs et dans ce cas verifier si la valeur des 4 premiers bytes est égal à 0 


### tests sur les ajouts et modifications

- verifier que la mise à jours du header se fait correctement apres l'ajout d'un point

- verifier que l'ajout d'un point se fait correctement 

- verifier que lors de la suppression d'un point les 4 premiers bytes se mettent correctemetn à jours 

- verifier que l'ajout d'un point se fait correctement 

- verifier que la modification d'une coordonnée est bien prise en compte 

- verifier si supprimer tout les points donne un set vide avec les 4 premiers bytes à 0 

### tests sur le contenu du set

- verifier si les nombres negatifs sont conservés lors de l'ajout 

- verifier que les 4 premiers bytes correspondent reelement au nombre de points 

- Verifier que le code refuse les valeurs impossibles 



## Tests sur Triangle (structure) 

- verifier que pour un enssemble de triangle vide les 4 premiers bytes des sommets et des triangles peuvent etres a 0 sans produire d'erreurs 

- verifier que le nombre de sommets corresppond bien au nombre de sommets encodés (4*3*nb triangles)

- verifier que les 4 premeirs bytes correspondent bien au nombre de triangles 

- verifier qu'il ne reste pas d'octets en trop apres le dernier triangle

### tests sur les indices de triangles 

- verifier que les points des triangles pointent bien vers des sommets existants 

- verifier que les triangles avec deux fois le meme sommet sont refuser 

- verifier que les points ne sont pas alignés 

### tests sur les ajouts et modifications

- verifier que la mise à jours du header se fait correctement apres l'ajout d'un point

- verifier que l'ajout d'un point se fait correctement 

- verifier que lors de la suppression d'un point les 4 premiers bytes se mettent correctemetn à jours 

- verifier que l'ajout d'un sommet se fait correctement 

- verifier que la modification d'une coordonnée est bien prise en compte 

- verifier si supprimer tout les sommets donne un set vide avec les 4 premiers bytes à 0 


## Tests sur Triangulator 

- verifier que pour 3 points non alignés il retourne un triangle correct

- verifier que pour 3 points alignés il retourne une ligne droite 

- verifier que pour un pointSet vide il retourne une liste vide de Triangle sans erreur 

- verifier qu'il ne prenne pas en compte les valeurs impossibles 


# Tests de performance 

## PointSet
- verifier que la lecture d'un pointSet trop grand se fait dans un temps raisonnable 

- veriffier que un pointSet trop grand ne provque pas d'erreur de mémoire 

- verifier que les performances restent stables meme apres plusiers executions 

## Triangulator
- verifier que pour un ensemble de points de taille moyenne la triangulation se fait dans un temps raisonnable

- verifier que la triangumation ne fait pas exploser l'utilisation de la mémoire 

- verifier que les performances restent stables meme apres plusiers executions 

# Tests d'integration

- verifier que lorsque le client envoie un ensemble de points, le PointSetManager les enregistre, le Triangulator les récupere, effectue la triangulation et renvoie bien le résultat attendu

- verifier que les résultats du Triangulator correspondent bien aux points d’origine

- verifier que l’ensemble du système reste fonctionnel même après plusieurs utilisation 