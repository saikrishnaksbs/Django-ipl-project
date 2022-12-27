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
Django's middleware can be divided into 2 types: built-in and custom.
**Built-in Middleware**: These are the default middlewares that come with Django. Few of the built-in middlewares are:

-   Cache middleware
-   Common middleware
-   GZip middleware
-   Message middleware
-   Security middleware
-   Session middleware
-   Site middleware
-   Authentication middleware
-   CSRF protection middleware

**Custom Middleware**: These are the middleware that a user creates for their purpose.

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
1. Sanitize data input in an HTTP request before reflecting it back, ensuring all data is validated, filtered or escaped before echoing anything back to the user, such as the values of query parameters during searches.
2. Convert special characters such as ?, &, /, <, > and spaces to their respective HTML or URL encoded equivalents.
3. Give users the option to disable client-side scripts.
4. Redirect invalid requests.
5. Detect simultaneous logins, including those from two separate IP addresses, and invalidate those sessions.
6. Use and enforce a Content Security Policy (source: Wikipedia) to disable any features that might be manipulated for an XSS attack.
### Click Jacking
Clickjacking is an interface-based attack in which a user is tricked into clicking on actionable content on a hidden website by clicking on some other content in a decoy website. Consider the following example:
A web user accesses a decoy website (perhaps this is a link provided by an email) and clicks on a button to win a prize. Unknowingly, they have been deceived by an attacker into pressing an alternative hidden button and this results in the payment of an account on another site. This is an example of a clickjacking attack. The technique depends upon the incorporation of an invisible, actionable web page (or multiple pages) containing a button or hidden link, say, within an iframe. The iframe is overlaid on top of the user's anticipated decoy web page content. This attack differs from a CSRF attack in that the user is required to perform an action such as a button click whereas a CSRF attack depends upon forging an entire request without the user's knowledge or input.Protection against CSRF attacks is often provided by the use of a CSRF token: a session-specific, single-use number or nonce. Clickjacking attacks are not mitigated by the CSRF token as a target session is established with content loaded from an authentic website and with all requests happening on-domain. CSRF tokens are placed into requests and passed to the server as part of a normally behaved session. The difference compared to a normal user session is that the process occurs within a hidden iframe.

**How to prevent click jacking**

Modern browsers honor the X-Frame-Options HTTP header that indicates whether or not a resource is allowed to load within a frame or iframe. If the response contains the header with a value of SAMEORIGIN then the browser will only load the resource in a frame if the request originated from the same site. If the header is set to DENY then the browser will block the resource from loading in a frame no matter which site made the request.
Django provides a few ways to include this header in responses from your site:
1. A middleware that sets the header in all responses.
2. A set of view decorators that can be used to override the middleware or to only set the header for certain views
The X-Frame-Options HTTP header will only be set by the middleware or view decorators if it is not already present in the response.

### What is (WSGI)
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


**To invoke the Python shell, use this command**

    python manage.py shell

**How to get all records from table(Model)**

    >>> from sampleapp.models import Student  
    >>> queryset = Student.objects.all()  
    >>> queryset  
    <QuerySet [<Student: Ritesh Tiwari>, <Student: Yash Sharma>, <Student: Arpita Sharma>, <Student: Prince Sharma>, <Student: Megha Bhardwaj>, <Student: Akash Mishra>]>  


**How to add record to table(Model)**

We will use the Student.objects.create() and pass the fields along with its value as argument. Let's see the below example.

    >>> queryset = Student.objects.create(username = 'rahul20', first_name = 'Rahul', last_name = 'Shakya', mobile = '77777', email = 'rahul@gmail.com')  

    >>> queryset.save()  

**Retrieving Single Objects from QuerySets**

Suppose we need a specific object from a queryset to matching the result. We can do this using the get() method. The get() returns the single object directly. Let's see the following example.

    >>> from sampleapp.models import Student  
    >>> queryset = Student.objects.get(pk = 1)  
    >>> queryset  
    <Student: Ritesh Tiwari>  

    >>> queryset = Student.objects.get(mobile = 22222)   
    >>> queryset  
    <Student: Yash Sharma>  

**Filtering the Records**

