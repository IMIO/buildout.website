Known issues with plone.app.multilingual and archetypes.multilingual
====================================================================

1. Archetype content types in dexterity folderish content types
---------------------------------------------------------------

The TranslationGroup value for translated archetype object created in a dexterity folder is incorrect.


2. Dexterity and archetype content types in archetype folderish content types
-----------------------------------------------------------------------------

Translated (dexterity or archetypes objects created in an archetype folder are created in the language root folder.

For archetype object the TranslationGroup value is also incorrect.

3. TranslationGroup for archetype content types
-----------------------------------------------

The TranslationGroup value for translated archetype objects is sometimes incorrect.

Note: this happens only when memcached daemon is not running
