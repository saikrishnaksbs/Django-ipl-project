# Django Technical Paper
____
## Settings file:

### what is secret key?
It is the unique identification key of the project provided by Django.when you create a new Django project using startproject, the settings.py file is generated automatically and gets a random SECRET_KEY value. This value is the key to securing signed data – it is vital you keep this secure, or attackers could use it to generate their own signed values.This key is mostly used to sign session cookies. If one were to have this key, they would be able to modify the cookies sent by the application.
The secret key is used by:
-   All sessions if you are using any other session backend than django.contrib.sessions.backends.cache, or are using the default get_session_auth_hash().
-   All messages if you are using CookieStorage or FallbackStorage.
-   All PasswordResetView tokens.
-   Any usage of cryptographic signing, unless a different key is provided.
-   If you rotate your secret key, all of the above will be invalidated. Secret keys are not used for passwords of users and key rotation will not affect them.

**Generating a Django SECRET_KEY**

To generate a new key, we can use the get_random_secret_key() function present in django.core.management.utils. This function returns a 50 character string that consists of random characters. This string can be used as a SECRET_KEY.

    from django.core.management.utils import get_random_secret_key

    # generating and printing the SECRET_KEY
    print(get_random_secret_key())
    
### what are the default Django apps inside it?Are there more?

By default, INSTALLED_APPS contains the following apps, all of which come with Django:

**django.contrib.admin** – The admin site.
**django.contrib.auth**– An authentication system.
**django.contrib.contenttypes**– A framework for content types.
**django.contrib.sessions**– A session framework.
**django.contrib.messages**– A messaging framework.
**django.contrib.staticfiles** – A framework for managing static files.
These applications are included by default as a convenience for the common case.

Some of these applications make use of at least one database table, though, so we need to create the tables in the database before we can use them.

Default applications are included for the common case, but not everybody needs them. If we don’t need any or all of them, we can comment-out or delete the appropriate line(s) from INSTALLED_APPS before running migrate. The migrate command will only run migrations for apps in INSTALLED_APPS.

### What is middleware? What are different kinds of middleware? Read up a little on each security issue.
In Django, middleware is a lightweight plugin that processes during request and response execution. Middleware is used to perform a function in the application. The functions can be a security, session, csrf protection, authentication etc.Django provides various built-in middleware and also allows us to write our own middleware. See, settings.py file of Django project that contains various middleware, that is used to provides functionalities to the application.
There are a lot of inbuilt middleware that are a part of a Django project. A few of the most commonly used are mentioned below.

Kinds of Middleware in Django
Django's middleware can be divided into 2 types: built-in and custom.

Built-in Middleware: These are the default middlewares that come with Django. Few of the built-in middlewares are:

-   Cache middleware
-   Common middleware
-   GZip middleware
-   Message middleware
-   Security middleware
-   Session middleware
-   Site middleware
-   Authentication middleware
-   CSRF protection middleware

Custom Middleware: These are the middleware that a user creates for their purpose.

### Read up on Django security
Django has some built-in features that handle user-submitted data to make it safe for an application. These features escape possible dangerous characters in requests, making the data safe for the application to use.The first rule of web application security is to never trust user-submitted data. Of course, the majority of the data you receive from the user side will be legit and safe. But an attacker can also maliciously craft data to damage your application or system. For example, if your application uses a SQL database and executes queries based on user input, a malicious actor can craft input that executes a query it's not supposed to. And malicious data from the user side means more than data entered in user input fields, like in forms. An attacker can also manipulate web requests, and Django’s got that covered too. Django contains clickjacking protection in the form of the X-Frame-Options middleware which, in a supporting browser, can prevent a site from being rendered inside a frame. Enforcing SSL/HTTPS.
### CSRF
CSRF stands for Cross Site Request Forgery, and it is said to occurs when a malicious Web site deceives users into unwillingly and unknowingly loading a URL from a site where they've previously been authenticated, thus exploiting their status and also putting the data at risk.
Django features a percent csrf token percent tag that is used to prevent malicious attacks. When generating the page on the server, it generates a token and ensures that any requests coming back in are cross-checked against this token. The token is not included in the incoming requests; thus they are not executed.
In the word count Django project Django renders a html page that contains a form which takes the input of text from the user and returns the word count of the text.
In this form, the csrf token is inserted to prevent the attack on this data.

    <h1>
    WORD COUNT
    </h1>
    <a href="/home/">My Home</a>
    {% csrf_token %} //csrf token inserted here.
    <form action="count">
    <textarea cols="50" rows="10" name="FullText"></textarea>
    <br/>
    <input type="submit" value="CountMe"/>
    </form>