In the earlier example, the QuerySet returned by all() describes the all record in the database table. But sometimes, we need to select the subset of complete set of object and it can be done by adding the filter conditions.

In the below example, we will fetch the data which first name starts with the R.

    >>> queryset = Student.objects.filter(first_name__startswith = 'R')  
    >>> queryset  
    <QuerySet [<Student: Ritesh Tiwari>, <Student: Rahul Shakya>]>  

    >>> str(queryset.query)  
    'SELECT "sampleapp_student"."id", "sampleapp_student"."username", "sampleapp_student"."first_name", "sampleapp_student"."last_name", "sampleapp_student"."mobile", "sampleapp_student"."email" FROM "sampleapp_student" WHERE "sampleapp_student"."first_name" LIKE R%  

**Using exclude() Method**

It returns a new QuerySet containing objects that do not match the given lookup parameter. In other words, it excluded the records according the lookup condition. Let's understand the following example.


    >>> queryset = Student.objects.exclude(first_name__startswith = 'R')   
    >>> queryset  
    , , , , ]>

**OR queries in Django ORM**

The OR operation is performed when we need the record filtering with two or more conditions. In the below example, we will get the student whose first_name starts with 'A' and last_name starts with 'M'.

Django allows us to do this in two ways.

queryset_1 |queryset_2

