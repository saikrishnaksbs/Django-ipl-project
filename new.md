## Models file

### what is ondelete cascade?

on_delete is one of the parameter which helps to perform database-related task efficiently. This parameter is used when a relationship is established in Django. The on_delete parameter allows us to work with the foreign key.

Syntax of Django on_delete

    field name = models.ForeignKey(WASD, on_delete = OPERATION TYPE)  

on_delete includes the following options -

-   CASCADE
-   PROTECT
-   SET_NULL
-   SET_DEFAULT
-   SET()
-   DO_NOTHING