**Preventing CSRF Attack**
The first step is to make sure all GET requests are free of side effects. That way, if a malicious site includes one of your pages as an , it will not have a negative effect.That leaves the POST requests to be attended. So, we move on to the next step.
The second step is to give each POST a hidden field whose value is secret and is generated from the user’s session ID.
Then, when processing the form on the server side, check for that secret field and raise an error if it does not validate.

### XSS
A cross-site scripting attack occurs when the attacker tricks a legitimate web-based application or site to accept a request as originating from a trusted source.
This is done by escaping the context of the web application; the web application then delivers that data to its users along with other trusted dynamic content, without validating it. The browser unknowingly executes malicious script on the client side (through client-side languages; usually JavaScript or HTML) in order to perform actions that are otherwise typically blocked by the browser’s Same Origin Policy.
Injecting malicious code is the most prevalent manner by which XSS is exploited; for this reason, escaping characters in order to prevent this manipulation is the top method for securing code against this vulnerability.Escaping means that the application is coded to mark key characters, and particularly key characters included in user input, to prevent those characters from being interpreted in a dangerous context. For example, in HTML, < can be coded as &lt; and > can be coded as &gt; in order to be interpreted and displayed as themselves in text, while within the code itself, they are used for HTML tags. If malicious content is injected into an application that escapes special characters and that malicious content uses < and > as HTML tags, those characters are nonetheless not interpreted as HTML tags by the browser if they’ve been correctly escaped in the application code and in this way the attempted attack is diverted.The most prominent use of XSS is to steal cookies (source: OWASP HttpOnly) and hijack user sessions, but XSS exploits have been used to expose sensitive information, enable access to privileged services and functionality and deliver malware.
___XSS Protection on Django___
Unlike most web development frameworks, the developers of the Django framework have considered the security aspects. As a result, Django comes with built-in security features against XSS attacks. XSS attacks happen through injections — injection of scripts that contain HTML tags. Django sure provides a layer of security by escaping HTML characters. But malicious actors would already know that. Attackers are getting more creative day by day and come up with ways to get over default security features.
___How to prevent attacks___
1.Sanitize data input in an HTTP request before reflecting it back, ensuring all data is validated, filtered or escaped before echoing anything back to the user, such as the values of query parameters during searches.
2.Convert special characters such as ?, &, /, <, > and spaces to their respective HTML or URL encoded equivalents.
3.Give users the option to disable client-side scripts.
4.Redirect invalid requests.
5.Detect simultaneous logins, including those from two separate IP addresses, and invalidate those sessions.
6.Use and enforce a Content Security Policy (source: Wikipedia) to disable any features that might be manipulated for an XSS attack.
### Click Jacking
Clickjacking is an interface-based attack in which a user is tricked into clicking on actionable content on a hidden website by clicking on some other content in a decoy website. Consider the following example:
A web user accesses a decoy website (perhaps this is a link provided by an email) and clicks on a button to win a prize. Unknowingly, they have been deceived by an attacker into pressing an alternative hidden button and this results in the payment of an account on another site. This is an example of a clickjacking attack. The technique depends upon the incorporation of an invisible, actionable web page (or multiple pages) containing a button or hidden link, say, within an iframe. The iframe is overlaid on top of the user's anticipated decoy web page content. This attack differs from a CSRF attack in that the user is required to perform an action such as a button click whereas a CSRF attack depends upon forging an entire request without the user's knowledge or input.Protection against CSRF attacks is often provided by the use of a CSRF token: a session-specific, single-use number or nonce. Clickjacking attacks are not mitigated by the CSRF token as a target session is established with content loaded from an authentic website and with all requests happening on-domain. CSRF tokens are placed into requests and passed to the server as part of a normally behaved session. The difference compared to a normal user session is that the process occurs within a hidden iframe.

**How to prevent click jacking**

Modern browsers honor the X-Frame-Options HTTP header that indicates whether or not a resource is allowed to load within a frame or iframe. If the response contains the header with a value of SAMEORIGIN then the browser will only load the resource in a frame if the request originated from the same site. If the header is set to DENY then the browser will block the resource from loading in a frame no matter which site made the request.
Django provides a few ways to include this header in responses from your site:
1.A middleware that sets the header in all responses.
2.A set of view decorators that can be used to override the middleware or to only set the header for certain views
The X-Frame-Options HTTP header will only be set by the middleware or view decorators if it is not already present in the response.