filter(Q(<condition_1>) | Q(<condition_2>

    >>> queryset = Student.objects.filter(first_name__startswith = 'R') | Student.objects.filter(last_name__startswith = 'S')     
    >>> queryset  
    <QuerySet [<Student: Ritesh Tiwari>, <Student: Yash Sharma>, <Student: Arpita Sharma>, <Student: Prince Sharma>, <Student: Rahul Shakya>]>  

    >>> str(queryset.query)   
    'SELECT "sampleapp_student"."id", "sampleapp_student"."username", "sampleapp_student"."first_name", "sampleapp_student"."last_name", "sampleapp_student"."mobile", "sampleapp_student"."email" FROM "sampleapp_student" WHERE ("sampleapp_student"."first_name" LIKE R% ESCAPE \'\\\' OR "sampleapp_student"."last_name" LIKE S% ESCAPE \'\\\')'


**AND queries in Django ORM**

The AND operation is performed when we need the record matching with two or more conditions. In the below example, we will get the student whose first_name starts with 'P' and last_name starts with 'S'.

Django allows us to do this in three ways.

    1 queryset_1 & queryset_2
    
    2. filter(<condition_1>, <condition_2>)
    
    3. filter(Q(condition_1) & Q(condition_2))

    >>> queryset = Student.objects.filter(first_name__startswith = 'P') & Student.objects.filter(last_name__startswith = 'S')   
    >>> queryset  
    <QuerySet [<Student: Prince Sharma>]>  

We can also use the following query.

    queryset2 = User.objects.filter( first_name__startswith='A', last_name__startswith='S' )  

or 

    queryset3 = User.objects.filter(Q(first_name__startswith='R') & Q(last_name__startswith='D'))

**Creating Multiple Object**

Sometimes we want create multiple objects in one shot. Suppose we want to create new objects at once and we don't want to run the multiple queries to the database. Django ORM provides the bulk_create to create multiple objects in one way.

    >>> Student.objects.all().count()  
    7  

**createating the multiple records in one query.**

    Student.objects.bulk_create([Student(first_name = 'Jai', last_name = 'Shah', mobile = '88888', email = 'shah@reddif.com'),Student(first_name = 'Tarak', last_name = 'Mehta', mobile = '9999', email = 'tarak@reddif.com'), Student(first_name = 'SuryaKumar', last_name = 'Yadav', mobile = '00000', email = 'yadav@reddif.com')])  
    [<Student: Jai Shah>, <Student: Tarak Mehta>, <Student: SuryaKumar Yadav>]  

**Limiting QuerySets**

We can set the limit on the queryset using the Python list's slicing syntax. This is equivalent operation of SQL's LIMIT and OFFSET clauses. Let's see the following query.

    >>> Student.objects.all()[:4]  
    <QuerySet [<Student: Ritesh Tiwari>, <Student: Yash Sharma>, <Student: Arpita Sharma>, <Student: Prince Sharma>]>

Below query will return first record to fifth record.

    >>> Student.objects.all()[1:6]     
    <QuerySet [<Student: Yash Sharma>, <Student: Arpita Sharma>, <Student: Prince Sharma>, <Student: Megha Bhardwaj>, <Student: Akash Mishra>]>  

**Order a QuerySets in ascending or descending order**

Django provides the order_by method for ordering the queryset. This method takes the field name which we want to Order (ascending and descending) the result. Let's see the following example.

Example - **Ascending order**

    >>> from sampleapp.models import Student  
    >>> Student.objects.all().order_by('mobile')      
    <QuerySet [<Student: SuryaKumar Yadav>, <Student: Ritesh Tiwari>, <StudentTo get the SQL query, we need to use the str() and pass the queryset object along with query.

    >>> str(queryset.query)  
    'SELECT "sampleapp_student"."id", "sampleapp_student"."username", "sampleapp_student"."first_name", "sampleapp_student"."last_name", "sampleapp_student"."mobile", "sampleapp_student"."email" FROM "sampleapp_student"'  
    : Yash Sharma>, <Student: Arpita Sharma>, <Student: Prince Sharma>, <Student: Megha Bhardwaj>, <Student: Akash Mishra>, <Student: Rahul Shakya>, <Student: Jai Shah>, <Student: Tarak Mehta>]>  

**For descending order, we will use the Not '-' before the query field.**

    >>> from sampleapp.models import Student    
    >>> Student.objects.all().order_by('-mobile')  
    <QuerySet [<Student: Tarak Mehta>, <Student: Jai Shah>, <Student: Rahul Shakya>, <Student: Akash Mishra>, <Student: Megha Bhardwaj>, <Student: Prince Sharma>, <Student: Arpita Sharma>, <Student: Yash Sharma>, <Student: Ritesh Tiwari>, <Student: SuryaKumar Yadav>]>  

**We can also pass the multiple fields in the order_by function.**

    >>> Student.objects.all().order_by('first_name','-mobile')   
    <QuerySet [<Student: Akash Mishra>, <Student: Arpita Sharma>, <Student: Jai Shah>, <Student: Megha Bhardwaj>, <Student: Prince Sharma>, <Student:Rahul Shakya>, <Student: Ritesh Tiwari>, <Student: SuryaKumar Yadav>, <Student: Tarak Mehta>, <Student: Yash Sharma>]>  

**Order on a field from a related model (with foreign key)**

Now, we will learn how we can order the data in the relation model. We create another model called Teacher which is a related model of Student model.

    >>> Student.objects.all().order_by('teacher__id', 'first_name')       
    <QuerySet [<Student: Prince Sharma>, <Student: Ritesh Tiwari>, <Student: SuryaKumar Yadav>, <Student: Tarak Mehta>, <Student: Arpita Sharma>, <Student: Megha Bhardwaj>, <Student: Jai Shah>, <Student: Rahul Shakya>, <Student: Yash Sharma>, <Student: Akash Mishra>]>

Query field lookups are nothing but a condition which specifies same as the SQL WHERE clause. They are stated as keyword arguments to the QuerySet methods such as filter(), exclude(), and get().

**Example**-

    Student.objects.filter(first_name__startswith = 'Ritesh')   
    <QuerySet [<Student: Ritesh Tiwari>]>  

-   **exact**
It returns the exact result according to the search.

    >>> Student.objects.get(first_name__exact = 'Arpita')           
    <Student: Arpita Sharma>  

Lookup should be used after the __ double underscore. We can use the case-insensitive version called iexact.

-   **contains**

    >>> from sampleapp.models import Student  
    >>> Student.objects.filter(last_name__contains = 'Shar')       
    <QuerySet [<Student: Yash Sharma>, <Student: Arpita Sharma>, <Student: Prince Sharma>]>  

**Join operations in Django**
The SQL join combines data or rows from two or more tables based on a common field between them. We can perform join operation in many ways. Let's understand the following example.

    >>> q = Student.objects.select_related('teacher')  
    >>>q  
    <QuerySet [<Student: Ritesh Tiwari>, <Student: Yash Sharma>, <Student: Arpita Sharma>, <Student: Prince Sharma>, <Student: Megha Bhardwaj>, <Student: Akash Mishra>, <Student: Rahul Shakya>, <Student: Jai Shah>, <Student: Tarak Mehta>, <Student: SuryaKumar Yadav>]>  
    >>>print(q.query)  
    SELECT "sampleapp_student"."id", "sampleapp_student"."username", "sampleapp_student"."first_name", "sampleapp_student"."last_name", "sampleapp_student"."mobile", "sampleapp_student"."email", "sampleapp_student"."teacher_id", "sampleapp_teacher"."id", "sampleapp_teacher"."teacher_name" FROM "sampleapp_student" LEFT OUTER JOIN "sampleapp_teacher" ON ("sampleapp_student"."teacher_id" = "sampleapp_teacher"."id")  

**Group record in Django ORM**

Django ORM provides the grouping facility using the aggregation functions like Max, Min, Avg, and Sum. Sometimes we need to get the aggregate values from the objects. Let's understand the following example.

    >>> from django.db.models import Avg, Max, Min, Sum, Count  
    >>> Student.objects.all().aggregate(Avg('id'))  
    {'id__avg': 5.5}  
    >>> Student.objects.all().aggregate(Min('id'))    
    {'id__min': 1}  
    >>> Student.objects.all().aggregate(Max('id'))   
    {'id__max': 10}  
    >>> Student.objects.all().aggregate(Sum('id'))   
    {'id__sum': 55}  

**Truncate like operation using Django ORM**

Truncate in SQL means clear the table data for future use. Django doesn't provide the built-in methods to truncate the table, but we can use the delete() method to get the similar result. Let's understand the following example.

    >>> Student.objects.all().count()  
    10  
    >>> Student.objects.all().delete()  
    (10, {'sampleapp.Student': 10})  
    >>> Student.objects.all().count()  
    0  
    >>> Student.objects.all()       
    <QuerySet []>  

**Union of Data**

Union means getting the record which are common in both query sets. Let's see how we can do this.

    >>> q1 = Student.objects.filter(id__gte = 15)    
    >>> q1  
    <QuerySet [<Student: Megha Bhardwaj>, <Student: Akash Mishra>]>  
    >>> q2 = Student.objects.filter(id__lte = 15)    
    >>> q2  
    <QuerySet [<Student: Ritesh Tiwari>, <Student: Yash Sharma>, <Student: Arpita Sharma>, <Student: Prince Sharma>, <Student: Megha Bhardwaj>]>  
    >>> q1.union(q2)  
    <QuerySet [<Student: Ritesh Tiwari>, <Student: Yash Sharma>, <Student: Arpita Sharma>, <Student: Prince Sharma>, <Student: Megha Bhardwaj>, <Student: Akash Mishra>]>  

If null=True means the field value is set as NULL i.e. no data. It is basically for the database column value.

    date = models.DateTimeField(null=True)  

The blank = True specifies whether field is required in forms.

    title = models.CharField(blank=True) // title can be kept blank. In the database ("") will be stored.  

If we set null=True blank=True, means that the field is optional in all circumstances.

    teacher = models.ForeignKey(null=True, blank=True) // The exception is CharFields() and TextFields(), which in Django are never saved as ?→NULL. Blank values are stored in the DB as an empty string ('').  

cheatsheet for orm - 

### Turning ORM to SQL in Django Shell

To get the SQL query, we need to use the str() and pass the queryset object along with query.

    >>> str(queryset.query)
    'SELECT "sampleapp_student"."id", "sampleapp_student"."username", "sampleapp_student"."first_name", "sampleapp_student"."last_name", "sampleapp_student"."mobile", "sampleapp_student"."email" FROM "sampleapp_student"'  


### What are Aggregations?

The meaning of aggregation is “the collection of  related items of content so that they can be  displayed or linked to”. there are different situations that you will need to use Aggregation in Django, for example:


1.for finding “maximum”, “minimum” value of column in database table in django models.
2.for finding “count” of records in database table  based on a column.
3.for finding “average” value of a group of similar  objects.
4.also for finding sum of values in a column.
In most of the cases we use aggregation on  columns of data type “integer”, “float”, “date”,  “datetime” etc.
essentially, aggregations are nothing but a way to perform an operation on group of rows. In databases, they are represented by operators as sum, avg etc. to do these operations  Django added two new methods to querysets.

Django ORM provides the grouping facility using the aggregation functions like Max, Min, Avg, and Sum. Sometimes we need to get the aggregate values from the objects. Let's understand the following example.

    >>> from django.db.models import Avg, Max, Min, Sum, Count  
    >>> Student.objects.all().aggregate(Avg('id'))  
    {'id__avg': 5.5}  
    >>> Student.objects.all().aggregate(Min('id'))    
    {'id__min': 1}  
    >>> Student.objects.all().aggregate(Max('id'))   
    {'id__max': 10}  
    >>> Student.objects.all().aggregate(Sum('id'))   
    {'id__sum': 55}  


### What are Annotations?

Django annotations are a way of enriching the objects returned in QuerySets. That is, when you run queries against your models you can ask for new fields, whose values will be dynamically computed, to be added when evaluating the query. These fields will be accessible as if they were normal attributes of a model.

The difference between aggrergate and annotate is that, aggregate calculates values for the entire queryset. Annotate calculates summary values for each item in the queryset.

Syntax:

    Annotated_output = Model.Objects.annotate(variable=aggregate_function(columnname))

**How Annotate Works?**

1. The process in which annotate works is simple ; it expects the model for which the annotation is performed and the aggregate function through which the annotation is going to be wrapped upon.

2. The annotate function allows the aggregate method to be encapsulated within it. The column which is going to be considered for annotation has to be declared within the aggregate function.

3. The column value will be expected to be enclosed within a pair of single quotations. In addition, the output of the annotate will be assigned to the annotated output variable, which can be flexibly used for identifying the output of the annotation.


Annotations with Count Aggregator Examples

Let’s now have a look at a simple annotation and its syntax.

Here we are asking for Provider records. For each provider, we’re adding the field circuit_count. That field will record a number of the circuits linked to each of the providers.

    from django.db.models import Count

    providers = Provider.objects.annotate(circuit_count=Count("circuits"))

with order_by

    providers = Provider.objects.annotate(circuit_count=Count("circuits")).order_by("-circuit_count")

Query to return only selected fields and their values. We’ll do this by appending the values() method.


    providers = Provider.objects.annotate( \
    circuit_count=Count("circuits")) \
    .order_by("-circuit_count") \
    .values("name", "circuit_count")

with filter

    providers = Provider.objects.annotate( \
        circuit_count=Count("circuits")) \
        .filter(circuit_count__gt=0) \
        .order_by("-circuit_count") \
        .values("name", "circuit_count")
    >>> providers
    <RestrictedQuerySet [{'name': 'NTT', 'circuit_count': 40}, {'name': 'Telia Carrier', 'circuit_count': 40}]>


### What is a migration file? Why is it needed?

Migrations are Django’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. They’re designed to be mostly automatic, but you’ll need to know when to make migrations, when to run them, and the common problems you might run into.
**The Commands**:
There are several commands which you will use to interact with migrations and Django’s handling of database schema:

**migrate** which is responsible for applying and unapplying migrations.

**makemigrations** which is responsible for creating new migrations based on the changes you have made to your models.

**sqlmigrate** which displays the SQL statements for a migration.

**showmigrations** which lists a project’s migrations and their status.

The migration files for each app live in a “migrations” directory inside of that app, and are designed to be committed to, and distributed as part of, its codebase. You should be making them once on your development machine and then running the same migrations on your colleagues’ machines, your staging machines, and eventually your production machines.
Migrations will run the same way on the same dataset and produce consistent results, meaning that what you see in development and staging is, under the same circumstances, exactly what will happen in production.
Django will make migrations for any change to your models or fields - even options that don’t affect the database - as the only way it can reconstruct a field correctly is to have all the changes in the history, and you might need those options in some data migrations


### What are SQL transactions?

A transaction is a sequence of operations performed (using one or more SQL statements) on a database as a single logical unit of work. The effects of all the SQL statements in a transaction can be either all committed (applied to the database) or all rolled back (undone from the database). A database transaction must be atomic, consistent, isolated and durable.A SQL transaction is a grouping of one or more SQL statements that interact with a database. A transaction in its entirety can commit to a database as a single logical unit or rollback (become undone) as a single logical unit. In SQL, transactions are essential for maintaining database integrity. They are used to preserve integrity when multiple related operations are executed concurrently, or when multiple users interact with a database concurrently.


### What are atomic transactions?

An atomic transaction is an indivisible and irreducible series of database operations such that either all occurs, or nothing occurs. A guarantee of atomicity prevents updates to the database occurring only partially, which can cause greater problems than rejecting the whole series outright.A short-lived transaction with the property “all or nothing”, i.e.,subtransactions in an atomic transaction all commit or abort.

Atomic can be used as both a decorator or as a context_manager. So if we use it as a context manager, then 

    from django.db import transaction

    try:
        with transaction.atomic():
            user = User.create(
                cd['name'], cd['email'], 
                cd['password'], cd['last_4_digits'])

            if customer:
                user.stripe_id = customer.id
                user.save()
            else:
                UnpaidUsers(email=cd['email']).save()

    except IntegrityError:
        form.addError(cd['email'] + ' is already a member')

Note the line with transaction.atomic(). All code inside that block will be executed inside a transaction. So if we re-run our tests, they all should pass! Remember a transaction is a single unit of work, so everything inside the context manager gets rolled back together when the UnpaidUsers call fails.

Using a decorator

We can also try adding atomic as a decorator.

@transaction.atomic():
def register(request):
    # ...snip....

    try:
        user = User.create(
            cd['name'], cd['email'], 
            cd['password'], cd['last_4_digits'])

        if customer:
            user.stripe_id = customer.id
            user.save()
        else:
                UnpaidUsers(email=cd['email']).save()

    except IntegrityError:
        form.addError(cd['email'] + ' is already a member')


**SavePoints**

Even though transactions are atomic they can be further broken down into savepoints. Think of savepoints as partial transactions.

So if you have a transaction that takes four SQL statements to complete, you could create a savepoint after the second statement. Once that savepoint is created, even if the 3rd or 4th statement fail you can do a partial rollback, getting rid of the 3rd and 4th statement but keeping the first two.

So it’s basically like splitting a transaction into smaller lightweight transactions allowing you to do partial rollbacks or commits.

    @transaction.atomic()
    def save_points(self,save=True):

        user = User.create('jj','inception','jj','1234')
        sp1 = transaction.savepoint()

        user.name = 'starting down the rabbit hole'
        user.stripe_id = 4
        user.save()

        if save:
            transaction.savepoint_commit(sp1)
        else:
            transaction.savepoint_rollback(sp1)

## Rreferences

1. https://blog.networktocode.com/post/nautobot-and-django-query-annotations-part-1/#:~:text=What%20Are%20Annotations,added%20when%20evaluating%20the%20query.

2. https://docs.djangoproject.com/en/4.1/topics/db/aggregation/

3. https://able.bio/dfernsby/django-queryset-annotations-with-conditions--19d4cb4b

4. https://www.educba.com/django-annotate/

5. https://medium.com/@singhgautam7/django-annotations-steroids-to-your-querysets-766231f0823a

6. https://stackoverflow.com/questions/7981837/difference-between-djangos-annotate-and-aggregate-methods

7. https://tutorial.djangogirls.org/en/django_orm/

8. https://www.javatpoint.com/django-orm-queries

9. https://docs.djangoproject.com/en/4.1/topics/db/queries/

10. https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/

11. https://medium.com/analytics-vidhya/what-is-wsgi-web-server-gateway-interface-ed2d290449e

12. https://docs.djangoproject.com/en/1.8/intro/tutorial01/

13. https://medium.com/codex/understanding-djangos-apps-and-appconfig-2cb57e44c80e

14.https://docs.djangoproject.com/en/4.1/ref/applications/

15. https://www.geeksforgeeks.org/django-settings-file-step-by-step-explanation/

16. https://medium.com/codex/understanding-djangos-apps-and-appconfig-2cb57e44c80e

17. https://docs.gitguardian.com/secrets-detection/detectors/specifics/django_secret_key#:~:text=Summary%3A%20The%20Django%20secret%20key,cookies%20sent%20by%20the%20application.

18. https://stackoverflow.com/questions/7382149/whats-the-purpose-of-django-setting-secret-key

19. https://www.educative.io/answers/how-to-generate-a-django-secretkey

