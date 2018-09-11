.. toctree::
   :maxdepth: 2

Gestion des utilisateurs
========================

La gestion des utilisateurs et groupes est réservé aux utilisateurs ayant les droits administrateur du site ou administrateur.

Création d'un utilisateur
-------------------------

Allez dans *configuration du site* > *Utilisateurs et Groupes* et cliquer sur le bouton *ajouter*.

Un formulaire d'inscription va alors vous êtes proposé. Pour le champ *identifiant*, nous avons pris comme convention de mettre la première lettre du prénom et le nom de l'utilisateur, le tout attaché et en lettres minuscules. Par exemple, l'utilisateur Pierre Dupond aura comme identifiant \"pdupond\".

Le mot passe peut être choisi soit lors de la création de l'utilisateur, soit directement par l'utilisateur si vous cochez la case *Envoyer un mail de confirmation avec un lien pour choisir le mot de passe*.

Vous pouvez aussi le rajouter dans différents groupes.
Si vous cocher le groupe *Site Administrators* l'utilisateur aura le doit d'ajouter, modifier du contenu sur tout votre site. Il aura également la possibilité de configurer une partie du site, par exemple ajouter des utilisateurs, configurer l'envois des mails , changer le temps défilement du slider, etc.
Si vous l'ajoutez au groupe "Administrators" l'utilisateur aura le droit de tout modifier dans le site mais aura aussi accès à toute la configuration, c'est-à-dire Activer/désactiver des modules mais surtout il aura accès à Interface d'administration de Zope (ZMI) .

Lorsque vous avez ajouté votre utilisateur, vous ne devez cocher aucun droit ; seule la case membre doit être cochée.

Pour faciliter la gestion des utilisateurs, nous vous conseillons de créer des groupes, ce qui permet de rassembler le même type d'utilisateurs. Par exemple, lorsque plusieurs utilisateurs sont susceptibles d'ajouter ou de modifier du contenu dans la bibliothèque, il faut créer un groupe \"bibliothèque\" et lui assigner les droits nécessaires.

Vous pourrez créer un groupe dans l'onglet *groupes*, situé dans le panneau de gestion des utilisateurs. Lorsque vous créez un groupe, aucun droit ne doit être donné (cfr ci-dessous).

Donner des droits sur une partie du site
----------------------------------------

Afin que des utilisateurs définis puissent modifier le contenu dans une partie du site, autrement dit le contenu d'un dossier, rendez vous sur ce dossier, passez en mode *contenu* si vous avez une vue par défaut, puis onglet *Partage* et selectionnez le groupe adéquat. Enfin, cochez les droits *Peut Modifier* et *Peut Voir*. Les utilisateurs pourront dès lors modifier le dossier ainsi que son contenu.

De la même manière, si un des utilisateurs du groupe bibliothèque doit avoir des droits plus important, comme ajouter du contenu, cochez, pour cet utilisateur, le droit *Peut Ajouter*.
