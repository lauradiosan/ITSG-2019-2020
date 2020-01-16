#AI - Face Recognition

It contains a Spring Boot basic structure and a thymeleaf structure with some basic screens.


#Technologies used:
* Spring Boot
* Thymeleaf 
* Jquery  v 2.1.4
* Bootstrap v 3.3.4


#The Application structure:
```

├───client
│   ├───src
│   │   └───main
│   │       ├───java
│   │       │   └───ro
│   │       │       └───ubbcluj
│   │       │           ├───controller
│   │       │           ├───model
│   │       │           │   ├───enums
│   │       │           │   ├───filters
│   │       │           │   └───frontObjects
│   │       │           ├───security
│   │       │           └───utils
│   │       └───resources
│   │           ├───static
│   │           │   ├───css
│   │           │   ├───images
│   │           │   │   ├───action
│   │           │   │   ├───carrousel
│   │           │   │   └───error
│   │           │   └───js
│   │           └───templates
│   │               ├───applications
│   │               ├───common
│   │               ├───fragments
│   │               ├───announcementManagement
│   │               └───userManagement
│   └───target
├───core
│   ├───src
│   │   ├───main
│   │   │   └───java
│   │   │       └───ro
│   │   │           └───ubbcluj
│   │   │               ├───converter
│   │   │               ├───dto
│   │   │               ├───exception
│   │   │               ├───interfaces
│   │   │               ├───pagination
│   │   │               ├───service
│   │   │               └───util
│   │   └───test
│   │       └───java
│   │           ├───com
│   │           └───ro
│   │               └───ubbcluj
│   │                   └───junit
│   └───target
├───diagrams
├───repository
│   ├───src
│   │   └───main
│   │       ├───java
│   │       │   └───ro
│   │       │       └───ubbcluj
│   │       │           ├───entity
│   │       │           ├───enums
│   │       │           └───repository
│   │       └───resources
│   │           └───sqlScripts
│   └───target
└───test
    └───src
        └───test
            ├───java
            │   ├───com
            │   └───ro
            │       └───ubbcluj
            │           └───service
            │               └───test
            └───resources

```