### What is (WSGI)[WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface)
Web Server Gateway Interface(WSGI) is a specification that describes the communication between web servers and Python web applications or frameworks. It explains how a web server communicates with python web applications/frameworks and how web applications/frameworks can be chained for processing a request.Python standard WSGI has been explained in detail with PEP 3333.Django's primary deployment platform is WSGI, the Python standard for web servers and applications. Django's startproject management command sets up a minimal default WSGI configuration for you, which you can tweak as needed for your project, and direct any WSGI-compliant application server to use.

**Configuring the settings module**

When the WSGI server loads your application, Django needs to import the settings module — that’s where your entire application is defined.
Django uses the DJANGO_SETTINGS_MODULE environment variable to locate the appropriate settings module. It must contain the dotted path to the settings module. You can use a different value for development and production; it all depends on how you organize your settings.

If this variable isn’t set, the default wsgi.py sets it to mysite.settings, where mysite is the name of your project. That’s how runserver discovers the default settings file by default.

**Applying WSGI middleware**
To apply WSGI middleware you can wrap the application object. For instance you could add these lines at the bottom of wsgi.py:

    from helloworld.wsgi import HelloWorldApplication
    application = HelloWorldApplication(application)

You could also replace the Django WSGI application with a custom WSGI application that later delegates to the Django WSGI application, if you want to combine a Django application with a WSGI application of another framework.

## Models file

### what is ondelete cascade?
The ondelete is one of the parameter which helps to perform database-related task efficiently. This parameter is used when a relationship is established in Django. The ondelete parameter allows us to work with the foreign key. It is clear that whenever the foreign key concept comes into the scenario, the on_delete parameter is expected to be declared as one among the parameters in the foreign key.
**ondelete cascade**
When we set the on_delete parameter as CASCADE, deleting the reference object will also delete the referred object. This option is most useful in many relationships. Suppose a post has comments; when the Post is deleted, all the comments on that Post will automatically delete. We don't want a comment saving in the database when the associated Post is deleted.

### A broad understanding of Fields and Validators available to you

**Fields** in Django are the data types to store a particular type of data. For example, to store an integer, IntegerField would be used. These fields have in-built validation for a particular data type, that is you can not store “abc” in an IntegerField. Similarly, for other fields. This post revolves around major fields one can use in Django Models. 

**Field types**

Each field in the model should be an instance of the appropriate Field class. Django uses field class types to determine a few things: 

1. The column type, which tells the database what kind of data to store (e.g. INTEGER, VARCHAR, TEXT).
2. The default HTML widget to use when rendering a form field 
3. The minimal validation requirements, used in Django’s admin and in automatically-generated forms.Here is a list of all Field types used in Django.  

___AutoField___: It is an IntegerField that automatically increments.

___BigAutoField___: It is a 64-bit integer, much like an AutoField except that it is guaranteed to fit numbers from 1 to 9223372036854775807.

___BigIntegerField___:It is a 64-bit integer, much like an IntegerField except that it is guaranteed to fit numbers from -9223372036854775808 to 9223372036854775807.

___BinaryField___:A field to store raw binary data. 

___BooleanField___:A true/false field. 

___CharField___:A field to store text-based values.

___DateField___:A date, represented in Python by a datetime.date instance

___DateTimeField___:It is used for date and time, represented in Python by a datetime.datetime instance.

___DecimalField___:It is a fixed-precision decimal number, represented in Python by a Decimal instance.

___DurationField___:A field for storing periods of time.

___EmailField___:It is a CharField that checks that the value is a valid email address.

___FileField___:It is a file-upload field.

___FloatField___:It is a floating-point number represented in Python by a float instance.

___ImageField___:It inherits all attributes and methods from FileField, but also validates that the uploaded object is a valid image.

___IntegerField___:It is an integer field. Values from -2147483648 to 2147483647 are safe in all databases supported by Django.

___GenericIPAddressField___:An IPv4 or IPv6 address, in string format

___Validator___ A validator is a computer program used to check the validity or syntactical correctness of a fragment of code or document.Validators can be used in Django in the models level or the level of the form. 
These validators are responsible for validating a field. The validators help to analyse the nature of the field with the value filled in the field. 
More importantly, these validators adjudicate the data being passed and post the errors onto the screen. This is the key benefit of Django validators. The Django validators can be done using methods such as clean() or even using field-level validators. It depends on the validator message used.
___syntax___:
    
    Raise validationerror(“”)

