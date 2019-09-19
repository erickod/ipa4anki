from pip._internal import main

def install(package):
    print("We're installing the %s" %package)
    main(["install", "--user", package])