The process of raising a validation error is taken place through validators. This can be archived by means of the validation error exception, which can be raised at a form level and even at a field level. Here using this will raise the error and display it onto the console. The message which is expected to be raised has to be placed inbetween the double-quotes. The value between the double quotes will be displayed as the message associated to the error.
 Methods like clean() or even clean_fieldname can be used for raising these validation based errors. The validation errors can also be used to check all types of fields used across the forms section. The error message alerted onto the screen from the syntax will be very useful in determining the type of message being printed.

### Understanding the difference between Python module and Python class?

The difference between a class and a module in python is that a class is used to define a blueprint for a given object, whereas a module is used to reuse a given piece of code inside another program.

A class can have its own instance, but a module cannot be instantiated. We use the ‘class’ keyword to define a class, whereas to use modules, we use the ‘import’ keyword. We can inherit a particular class and modify it using inheritance. But while using modules, it is simply a code containing variables, functions, and classes.

Modules are files present inside a package, whereas a class is used to encapsulate data and functions together inside the same unit.

## Django ORM
_______
### Using ORM queries in Django Shell

### Turning ORM to SQL in Django Shell

### What are Aggregations?
The meaning of aggregation is “the collection of  related items of content so that they can be  displayed or linked to”. there are different situations that you will need to use Aggregation in Django, for example:

1.for finding “maximum”, “minimum” value of column in database table in django models.
2.for finding “count” of records in database table  based on a column.
3.for finding “average” value of a group of similar  objects.
4.also for finding sum of values in a column.
In most of the cases we use aggregation on  columns of data type “integer”, “float”, “date”,  “datetime” etc.
essentially, aggregations are nothing but a way to perform an operation on group of rows. In databases, they are represented by operators as sum, avg etc. to do these operations  Django added two new methods to querysets.


### What are Annotations?

Django annotations are a way of enriching the objects returned in QuerySets. That is, when you run queries against your models you can ask for new fields, whose values will be dynamically computed, to be added when evaluating the query. These fields will be accessible as if they were normal attributes of a model.

**How Annotate Works?**

1.The process in which annotate works is very simple and lean; it expects the model for which the annotation is performed and the aggregate function through which the annotation is going to be wrapped upon.
2.The annotate function allows the aggregate method to be encapsulated within it. The column which is going to be considered for annotation has to be declared within the aggregate function.
3.The column value will be expected to be enclosed within a pair of single quotations. In addition, the output of the annotate will be assigned to the annotated output variable, which can be flexibly used for identifying the output of the annotation.

### What is a migration file? Why is it needed?
Migrations are Django’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. They’re designed to be mostly automatic, but you’ll need to know when to make migrations, when to run them, and the common problems you might run into.
___The Commands___:
There are several commands which you will use to interact with migrations and Django’s handling of database schema:

    ___migrate___: which is responsible for applying and unapplying migrations.
    ___makemigrations___ which is responsible for creating new migrations based on the changes you have made to your models.
    ___sqlmigrate___ which displays the SQL statements for a migration.
    ___showmigrations___ which lists a project’s migrations and their status.

The migration files for each app live in a “migrations” directory inside of that app, and are designed to be committed to, and distributed as part of, its codebase. You should be making them once on your development machine and then running the same migrations on your colleagues’ machines, your staging machines, and eventually your production machines.
Migrations will run the same way on the same dataset and produce consistent results, meaning that what you see in development and staging is, under the same circumstances, exactly what will happen in production.
Django will make migrations for any change to your models or fields - even options that don’t affect the database - as the only way it can reconstruct a field correctly is to have all the changes in the history, and you might need those options in some data migrations

### What are SQL transactions?

A transaction is a sequence of operations performed (using one or more SQL statements) on a database as a single logical unit of work. The effects of all the SQL statements in a transaction can be either all committed (applied to the database) or all rolled back (undone from the database). A database transaction must be atomic, consistent, isolated and durable.A SQL transaction is a grouping of one or more SQL statements that interact with a database. A transaction in its entirety can commit to a database as a single logical unit or rollback (become undone) as a single logical unit. In SQL, transactions are essential for maintaining database integrity. They are used to preserve integrity when multiple related operations are executed concurrently, or when multiple users interact with a database concurrently.

### What are atomic transactions?
An atomic transaction is an indivisible and irreducible series of database operations such that either all occurs, or nothing occurs. A guarantee of atomicity prevents updates to the database occurring only partially, which can cause greater problems than rejecting the whole series outright.A short-lived transaction with the property “all or nothing”, i.e.,subtransactions in an atomic transaction all commit or abort.